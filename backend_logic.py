import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from backend_data import LAKES

COLS = ["Time", "Village", "Lake", "Reporter", "Note"]


@st.cache_data(ttl=300)
def get_all_lakes_live_telemetry():
    """Fetches real-time temperature, precipitation, and telemetry for ALL 7 glacial lakes simultaneously."""
    lats = ",".join(str(x[2]) for x in LAKES)
    lons = ",".join(str(x[3]) for x in LAKES)
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            timeout=10,
            params={
                "latitude": lats,
                "longitude": lons,
                "current": "temperature_2m,precipitation,rain,snowfall",
                "hourly": "temperature_2m,relative_humidity_2m",
                "timezone": "Asia/Karachi",
            },
        )
        r.raise_for_status()
        payload = r.json()
        if isinstance(payload, dict):
            payload = [payload]

        live_rows = []
        for idx, (name, dist, lat, lon, villages, weight) in enumerate(LAKES):
            curr = payload[idx].get("current", {})
            temp_c = curr.get("temperature_2m", 5.0)
            precip = curr.get("precipitation", 0.0)
            live_rows.append({
                "Lake": name,
                "District": dist,
                "lat": lat,
                "lon": lon,
                "Villages": villages,
                "Weight": weight,
                "Live_Temp_C": round(float(temp_c), 1),
                "Precip_mm": round(float(precip), 1),
            })

        h = payload[0]["hourly"]
        wx_df = pd.DataFrame({
            "Time": pd.to_datetime(h["time"]),
            "Temperature (°C)": h["temperature_2m"],
            "Humidity (%)": h["relative_humidity_2m"],
        })
        return pd.DataFrame(live_rows), wx_df, True, datetime.now().strftime("%H:%M:%S")
    except Exception:
        t = pd.date_range(end=datetime.now(), periods=48, freq="h")
        wx_df = pd.DataFrame({
            "Time": t,
            "Temperature (°C)": [4 + (i % 8) * 0.8 for i in range(48)],
            "Humidity (%)": [60 - i % 5 for i in range(48)],
        })
        fallback_rows = [
            {"Lake": n, "District": d, "lat": la, "lon": lo, "Villages": v, "Weight": w, "Live_Temp_C": 6.2, "Precip_mm": 0.0}
            for n, d, la, lo, v, w in LAKES
        ]
        return pd.DataFrame(fallback_rows), wx_df, False, datetime.now().strftime("%H:%M:%S")


def level(score):
    return "HIGH" if score >= 65 else "MEDIUM" if score >= 35 else "LOW"


def evaluate_system(live_df, reports, mode="Autonomous Live", sim_temp=6.5, sim_lake=12):
    counts = reports["Lake"].value_counts()
    rows = []
    for r in live_df.itertuples():
        rep_count = int(counts.get(r.Lake, 0))
        if mode == "Autonomous Live":
            temp_used = r.Live_Temp_C
            est_expansion = max(0, round((temp_used - 2.0) * 2.5 + r.Precip_mm * 3.0, 1))
            raw_score = (max(0, temp_used) / 15.0 * 55) + (min(50, est_expansion) / 50.0 * 35) + (rep_count * 12)
        else:
            temp_used = max(r.Live_Temp_C, sim_temp)
            est_expansion = sim_lake
            raw_score = (temp_used / 15.0 * 50) + (sim_lake / 50.0 * 50) + (rep_count * 10)

        final_score = min(100, max(0, round(raw_score * r.Weight)))
        discharge = round(max(0, temp_used) * 210 + est_expansion * 18)
        rows.append({
            "Lake": r.Lake,
            "District": r.District,
            "lat": r.lat,
            "lon": r.lon,
            "Temp (°C)": temp_used,
            "Est. Growth (%)": est_expansion,
            "Discharge (m³/s)": discharge,
            "Villages": r.Villages,
            "Reports": rep_count,
            "Score": final_score,
            "Risk": level(final_score),
        })

    df = pd.DataFrame(rows)
    max_score = int(df["Score"].max())
    top_lake = df.sort_values("Score", ascending=False).iloc[0]
    critical_lakes = df[df["Risk"] == "HIGH"]

    return {
        "df": df,
        "score": max_score,
        "base": round(live_df["Live_Temp_C"].mean(), 1),
        "temp": top_lake["Temp (°C)"],
        "lake": top_lake["Est. Growth (%)"],
        "discharge": int(top_lake["Discharge (m³/s)"]),
        "critical": len(critical_lakes) > 0,
        "critical_lakes": critical_lakes,
        "alert_villages": int(df[df["Risk"].isin(["HIGH", "MEDIUM"])]["Villages"].sum()),
    }


def load_reports():
    return pd.read_csv("reports.csv") if os.path.exists("reports.csv") else pd.DataFrame(columns=COLS)


def add_report(village, lake, name, note):
    row = pd.DataFrame([dict(zip(COLS, [datetime.now().strftime("%Y-%m-%d %H:%M"), village, lake, name, note]))])
    st.session_state.reports = pd.concat([st.session_state.reports, row], ignore_index=True)
    st.session_state.reports.to_csv("reports.csv", index=False)