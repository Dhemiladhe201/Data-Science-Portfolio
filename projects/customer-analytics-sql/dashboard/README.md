# Browser dashboard — independent preview

Open `index.html` in your browser. It initially shows a clearly labelled **illustrative preview** so the layout is visible without any setup.

To display the project's actual SQL results (still synthetic records):

1. Run `python projects/customer-analytics-sql/src/run_analysis.py` from the repository root.
2. Open this dashboard in a browser and select **Load SQL result CSVs**.
3. Select all four files from `projects/customer-analytics-sql/outputs/`. The charts and KPI cards will update immediately.

This is a standalone HTML dashboard with native SVG charts and no server dependency. It is **not a Power BI .pbix report**. Follow [the Power BI build guide](../POWER_BI_BUILD.md) to create the actual Power BI deliverable.

The dashboard uses only data you select in your browser; it does not upload files to a server.
