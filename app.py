import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="SARAB - GLOF Early Warning", layout="wide")

st.title("🧊 SARAB - GLOF Early Warning System")
st.markdown("Chitral, KP - Glacier Lake Outburst Flood Detection")

# Sidebar
st.sidebar.header("Lake Status")
lake_size = st.sidebar.slider("Current Lake Size (sq meters)", 1000, 10000, 7500)
temp = st.sidebar.slider("Temperature at Glacier (°C)", -5, 15, 8)
days_hot = st.sidebar.slider("Hot days in row", 0, 7, 4)

# Logic
risk = "GREEN - Safe"
color = "green"
if lake_size > 6000 and temp > 5 and days_hot >= 3:
    risk = "RED - HIGH RISK! Evacuate"
    color = "red"
elif lake_size > 5000 and temp > 3:
    risk = "YELLOW - Medium Risk, Watch"
    color = "orange"

st.sidebar.markdown(f"### Risk: :{color}[{risk}]")

# Columns
col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Map - Dangerous Lakes in Chitral")
    m = folium.Map(location=[35.85, 71.78], zoom_start=9)
    folium.Marker([36.05, 71.80], tooltip="Reshun Lake", popup=f"Risk: {risk}", icon=folium.Icon(color=color)).add_to(m)
    folium.Marker([35.90, 71.70], tooltip="Booni Lake", popup="Safe", icon=folium.Icon(color="green")).add_to(m)
    st_folium(m, width=700, height=400)

with col2:
    st.subheader(f"Alert Level: {risk}")
    if color == "red":
        st.error("🚨 WHATSAPP ALERT: Reshun Gol Nullah me pani khatarnak hadd tak barh gaya hai. Gaon khali karein. - SARAB System")
    elif color == "orange":
        st.warning("⚠️ Alert: Lake size increasing. Inform PDMA.")
    else:
        st.success("✅ All Safe. No GLOF risk today.")
    
    st.subheader("Last 7 Days Temperature")
    data = pd.DataFrame({"Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], "Temp": [2,4,5,7,8,8, temp]})
    st.line_chart(data, x="Day", y="Temp")

st.info("Demo Data: If SARAB existed in July 2023, it would have warned 5 days before Reshun flood.")