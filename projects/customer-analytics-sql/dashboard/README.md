# Browser dashboard — synthetic SQL results

Open `index.html` in your browser. The default charts and KPIs are pre-populated with results from the project's **synthetic** retail generator and SQL queries (seed 42).

The generated sample is bundled in `sample-results.js` so the dashboard works offline; you do not need to install a local server.

For an independent rerun:

1. Install the project dependencies and run `python projects/customer-analytics-sql/src/run_analysis.py` from the repository root.
2. Open the dashboard and select **Load SQL result CSVs**.
3. Select all four generated files under `projects/customer-analytics-sql/outputs/`. The charts update from those files.

The synthetic input deliberately assigns around 22% of customers to a **non-purchasing group** to make conversion/segmentation calculations meaningful; that is a modelling assumption, not an empirical finding.

This is a browser-based dashboard, **not a Power BI .pbix report**. Use [the Power BI guide](../POWER_BI_BUILD.md) for a Power BI Desktop implementation.

No browser-uploaded CSV data is sent to a server.
