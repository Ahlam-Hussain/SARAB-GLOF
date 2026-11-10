import folium
import streamlit as st
from streamlit_folium import st_folium

import frontend_theme as theme
from backend_data import TILES

COLOUR = {"HIGH": "red", "MEDIUM": "orange", "LOW": "green"}
BADGE = {"HIGH": "🔴 HIGH", "MEDIUM": "🟡 MEDIUM", "LOW": "🟢 LOW"}


def render(s):
    df = s["df"]
    m = folium.Map(location=[36.2, 73.2], zoom_start=7, tiles=None)
    for i, (name, url, attr) in enumerate(TILES):
        folium.TileLayer(url, name=name, attr=attr, show=(i == 0)).add_to(m)
    for r in df.itertuples():
        folium.Marker([r.lat, r.lon], tooltip=r.Lake, icon=folium.Icon(color=COLOUR[r.Risk], icon="tint", prefix="fa"),
                      popup=f"<b>{r.Lake}</b><br>{r.District}<br>Risk: {r.Risk} ({r.Score})<br>Villages: {r.Villages}<br>Reports: {r.Reports}").add_to(m)
        folium.Circle([r.lat, r.lon], radius=1500 + r.Score * 60, color=COLOUR[r.Risk], fill=True, fill_opacity=0.25).add_to(m)
    folium.LayerControl().add_to(m)
    st_folium(m, height=460, use_container_width=True, returned_objects=[])
    theme.table(df.assign(Status=df.Risk.map(BADGE))[["Lake", "District", "Status", "Score", "Villages", "Reports"]])
