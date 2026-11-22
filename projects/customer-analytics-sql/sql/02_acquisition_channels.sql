-- Include all acquired customers, not just those with purchases.
WITH value_by_customer AS (
 SELECT c.customer_id, c.acquisition_channel,
        COALESCE(SUM(CASE WHEN o.status='completed' THEN o.amount_gbp ELSE 0 END),0) AS lifetime_revenue
 FROM customers c
 LEFT JOIN orders o ON o.customer_id=c.customer_id
 GROUP BY c.customer_id,c.acquisition_channel
)
SELECT acquisition_channel, COUNT(*) AS acquired_customers,
       SUM(CASE WHEN lifetime_revenue > 0 THEN 1 ELSE 0 END) AS paying_customers,
       ROUND(SUM(lifetime_revenue),2) AS total_revenue_gbp,
       ROUND(AVG(lifetime_revenue),2) AS average_revenue_per_customer_gbp
FROM value_by_customer
GROUP BY acquisition_channel
ORDER BY total_revenue_gbp DESC;
