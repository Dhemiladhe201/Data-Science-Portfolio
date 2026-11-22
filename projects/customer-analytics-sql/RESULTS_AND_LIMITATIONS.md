# Notes from the generated sample (synthetic data)

Run the SQL scripts before drawing any conclusions. For the fixed random seed and 1,000 fictional customers, the example produces:

| Metric | Value |
| --- | ---: |
| Acquired signups | 1,000 |
| Customers with at least one completed order | 780 |
| Paying customer rate | 78.0% |
| Completed orders | 8,183 |
| Revenue over the simulated period | £404,503.00 |
| High-value active segment | 221 customers |
| High-value at-risk segment | 13 customers |
| Never purchased | 220 customers |

These figures are **not predictions, benchmarks or outcomes at a real retailer**. The generator intentionally draws a subset of buyers, so the 78% conversion rate should not be interpreted as independently discovered behaviour.

## Practical interpretation

The fact that total simulated monthly revenue grows over time is partly a consequence of new customers entering the generator. It doesn't prove marketing effectiveness or organic growth. Channel totals are descriptive only: without customer acquisition costs, a channel revenue comparison is **not** ROI.

Cohort sizes vary considerably; later cohorts may have few observations and unstable percentages. A responsible report would add cohort sizes, filter very small groups and distinguish incomplete recent cohorts.

A real company would require reconciled finance data, explicit refund treatment, an agreed conversion definition, acquisition spend and privacy review before using the dashboard to make decisions.
