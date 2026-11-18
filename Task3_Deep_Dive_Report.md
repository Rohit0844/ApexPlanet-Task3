# Task 3 — Deep-Dive Analysis & Interactive Dashboarding

**Intern:** Rohit Joshi  
**Program:** ApexPlanet Software Pvt. Ltd. — Data Analytics Internship  
**Deep-dive selected:** Rule-based Customer Segmentation

## 1. Objective
Define core sales KPIs, examine customer value segments, and provide an interactive dashboard to explore sales performance.

## 2. Dataset
- Source: cleaned sales dataset prepared in Task 1 and analyzed in Task 2.
- Rows: 1,000
- Columns: 15
- Date coverage: 2025-01-01 to 2026-01-01
- Distinct orders: 992
- Distinct customers: 947

## 3. Core KPIs

| KPI | Formula | Business rationale |
|---|---|---|
| Total Revenue | SUM(Total_Sales) | Measures sales value generated |
| Distinct Orders | COUNT(DISTINCT Order_ID) | Counts orders without double-counting repeated order rows |
| Average Order Value (AOV) | Total Revenue / Distinct Orders | Measures average revenue per order |
| Unique Customers | COUNT(DISTINCT Customer_ID) | Measures customer reach |
| Units Sold | SUM(Quantity) | Measures product volume |

### Dataset-wide KPI snapshot
- Total Revenue: ₹139,399,439.65
- Distinct Orders: 992
- Average Order Value: ₹140,523.63
- Unique Customers: 947
- Units Sold: 5,435

## 4. Deep-Dive: Customer Segmentation
Customer-level metrics were calculated by grouping records on `Customer_ID`: total spend, distinct order count, units purchased, last order date and recency relative to the latest date in the dataset.

Business-rule segments:
- **High-Value Customer:** total customer spend is at or above the 75th percentile of customer spend.
- **Repeat Customer:** more than one distinct order and spend below the high-value threshold.
- **Standard:** all remaining customers.

Customer counts in the full dataset:
- High-Value Customer: 237
- Repeat Customer: 20
- Standard: 690

This segmentation is deliberately interpretable and reproducible. It is not a predictive model and does not establish customer loyalty or future value.

## 5. Dashboard Features
The Streamlit dashboard provides:
- Date, city, category and gender filters.
- KPI cards for revenue, distinct orders, AOV, unique customers and units.
- Monthly revenue trend and category revenue.
- Customer segment distribution and segment revenue.
- Customer value explorer with segment selector.
- Top cities and products by revenue.

## 6. Findings and Interpretation
Use the dashboard filters to explore which categories and cities contribute most to revenue, how monthly revenue changes, and how revenue is distributed across customer segments. The dashboard is designed to support interactive exploration rather than assert that one segment causes higher sales.

## 7. Data Limitations
- The source is one transaction-level sales table.
- No website sessions, leads, checkout stages or funnel events are present; funnel analysis is therefore not supported.
- Most customers have only one or a small number of recorded orders. Retention and churn conclusions would be weak.
- The available data is an observed sample, not necessarily a complete business population.
- The segment thresholds are business rules, not externally validated business definitions.

## 8. Reproducibility
Run from the project root:
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## 9. Conclusion
The project defines five practical KPIs, performs an interpretable customer segmentation deep-dive, and delivers a filterable interactive sales dashboard. The dashboard can be published through Streamlit Community Cloud after the repository is pushed to GitHub.
