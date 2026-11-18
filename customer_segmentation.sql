-- ApexPlanet Task 3: KPI and customer segmentation queries (SQLite)
-- Run against sales table imported from data/cleaned_sales_dataset.csv

-- Core KPIs
SELECT
  SUM(Total_Sales) AS total_revenue,
  COUNT(DISTINCT Order_ID) AS distinct_orders,
  ROUND(SUM(Total_Sales) * 1.0 / COUNT(DISTINCT Order_ID), 2) AS average_order_value,
  COUNT(DISTINCT Customer_ID) AS unique_customers,
  SUM(Quantity) AS units_sold
FROM sales;

-- Customer-level profile
WITH customer_metrics AS (
  SELECT Customer_ID,
         SUM(Total_Sales) AS customer_spend,
         COUNT(DISTINCT Order_ID) AS order_count,
         SUM(Quantity) AS units_purchased,
         MAX(Order_Date) AS last_order_date
  FROM sales
  GROUP BY Customer_ID
),
threshold AS (
  SELECT
    (SELECT customer_spend
     FROM customer_metrics
     ORDER BY customer_spend
     LIMIT 1 OFFSET (SELECT CAST(COUNT(*) * 0.75 AS INTEGER) FROM customer_metrics)
    ) AS p75_spend
)
SELECT c.*,
       CASE
         WHEN c.customer_spend >= t.p75_spend THEN 'High-Value Customer'
         WHEN c.order_count > 1 THEN 'Repeat Customer'
         ELSE 'Standard'
       END AS customer_segment
FROM customer_metrics c CROSS JOIN threshold t
ORDER BY c.customer_spend DESC;
