import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import math

# 1. KONFIGURATION & DATEN
st.set_page_config(layout="wide", page_title="Pflanzen-Planer Dashboard")

# Google Sheet Export Link
SHEET_ID = "1cbOPNq-CrYrin-U0OkUJ5AE2AWF6Ba7RqIHlVOtUCK0"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Fenster-Koordinaten aus deinem Bild
FENSTER = [
    {"name": "Wohnzimmer West", "x": 125, "y_range": (80, 365), "typ": "West"},
    {"name": "Küche Süd 1", "x_range": (620, 680), "y": 415, "typ": "Süd"},
    {"name": "Küche Süd 2", "x": 745, "y_range": (250, 397), "typ": "Süd"},
    {"name": "WC Nord", "x": 745, "y_range": (20, 70), "typ": "Nord"}
]

# 2. FUNKTIONEN
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except:
        st.error("Konnte Google Sheet nicht laden. Prüfe die Freigabe!")
        return pd.DataFrame(columns=["Name", "Lichtbedarf (1-10)", "Giessen (Tage)", "Info"])

def berechne_lichtwert(px, py):
    # Einfache Logik: Distanz zum nächsten Fenster
    min_dist = 1000
    for f in FENSTER:
        # Mitte des Fensters für Distanzberechnung
        fx = f.get("x", sum(f.get("x_range", [0,0]))/2)
        fy = f.get("y", sum(f.get("y_range", [0,0]))/2)
        dist = math.sqrt((px - fx)**2 + (py - fy)**2)
        if dist < min_dist:
            min_dist = dist
    
    # Lichtwert sinkt mit Distanz (Max 10 bei Distanz 0)
    licht = max(1, 10 - (min_dist / 60)) 
    return round(licht, 1)

# 3. DASHBOARD LAYOUT
st.title("🌿 Mein interaktiver Pflanzen-Grundriss")

df_plants = load_data()

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Bibliothek & Auswahl")
    selected_plant_name = st.selectbox("Wähle eine Pflanze aus deinem Sheet:", df_plants["Name"].tolist())
    plant_info = df_plants[df_plants["Name"] == selected_plant_name].iloc[0]
    
    st.info(f"**Bedarf:** Licht {plant_info['Lichtbedarf (1-10)']}/10, Gießen alle {plant_info['Giessen (Tage)']} Tage.")
    st.write(f"*Info:* {plant_info['Info']}")

with col1:
    # Grundriss laden
    img = Image.open("Grundriss EG.png") # Datei muss im selben Ordner liegen
    
    # Session State für Position
    if 'pos' not in st.session_state:
        st.session_state.pos = [300, 300]

    # Plotly Map erstellen
    fig = go.Figure()

    # Hintergrundbild hinzufügen
    fig.add_layout_image(
        dict(
            source=img,
            xref="x", yref="y",
            x=0, y=0,
            sizex=610, sizey=630, # Deine Maße
            sizing="stretch",
            layer="below"
        )
    )

    # Pflanzen-Icon als Punkt
    fig.add_trace(go.Scatter(
        x=[st.session_state.pos[0]],
        y=[st.session_state.pos[1]],
        mode="markers+text",
        marker=dict(size=25, color="green", symbol="leaf"),
        text=[selected_plant_name],
        textposition="top center",
        name="Pflanze"
    ))

    fig.update_xaxes(range=[0, 610], visible=False)
    fig.update_yaxes(range=[630, 0], visible=False) # Invertiert für korrekte Bilddarstellung
    fig.update_layout(width=700, height=700, margin=dict(l=0, r=0, t=0, b=0), clickmode='event+select')

    # Interaktion: Klick im Plotly Chart abfangen
    selected_point = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
    
    # Update Position bei Klick
    if selected_point and "points" in selected_point["selection"]:
        if len(selected_point["selection"]["points"]) > 0:
            # Hier simulieren wir die neue Position (Plotly in Streamlit ist noch begrenzt bei Drag)
            pass 

    # Manuelle Steuerung für die Demo, da echtes Drag&Drop in Web-Apps komplex ist
    st.write("Setze die Koordinaten für die Pflanze:")
    ix = st.slider("X-Position", 0, 610, st.session_state.pos[0])
    iy = st.slider("Y-Position", 0, 630, st.session_state.pos[1])
    st.session_state.pos = [ix, iy]

    # AUSWERTUNG
    ist_licht = berechne_lichtwert(ix, iy)
    soll_licht = float(plant_info['Lichtbedarf (1-10)'])

    st.subheader(f"Standort-Check: {selected_plant_name}")
    if ist_licht >= soll_licht - 1:
        st.success(f"✅ Guter Standort! Verfügbares Licht: ca. {ist_licht}. Bedarf: {soll_licht}")
    elif ist_licht >= soll_licht - 3:
        st.warning(f"⚠️ Grenzwertig. Lichtwert: {ist_licht}. Die Pflanze könnte langsamer wachsen.")
    else:
        st.error(f"❌ Zu dunkel! Lichtwert nur {ist_licht}. Hier wird die Pflanze eingehen.")