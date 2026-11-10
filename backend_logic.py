import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from backend_data import LAKES

COLS = ["Time", "Village", "Lake", "Reporter", "Note"]


@st.cache_data(ttl=600)
def get_weather():
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast", timeout=10, params={
            "latitude": 35.85, "longitude": 71.78, "elevation": 3800,
            "hourly": "temperature_2m,relative_humidity_2m", "timezone": "Asia/Karachi"})
        r.raise_for_status()
        h = r.json()["hourly"]
        return pd.DataFrame({"Time": pd.to_datetime(h["time"]), "Temperature (°C)": h["temperature_2m"],
                             "Humidity (%)": h["relative_humidity_2m"]}), True
    except Exception:
        t = pd.date_range(end=datetime.now(), periods=48, freq="h")
        return pd.DataFrame({"Time": t, "Temperature (°C)": [4 + (i % 8) * 0.8 for i in range(48)],
                             "Humidity (%)": [60 - i % 5 for i in range(48)]}), False


def level(score):
    return "HIGH" if score >= 65 else "MEDIUM" if score >= 35 else "LOW"


def compute(wx, temp_slider, lake):
    base = round(wx["Temperature (°C)"].head(24).mean(), 1)
    temp = max(base, temp_slider)
    return dict(base=base, temp=temp, lake=lake, score=min(100, round(temp / 15 * 50 + lake / 50 * 50)),
                discharge=round(temp * 210 + lake * 18), critical=temp > 8 and lake >= 20)


def lake_table(score, reports):
    counts = reports["Lake"].value_counts()
    df = pd.DataFrame([dict(Lake=n, District=d, lat=la, lon=lo, Villages=v, Score=min(100, round(score * w)),
                            Reports=int(counts.get(n, 0))) for n, d, la, lo, v, w in LAKES])
    df["Risk"] = df.Score.map(level)
    return df


def load_reports():
    return pd.read_csv("reports.csv") if os.path.exists("reports.csv") else pd.DataFrame(columns=COLS)


def add_report(village, lake, name, note):
    row = pd.DataFrame([dict(zip(COLS, [datetime.now().strftime("%Y-%m-%d %H:%M"), village, lake, name, note]))])
    st.session_state.reports = pd.concat([st.session_state.reports, row], ignore_index=True)
    st.session_state.reports.to_csv("reports.csv", index=False)
