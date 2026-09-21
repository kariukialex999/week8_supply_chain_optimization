# Week 8: Supply Chain Optimization

## Project Overview

This project demonstrates end-to-end supply chain analytics including demand forecasting, inventory optimization, and distribution network optimization using linear programming.

## Repository Structure

```
week8_supply_chain_optimization/
|-- week8_supply_chain_optimization.ipynb   # Main Jupyter notebook (Part A)
|-- create_slide_deck.py                    # Script to generate PDF slides
|-- slide_deck_content.md                   # Slide content in markdown format
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

### 2. Run the Jupyter Notebook

```bash
jupyter notebook week8_supply_chain_optimization.ipynb
```

### 3. Generate Slide Deck PDF

```bash
python create_slide_deck.py
```

This creates `Week8_Quarterly_Ops_Review.pdf` in the project directory.

## Key Results

| Metric | Value |
|--------|-------|
| Forecast MAPE | ~7.6% |
| Service Level (with SS) | ~97.8% |
| Annual Savings | ~$864K |
| Distribution Cost Reduction | 15% |

## Technologies Used

- **Python 3.9+**
- **Prophet** - Time series forecasting
- **PuLP** - Linear programming
- **Pandas/NumPy** - Data manipulation
- **Matplotlib/Seaborn** - Visualization
- **ReportLab** - PDF generation

## Author

Operations Analytics Team - September 2026
