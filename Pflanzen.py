import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import math

# 1. KONFIGURATION
st.set_page_config(layout="wide", page_title="Pflanzen-Planer Dashboard")

# Google Sheet Export Link (Deine ID)
SHEET_ID = "1cbOPNq-CrYrin-U0OkUJ5AE2AWF6Ba7RqIHlVOtUCK0"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Deine Fenster-Koordinaten
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
        # Erzwungene UTF-8 Kodierung für Umlaute
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden des Google Sheets: {e}")
        # Fallback-Daten, falls das Sheet nicht erreichbar ist
        return pd.DataFrame({
            "Name": ["Beispielpflanze"], 
            "Lichtbedarf (1-10)": [5], 
            "Giessen (Tage)": [7], 
            "Info": ["Bitte prüfe den Google Sheet Link."]
        })

def berechne_lichtwert(px, py):
    min_dist = 1000
    for f in FENSTER:
        # Wir nehmen die Mitte des Fensters als Lichtquelle
        if "x" in f:
            fx = f["x"]
            fy = (f["y_range"][0] + f["y_range"][1]) / 2
        else:
            fx = (f["x_range"][0] + f["x_range"][1]) / 2
            fy = f["y"]
        
        dist = math.sqrt((px - fx)**2 + (py - fy)**2)
        if dist < min_dist:
            min_dist = dist
    
    # Lichtwert-Berechnung: Je näher am Fenster, desto näher an 10
    # Bei ca. 500 Pixeln Abstand landet der Wert bei 1 (Schatten)
    licht = max(1, 10 - (min_dist / 55)) 
    return round(licht, 1)

# 3. DASHBOARD LAYOUT
st.title("🌿 Mein interaktiver Pflanzen-Grundriss")

df_plants = load_data()

# Spaltenaufteilung
col_map, col_info = st.columns([2, 1])

with col_info:
    st.subheader("Pflanzen-Bibliothek")
    # Dropdown zur Auswahl der Pflanze aus dem Google Sheet
    selected_name = st.selectbox("Wähle eine Pflanze:", df_plants["Name"].unique())
    plant_data = df_plants[df_plants["Name"] == selected_name].iloc[0]
    
    st.metric("Lichtbedarf", f"{plant_data['Lichtbedarf (1-10)']}/10")
    st.metric("Gießintervall", f"Alle {plant_data['Giessen (Tage)']} Tage")
    
    with st.expander("Weitere Infos"):
        st.write(plant_data["Info"])

with col_map:
    # BILD LADEN - Hier ist die Korrektur der Endung .PNG
    try:
        img = Image.open("Grundriss EG.PNG")
        
        # Steuerung der Position über Slider (für mobile Nutzung stabilste Lösung)
        st.write("Verschiebe das Icon auf dem Grundriss:")
        c1, c2 = st.columns(2)
        with c1:
            ix = st.slider("X-Achse (Links-Rechts)", 0, 610, 300)
        with c2:
            iy = st.slider("Y-Achse (Oben-Unten)", 0, 630, 300)

        # Plotly Chart erstellen
        fig = go.Figure()

        # Grundriss als Hintergrund
        fig.add_layout_image(
            dict(
                source=img,
                xref="x", yref="y",
                x=0, y=0,
                sizex=610, sizey=630,
                sizing="stretch",
                layer="below"
            )
        )

        # Die Pflanze als grüner Punkt/Icon
        fig.add_trace(go.Scatter(
            x=[ix], y=[iy],
            mode="markers+text",
            marker=dict(size=20, color="MediumSeaGreen", symbol="circle"),
            text=[selected_name],
            textposition="top center",
            textfont=dict(color="white")
        ))

        # Achsen-Einstellungen (Invertiert Y, damit Oben=0 ist wie im Bild)
        fig.update_xaxes(range=[0, 610], visible=False)
        fig.update_yaxes(range=[630, 0], visible=False)
        fig.update_layout(
            width=700, height=700, 
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # AUSWERTUNG
        ist_licht = berechne_lichtwert(ix, iy)
        soll_licht = float(plant_data['Lichtbedarf (1-10)'])

        st.divider()
        st.subheader("Standort-Analyse")
        
        if ist_licht >= soll_licht:
            st.success(f"🌟 Perfekt! Dieser Platz bietet einen Lichtwert von ca. {ist_licht}. (Bedarf: {soll_licht})")
        elif ist_licht >= soll_licht - 2:
            st.warning(f"⛅ Akzeptabel. Der Lichtwert liegt bei {ist_licht}. Die Pflanze braucht eigentlich {soll_licht}.")
        else:
            st.error(f"🌑 Zu dunkel! Nur {ist_licht} Lichtpunkte verfügbar. Stell die {selected_name} näher an ein Fenster!")

    except FileNotFoundError:
        st.error("Fehler: Die Datei 'Grundriss EG.PNG' wurde nicht gefunden. Bitte prüfe den Namen auf GitHub.")
