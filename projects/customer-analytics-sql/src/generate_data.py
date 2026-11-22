"""Create a reproducible SQLite retail dataset using synthetic records."""
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def generate(db_path=None, seed=42, customers=1000, orders=9000):
    path = Path(db_path) if db_path else ROOT / "outputs" / "retail.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    with sqlite3.connect(path) as conn:
        conn.executescript("""
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS customers;
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            signup_date TEXT NOT NULL,
            region TEXT NOT NULL,
            acquisition_channel TEXT NOT NULL
        );
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            amount_gbp REAL NOT NULL CHECK(amount_gbp >= 0),
            status TEXT NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        );
        """)
        start = date(2024, 1, 1)
        customers_data = []
        for i in range(1, customers + 1):
            signup = start + timedelta(days=rng.randint(0, 560))
            customers_data.append((
                i, signup.isoformat(),
                rng.choice(["London", "North", "Midlands", "Scotland"]),
                rng.choices(["Organic", "Paid Search", "Referral", "Social"],
                            weights=[0.38, 0.30, 0.18, 0.14])[0]
            ))
        conn.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers_data)
        # By design, some signups never purchase; this is a simulation assumption.
        buyer_pool = rng.sample(customers_data, k=max(1, round(customers * 0.78)))
        orders_data = []
        for i in range(1, orders + 1):
            customer = rng.choice(buyer_pool)
            signed_up = date.fromisoformat(customer[1])
            last_day = (date(2026, 6, 30) - signed_up).days
            order_date = signed_up + timedelta(days=rng.randint(0, last_day))
            amount = round(max(4.99, rng.lognormvariate(3.7, 0.65)), 2)
            status = rng.choices(["completed", "cancelled", "refunded"],
                                 weights=[0.91, 0.06, 0.03])[0]
            orders_data.append((i, customer[0], order_date.isoformat(), amount, status))
        conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders_data)
    return path

if __name__ == "__main__":
    print(generate())
