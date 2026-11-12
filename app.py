import time
import streamlit as st

import frontend_theme as theme
from backend_data import EVENTS
from backend_logic import evaluate_system, get_all_lakes_live_telemetry, load_reports
import frontend_alert_tab as alert_tab
import frontend_climate_tab as climate_tab
import frontend_map_tab as map_tab
import frontend_report_tab as report_tab

st.set_page_config(page_title="Sar-Ab | Autonomous GLOF Early Warning", page_icon="🏔️", layout="wide")


def load_event():
    st.session_state.temp, st.session_state.lake = EVENTS[st.session_state.event][:2]


st.session_state.setdefault("dark", True)
st.session_state.setdefault("mode", "Autonomous Live")
st.session_state.setdefault("auto_refresh", True)
st.session_state.setdefault("event", "Normal baseline")
if "temp" not in st.session_state:
    load_event()
if "reports" not in st.session_state:
    st.session_state.reports = load_reports()
st.session_state.setdefault("alerts", [])
theme.inject()

# ---------- sidebar ----------
sb = st.sidebar
sb.toggle("🌙 Dark mode", key="dark")
sb.radio("📡 Operating Mode", ["Autonomous Live", "Scenario Simulator"], key="mode")

if st.session_state.mode == "Autonomous Live":
    sb.success("Autonomous watchdog active: continuously polling 7 glacial lake coordinates via Open-Meteo & satellite layers.")
    sb.toggle("🔄 Auto-poll feed every 60s", key="auto_refresh")
else:
    sb.header("⚙️ Scenario simulator")
    sb.caption("Override live telemetry to stress-test historical GLOF disasters.")
    sb.selectbox("Load historical event", list(EVENTS), key="event", on_change=load_event)
    sb.caption(EVENTS[st.session_state.event][2])
    sb.slider("🌡️ High-altitude temperature (°C)", 0.0, 15.0, step=0.5, key="temp")
    sb.slider("🌊 Lake surface expansion (%)", 0, 50, key="lake")

with sb.expander("How the autonomous engine works"):
    st.write(
        "In Autonomous Live mode, Sar-Ab queries real-time high-altitude temperatures and precipitation across 7 glacial lakes "
        "in Chitral, Hunza, Nagar, and Ghizer, fuses them with verified villager reports, and automatically "
        "flags downstream villages at risk."
    )

# ---------- live telemetry & evaluation ----------
live_df, wx, live, last_sync = get_all_lakes_live_telemetry()
s = evaluate_system(
    live_df,
    st.session_state.reports,
    mode=st.session_state.mode,
    sim_temp=st.session_state.temp,
    sim_lake=st.session_state.lake,
)
s.update(wx=wx, live=live)

# ---------- hero ----------
h1, h2 = st.columns([3, 1.3])
h1.markdown(
    '<div class="hero"><h1>Sar-Ab <span>سر آب</span></h1>'
    '<p>Autonomous Glacial Lake Outburst Flood (GLOF) Early Warning & Community Telemetry System</p></div>',
    unsafe_allow_html=True,
)
h2.markdown(
    f'<div style="text-align:right;padding-top:1rem">'
    f'<span class="pill">{"🟢 Live API Feed" if live else "🟡 Offline Cache"}</span>'
    f'<span class="pill">Synced {last_sync}</span></div>',
    unsafe_allow_html=True,
)

# ---------- autonomous early-warning alarm banner ----------
g, k = st.columns([1, 1.6])
g.markdown(theme.gauge(s["score"]), unsafe_allow_html=True)

if s["critical"]:
    flagged = ", ".join(f"{r.Lake} ({r.District} — {r.Villages} villages)" for r in s["critical_lakes"].itertuples())
    k.markdown(
        f'<div class="alert red"><b>🚨 AUTOMATIC GLOF ALARM TRIGGERED</b><br>'
        f'High-risk threshold breached at: <b>{flagged}</b>.<br>'
        f'Immediate downstream evacuation advisory active for <b>{s["alert_villages"]} villages</b>.</div>',
        unsafe_allow_html=True,
    )
else:
    k.markdown(
        f'<div class="alert green"><b>✅ CONTINUOUS MONITORING ACTIVE — ALL BASINS NOMINAL</b><br>'
        f'All 7 glacial lakes are within safe thermal & discharge limits. Watching {int(s["df"].Villages.sum())} downstream villages.</div>',
        unsafe_allow_html=True,
    )

a, b = k.columns(2)
a.markdown(theme.card("Peak Basin Temp", f"{s['temp']} °C", f"7-lake live average: {s['base']} °C"), unsafe_allow_html=True)
b.markdown(theme.card("Est. Surface Expansion", f"+{s['lake']}%", st.session_state.mode), unsafe_allow_html=True)
c, d = k.columns(2)
c.markdown(theme.card("Peak Water Discharge", f"{s['discharge']:,} m³/s" + (" ⚠️" if s["discharge"] > 1800 else ""), "Safety threshold: 1,800 m³/s"), unsafe_allow_html=True)
d.markdown(theme.card("Villages Watched / Alerted", f"{s['alert_villages']} / {int(s['df'].Villages.sum())}", f"{int(s['df'].Reports.sum())} verified community reports"), unsafe_allow_html=True)

# ---------- tabs ----------
t1, t2, t3, t4 = st.tabs(["🗺️ Live Satellite & Lake Map", "📈 Climate & Discharge Trends", "📱 Gaon ki Khabar (Live Feed)", "📢 Alert Centre"])
with t1:
    map_tab.render(s)
with t2:
    climate_tab.render(s)
with t3:
    report_tab.render(s)
with t4:
    alert_tab.render(s)

st.divider()
st.caption("Sar-Ab · Continuous Multi-Lake Telemetry (Open-Meteo + Esri Satellite Basemaps + Ground Crowdsourcing)")

# Continuous background polling loop when in Autonomous Live mode
if st.session_state.mode == "Autonomous Live" and st.session_state.auto_refresh:
    time.sleep(60)
    st.rerun()
