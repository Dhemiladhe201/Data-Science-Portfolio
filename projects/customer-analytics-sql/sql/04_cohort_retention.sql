-- First completed purchase defines cohort and repeat buying defines retention.
WITH buyer_months AS (
 SELECT DISTINCT customer_id, substr(order_date,1,7) AS month,
        CAST(substr(order_date,1,4) AS INTEGER)*12+CAST(substr(order_date,6,2) AS INTEGER) AS month_index
 FROM orders WHERE status='completed'
), first_buy AS (
 SELECT customer_id, MIN(month_index) AS cohort_index, MIN(month) AS cohort_month
 FROM buyer_months GROUP BY customer_id
), activity AS (
 SELECT f.cohort_month, b.month_index-f.cohort_index AS months_since_first_purchase,
        COUNT(DISTINCT b.customer_id) AS active_buyers
 FROM buyer_months b JOIN first_buy f ON b.customer_id=f.customer_id
 GROUP BY f.cohort_month, months_since_first_purchase
), cohort_size AS (
 SELECT cohort_month, COUNT(*) AS cohort_customers
 FROM first_buy GROUP BY cohort_month
)
SELECT a.cohort_month, a.months_since_first_purchase,a.active_buyers,
       c.cohort_customers, ROUND(100.0*a.active_buyers/c.cohort_customers,1) AS retention_pct
FROM activity a JOIN cohort_size c ON a.cohort_month=c.cohort_month
WHERE a.months_since_first_purchase BETWEEN 0 AND 6
ORDER BY a.cohort_month,a.months_since_first_purchase;
