# Hackathon #2 Reflection

## Team Performance Analysis

### Division of Work

Our team strategically divided responsibilities across three workstreams. **Team Member A** led the **Forecasting** track, building the Prophet model with external regressors for holidays and promotions. **Team Member B** focused on **Optimization**, handling safety stock calculations, inventory simulation, and the PuLP-based distribution problem. **Team Member C** owned the **Presentation**, synthesizing results into executive-ready slides and preparing the Q&A simulation. We held 30-minute syncs every two hours to ensure alignment and resolve blockers.

### Biggest Analytical Hurdle

The most significant challenge was **calibrating the safety stock model to match realistic stockout costs**. Initial simulations showed implausible results because our stockout cost assumptions were too low. We iterated through three rounds of parameter tuning, cross-referencing industry benchmarks and historical expediting invoices, before landing on defensible numbers. This taught us that optimization outputs are only as good as the cost inputs - garbage in, garbage out.

### Ensuring Actionable Recommendations

To ensure our final recommendation was actionable, we applied three filters: (1) **quantified ROI** - every recommendation included investment, expected return, and payback period; (2) **implementation clarity** - we specified what changes, who owns it, and when; (3) **executive alignment** - we pre-tested the CFO question to ensure our rationale would withstand financial scrutiny. The result was a recommendation that leadership could approve in the meeting rather than defer for further analysis.

---

*Word count: 238*
