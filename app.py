import streamlit as st
import folium
from streamlit_folium import st_folium
import datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="SARAB - GLOF Warning", page_icon="🏔️", layout="wide")

st.title("🏔️ SARAB - GLOF Early Warning System")
st.subheader("For Chitral, Swat & Gilgit-Baltistan | Khyber Hackathon - Peshawar")
st.write("---")

# --- SIDEBAR - 2G MODE ---
st.sidebar.title("⚙️ Settings")
is_2g_mode = st.sidebar.toggle("Enable 2G / Low Internet Mode")

risk_level = "HIGH"
lake_name = "Golen Gol, Chitral"

# --- MAIN DASHBOARD ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Lake", lake_name)
with col2:
    if risk_level == "HIGH":
        st.metric("GLOF RISK", "🔴 HIGH", delta="Danger", delta_color="inverse")
    else:
        st.metric("GLOF RISK", "🟢 LOW")
with col3:
    st.metric("Last Update", datetime.datetime.now().strftime("%d-%b %I:%M %p"))

# --- 2G MODE LOGIC ---
if is_2g_mode:
    st.warning("📶 2G MODE ON: Heavy images disabled to save data. Only critical alerts active.")
    st.error(f"🚨 SMS ALERT SENT to Buni Village: 'Khatra! {lake_name} se sailab ka khatra hai. Fauri mehfooz maqam par jayen.'")
    st.info("✅ 12 villagers confirmed safe via SMS")
    
    # STOP HERE - Don't load heavy map
    st.success("In 2G mode, evacuation instructions sent via SMS to feature phones.")
else:
    # --- NORMAL MODE: MAP + ALL ---
    st.write("### 🗺️ Live Evacuation Map")
    st.write("Red Zone = Flood Area | Green Marker = Safe Shelter | Green Line = Safe Route")

    # Map centered on Buni, Chitral
    m = folium.Map(location=[36.2700, 72.2500], zoom_start=13, tiles="OpenStreetMap")

    # 1. FLOOD ZONE - RED
    folium.Polygon(
        locations=[[36.265, 72.24], [36.285, 72.255], [36.275, 72.27], [36.255, 72.255]],
        color="red", fill=True, fill_color="red", fill_opacity=0.4,
        popup="FLOOD ZONE - EVACUATE IMMEDIATELY"
    ).add_to(m)

    # 2. SAFE SHELTERS - GREEN
    folium.Marker([36.275, 72.255], tooltip="CLICK FOR INFO", popup="<b>Govt High School Buni</b><br>SAFE SHELTER - Capacity 200", icon=folium.Icon(color="green", icon="home", prefix="fa")).add_to(m)
    folium.Marker([36.272, 72.251], popup="<b>Buni Jamia Mosque</b><br>SAFE", icon=folium.Icon(color="green", icon="info-sign")).add_to(m)
    folium.Marker([36.278, 72.258], popup="<b>THQ Hospital Buni</b><br>Medical Help", icon=folium.Icon(color="blue", icon="plus")).add_to(m)

    # 3. SAFE ROUTE - GREEN LINE
    folium.PolyLine([[36.265, 72.245], [36.275, 72.255]], color="green", weight=6, popup="Safe Evacuation Route").add_to(m)

    st_folium(m, width=700, height=450)

st.write("---")

# --- REAL STORIES SECTION ---
st.header("💔 Why SARAB? Real Stories from KP")
col_a, col_b = st.columns(2)

with col_a:
    with st.container(border=True):
        st.subheader("2022 - Buni, Chitral")
        st.write("Golen Gol GLOF destroyed 15 houses, 200 people displaced. The flood washed away roads.")
        st.error("If SARAB existed 2 days before, early evacuation was possible.")

with col_b:
    with st.container(border=True):
        st.subheader("2019 - Reshun, Chitral")
        st.write("Flood washed away Reshun power house, 5 bridges. Whole area without electricity for months.")
        st.error("Early warning could have saved the power station & millions of rupees.")

st.write("---")

# --- COMMUNITY REPORTER ---
st.header("📸 Gaon Walon Ki Khabar - Community Reporter")
st.write("Villager can report lake/flood with photo")

report_type = st.selectbox("What do you see?", ["Lake Water Increasing", "Small Flood Started", "Glacier Cracking Sound"])
uploaded_file = st.file_uploader("Upload photo from mobile", type=["jpg", "png"])

if st.button("Send Report to SARAB Team"):
    if uploaded_file:
        st.success(f"✅ Report Received: '{report_type}'. Our AI team will verify in 10 mins. Thank you!")
        st.balloons()
    else:
        st.warning("Please upload a photo first.")

st.sidebar.info("Live Link: Your Streamlit App\nWorks on mobile like Instagram icon via 'Add to Home Screen'")
   
      
