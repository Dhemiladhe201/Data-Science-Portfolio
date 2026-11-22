# Customer analytics with SQL

A small retail reporting project built to practise translating business questions into SQL. The dataset is **synthetic**; no real client transactions are used.

## Questions asked
1. How do completed orders, active customers and revenue change by month?
2. Which acquisition channels contribute the most revenue?
3. Which customers are high-value and active, and which appear at risk of lapsing?
4. What share of each first-purchase cohort returns in later months?

The generator deliberately assigns about 22% of synthetic signups to a non-purchasing group, so customer-conversion and segmentation calculations have a meaningful denominator. This percentage is an assumption, not an observed commercial benchmark.

The project creates a SQLite database with `customers` and `orders`, executes four queries and exports CSV files that can be used in Power BI.

## Run from the repository root
```bash
python -m pip install -r projects/customer-analytics-sql/requirements.txt
python projects/customer-analytics-sql/src/run_analysis.py
python -m unittest discover -s projects/customer-analytics-sql/tests -v
```

The generator uses a fixed seed. The database and CSVs are saved under `outputs/`, which is excluded from Git.

## Reporting choices
- Revenue includes **completed** orders only; refunded orders are excluded rather than treated as a negative adjustment.
- Cohorts start at the **first completed purchase**, not signup.
- Retention means at least one completed purchase in that month; it isn't subscription retention.
- Segmentation thresholds are illustrative, not a validated customer-lifetime-value model.
- Channel revenue is not return on ad spend: no acquisition cost data exists.

## Results and dashboard

- [Browser dashboard with generated sample SQL results](dashboard/)
- [Interpretation and limitations](RESULTS_AND_LIMITATIONS.md)
- [Power BI Desktop build instructions](POWER_BI_BUILD.md)

## Suggested dashboard
In Power BI, show monthly revenue and average order value, acquisition channels, customer segments and a cohort-retention heatmap. Label the dashboard clearly as synthetic data.

## What I'd improve before using a real retail dataset
Reconcile revenue against finance, model refunds and taxes, inspect acquisition attribution and check whether customer-level reporting is appropriate under privacy requirements.
