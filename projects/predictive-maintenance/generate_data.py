"""Synthetic sensor histories. No real factory or employer data is used."""
from datetime import date
import numpy as np
import pandas as pd

SENSOR_COLUMNS = ["temperature_c", "vibration_mm_s", "pressure_kpa"]

def generate_sensor_data(n_assets=40, seed=42):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    rows = []
    for asset_id in range(1, n_assets + 1):
        wear = float(rng.uniform(0.03, 0.35))
        for day in dates:
            wear += float(rng.uniform(0.005, 0.018))
            temp = 57.0 + 15.0 * wear + float(rng.normal(0, 2.1))
            vibration = 1.1 + 2.5 * wear + float(rng.normal(0, 0.21))
            pressure = 110.0 - 8.5 * wear + float(rng.normal(0, 1.8))
            chance = float(np.clip(0.001 + 0.032 * max(0, wear - 1.1), 0.001, 0.16))
            failed_today = int(rng.random() < chance)
            rows.append((asset_id, day, temp, vibration, pressure, failed_today))
            if failed_today:
                wear = float(rng.uniform(0.03, 0.2))
    frame = pd.DataFrame(rows, columns=["asset_id", "date", *SENSOR_COLUMNS, "failed_today"])
    return frame

def add_past_features_and_target(data, horizon=7):
    """Features use past/current readings; labels use only future failure events."""
    data = data.sort_values(["asset_id", "date"]).copy()
    groups = data.groupby("asset_id", sort=False)
    for feature in SENSOR_COLUMNS:
        data[feature + "_7d_avg"] = (
            groups[feature].transform(lambda s: s.rolling(7, min_periods=1).mean())
        )
    next_failure = np.zeros(len(data), dtype=int)
    for day_ahead in range(1, horizon + 1):
        shifted = groups["failed_today"].shift(-day_ahead).fillna(0).to_numpy()
        next_failure += shifted.astype(int)
    data["failure_next_7d"] = (next_failure > 0).astype(int)
    # Avoid records with an incomplete future forecast window.
    last_usable_date = data["date"].max() - pd.Timedelta(days=horizon)
    return data.loc[
        (data["date"] <= last_usable_date) & (data["failed_today"] == 0)
    ].reset_index(drop=True)

def split_by_time(data):
    """Seven-day embargo between adjacent periods keeps label windows separate."""
    train = data.loc[data["date"] <= "2025-08-15"].copy()
    valid = data.loc[(data["date"] >= "2025-08-23") & (data["date"] <= "2025-10-15")].copy()
    test = data.loc[data["date"] >= "2025-10-23"].copy()
    assert train["date"].max() + pd.Timedelta(days=7) < valid["date"].min()
    assert valid["date"].max() + pd.Timedelta(days=7) < test["date"].min()
    return train, valid, test

if __name__ == "__main__":
    data = add_past_features_and_target(generate_sensor_data())
    print("Rows:", len(data), "Positive fraction:", round(data["failure_next_7d"].mean(), 4))
