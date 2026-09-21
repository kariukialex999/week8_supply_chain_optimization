#!/usr/bin/env python3
"""Run the Week 8 Supply Chain Optimization analysis and generate all outputs."""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from prophet import Prophet
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.seasonal import seasonal_decompose
from pulp import *
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')

print("="*70)
print("WEEK 8: SUPPLY CHAIN OPTIMIZATION")
print("="*70)

# ============================================================================
# 1. DATA PREPARATION
# ============================================================================
print("\n[1/5] DATA PREPARATION")

def generate_demand_data(start_date='2024-01-01', periods=730):
    np.random.seed(42)
    dates = pd.date_range(start=start_date, periods=periods, freq='D')
    base_demand = 500
    trend = np.linspace(0, periods * 0.5, periods)
    weekly_pattern = np.array([1.1, 1.15, 1.12, 1.08, 1.2, 0.85, 0.75])
    weekly_seasonality = np.array([weekly_pattern[d.weekday()] for d in dates])
    yearly_seasonality = 1 + 0.2 * np.sin(2 * np.pi * (np.arange(periods) - 90) / 365)
    
    holidays = ['2024-01-01', '2024-01-15', '2024-02-14', '2024-02-19',
        '2024-05-27', '2024-07-04', '2024-09-02', '2024-10-14',
        '2024-11-28', '2024-11-29', '2024-12-25', '2024-12-31',
        '2025-01-01', '2025-01-20', '2025-02-14', '2025-02-17',
        '2025-05-26', '2025-07-04', '2025-09-01', '2025-10-13',
        '2025-11-27', '2025-11-28', '2025-12-25', '2025-12-31',
        '2026-01-01', '2026-01-19', '2026-02-14', '2026-02-16',
        '2026-05-25', '2026-07-04', '2026-09-07']
    holiday_dates = pd.to_datetime(holidays)
    holiday_effect = np.array([1.3 if d in holiday_dates else 1.0 for d in dates])
    
    promotion_days = np.random.choice(periods, size=periods//15, replace=False)
    promotion_effect = np.ones(periods)
    promotion_effect[promotion_days] = 1.25
    is_promotion = np.zeros(periods)
    is_promotion[promotion_days] = 1
    
    weather_impact = np.ones(periods)
    for i, d in enumerate(dates):
        if d.month in [12, 1, 2]:
            weather_impact[i] = np.random.uniform(0.85, 1.1)
        else:
            weather_impact[i] = np.random.uniform(0.95, 1.05)
    
    noise = np.random.normal(1, 0.08, periods)
    demand = (base_demand + trend) * weekly_seasonality * yearly_seasonality * \
             holiday_effect * promotion_effect * weather_impact * noise
    demand = np.maximum(demand, 100).astype(int)
    
    return pd.DataFrame({
        'date': dates, 'demand': demand,
        'is_holiday': [1 if d in holiday_dates else 0 for d in dates],
        'is_promotion': is_promotion.astype(int),
        'day_of_week': [d.weekday() for d in dates],
        'month': [d.month for d in dates],
        'weather_impact': weather_impact
    })

df = generate_demand_data()
df.to_csv('historical_demand_data.csv', index=False)
print(f"  Dataset: {df.shape[0]} days, {df['date'].min().date()} to {df['date'].max().date()}")
print(f"  Saved: historical_demand_data.csv")

# Demand analysis plot
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
axes[0,0].plot(df['date'], df['demand'], alpha=0.7, linewidth=0.8)
axes[0,0].plot(df['date'], df['demand'].rolling(30).mean(), color='red', linewidth=2, label='30-day MA')
axes[0,0].set_title('Daily Demand Over Time', fontweight='bold')
axes[0,0].legend()

weekly = df.groupby('day_of_week')['demand'].mean()
axes[0,1].bar(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], weekly.values, color=sns.color_palette('husl',7))
axes[0,1].set_title('Average Demand by Day of Week', fontweight='bold')
axes[0,1].axhline(weekly.mean(), color='red', linestyle='--')

monthly = df.groupby('month')['demand'].mean()
axes[1,0].bar(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], monthly.values, color=sns.color_palette('coolwarm',12))
axes[1,0].set_title('Average Demand by Month', fontweight='bold')

axes[1,1].hist(df['demand'], bins=50, edgecolor='black', alpha=0.7)
axes[1,1].axvline(df['demand'].mean(), color='red', linestyle='--', label=f'Mean: {df["demand"].mean():.0f}')
axes[1,1].set_title('Distribution of Daily Demand', fontweight='bold')
axes[1,1].legend()

plt.tight_layout()
plt.savefig('demand_analysis.png', dpi=150)
plt.close()
print("  Saved: demand_analysis.png")

# ============================================================================
# 2. PROPHET FORECASTING
# ============================================================================
print("\n[2/5] PROPHET FORECASTING")

prophet_df = df[['date', 'demand', 'is_promotion']].copy()
prophet_df.columns = ['ds', 'y', 'promotion']
train_df = prophet_df.iloc[:-60]
test_df = prophet_df.iloc[-60:]

holidays = pd.DataFrame({
    'holiday': 'us_holiday',
    'ds': pd.to_datetime(['2024-01-01','2024-07-04','2024-11-28','2024-12-25',
        '2025-01-01','2025-07-04','2025-11-27','2025-12-25',
        '2026-01-01','2026-07-04','2026-11-26','2026-12-25']),
    'lower_window': -1, 'upper_window': 1
})

print("  Training model...")
model = Prophet(holidays=holidays, yearly_seasonality=True, weekly_seasonality=True,
    daily_seasonality=False, seasonality_mode='multiplicative',
    changepoint_prior_scale=0.05, interval_width=0.95)
model.add_regressor('promotion', mode='multiplicative')
model.fit(train_df)

future = model.make_future_dataframe(periods=90)
future['promotion'] = future['ds'].map(prophet_df.set_index('ds')['promotion'].to_dict()).fillna(0)
forecast = model.predict(future)

# Metrics
test_forecast = forecast[forecast['ds'].isin(test_df['ds'])]
y_actual, y_pred = test_df['y'].values, test_forecast['yhat'].values
mape = np.mean(np.abs((y_actual - y_pred) / y_actual)) * 100
rmse = np.sqrt(mean_squared_error(y_actual, y_pred))
mae = mean_absolute_error(y_actual, y_pred)

print(f"  MAPE: {mape:.2f}%")
print(f"  RMSE: {rmse:.2f} units")
print(f"  MAE: {mae:.2f} units")

# Forecast plot
fig = model.plot(forecast, figsize=(14, 6))
plt.title('Demand Forecast with Prophet', fontweight='bold')
plt.axvline(x=train_df['ds'].max(), color='red', linestyle='--', label='Train/Test Split')
plt.legend()
plt.tight_layout()
plt.savefig('prophet_forecast.png', dpi=150)
plt.close()
print("  Saved: prophet_forecast.png")

# Components plot
fig = model.plot_components(forecast, figsize=(14, 10))
plt.tight_layout()
plt.savefig('prophet_components.png', dpi=150)
plt.close()
print("  Saved: prophet_components.png")

# Evaluation plot
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(test_df['ds'], y_actual, label='Actual', color='blue', linewidth=2)
ax.plot(test_df['ds'], y_pred, label='Predicted', color='red', linewidth=2, linestyle='--')
ax.fill_between(test_forecast['ds'], test_forecast['yhat_lower'], test_forecast['yhat_upper'], alpha=0.3, color='red')
ax.set_title(f'Actual vs Predicted (MAPE: {mape:.2f}%)', fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('forecast_evaluation.png', dpi=150)
plt.close()
print("  Saved: forecast_evaluation.png")

# ============================================================================
# 3. INVENTORY OPTIMIZATION
# ============================================================================
print("\n[3/5] INVENTORY OPTIMIZATION")

LEAD_TIME, SERVICE_LEVEL = 7, 0.95
forecast_period = forecast[forecast['ds'] > train_df['ds'].max()].head(60)
avg_daily_demand = forecast_period['yhat'].mean()
std_daily_demand = forecast_period['yhat'].std()

z_score = stats.norm.ppf(SERVICE_LEVEL)
SAFETY_STOCK = z_score * std_daily_demand * np.sqrt(LEAD_TIME)
REORDER_POINT = avg_daily_demand * LEAD_TIME + SAFETY_STOCK

print(f"  Avg Daily Demand: {avg_daily_demand:.0f} units")
print(f"  Safety Stock (95%): {SAFETY_STOCK:.0f} units")
print(f"  Reorder Point: {REORDER_POINT:.0f} units")

# Simulation
def simulate_inventory(demand_data, rop, order_qty, lead_time, days=365):
    inventory = rop + order_qty // 2
    pending = []
    levels, stockouts = [], 0
    for day in range(days):
        for arr, qty in pending[:]:
            if arr == day:
                inventory += qty
                pending.remove((arr, qty))
        demand = demand_data[day % len(demand_data)]
        if inventory >= demand:
            inventory -= demand
        else:
            stockouts += 1
            inventory = 0
        if inventory <= rop and not pending:
            pending.append((day + lead_time, order_qty))
        levels.append(inventory)
    return levels, stockouts

ORDER_QTY = int(avg_daily_demand * LEAD_TIME * 2)
demand_data = df['demand'].values

levels_no_ss, stockouts_no_ss = simulate_inventory(demand_data, int(avg_daily_demand * LEAD_TIME), ORDER_QTY, LEAD_TIME)
levels_with_ss, stockouts_with_ss = simulate_inventory(demand_data, int(REORDER_POINT), ORDER_QTY, LEAD_TIME)

print(f"  Stockouts WITHOUT safety stock: {stockouts_no_ss} days")
print(f"  Stockouts WITH safety stock: {stockouts_with_ss} days")
print(f"  Service level improvement: {(365-stockouts_no_ss)/365*100:.1f}% -> {(365-stockouts_with_ss)/365*100:.1f}%")

# Simulation plot
fig, axes = plt.subplots(2, 1, figsize=(14, 10))
axes[0].plot(levels_no_ss, linewidth=1, alpha=0.8)
axes[0].axhline(avg_daily_demand * LEAD_TIME, color='orange', linestyle='--', linewidth=2, label='ROP (no SS)')
axes[0].set_title(f'WITHOUT Safety Stock (Stockouts: {stockouts_no_ss} days, SL: {(365-stockouts_no_ss)/365*100:.1f}%)', fontweight='bold')
axes[0].set_ylabel('Inventory')
axes[0].legend()

axes[1].plot(levels_with_ss, linewidth=1, alpha=0.8, color='green')
axes[1].axhline(REORDER_POINT, color='orange', linestyle='--', linewidth=2, label=f'ROP: {REORDER_POINT:.0f}')
axes[1].axhline(SAFETY_STOCK, color='red', linestyle='--', linewidth=2, label=f'SS: {SAFETY_STOCK:.0f}')
axes[1].set_title(f'WITH Safety Stock (Stockouts: {stockouts_with_ss} days, SL: {(365-stockouts_with_ss)/365*100:.1f}%)', fontweight='bold')
axes[1].set_xlabel('Day')
axes[1].set_ylabel('Inventory')
axes[1].legend()

plt.tight_layout()
plt.savefig('inventory_simulation.png', dpi=150)
plt.close()
print("  Saved: inventory_simulation.png")

# Safety stock analysis plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sl_range = np.linspace(0.80, 0.995, 100)
ss_range = [stats.norm.ppf(sl) * std_daily_demand * np.sqrt(LEAD_TIME) for sl in sl_range]
axes[0].plot(sl_range * 100, ss_range, linewidth=2)
axes[0].axhline(SAFETY_STOCK, color='red', linestyle='--', label=f'95% SL = {SAFETY_STOCK:.0f}')
axes[0].axvline(95, color='red', linestyle='--', alpha=0.5)
axes[0].set_title('Safety Stock vs Service Level', fontweight='bold')
axes[0].set_xlabel('Service Level (%)')
axes[0].set_ylabel('Safety Stock (Units)')
axes[0].legend()

axes[1].barh(['Safety Stock', 'Lead Time Demand', 'Reorder Point'], 
             [SAFETY_STOCK, avg_daily_demand*LEAD_TIME, REORDER_POINT],
             color=['red', 'blue', 'orange'])
axes[1].set_title('Inventory Policy Components', fontweight='bold')
axes[1].set_xlabel('Units')

plt.tight_layout()
plt.savefig('safety_stock_analysis.png', dpi=150)
plt.close()
print("  Saved: safety_stock_analysis.png")

# ============================================================================
# 4. LINEAR PROGRAMMING
# ============================================================================
print("\n[4/5] LINEAR PROGRAMMING OPTIMIZATION")

warehouses = ['W1_Central', 'W2_North', 'W3_South']
warehouse_capacity = {'W1_Central': 2000, 'W2_North': 1500, 'W3_South': 1800}
stores = ['Store_A', 'Store_B', 'Store_C', 'Store_D', 'Store_E']
store_demand = {'Store_A': 800, 'Store_B': 650, 'Store_C': 900, 'Store_D': 550, 'Store_E': 700}
transport_cost = {
    ('W1_Central', 'Store_A'): 2.5, ('W1_Central', 'Store_B'): 3.0, ('W1_Central', 'Store_C'): 2.8,
    ('W1_Central', 'Store_D'): 3.5, ('W1_Central', 'Store_E'): 2.2,
    ('W2_North', 'Store_A'): 3.2, ('W2_North', 'Store_B'): 2.0, ('W2_North', 'Store_C'): 3.8,
    ('W2_North', 'Store_D'): 2.5, ('W2_North', 'Store_E'): 3.0,
    ('W3_South', 'Store_A'): 2.8, ('W3_South', 'Store_B'): 3.5, ('W3_South', 'Store_C'): 2.0,
    ('W3_South', 'Store_D'): 3.0, ('W3_South', 'Store_E'): 2.5,
}

prob = LpProblem("Distribution", LpMinimize)
routes = [(w, s) for w in warehouses for s in stores]
ship = LpVariable.dicts("Ship", routes, lowBound=0)
prob += lpSum([transport_cost[(w,s)] * ship[(w,s)] for (w,s) in routes])
for s in stores:
    prob += lpSum([ship[(w,s)] for w in warehouses]) >= store_demand[s]
for w in warehouses:
    prob += lpSum([ship[(w,s)] for s in stores]) <= warehouse_capacity[w]

prob.solve(PULP_CBC_CMD(msg=0))
total_cost = value(prob.objective)
total_demand = sum(store_demand.values())

print(f"  Status: {LpStatus[prob.status]}")
print(f"  Minimum Daily Cost: ${total_cost:,.2f}")
print(f"  Cost per Unit: ${total_cost/total_demand:.2f}")

# Distribution heatmap
results = pd.DataFrame(index=warehouses, columns=stores)
for w in warehouses:
    for s in stores:
        results.loc[w,s] = ship[(w,s)].varValue or 0
results = results.astype(float)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(results, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax)
ax.set_title('Optimal Distribution Plan (Units/Day)', fontweight='bold')
plt.tight_layout()
plt.savefig('distribution_optimization.png', dpi=150)
plt.close()
print("  Saved: distribution_optimization.png")

# ============================================================================
# 5. SUMMARY
# ============================================================================
print("\n[5/5] GENERATING SUMMARY")

summary = pd.DataFrame({
    'Metric': ['Forecast MAPE (%)', 'Forecast RMSE (units)', 'Avg Daily Demand (units)',
               'Safety Stock (units)', 'Reorder Point (units)', 'Service Level with SS (%)',
               'Daily Distribution Cost ($)', 'Cost per Unit ($)'],
    'Value': [round(mape,2), round(rmse,2), round(avg_daily_demand,0),
              round(SAFETY_STOCK,0), round(REORDER_POINT,0), 
              round((365-stockouts_with_ss)/365*100,1),
              round(total_cost,2), round(total_cost/total_demand,2)]
})
summary.to_csv('optimization_summary.csv', index=False)
print("  Saved: optimization_summary.csv")

print("\n" + "="*70)
print("RESULTS SUMMARY")
print("="*70)
print(summary.to_string(index=False))

print("\n" + "="*70)
print("ALL OUTPUT FILES GENERATED:")
print("="*70)
print("  1. historical_demand_data.csv")
print("  2. demand_analysis.png")
print("  3. prophet_forecast.png")
print("  4. prophet_components.png")
print("  5. forecast_evaluation.png")
print("  6. inventory_simulation.png")
print("  7. safety_stock_analysis.png")
print("  8. distribution_optimization.png")
print("  9. optimization_summary.csv")
print("\n[SUCCESS] Analysis complete!")
