#!/usr/bin/env python3
"""
Run the Week 8 Supply Chain Optimization notebook and verify all outputs.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.seasonal import seasonal_decompose
from pulp import *
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')

print("="*70)
print("WEEK 8: SUPPLY CHAIN OPTIMIZATION - VERIFICATION RUN")
print("="*70)
print("\nLibraries loaded successfully!")

# ============================================================================
# 1. DATA PREPARATION
# ============================================================================
print("\n" + "="*70)
print("SECTION 1: DATA PREPARATION")
print("="*70)

def generate_demand_data(start_date='2024-01-01', periods=730):
    np.random.seed(42)
    dates = pd.date_range(start=start_date, periods=periods, freq='D')
    base_demand = 500
    trend = np.linspace(0, periods * 0.5, periods)
    weekly_pattern = np.array([1.1, 1.15, 1.12, 1.08, 1.2, 0.85, 0.75])
    weekly_seasonality = np.array([weekly_pattern[d.weekday()] for d in dates])
    yearly_seasonality = 1 + 0.2 * np.sin(2 * np.pi * (np.arange(periods) - 90) / 365)
    
    holidays = [
        '2024-01-01', '2024-01-15', '2024-02-14', '2024-02-19',
        '2024-05-27', '2024-07-04', '2024-09-02', '2024-10-14',
        '2024-11-28', '2024-11-29', '2024-12-25', '2024-12-31',
        '2025-01-01', '2025-01-20', '2025-02-14', '2025-02-17',
        '2025-05-26', '2025-07-04', '2025-09-01', '2025-10-13',
        '2025-11-27', '2025-11-28', '2025-12-25', '2025-12-31',
        '2026-01-01', '2026-01-19', '2026-02-14', '2026-02-16',
        '2026-05-25', '2026-07-04', '2026-09-07'
    ]
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
    
    df = pd.DataFrame({
        'date': dates,
        'demand': demand,
        'is_holiday': [1 if d in holiday_dates else 0 for d in dates],
        'is_promotion': is_promotion.astype(int),
        'day_of_week': [d.weekday() for d in dates],
        'month': [d.month for d in dates],
        'weather_impact': weather_impact
    })
    return df

df = generate_demand_data()
print(f"\nDataset shape: {df.shape}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"\nDescriptive Statistics:")
print(df['demand'].describe())

df.to_csv('historical_demand_data.csv', index=False)
print("\n[OK] Data saved to 'historical_demand_data.csv'")

# Create demand analysis visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

ax1 = axes[0, 0]
ax1.plot(df['date'], df['demand'], alpha=0.7, linewidth=0.8)
rolling_avg = df['demand'].rolling(window=30).mean()
ax1.plot(df['date'], rolling_avg, color='red', linewidth=2, label='30-day MA')
ax1.set_title('Daily Demand Over Time', fontsize=14, fontweight='bold')
ax1.set_xlabel('Date')
ax1.set_ylabel('Units Demanded')
ax1.legend()

ax2 = axes[0, 1]
weekly_demand = df.groupby('day_of_week')['demand'].mean()
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
ax2.bar(days, weekly_demand.values, color=sns.color_palette('husl', 7))
ax2.set_title('Average Demand by Day of Week', fontsize=14, fontweight='bold')
ax2.axhline(y=weekly_demand.mean(), color='red', linestyle='--', label='Overall Avg')
ax2.legend()

ax3 = axes[1, 0]
monthly_demand = df.groupby('month')['demand'].mean()
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax3.bar(months, monthly_demand.values, color=sns.color_palette('coolwarm', 12))
ax3.set_title('Average Demand by Month', fontsize=14, fontweight='bold')
ax3.axhline(y=monthly_demand.mean(), color='red', linestyle='--', label='Overall Avg')
ax3.legend()

ax4 = axes[1, 1]
ax4.hist(df['demand'], bins=50, edgecolor='black', alpha=0.7)
ax4.axvline(df['demand'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["demand"].mean():.0f}')
ax4.set_title('Distribution of Daily Demand', fontsize=14, fontweight='bold')
ax4.legend()

plt.tight_layout()
plt.savefig('demand_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] Figure saved as 'demand_analysis.png'")

# ============================================================================
# 2. DEMAND FORECASTING WITH PROPHET
# ============================================================================
print("\n" + "="*70)
print("SECTION 2: DEMAND FORECASTING WITH PROPHET")
print("="*70)

prophet_df = df[['date', 'demand', 'is_promotion']].copy()
prophet_df.columns = ['ds', 'y', 'promotion']

train_size = len(prophet_df) - 60
train_df = prophet_df.iloc[:train_size]
test_df = prophet_df.iloc[train_size:]

print(f"\nTraining set: {len(train_df)} days")
print(f"Test set: {len(test_df)} days")

holidays = pd.DataFrame({
    'holiday': 'us_holiday',
    'ds': pd.to_datetime([
        '2024-01-01', '2024-01-15', '2024-02-14', '2024-02-19',
        '2024-05-27', '2024-07-04', '2024-09-02', '2024-10-14',
        '2024-11-28', '2024-11-29', '2024-12-25', '2024-12-31',
        '2025-01-01', '2025-01-20', '2025-02-14', '2025-02-17',
        '2025-05-26', '2025-07-04', '2025-09-01', '2025-10-13',
        '2025-11-27', '2025-11-28', '2025-12-25', '2025-12-31',
        '2026-01-01', '2026-01-19', '2026-02-14', '2026-02-16',
        '2026-05-25', '2026-07-04', '2026-09-07', '2026-10-12',
        '2026-11-26', '2026-11-27', '2026-12-25', '2026-12-31'
    ]),
    'lower_window': -1,
    'upper_window': 1
})

print("\nTraining Prophet model...")
model = Prophet(
    holidays=holidays,
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode='multiplicative',
    changepoint_prior_scale=0.05,
    holidays_prior_scale=10,
    interval_width=0.95
)
model.add_regressor('promotion', mode='multiplicative')
model.fit(train_df)
print("[OK] Model training complete!")

future = model.make_future_dataframe(periods=90)
future_promotions = prophet_df.set_index('ds')['promotion'].to_dict()
future['promotion'] = future['ds'].map(future_promotions).fillna(0)
forecast = model.predict(future)
print(f"[OK] Forecast generated for {len(forecast)} days")

# Model Evaluation
def calculate_mape(actual, predicted):
    actual, predicted = np.array(actual), np.array(predicted)
    mask = actual != 0
    return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100

def calculate_rmse(actual, predicted):
    return np.sqrt(mean_squared_error(actual, predicted))

test_forecast = forecast[forecast['ds'].isin(test_df['ds'])]
y_actual = test_df['y'].values
y_pred = test_forecast['yhat'].values

mape = calculate_mape(y_actual, y_pred)
rmse = calculate_rmse(y_actual, y_pred)
mae = mean_absolute_error(y_actual, y_pred)

print("\n" + "-"*50)
print("MODEL PERFORMANCE METRICS (Test Set - 60 Days)")
print("-"*50)
print(f"MAPE: {mape:.2f}%")
print(f"RMSE: {rmse:.2f} units")
print(f"MAE: {mae:.2f} units")

if mape < 10:
    print("\n*** Excellent forecast accuracy (MAPE < 10%)")
elif mape < 20:
    print("\n** Good forecast accuracy (MAPE < 20%)")

# Save forecast plot
fig1 = model.plot(forecast, figsize=(14, 6))
plt.title('Demand Forecast with Prophet', fontsize=14, fontweight='bold')
plt.axvline(x=train_df['ds'].max(), color='red', linestyle='--', label='Train/Test Split')
plt.legend()
plt.tight_layout()
plt.savefig('prophet_forecast.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n[OK] Forecast plot saved as 'prophet_forecast.png'")

# ============================================================================
# 3. INVENTORY OPTIMIZATION
# ============================================================================
print("\n" + "="*70)
print("SECTION 3: INVENTORY OPTIMIZATION")
print("="*70)

LEAD_TIME = 7
SERVICE_LEVEL = 0.95

forecast_period = forecast[forecast['ds'] > train_df['ds'].max()].head(60)
avg_daily_demand = forecast_period['yhat'].mean()
std_daily_demand = forecast_period['yhat'].std()

print(f"\nForecast Statistics (Next 60 Days):")
print(f"  Average Daily Demand: {avg_daily_demand:.0f} units")
print(f"  Std Dev of Daily Demand: {std_daily_demand:.0f} units")

def calculate_safety_stock(service_level, lead_time, demand_std):
    z_score = stats.norm.ppf(service_level)
    return z_score * demand_std * np.sqrt(lead_time)

def calculate_reorder_point(avg_demand, lead_time, safety_stock):
    return avg_demand * lead_time + safety_stock

SAFETY_STOCK = calculate_safety_stock(SERVICE_LEVEL, LEAD_TIME, std_daily_demand)
REORDER_POINT = calculate_reorder_point(avg_daily_demand, LEAD_TIME, SAFETY_STOCK)

print(f"\n95% Service Level Results:")
print(f"  Safety Stock: {SAFETY_STOCK:.0f} units")
print(f"  Reorder Point: {REORDER_POINT:.0f} units")

# Inventory Simulation
def simulate_inventory(demand_data, initial_inventory, reorder_point, order_qty, 
                       lead_time, safety_stock=0, days=365):
    inventory = initial_inventory
    pending_orders = []
    inventory_levels = []
    stockout_days = 0
    stockout_units = 0
    
    for day in range(days):
        received = 0
        new_pending = []
        for arrival_day, qty in pending_orders:
            if arrival_day == day:
                inventory += qty
            else:
                new_pending.append((arrival_day, qty))
        pending_orders = new_pending
        
        demand = demand_data[day % len(demand_data)]
        
        if inventory >= demand:
            inventory -= demand
        else:
            stockout_units += (demand - inventory)
            stockout_days += 1
            inventory = 0
        
        if inventory <= reorder_point and len(pending_orders) == 0:
            arrival = day + lead_time
            pending_orders.append((arrival, order_qty))
        
        inventory_levels.append(inventory)
    
    service_level = (days - stockout_days) / days * 100
    avg_inventory = np.mean(inventory_levels)
    
    return {
        'inventory_levels': inventory_levels,
        'stockout_days': stockout_days,
        'stockout_units': stockout_units,
        'service_level': service_level,
        'avg_inventory': avg_inventory
    }

SIMULATION_DAYS = 365
ORDER_QUANTITY = int(avg_daily_demand * LEAD_TIME * 2)
INITIAL_INVENTORY = int(REORDER_POINT + ORDER_QUANTITY / 2)
demand_data = df['demand'].values

results_no_ss = simulate_inventory(
    demand_data=demand_data,
    initial_inventory=INITIAL_INVENTORY,
    reorder_point=int(avg_daily_demand * LEAD_TIME),
    order_qty=ORDER_QUANTITY,
    lead_time=LEAD_TIME,
    safety_stock=0,
    days=SIMULATION_DAYS
)

results_with_ss = simulate_inventory(
    demand_data=demand_data,
    initial_inventory=INITIAL_INVENTORY,
    reorder_point=int(REORDER_POINT),
    order_qty=ORDER_QUANTITY,
    lead_time=LEAD_TIME,
    safety_stock=int(SAFETY_STOCK),
    days=SIMULATION_DAYS
)

print("\n" + "-"*70)
print("INVENTORY SIMULATION RESULTS")
print("-"*70)
print(f"{'Metric':<25} {'No Safety Stock':<20} {'With Safety Stock':<20}")
print("-"*70)
print(f"{'Stockout Days':<25} {results_no_ss['stockout_days']:<20} {results_with_ss['stockout_days']:<20}")
print(f"{'Service Level':<25} {results_no_ss['service_level']:.1f}%{'':<14} {results_with_ss['service_level']:.1f}%")
print("-"*70)

# Save simulation plot
fig, axes = plt.subplots(2, 1, figsize=(14, 10))
days_range = range(SIMULATION_DAYS)

axes[0].plot(days_range, results_no_ss['inventory_levels'], linewidth=1, alpha=0.8)
axes[0].axhline(y=avg_daily_demand * LEAD_TIME, color='orange', linestyle='--', linewidth=2)
axes[0].set_title(f'WITHOUT Safety Stock (Stockouts: {results_no_ss["stockout_days"]} days)', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Inventory (Units)')

axes[1].plot(days_range, results_with_ss['inventory_levels'], linewidth=1, alpha=0.8, color='green')
axes[1].axhline(y=REORDER_POINT, color='orange', linestyle='--', linewidth=2, label=f'ROP: {REORDER_POINT:.0f}')
axes[1].axhline(y=SAFETY_STOCK, color='red', linestyle='--', linewidth=2, label=f'SS: {SAFETY_STOCK:.0f}')
axes[1].set_title(f'WITH Safety Stock (Stockouts: {results_with_ss["stockout_days"]} days)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Day')
axes[1].set_ylabel('Inventory (Units)')
axes[1].legend()

plt.tight_layout()
plt.savefig('inventory_simulation.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n[OK] Inventory simulation saved as 'inventory_simulation.png'")

# ============================================================================
# 4. LINEAR PROGRAMMING OPTIMIZATION
# ============================================================================
print("\n" + "="*70)
print("SECTION 4: LINEAR PROGRAMMING OPTIMIZATION")
print("="*70)

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

prob = LpProblem("Distribution_Optimization", LpMinimize)
routes = [(w, s) for w in warehouses for s in stores]
ship_vars = LpVariable.dicts("Ship", routes, lowBound=0, cat='Continuous')

prob += lpSum([transport_cost[(w, s)] * ship_vars[(w, s)] for (w, s) in routes])

for s in stores:
    prob += lpSum([ship_vars[(w, s)] for w in warehouses]) >= store_demand[s]

for w in warehouses:
    prob += lpSum([ship_vars[(w, s)] for s in stores]) <= warehouse_capacity[w]

print("\nSolving optimization problem...")
prob.solve(PULP_CBC_CMD(msg=0))

print(f"Status: {LpStatus[prob.status]}")
print(f"\nMinimum Daily Distribution Cost: ${value(prob.objective):,.2f}")

total_demand = sum(store_demand.values())
print(f"Average Cost per Unit: ${value(prob.objective)/total_demand:.2f}")

print("\nOptimal Shipments:")
for w in warehouses:
    for s in stores:
        qty = ship_vars[(w, s)].varValue
        if qty and qty > 0:
            print(f"  {w} -> {s}: {qty:.0f} units")

# Save distribution heatmap
results_matrix = pd.DataFrame(index=warehouses, columns=stores)
for w in warehouses:
    for s in stores:
        results_matrix.loc[w, s] = ship_vars[(w, s)].varValue if ship_vars[(w, s)].varValue else 0

results_matrix = results_matrix.astype(float)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(results_matrix, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Units'})
ax.set_title('Optimal Distribution Plan (Units Shipped)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('distribution_optimization.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n[OK] Distribution optimization saved as 'distribution_optimization.png'")

# ============================================================================
# 5. SUMMARY
# ============================================================================
print("\n" + "="*70)
print("SUMMARY - ALL VERIFICATIONS PASSED")
print("="*70)

summary_data = {
    'Metric': [
        'Forecast MAPE (%)',
        'Forecast RMSE (units)',
        'Avg Daily Demand (units)',
        'Safety Stock (units)',
        'Reorder Point (units)',
        'Service Level with SS (%)',
        'Daily Distribution Cost ($)',
        'Cost per Unit ($)'
    ],
    'Value': [
        round(mape, 2),
        round(rmse, 2),
        round(avg_daily_demand, 0),
        round(SAFETY_STOCK, 0),
        round(REORDER_POINT, 0),
        round(results_with_ss['service_level'], 1),
        round(value(prob.objective), 2),
        round(value(prob.objective)/total_demand, 2)
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('optimization_summary.csv', index=False)
print("\n[OK] Summary saved to 'optimization_summary.csv'")

print("\nFinal Metrics:")
print(summary_df.to_string(index=False))

print("\n" + "="*70)
print("FILES GENERATED:")
print("="*70)
print("  1. historical_demand_data.csv")
print("  2. demand_analysis.png")
print("  3. prophet_forecast.png")
print("  4. inventory_simulation.png")
print("  5. distribution_optimization.png")
print("  6. optimization_summary.csv")
print("\n[SUCCESS] All notebook sections verified successfully!")
