-- Illustrative RFM-style groupings with a fixed reference date.
WITH totals AS (
 SELECT c.customer_id,
        CAST(julianday('2026-07-01')-julianday(MAX(CASE WHEN o.status='completed' THEN o.order_date END)) AS INT) AS recency_days,
        SUM(CASE WHEN o.status='completed' THEN 1 ELSE 0 END) AS frequency,
        ROUND(SUM(CASE WHEN o.status='completed' THEN o.amount_gbp ELSE 0 END),2) AS monetary_gbp
 FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id
 GROUP BY c.customer_id
), ranked AS (
 SELECT *, NTILE(4) OVER (ORDER BY monetary_gbp) AS monetary_quartile
 FROM totals
)
SELECT customer_id,recency_days,frequency,monetary_gbp,
 CASE WHEN frequency=0 THEN 'never_purchased'
      WHEN recency_days<=90 AND monetary_quartile=4 THEN 'high_value_active'
      WHEN recency_days>180 AND monetary_quartile>=3 THEN 'high_value_at_risk'
      ELSE 'other'
 END AS customer_segment
FROM ranked ORDER BY monetary_gbp DESC;
