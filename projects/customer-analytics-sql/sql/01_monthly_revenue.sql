-- Revenue and active buyers from completed orders.
WITH completed AS (
 SELECT substr(order_date,1,7) AS month, customer_id, amount_gbp
 FROM orders
 WHERE status = 'completed'
)
SELECT month,
       COUNT(*) AS orders,
       COUNT(DISTINCT customer_id) AS active_customers,
       ROUND(SUM(amount_gbp),2) AS revenue_gbp,
       ROUND(AVG(amount_gbp),2) AS average_order_value_gbp
FROM completed
GROUP BY month ORDER BY month;
