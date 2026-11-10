import altair as alt
import streamlit as st

THEMES = {
    "dark": dict(bg="#07131f", bg2="#0e2233", text="#e8f7fb", muted="#8fb4c4", card1="#10283a", card2="#0a1a28",
                 line="#1d4a63", accent="#7fe0e8", onaccent="#07131f", redbg="#3a0d14", redtx="#ffd6d8",
                 grnbg="#0b2e2a", grntx="#c9f5ec", c1="#7fe0e8", c2="#3b82f6"),
    "light": dict(bg="#f2f8fb", bg2="#e2eef4", text="#0b2a3b", muted="#4a6b7a", card1="#ffffff", card2="#e9f4f8",
                  line="#b9d3df", accent="#0e7c86", onaccent="#ffffff", redbg="#fde8ea", redtx="#7a1220",
                  grnbg="#dff5ef", grntx="#0b4a3d", c1="#0e7c86", c2="#1f5fbf"),
}

CSS = """
.block-container{padding-top:1.5rem}
.stApp,[data-testid=stHeader]{background:var(--bg)}
[data-testid=stSidebar]{background:var(--bg2)}
.stApp,.stApp p,.stApp span,.stApp label,.stApp li,.stApp h1,.stApp h2,.stApp h3,.stApp small{color:var(--text)}
[data-baseweb=input],[data-baseweb=textarea],[data-testid=stFileUploaderDropzone]{background:var(--bg2)!important}
[data-baseweb=select],[data-baseweb=select] *,[data-baseweb=popover],[data-baseweb=popover] *,[data-baseweb=menu],[data-baseweb=menu] *,[role=listbox],[role=listbox] *{background:var(--bg2)!important;color:var(--text)!important}
[role=option]:hover,[role=option][aria-selected=true]{background:var(--line)!important}
input,textarea{color:var(--text)!important;-webkit-text-fill-color:var(--text)!important}
.stButton>button{background:var(--accent);border:0}
.stApp .stButton>button p{color:var(--onaccent)}
.stApp .hero h1{font-family:Georgia,serif;font-size:3.2rem;margin:0}
.stApp .hero h1 span{font-size:1.3rem;color:var(--accent)}
.stApp .hero p{color:var(--muted);margin:.2rem 0 0}
.stApp .pill{display:inline-block;padding:3px 12px;margin-left:6px;border:1px solid var(--line);border-radius:14px;color:var(--accent);font-size:.8rem}
.card{background:linear-gradient(160deg,var(--card1),var(--card2));border:1px solid var(--line);border-radius:14px;padding:.9rem 1.1rem;margin-bottom:.8rem}
.stApp .card small{color:var(--muted)}
.stApp .card b{display:block;font-size:1.6rem;color:var(--text)}
.alert{border-radius:14px;padding:1rem 1.2rem;margin-bottom:1rem}
.alert.red{background:var(--redbg);border:1px solid #e5484d;color:var(--redtx);animation:pulse 2s infinite}
.alert.green{background:var(--grnbg);border:1px solid #2bb39a;color:var(--grntx)}
.tbl{overflow-x:auto}
.tbl table{width:100%;border-collapse:collapse}
.tbl th,.tbl td{padding:.5rem .8rem;border-bottom:1px solid var(--line);text-align:left!important}
.tbl th{color:var(--muted)}
@keyframes pulse{50%{opacity:.6}}
@media (prefers-reduced-motion:reduce){.alert.red{animation:none}}
"""


def colors():
    return THEMES["dark" if st.session_state.get("dark", True) else "light"]


def inject():
    vars_ = ";".join(f"--{k}:{v}" for k, v in colors().items())
    st.markdown(f"<style>:root{{{vars_}}}{CSS}</style>", unsafe_allow_html=True)


def card(label, value, sub=""):
    return f'<div class="card"><small>{label}</small><b>{value}</b><small>{sub}</small></div>'


def gauge(score):
    return f"""<div style="width:260px;margin:auto;text-align:center">
<div style="position:relative;width:260px;height:130px;overflow:hidden">
<div style="width:260px;height:260px;border-radius:50%;background:conic-gradient(from 270deg,#1f77b4 0 63deg,#ef8a17 63deg 117deg,#e5484d 117deg 180deg,transparent 180deg)"></div>
<div style="position:absolute;top:35px;left:35px;width:190px;height:190px;border-radius:50%;background:var(--bg)"></div>
<div style="position:absolute;left:128px;bottom:0;width:4px;height:112px;background:var(--text);border-radius:2px;transform-origin:bottom center;transform:rotate({score * 1.8 - 90}deg)"></div>
</div><b style="font-size:2.4rem;color:var(--text)">{score}</b><br><small style="color:var(--muted)">GLOF risk index</small></div>"""


def table(df):
    html = df.fillna("").to_html(index=False, border=0).replace("\n", "")
    st.markdown(f'<div class="tbl">{html}</div>', unsafe_allow_html=True)


def line(df, xtype, palette):
    x = df.index.name
    d = df.reset_index().melt(x, var_name="Series", value_name="Value")
    t = colors()
    chart = alt.Chart(d).mark_line().encode(
        x=alt.X(f"{x}:{xtype}", title=None), y=alt.Y("Value:Q", title=None),
        color=alt.Color("Series:N", scale=alt.Scale(range=palette), legend=alt.Legend(orient="bottom", title=None)),
    ).properties(width="container", height=280)
    chart = (chart.configure(background="transparent").configure_view(stroke=None)
             .configure_axis(labelColor=t["muted"], gridColor=t["line"], domainColor=t["line"])
             .configure_legend(labelColor=t["text"]))
    st.altair_chart(chart, theme=None)
