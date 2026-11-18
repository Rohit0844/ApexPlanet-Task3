# ApexPlanet Task 3 — Deep-Dive Analysis & Interactive Dashboarding

**Project:** Sales Intelligence Dashboard with Customer Segmentation  
**Author:** Rohit Joshi

## Folder structure
- `data/cleaned_sales_dataset.csv` — Task 1/2 prepared dataset
- `dashboard/app.py` — interactive Streamlit dashboard
- `reports/Task3_Deep_Dive_Report.md` — KPI definitions, segmentation method, findings and limitations
- `requirements.txt` — Python dependencies

## Run the dashboard locally
1. Install Python 3.10 or newer.
2. Open Command Prompt / Terminal in this project folder.
3. Run:
   ```bash
   pip install -r requirements.txt
   streamlit run dashboard/app.py
   ```
4. A browser tab should open with the dashboard. If not, copy the Local URL shown in the terminal (usually `http://localhost:8501`).

## Publish a live dashboard (Streamlit Community Cloud)
1. Upload this project folder to a public GitHub repository named `Rohit-Joshi-ApexPlanet-Task3`.
2. Open https://share.streamlit.io/ and sign in using GitHub.
3. Select **Create app**, choose your repository and branch.
4. Set the Main file path to `dashboard/app.py`.
5. Click **Deploy**. Copy the generated public app URL for your internship submission.
6. Do not submit a live URL until deployment succeeds and you have tested the filters.

## KPI definitions
- Total Revenue = SUM(Total_Sales)
- Distinct Orders = COUNT(DISTINCT Order_ID)
- Average Order Value = Total Revenue / Distinct Orders
- Unique Customers = COUNT(DISTINCT Customer_ID)
- Units Sold = SUM(Quantity)

## Deep-dive
Rule-based customer segmentation using total customer spend and distinct order count. See the report for thresholds, rationale and limitations.

## Important data note
The source data has no funnel-event fields and limited repeat-order history. The project therefore does not claim funnel conversion, churn prediction or robust retention analysis. Customer segments are descriptive business-rule groups.
