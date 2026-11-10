from datetime import datetime

import pandas as pd
import streamlit as st

import frontend_theme as theme
from backend_data import MESSAGES


def render(s):
    df = s["df"]
    st.write("Pick a lake and a language, preview the warning, then send it. Sending is simulated: no real SMS goes out.")
    target = st.selectbox("Lake", df.sort_values("Score", ascending=False).Lake)
    lang = st.radio("Language", list(MESSAGES), horizontal=True)
    st.markdown(f'<div class="card" dir="{"ltr" if lang == "English" else "rtl"}" style="font-size:1.15rem">{MESSAGES[lang].format(lake=target)}</div>', unsafe_allow_html=True)
    n = int(df[df.Lake == target].Villages.iloc[0])
    if st.button("📲 Send alert (simulation)"):
        st.session_state.alerts.append(dict(Time=datetime.now().strftime("%H:%M:%S"), Lake=target, Language=lang, Villages=n))
        st.success(f"Demo: alert queued for {n} villages near {target}.")
    if st.session_state.alerts:
        theme.table(pd.DataFrame(st.session_state.alerts).iloc[::-1])
    st.caption("Roadmap: add Khowar, the main language of Chitral, and connect a real SMS gateway.")
