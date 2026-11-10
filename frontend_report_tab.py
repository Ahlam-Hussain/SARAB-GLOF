import streamlit as st

from backend_data import VILLAGES
from backend_logic import add_report
import frontend_theme as theme


def render(s):
    if "flash" in st.session_state:
        st.success(st.session_state.pop("flash"))
        st.balloons()
    st.write("Seen muddy water, a sudden rise or a blocked stream? Send a photo and the monitoring team will verify it.")
    village = st.selectbox("Village", VILLAGES)
    near = st.selectbox("Nearest lake", s["df"].Lake)
    name = st.text_input("Your name")
    st.text_input("Mobile number (optional, not stored in this demo)")
    note = st.text_area("What did you see?")
    photo = st.file_uploader("Photo of the flood or glacier", type=["jpg", "jpeg", "png"])
    if photo:
        st.image(photo, caption="Preview", width=300)
    if st.button("🚨 Send flood report"):
        if name and photo:
            add_report(village, near, name, note)
            st.session_state.flash = f"Report received for {village}. The team will verify it before any alert is sent."
            st.rerun()
        else:
            st.error("Please enter your name and add a photo.")
    if len(st.session_state.reports):
        st.subheader("Recent reports")
        theme.table(st.session_state.reports.iloc[::-1])
