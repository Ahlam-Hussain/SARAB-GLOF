import streamlit as st

import frontend_theme as theme
from backend_data import EVENTS
from backend_logic import compute, get_weather, lake_table, load_reports
import frontend_alert_tab as alert_tab
import frontend_climate_tab as climate_tab
import frontend_map_tab as map_tab
import frontend_report_tab as report_tab

st.set_page_config(page_title="Sar-Ab | GLOF Early Warning", page_icon="🏔️", layout="wide")


def load_event():
    st.session_state.temp, st.session_state.lake = EVENTS[st.session_state.event][:2]


st.session_state.setdefault("dark", True)
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
sb.header("⚙️ Scenario simulator")
sb.caption("Change the conditions live and watch every lake, the map and the alerts react.")
sb.selectbox("Load historical event", list(EVENTS), key="event", on_change=load_event)
sb.caption(EVENTS[st.session_state.event][2])
sb.slider("🌡️ High-altitude temperature (°C)", 0.0, 15.0, step=0.5, key="temp")
sb.slider("🌊 Lake surface expansion (%)", 0, 50, key="lake")
with sb.expander("How the score works"):
    st.write("Risk index = temperature (50%) + lake expansion (50%), scaled per lake by a vulnerability weight. "
             "Discharge = temperature × 210 + expansion × 18. This is an illustrative model, not a calibrated forecast.")

# ---------- numbers ----------
wx, live = get_weather()
s = compute(wx, st.session_state.temp, st.session_state.lake)
s.update(wx=wx, live=live, df=lake_table(s["score"], st.session_state.reports))
s["alert_villages"] = int(s["df"][s["df"].Risk == "HIGH"].Villages.sum())

# ---------- hero ----------
h1, h2 = st.columns([3, 1])
h1.markdown('<div class="hero"><h1>Sar-Ab <span>سر آب</span></h1>'
            '<p>Head of Water · early warning for glacial lake floods in high-altitude communities</p></div>', unsafe_allow_html=True)
h2.markdown(f'<div style="text-align:right;padding-top:1rem"><span class="pill">{"● Live weather" if live else "○ Offline demo weather"}</span>'
            '<span class="pill">Simulation</span></div>', unsafe_allow_html=True)

g, k = st.columns([1, 1.6])
g.markdown(theme.gauge(s["score"]), unsafe_allow_html=True)
if s["critical"]:
    k.markdown('<div class="alert red"><b>🚨 Critical GLOF warning</b><br>High temperature and fast lake growth mean immediate flood risk downstream.</div>', unsafe_allow_html=True)
else:
    k.markdown('<div class="alert green"><b>✅ Status: nominal</b><br>All monitored lakes are inside the simulated safety limits.</div>', unsafe_allow_html=True)
a, b = k.columns(2)
a.markdown(theme.card("Altitude temperature", f"{s['temp']} °C", f"Forecast baseline {s['base']} °C at 3,800 m"), unsafe_allow_html=True)
b.markdown(theme.card("Lake area change", f"+{s['lake']}%", "Simulated"), unsafe_allow_html=True)
c, d = k.columns(2)
c.markdown(theme.card("Water discharge", f"{s['discharge']:,} m³/s" + (" ⚠️" if s["discharge"] > 1800 else ""), "Illustrative limit 1,800 m³/s"), unsafe_allow_html=True)
d.markdown(theme.card("Villages on alert", s["alert_villages"], f"{int(s['df'].Reports.sum())} community reports"), unsafe_allow_html=True)

# ---------- tabs: one file per tab in tabs/ ----------
t1, t2, t3, t4 = st.tabs(["🗺️ Lake map", "📈 Climate trends", "📱 Gaon ki Khabar (report)", "📢 Alert centre"])
with t1:
    map_tab.render(s)
with t2:
    climate_tab.render(s)
with t3:
    report_tab.render(s)
with t4:
    alert_tab.render(s)

st.divider()
st.caption("Sar-Ab · Environment stream hackathon · All lake data and alerts are sample or simulated values.")
