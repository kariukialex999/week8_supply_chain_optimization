# Quarterly Operations Review - Slide Deck Content
## Q3 2026 Performance & Strategic Outlook

**Presenter:** Operations Analytics Team  
**Date:** September 21, 2026

---

## Slide 1: Title Slide

### Quarterly Operations Review
**Q3 2026 Performance & Strategic Outlook**

Supply Chain & Operations Analytics Team  
September 21, 2026

| Forecast Accuracy | Service Level | Cost Savings | Safety Index |
|-------------------|---------------|--------------|--------------|
| 92.4% | 97.8% | $847K | 98.2% |

---

## Slide 2: Executive Summary (BLUF)

### Bottom Line Up Front

Our supply chain optimization initiative has delivered **$847K in annual savings** through improved demand forecasting and inventory management.

**Key Achievements:**
- **Forecast accuracy improved to 92.4%** (MAPE of 7.6%) using Prophet model with holiday/promotion regressors
- **Service level increased from 89% to 97.8%** through optimized safety stock policy
- **Distribution costs reduced by 15%** via linear programming optimization
- **Stockout incidents reduced by 78%** compared to previous quarter

**Recommendation:** Approve full deployment of optimized inventory policy across all 5 distribution centers.

---

## Slide 3: Safety & Equipment Health

### Safety Performance (Weeks 6-7 Recap)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| TRIR (Total Recordable Incident Rate) | < 2.0 | 1.4 | On Track |
| Near-Miss Reports | > 50/month | 67 | Exceeds |
| Safety Training Completion | 100% | 98.2% | On Track |
| Equipment Downtime | < 3% | 2.1% | On Track |
| Predictive Maintenance Alerts | N/A | 23 resolved | Active |

**Key Insights:**
- Zero lost-time injuries for 127 consecutive days
- Predictive maintenance reduced unplanned downtime by 34%
- Forklift fleet health at 96% - scheduled Q4 maintenance for aging units

---

## Slide 4: Equipment Health Dashboard

### Critical Equipment Status

| Equipment | Health Score | Next Service | Risk Level |
|-----------|--------------|--------------|------------|
| Conveyor System A | 94% | Oct 15 | Low |
| Conveyor System B | 87% | Sep 28 | Medium |
| Packaging Line 1 | 96% | Nov 1 | Low |
| Packaging Line 2 | 91% | Oct 8 | Low |
| Forklift Fleet (12 units) | 89% | Rolling | Medium |
| HVAC - Warehouse | 82% | Sep 25 | Medium |

**Action Items:**
- Priority: HVAC maintenance scheduled for Sep 25 to prevent Q4 issues
- Conveyor B bearing replacement planned - parts on order
- Budget request: $45K for forklift battery replacements (3 units)

---

## Slide 5: Supply Chain - Demand Forecasting

### Prophet Model Performance

| Metric | Value | Industry Benchmark | Assessment |
|--------|-------|-------------------|------------|
| MAPE | 7.6% | < 15% | Excellent |
| RMSE | 48.2 units | N/A | Good |
| Forecast Horizon | 60 days | 30-90 days | Standard |
| External Factors | Holidays + Promotions | Varies | Enhanced |

**Key Findings:**
- Weekly seasonality: 20% higher demand Mon-Fri vs weekends
- Q4 holiday uplift: 25-35% above baseline (Nov-Dec)
- Promotion events drive 25% demand spikes - now predictable
- Weather integration planned for Q4 (potential 3% accuracy gain)

---

## Slide 6: Supply Chain - Inventory Optimization

### Safety Stock & Reorder Point Analysis

| Parameter | Old Policy | New Policy | Impact |
|-----------|------------|------------|--------|
| Service Level Target | 90% | 95% | +5% |
| Safety Stock | 892 units | 1,247 units | +355 units |
| Reorder Point | 4,392 units | 4,747 units | +355 units |
| Stockout Days/Year | 38 days | 8 days | -79% |
| Annual Holding Cost | $651K | $912K | +$261K |
| Annual Stockout Cost | $1,425K | $300K | -$1,125K |

### **NET ANNUAL SAVINGS: $864,000**
*(Stockout cost reduction minus additional holding cost)*

---

## Slide 7: Supply Chain - Distribution Network

### Linear Programming Optimization Results

| Route | Volume (units/day) | Cost/Unit | Daily Cost |
|-------|-------------------|-----------|------------|
| W1_Central -> Store_A | 800 | $2.50 | $2,000 |
| W2_North -> Store_B | 650 | $2.00 | $1,300 |
| W2_North -> Store_D | 550 | $2.50 | $1,375 |
| W3_South -> Store_C | 900 | $2.00 | $1,800 |
| W3_South -> Store_E | 700 | $2.50 | $1,750 |
| **TOTAL** | **3,600** | **Avg: $2.28** | **$8,225** |

**Optimization Impact:**
- 15% cost reduction vs. previous equal-distribution policy
- Warehouse utilization balanced: 67% (W1), 80% (W2), 89% (W3)
- Sensitivity analysis: Network can absorb 18% demand surge before capacity constraints

---

## Slide 8: Strategic Recommendations

### 1. Deploy Optimized Safety Stock Policy Enterprise-Wide
| Investment | Expected ROI | Payback | Risk |
|------------|--------------|---------|------|
| $261K (holding cost increase) | $864K net savings/year | 3.6 months | Low |

### 2. Expand W2_North Warehouse Capacity by 500 Units
| Investment | Expected ROI | Payback | Risk |
|------------|--------------|---------|------|
| $125K (infrastructure) | $180K/year (growth capacity) | 8.3 months | Medium |

### 3. Integrate Weather Data into Forecasting Model
| Investment | Expected ROI | Payback | Risk |
|------------|--------------|---------|------|
| $35K (API + development) | $95K/year (accuracy gains) | 4.4 months | Low |

### **TOTAL PROJECTED ANNUAL VALUE: $1.14M**

---

## Slide 9: Q&A Simulation

### CFO Question: "Why do we need so much safety stock? That ties up working capital."

**Response:**

Great question. The safety stock increase of 355 units represents a $261K increase in holding costs annually. However, our simulation data shows this investment prevents an estimated $1.125M in stockout costs - that's a **4.3:1 return ratio**.

**The math breaks down as follows:**

- **Without safety stock:** 38 stockout days/year = $1.425M lost (expediting + lost sales)
- **With optimized safety stock:** 8 stockout days/year = $300K lost
- **Additional holding cost:** $261K/year
- **Net benefit:** $1.125M - $261K = **$864K annual savings**

Additionally, our 95% service level protects customer relationships. Each stockout event risks losing a customer permanently - the lifetime value impact isn't captured in these numbers but represents significant additional downside protection.

**Working capital impact is offset by 3.6-month payback period.**

---

## Video Presentation Outline (15 minutes)

### Timing Guide:

| Section | Duration | Slides |
|---------|----------|--------|
| Introduction & BLUF | 2 min | 1-2 |
| Safety & Equipment | 3 min | 3-4 |
| Supply Chain Performance | 6 min | 5-7 |
| Strategic Recommendations | 3 min | 8 |
| Q&A Simulation | 1 min | 9 |

### Speaker Notes:

1. **Opening (30 sec):** "Good morning. Today I'll present our Q3 operations review with a focus on the supply chain optimization results from our recent initiative."

2. **BLUF (1.5 min):** Lead with the $847K savings headline. Emphasize this is validated through simulation, not projections.

3. **Safety Transition (30 sec):** "Before diving into supply chain, let me quickly recap our safety performance, which remains foundational to operations."

4. **Forecasting Deep Dive (3 min):** Explain Prophet model choice, the importance of holiday/promotion regressors, and MAPE interpretation.

5. **Inventory Optimization (3 min):** Walk through the safety stock calculation logic. Emphasize the simulation results showing 79% stockout reduction.

6. **Distribution (2 min):** Highlight that LP optimization is now automated and runs weekly.

7. **Recommendations (2 min):** Present each recommendation with ROI justification. Note the 3.6-month payback on the primary recommendation.

8. **CFO Q&A (1 min):** Demonstrate preparedness by proactively addressing the capital concern.

9. **Close (30 sec):** "I recommend we approve the safety stock policy deployment this quarter. Happy to take any questions."

---

*End of Slide Deck Content*
