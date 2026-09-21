# Week 8: Supply Chain Optimization

## Project Overview

This project demonstrates end-to-end supply chain analytics including demand forecasting, inventory optimization, and distribution network optimization using linear programming.

## Repository Structure

```
week8_supply_chain_optimization/
|-- week8_supply_chain_optimization.ipynb   # Main Jupyter notebook (Part A)
|-- run_analysis.py                         # Python script to run full analysis
|-- create_slide_deck.py                    # Script to generate PDF slides
|-- Week8_Quarterly_Ops_Review.pdf          # Slide deck (Part B)
|-- week8_supply_chain_optimization.mp4     # Video presentation (Part B)
|-- hackathon2_reflection.md                # Hackathon #2 reflection (Part C)
|-- requirements.txt                        # Python dependencies
|-- README.md                               # This file
```

## Part A: Technical Coding Challenge

### Jupyter Notebook Contents

1. **Data Preparation**
   - Synthetic demand data with trend, seasonality, and external factors
   - Data cleaning and validation
   - Trend and seasonality visualization

2. **Demand Forecasting**
   - Prophet model with holidays and promotions as external regressors
   - 60-day forecast horizon
   - Model evaluation using MAPE and RMSE
   - Cross-validation for robust assessment

3. **Inventory Optimization**
   - Safety Stock calculation for 95% service level
   - Reorder Point determination
   - Inventory simulation comparing policies with/without safety stock
   - Cost-benefit analysis

4. **Linear Programming (PuLP)**
   - Multi-warehouse distribution optimization
   - Minimize transportation costs while meeting demand
   - Capacity constraint handling
   - Sensitivity analysis

## Part B: Management Briefing

### Slide Deck (9 slides)

1. **Title Slide** - Key metrics overview
2. **Executive Summary** - BLUF with key achievements
3. **Safety Performance** - Weeks 6-7 recap
4. **Equipment Health** - Dashboard and action items
5. **Demand Forecasting** - Prophet model results
6. **Inventory Optimization** - Safety stock analysis
7. **Distribution Network** - LP optimization results
8. **Strategic Recommendations** - 3 actionable items with ROI
9. **Q&A Simulation** - CFO question and response

### Video Presentation (15 minutes)

The slide deck includes speaker notes and timing guide for the video recording.

## Part C: Hackathon Reflection

See `hackathon2_reflection.md` for the 200-word reflection on team performance.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Analysis (generates all outputs)

```bash
python run_analysis.py
```

### 3. Or run the Jupyter Notebook interactively

```bash
jupyter notebook week8_supply_chain_optimization.ipynb
```

### 4. Generate Slide Deck PDF

```bash
python create_slide_deck.py
```

## Key Results

| Metric | Value |
|--------|-------|
| Forecast MAPE | 9.72% |
| Service Level (with SS) | 100% |
| Safety Stock | 692 units |
| Reorder Point | 5,869 units |
| Daily Distribution Cost | $8,015 |

## Generated Outputs

- `historical_demand_data.csv` - 730 days of synthetic demand data
- `demand_analysis.png` - Trend and seasonality visualizations
- `prophet_forecast.png` - Prophet model forecast
- `prophet_components.png` - Trend, weekly, yearly components
- `forecast_evaluation.png` - Actual vs predicted comparison
- `inventory_simulation.png` - With/without safety stock simulation
- `safety_stock_analysis.png` - Service level analysis
- `distribution_optimization.png` - LP optimization heatmap
- `optimization_summary.csv` - Key metrics summary

## Technologies Used

- **Python 3.9+**
- **Prophet** - Time series forecasting
- **PuLP** - Linear programming
- **Pandas/NumPy** - Data manipulation
- **Matplotlib/Seaborn** - Visualization
- **ReportLab** - PDF generation

## Author

Operations Analytics Team - September 2026
