# Power BI build notes: customer analytics

This project already exports four SQL-derived CSV files. Use them to build an actual Power BI report **in Power BI Desktop**. The repository also contains an independent browser-based dashboard preview; that HTML file is **not** a .pbix report.

## 1. Generate the data

From the repository root:

```bash
python -m pip install -r projects/customer-analytics-sql/requirements.txt
python projects/customer-analytics-sql/src/run_analysis.py
```

Under `projects/customer-analytics-sql/outputs/`, you should now have:

- `01_monthly_revenue.csv`
- `02_acquisition_channels.csv`
- `03_customer_segments.csv`
- `04_cohort_retention.csv`

The files contain simulated retail data. Store the report locally as `Customer_Analytics.pbix`.

## 2. Import and name tables

In Power BI Desktop, choose *Get data → Text/CSV* for each CSV. Rename the resulting tables to `MonthlyRevenue`, `Channels`, `CustomerSegments`, and `CohortRetention`.

Set:
- `MonthlyRevenue[month]` as text in yyyy-mm format (sorts chronologically); optionally create a first-of-month date column.
- Revenue and monetary columns as **Decimal number**, currency **GBP**.
- Cohort `months_since_first_purchase` and count columns as **Whole number**.
- `CohortRetention[cohort_month]` as text for the matrix rows.
- Segment names as text; `CustomerSegments[customer_id]` as a whole number.

These four tables are separate aggregates. Do **not** create many-to-many relationships between them just because they share similar names or months. For detailed cross-filtering, build a star schema from the source `customers` and `orders` tables instead.

## 3. Measures

Create these measures (change the table names if you used different names):

```dax
Total Revenue GBP = SUM(MonthlyRevenue[revenue_gbp])

Total Orders = SUM(MonthlyRevenue[orders])

Average Order Value GBP =
    DIVIDE([Total Revenue GBP], [Total Orders])

Acquired Customers = SUM(Channels[acquired_customers])

Paying Customer Rate =
    DIVIDE(SUM(Channels[paying_customers]),
           SUM(Channels[acquired_customers]))

Month-1 Cohort Retention =
    VAR MonthOne = FILTER(CohortRetention,
                          CohortRetention[months_since_first_purchase] = 1)
    RETURN DIVIDE(SUMX(MonthOne, CohortRetention[active_buyers]),
                  SUMX(MonthOne, CohortRetention[cohort_customers]))
```

Note that `SUM(MonthlyRevenue[active_customers])` counts customer-months, **not** distinct customers across months. Avoid labelling that sum as "unique customers".

## 4. Layout

Use a clear two-page report:

**Page 1 — Commercial overview**
- Cards: Total Revenue, Total Orders, Average Order Value, Paying Customer Rate
- Line chart: revenue by month
- Horizontal bar: revenue by acquisition channel
- Table: acquisition channels with revenue per customer
- Note on footer: "Synthetic educational dataset; not a real employer report"

**Page 2 — Customer behaviour**
- Bar: count of customers by `customer_segment`
- Matrix: rows = cohort_month, columns = months_since_first_purchase, values = retention_pct; apply conditional background colour
- A small text box explaining that cohort month is *first completed purchase*, not signup

Use muted colours and precise units. Avoid decorative graphics that compete with the charts.

## 5. Quality checks before sharing screenshots

- Revenue in monthly table should reconcile with the sum of completed `orders.amount_gbp`.
- AOV should calculate as revenue divided by number of completed orders, not the average of monthly AOVs.
- Cohort month 0 retention should be 100% for eligible customers.
- Refunds are excluded rather than netted; explain this limitation.
- Channel revenue is not return on advertising spend without marketing cost data.

A completed .pbix report and its screenshots should only be shown after they have been constructed in Power BI Desktop and checked.
