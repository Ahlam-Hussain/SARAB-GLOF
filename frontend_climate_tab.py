import pandas as pd
import streamlit as st

import frontend_theme as theme


def render(s):
    t = theme.colors()
    st.caption("Hourly forecast for the Chitral basin, downscaled to 3,800 m (Open-Meteo)." + ("" if s["live"] else " Offline: showing demo values."))
    theme.line(s["wx"].set_index("Time"), "T", [t["c1"], t["c2"]])
    st.subheader("What if the lake keeps growing?")
    w = pd.DataFrame({"Expansion": range(0, 51, 5)}).set_index("Expansion")
    w["Discharge (m³/s)"] = s["temp"] * 210 + w.index * 18
    w["Safety limit"] = 1800
    theme.line(w, "Q", ["#e5484d", t["muted"]])
