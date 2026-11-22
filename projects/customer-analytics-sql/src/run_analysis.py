"""Run the four SQL reports and export CSVs for a BI dashboard."""
import sqlite3
from pathlib import Path
import pandas as pd
from generate_data import generate

ROOT = Path(__file__).resolve().parents[1]
def main():
    database = generate()
    with sqlite3.connect(database) as conn:
        for sql_file in sorted((ROOT / "sql").glob("*.sql")):
            query = sql_file.read_text(encoding="utf-8")
            frame = pd.read_sql_query(query, conn)
            output = ROOT / "outputs" / (sql_file.stem + ".csv")
            frame.to_csv(output, index=False)
            print(f"{sql_file.name}: {len(frame)} rows -> {output.name}")

if __name__ == "__main__":
    main()
