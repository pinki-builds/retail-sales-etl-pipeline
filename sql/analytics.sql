
-- 1. Total records and overall sales metrics
SELECT
    COUNT(*) AS total_rows,
    ROUND(SUM(Quantity * UnitPrice), 2) AS net_sales,
    COUNT(DISTINCT InvoiceNo) AS unique_invoices,
    COUNT(DISTINCT CustomerID) AS unique_customers
FROM retail_transactions;


-- 2. Top 10 products by net sales
SELECT
    StockCode,
    MAX(Description) AS product_name,
    ROUND(SUM(Quantity * UnitPrice), 2) AS net_sales
FROM retail_transactions
GROUP BY StockCode
ORDER BY net_sales DESC
LIMIT 10;


-- 3. Revenue by country
SELECT
    Country,
    ROUND(SUM(Quantity * UnitPrice), 2) AS net_sales
FROM retail_transactions
GROUP BY Country
ORDER BY net_sales DESC
LIMIT 10;


-- 4. Monthly sales trend
SELECT
    strftime('%Y-%m', InvoiceDate) AS sales_month,
    ROUND(SUM(Quantity * UnitPrice), 2) AS net_sales
FROM retail_transactions
GROUP BY sales_month
ORDER BY sales_month;


-- 5. Daily sales ranking using a window function
WITH daily_sales AS (
    SELECT
        date(InvoiceDate) AS sales_date,
        SUM(Quantity * UnitPrice) AS revenue
    FROM retail_transactions
    GROUP BY date(InvoiceDate)
)
SELECT
    sales_date,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM daily_sales
ORDER BY revenue_rank
LIMIT 10;
