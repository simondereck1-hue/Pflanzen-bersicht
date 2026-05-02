import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# KONFIGURATION
# ============================================================
st.set_page_config(
    layout="wide",
    page_title="Pflanzen-Planer",
    page_icon="🌿"
)

# Globale CSS-Overrides: Streamlit-UI komplett ausblenden
st.markdown("""
<style>
    /* Streamlit-Shell verstecken – wir übernehmen das komplette Layout */
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stApp { background: #0f1117; }
</style>
""", unsafe_allow_html=True)

# Google Sheet ID – hier anpassen
SHEET_ID = "1cbOPNq-CrYrin-U0OkUJ5AE2AWF6Ba7RqIHlVOtUCK0"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Grundriss-Bild-URL (GitHub Raw oder eigener Host)
# Tipp: Lade "Grundriss EG.PNG" in dein GitHub-Repo und ersetze diese URL.
GRUNDRISS_URL = "https://raw.githubusercontent.com/DEIN_USERNAME/DEIN_REPO/main/Grundriss%20EG.PNG"

# ============================================================
# HAUPT-KOMPONENTE – alles läuft im Browser
# ============================================================

html_app = f"""
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Google Fonts: Syne (Display) + DM Sans (Body) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">

<style>
/* ── DESIGN TOKENS ─────────────────────────────────────── */
:root {{
  --bg:           #0f1117;
  --surface:      #171b26;
  --surface-2:    #1e2433;
  --border:       rgba(255,255,255,0.07);
  --accent:       #4ade80;       /* Grün – Pflanzenwelt */
  --accent-dim:   rgba(74,222,128,0.15);
  --warn:         #fbbf24;
  --warn-dim:     rgba(251,191,36,0.15);
  --danger:       #f87171;
  --danger-dim:   rgba(248,113,113,0.15);
  --text-primary: #f0f4f8;
  --text-muted:   #6b7a99;
  --sidebar-w:    320px;
  --header-h:     56px;
  --radius:       12px;
  --radius-sm:    8px;
  --transition:   0.22s cubic-bezier(0.4,0,0.2,1);
}}

/* ── RESET & BASE ───────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; }}
body {{
  font-family: 'DM Sans', sans-serif;
  background: var(--bg);
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
}}

/* ── HEADER ─────────────────────────────────────────────── */
#header {{
  height: var(--header-h);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 12px;
  flex-shrink: 0;
  z-index: 100;
}}
#header .logo {{
  font-family: 'Syne', sans-serif;
  font-weight: 800;
  font-size: 18px;
  letter-spacing: -0.5px;
  color: var(--accent);
}}
#header .subtitle {{
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 300;
}}
#header .status {{
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-muted);
}}
#header .status-dot {{
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--text-muted);
  transition: background 0.3s;
}}
#header .status-dot.ok {{ background: var(--accent); box-shadow: 0 0 8px var(--accent); }}

/* ── MAIN LAYOUT ─────────────────────────────────────────── */
#main {{
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
}}

/* ── MAP AREA ────────────────────────────────────────────── */
#map-area {{
  flex: 1;
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(74,222,128,0.04) 0%, transparent 60%),
    var(--bg);
}}

#map-canvas {{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  /* Größe wird per JS gesetzt */
}}

/* Grundriss-Bild */
#floor-img {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  pointer-events: none;
  user-select: none;
  border-radius: var(--radius);
  opacity: 0.92;
}}

/* ── PFLANZEN-ICONS ─────────────────────────────────────── */
.plant-pin {{
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: grab;
  user-select: none;
  touch-action: none;
  transition: transform var(--transition), filter var(--transition), z-index 0s;
  z-index: 10;
  /* Koordinaten werden per JS gesetzt (transform: translate) */
}}
.plant-pin:hover {{
  z-index: 50;
  transform: translate(var(--tx), var(--ty)) scale(1.08) !important;
  filter: drop-shadow(0 4px 16px rgba(74,222,128,0.5));
}}
.plant-pin.dragging {{
  cursor: grabbing;
  z-index: 100;
  transition: none;
  filter: drop-shadow(0 8px 24px rgba(74,222,128,0.7));
  transform: translate(var(--tx), var(--ty)) scale(1.12) !important;
}}
.plant-pin.active .pin-bubble {{
  background: var(--accent);
  color: #0f1117;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(74,222,128,0.35);
}}
.plant-pin.active .pin-label {{
  color: var(--accent);
  font-weight: 500;
}}

/* Farbiger Kreis */
.pin-bubble {{
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: var(--surface-2);
  border: 2px solid rgba(74,222,128,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  transition: background var(--transition), border-color var(--transition), box-shadow var(--transition);
  box-shadow: 0 2px 12px rgba(0,0,0,0.4);
}}

/* Licht-Score-Indikator unter dem Bubble */
.pin-indicator {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 3px;
  background: var(--text-muted);
  transition: background 0.3s;
}}
.pin-indicator.ideal  {{ background: var(--accent);  box-shadow: 0 0 6px var(--accent); }}
.pin-indicator.ok     {{ background: var(--warn);    box-shadow: 0 0 6px var(--warn); }}
.pin-indicator.bad    {{ background: var(--danger);  box-shadow: 0 0 6px var(--danger); }}

.pin-label {{
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 4px;
  white-space: nowrap;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
  transition: color var(--transition);
}}

/* ── SIDEBAR ─────────────────────────────────────────────── */
#sidebar {{
  width: var(--sidebar-w);
  background: var(--surface);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
  position: relative;
}}

/* Sidebar – leerer Zustand */
#sidebar-empty {{
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--text-muted);
  padding: 32px;
  text-align: center;
}}
#sidebar-empty .empty-icon {{ font-size: 48px; opacity: 0.4; }}
#sidebar-empty p {{ font-size: 14px; line-height: 1.6; }}

/* Sidebar – Pflanzen-Detail */
#sidebar-detail {{
  flex: 1;
  display: none;
  flex-direction: column;
  overflow-y: auto;
  padding: 24px;
  gap: 20px;
}}
#sidebar-detail.visible {{ display: flex; }}

/* Scrollbar */
#sidebar-detail::-webkit-scrollbar {{ width: 4px; }}
#sidebar-detail::-webkit-scrollbar-track {{ background: transparent; }}
#sidebar-detail::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}

/* Pflanzenkopf */
.plant-header {{
  display: flex;
  align-items: flex-start;
  gap: 14px;
}}
.plant-header .big-emoji {{
  font-size: 40px;
  flex-shrink: 0;
  line-height: 1;
}}
.plant-header-text h2 {{
  font-family: 'Syne', sans-serif;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--text-primary);
}}
.plant-header-text .coords {{
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 4px;
  font-variant-numeric: tabular-nums;
}}

/* Score-Badge */
.score-badge {{
  border-radius: var(--radius);
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--surface-2);
}}
.score-badge .score-icon {{ font-size: 28px; }}
.score-badge .score-text h3 {{
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 600;
}}
.score-badge .score-text p {{
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
  line-height: 1.4;
}}
.score-badge.ideal {{ border: 1px solid rgba(74,222,128,0.3);  background: var(--accent-dim); }}
.score-badge.ideal .score-text h3 {{ color: var(--accent); }}
.score-badge.ok    {{ border: 1px solid rgba(251,191,36,0.3);  background: var(--warn-dim); }}
.score-badge.ok    .score-text h3 {{ color: var(--warn); }}
.score-badge.bad   {{ border: 1px solid rgba(248,113,113,0.3); background: var(--danger-dim); }}
.score-badge.bad   .score-text h3 {{ color: var(--danger); }}

/* Licht-Balken */
.light-bar-wrap {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}
.light-bar-label {{
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-muted);
}}
.light-bar-track {{
  height: 6px;
  border-radius: 3px;
  background: var(--surface-2);
  overflow: hidden;
  position: relative;
}}
.light-bar-fill {{
  height: 100%;
  border-radius: 3px;
  background: var(--accent);
  transition: width 0.5s cubic-bezier(0.4,0,0.2,1);
}}
.light-bar-need {{
  position: absolute;
  top: 0; bottom: 0;
  width: 2px;
  background: rgba(255,255,255,0.5);
  border-radius: 1px;
}}

/* Daten-Grid */
.data-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}}
.data-card {{
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px;
}}
.data-card .dc-label {{
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 6px;
}}
.data-card .dc-value {{
  font-family: 'Syne', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
}}
.data-card .dc-unit {{
  font-size: 13px;
  font-weight: 400;
  color: var(--text-muted);
  margin-left: 3px;
}}

/* Info-Box */
.info-box {{
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px;
}}
.info-box .ib-label {{
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 5px;
}}
.info-box .ib-text {{
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-primary);
}}

/* Divider */
.sb-divider {{
  height: 1px;
  background: var(--border);
}}

/* Pflanzenliste (Sidebar-Footer) */
#plant-list {{
  border-top: 1px solid var(--border);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 220px;
  overflow-y: auto;
  flex-shrink: 0;
}}
#plant-list::-webkit-scrollbar {{ width: 4px; }}
#plant-list::-webkit-scrollbar-track {{ background: transparent; }}
#plant-list::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}
.pl-header {{
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0 2px 4px;
}}
.pl-item {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background var(--transition);
}}
.pl-item:hover {{ background: var(--surface-2); }}
.pl-item.active {{ background: var(--accent-dim); }}
.pl-item .pl-emoji {{ font-size: 16px; width: 20px; text-align: center; }}
.pl-item .pl-name {{
  font-size: 13px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}
.pl-item .pl-dot {{
  width: 7px; height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
  background: var(--text-muted);
}}
.pl-item .pl-dot.ideal {{ background: var(--accent); }}
.pl-item .pl-dot.ok    {{ background: var(--warn); }}
.pl-item .pl-dot.bad   {{ background: var(--danger); }}

/* ── LOADING OVERLAY ──────────────────────────────────────── */
#loading {{
  position: fixed; inset: 0; z-index: 9999;
  background: var(--bg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  transition: opacity 0.5s, visibility 0.5s;
}}
#loading.hidden {{ opacity: 0; visibility: hidden; }}
#loading .ld-icon {{ font-size: 48px; animation: pulse 1.5s ease-in-out infinite; }}
#loading p {{ font-size: 14px; color: var(--text-muted); }}
@keyframes pulse {{ 0%,100%{{opacity:0.4}} 50%{{opacity:1}} }}

/* ── SCROLLBAR GLOBAL ─────────────────────────────────────── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}
</style>
</head>
<body>

<!-- Loading Screen -->
<div id="loading">
  <div class="ld-icon">🌿</div>
  <p>Pflanzendaten werden geladen…</p>
</div>

<!-- Header -->
<div id="header">
  <span class="logo">🌿 Pflanzen-Planer</span>
  <span class="subtitle">Grundriss-Ansicht</span>
  <div class="status">
    <div class="status-dot" id="status-dot"></div>
    <span id="status-text">Verbinden…</span>
  </div>
</div>

<!-- Main -->
<div id="main">

  <!-- Map -->
  <div id="map-area">
    <div id="map-canvas">
      <img id="floor-img" src="{GRUNDRISS_URL}" alt="Grundriss"
           draggable="false"
           onerror="this.src='https://placehold.co/700x700/171b26/4ade80?text=Grundriss+nicht+gefunden'">
      <!-- Pflanzen-Pins werden hier dynamisch eingefügt -->
    </div>
  </div>

  <!-- Sidebar -->
  <div id="sidebar">

    <!-- Leerer Zustand -->
    <div id="sidebar-empty">
      <div class="empty-icon">🪴</div>
      <p>Klicke auf eine Pflanze auf dem Grundriss,<br>um ihre Details zu sehen.</p>
    </div>

    <!-- Detailansicht -->
    <div id="sidebar-detail">
      <!-- Wird per JS befüllt -->
    </div>

    <!-- Pflanzenliste -->
    <div id="plant-list">
      <div class="pl-header">Alle Pflanzen</div>
      <!-- Wird per JS befüllt -->
    </div>

  </div>
</div>

<script>
// ============================================================
// KONSTANTEN
// ============================================================
const CSV_URL = "{CSV_URL}";

// Fenster-Definitionen (gespiegelt aus Python)
// Format: jedes Fenster hat einen "center" [x, y] in relativen Koordinaten (0-1)
const FENSTER = [
  {{ name: "Wohnzimmer West", center: [125/610, 222/630], typ: "West"  }},
  {{ name: "Küche Süd 1",     center: [650/610, 415/630], typ: "Süd"   }},
  {{ name: "Küche Süd 2",     center: [745/610, 323/630], typ: "Süd"   }},
  {{ name: "WC Nord",         center: [745/610,  45/630], typ: "Nord"  }},
];

// Emoji-Pool – wird anhand des Namens zugewiesen
const PLANT_EMOJIS = ["🌿","🌱","🪴","🌺","🌸","🌻","🌵","🎋","🌴","🌳","🍀","☘️","🌾","🌼","💐"];

// ============================================================
// STATE
// ============================================================
let plants = [];          // Array of plant objects
let activePlantIdx = null;

// ============================================================
// CSV LADEN & PARSEN
// ============================================================
async function loadPlants() {{
  setStatus(false, "Lade Daten…");
  try {{
    const res = await fetch(CSV_URL);
    if (!res.ok) throw new Error("HTTP " + res.status);
    const text = await res.text();
    plants = parseCSV(text);
    setStatus(true, plants.length + " Pflanzen geladen");
  }} catch(e) {{
    console.warn("CSV-Fehler:", e);
    // Fallback-Daten
    plants = [
      {{ name:"Monstera Deliciosa", licht:7, giessen:7, info:"Robuste Zimmerpflanze, mag indirektes Licht.", emoji:"🌿" }},
      {{ name:"Sukkulente",          licht:9, giessen:21,info:"Sehr genügsam, braucht viel Sonne.",           emoji:"🌵" }},
      {{ name:"Farn",                licht:3, giessen:3, info:"Mag es schattig und feucht.",                  emoji:"🌿" }},
      {{ name:"Orchidee",            licht:6, giessen:10,info:"Helles, indirektes Licht. Nicht zu viel Wasser.",emoji:"🌺"}},
    ];
    setStatus(false, "Offline-Modus");
  }}

  // Startpositionen verteilen
  plants.forEach((p, i) => {{
    if (p.x === undefined) {{
      // Raster-Startplatzierung damit nichts überlappt
      p.x = 0.2 + (i % 4) * 0.18;
      p.y = 0.25 + Math.floor(i / 4) * 0.3;
    }}
    if (!p.emoji) p.emoji = PLANT_EMOJIS[i % PLANT_EMOJIS.length];
  }});

  render();
  hideLoading();
}}

function parseCSV(text) {{
  const lines = text.trim().split("\\n");
  const headers = lines[0].split(",").map(h => h.trim().replace(/"/g,""));
  
  // Spalten-Mapping (flexibel)
  const colName   = findCol(headers, ["Name","name","Pflanze"]);
  const colLicht  = findCol(headers, ["Lichtbedarf (1-10)","Licht","licht","Light"]);
  const colGiess  = findCol(headers, ["Giessen (Tage)","Giessen","giessen","Watering"]);
  const colInfo   = findCol(headers, ["Info","info","Beschreibung","Description"]);

  return lines.slice(1).filter(l => l.trim()).map((line, i) => {{
    const cols = splitCSVLine(line);
    return {{
      name:    cols[colName]  || "Pflanze " + (i+1),
      licht:   parseFloat(cols[colLicht]) || 5,
      giessen: parseFloat(cols[colGiess]) || 7,
      info:    cols[colInfo]  || "",
      emoji:   PLANT_EMOJIS[i % PLANT_EMOJIS.length],
    }};
  }});
}}

function findCol(headers, candidates) {{
  for (const c of candidates) {{
    const idx = headers.findIndex(h => h.toLowerCase().includes(c.toLowerCase()));
    if (idx >= 0) return idx;
  }}
  return 0;
}}

function splitCSVLine(line) {{
  const result = [];
  let cur = "", inQ = false;
  for (const ch of line) {{
    if (ch === '"') {{ inQ = !inQ; continue; }}
    if (ch === ',' && !inQ) {{ result.push(cur.trim()); cur = ""; continue; }}
    cur += ch;
  }}
  result.push(cur.trim());
  return result;
}}

// ============================================================
// LICHTBERECHNUNG
// ============================================================
function berechne_lichtwert(px, py) {{
  // px, py sind relative Koordinaten (0-1)
  let minDist = Infinity;
  for (const f of FENSTER) {{
    const dx = px - f.center[0];
    const dy = py - f.center[1];
    const dist = Math.sqrt(dx*dx + dy*dy);
    if (dist < minDist) minDist = dist;
  }}
  // Skalierung: max Distanz ≈ 1.0, bei 0 → 10, bei 0.9 → 1
  const licht = Math.max(1, 10 - (minDist / 0.09));
  return Math.round(licht * 10) / 10;
}}

function getLichtStatus(istLicht, sollLicht) {{
  if (istLicht >= sollLicht)     return "ideal";
  if (istLicht >= sollLicht - 2) return "ok";
  return "bad";
}}

const STATUS_CONFIG = {{
  ideal: {{ icon:"🌟", label:"Idealer Standort", desc:"Das Lichtangebot übertrifft den Bedarf.", cls:"ideal" }},
  ok:    {{ icon:"⛅", label:"Akzeptabler Standort", desc:"Etwas weniger Licht als optimal, aber vertretbar.", cls:"ok" }},
  bad:   {{ icon:"🌑", label:"Zu dunkel", desc:"Bitte näher ans Fenster stellen.", cls:"bad" }},
}};

// ============================================================
// RENDER
// ============================================================
function getCanvas() {{ return document.getElementById("map-canvas"); }}

function render() {{
  const canvas = getCanvas();
  const img = document.getElementById("floor-img");
  const W = img.naturalWidth  || 610;
  const H = img.naturalHeight || 630;
  canvas.style.width  = W + "px";
  canvas.style.height = H + "px";

  // Existierende Pins entfernen
  canvas.querySelectorAll(".plant-pin").forEach(el => el.remove());

  plants.forEach((p, i) => {{
    const ist  = berechne_lichtwert(p.x, p.y);
    const stat = getLichtStatus(ist, p.licht);

    const pin = document.createElement("div");
    pin.className = "plant-pin" + (activePlantIdx === i ? " active" : "");
    pin.dataset.idx = i;

    const tx = Math.round(p.x * W - 21);   // 21 = halbe Bubble-Breite
    const ty = Math.round(p.y * H - 21);
    pin.style.setProperty("--tx", tx + "px");
    pin.style.setProperty("--ty", ty + "px");
    pin.style.transform = `translate(${{tx}}px, ${{ty}}px)`;

    pin.innerHTML = `
      <div class="pin-bubble">${{p.emoji}}</div>
      <div class="pin-indicator ${{stat}}"></div>
      <div class="pin-label">${{p.name}}</div>
    `;

    // Events
    setupDrag(pin, i);
    pin.addEventListener("click", (e) => {{
      e.stopPropagation();
      selectPlant(i);
    }});

    canvas.appendChild(pin);
  }});

  renderPlantList();
  if (activePlantIdx !== null) renderSidebar(activePlantIdx);
}}

// ============================================================
// DRAG & DROP
// ============================================================
function setupDrag(pin, idx) {{
  let startX, startY, startPX, startPY, dragging = false;
  const img = document.getElementById("floor-img");

  function getWH() {{
    const W = img.naturalWidth  || 610;
    const H = img.naturalHeight || 630;
    const rect = img.getBoundingClientRect();
    // Skalierungsfaktor: Bild kann via CSS skaliert sein
    const scaleX = (img.naturalWidth  || 610) / rect.width;
    const scaleY = (img.naturalHeight || 630) / rect.height;
    return {{ W, H, rect, scaleX, scaleY }};
  }}

  function onPointerDown(e) {{
    if (e.button !== undefined && e.button !== 0) return;
    e.preventDefault();
    e.stopPropagation();
    dragging = true;
    pin.classList.add("dragging");
    pin.setPointerCapture(e.pointerId);

    const client = getClientXY(e);
    startX = client.x;
    startY = client.y;
    startPX = plants[idx].x;
    startPY = plants[idx].y;
  }}

  function onPointerMove(e) {{
    if (!dragging) return;
    e.preventDefault();
    const client = getClientXY(e);
    const {{ rect, scaleX, scaleY }} = getWH();

    const dx = (client.x - startX) * scaleX;
    const dy = (client.y - startY) * scaleY;
    const W = img.naturalWidth  || 610;
    const H = img.naturalHeight || 630;

    plants[idx].x = Math.max(0, Math.min(1, startPX + dx / W));
    plants[idx].y = Math.max(0, Math.min(1, startPY + dy / H));

    // Live-Update des Pins ohne vollständiges Re-Render
    const tx = Math.round(plants[idx].x * W - 21);
    const ty = Math.round(plants[idx].y * H - 21);
    pin.style.setProperty("--tx", tx + "px");
    pin.style.setProperty("--ty", ty + "px");
    pin.style.transform = `translate(${{tx}}px, ${{ty}}px)`;

    // Indikator sofort aktualisieren
    const ist  = berechne_lichtwert(plants[idx].x, plants[idx].y);
    const stat = getLichtStatus(ist, plants[idx].licht);
    pin.querySelector(".pin-indicator").className = `pin-indicator ${{stat}}`;

    // Sidebar live updaten wenn aktiv
    if (activePlantIdx === idx) renderSidebar(idx);
  }}

  function onPointerUp(e) {{
    if (!dragging) return;
    dragging = false;
    pin.classList.remove("dragging");
    render(); // Vollständiges Re-Render für korrekte Z-Indizes
    if (activePlantIdx === idx) renderSidebar(idx);
  }}

  pin.addEventListener("pointerdown", onPointerDown);
  pin.addEventListener("pointermove", onPointerMove);
  pin.addEventListener("pointerup",   onPointerUp);
  pin.addEventListener("pointercancel", onPointerUp);
}}

function getClientXY(e) {{
  if (e.touches && e.touches.length) return {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
  return {{ x: e.clientX, y: e.clientY }};
}}

// ============================================================
// PLANT SELECTION
// ============================================================
function selectPlant(idx) {{
  activePlantIdx = (activePlantIdx === idx) ? null : idx;
  render();
  if (activePlantIdx !== null) renderSidebar(activePlantIdx);
  else showEmptySidebar();
}}

function showEmptySidebar() {{
  document.getElementById("sidebar-empty").style.display = "";
  document.getElementById("sidebar-detail").classList.remove("visible");
}}

// ============================================================
// SIDEBAR RENDER
// ============================================================
function renderSidebar(idx) {{
  const p  = plants[idx];
  const ist  = berechne_lichtwert(p.x, p.y);
  const stat = getLichtStatus(ist, p.licht);
  const sc   = STATUS_CONFIG[stat];
  const pct_ist  = (ist  / 10 * 100).toFixed(1);
  const pct_soll = (p.licht / 10 * 100).toFixed(1);
  const W = (document.getElementById("floor-img").naturalWidth  || 610);
  const H = (document.getElementById("floor-img").naturalHeight || 630);

  document.getElementById("sidebar-empty").style.display = "none";
  const detail = document.getElementById("sidebar-detail");
  detail.classList.add("visible");

  detail.innerHTML = `
    <div class="plant-header">
      <div class="big-emoji">${{p.emoji}}</div>
      <div class="plant-header-text">
        <h2>${{p.name}}</h2>
        <div class="coords">
          X: ${{Math.round(p.x * W)}}px · Y: ${{Math.round(p.y * H)}}px
        </div>
      </div>
    </div>

    <div class="score-badge ${{sc.cls}}">
      <div class="score-icon">${{sc.icon}}</div>
      <div class="score-text">
        <h3>${{sc.label}}</h3>
        <p>${{sc.desc}}</p>
      </div>
    </div>

    <div class="light-bar-wrap">
      <div class="light-bar-label">
        <span>💡 Lichtverfügbarkeit</span>
        <span>${{ist}} / 10</span>
      </div>
      <div class="light-bar-track">
        <div class="light-bar-fill" style="width: ${{pct_ist}}%;
          background: ${{stat==='ideal'?'var(--accent)':stat==='ok'?'var(--warn)':'var(--danger)'}}">
        </div>
        <div class="light-bar-need" style="left: ${{pct_soll}}%;" title="Lichtbedarf"></div>
      </div>
      <div class="light-bar-label">
        <span style="color:var(--text-muted)">Bedarf: ${{p.licht}}/10</span>
        <span style="color:var(--text-muted)">Verfügbar: ${{ist}}/10</span>
      </div>
    </div>

    <div class="data-grid">
      <div class="data-card">
        <div class="dc-label">💧 Gießen</div>
        <div class="dc-value">${{p.giessen}}<span class="dc-unit">Tage</span></div>
      </div>
      <div class="data-card">
        <div class="dc-label">☀️ Lichtbedarf</div>
        <div class="dc-value">${{p.licht}}<span class="dc-unit">/ 10</span></div>
      </div>
    </div>

    ${{p.info ? `
    <div class="info-box">
      <div class="ib-label">📋 Pflegehinweis</div>
      <div class="ib-text">${{p.info}}</div>
    </div>` : ""}}
  `;
}}

// ============================================================
// PLANT LIST (Sidebar Footer)
// ============================================================
function renderPlantList() {{
  const list = document.getElementById("plant-list");
  // Header beibehalten
  const header = list.querySelector(".pl-header");
  list.innerHTML = "";
  if (header) list.appendChild(header);
  else {{
    const h = document.createElement("div");
    h.className = "pl-header";
    h.textContent = "Alle Pflanzen";
    list.appendChild(h);
  }}

  plants.forEach((p, i) => {{
    const ist  = berechne_lichtwert(p.x, p.y);
    const stat = getLichtStatus(ist, p.licht);
    const item = document.createElement("div");
    item.className = "pl-item" + (activePlantIdx === i ? " active" : "");
    item.innerHTML = `
      <span class="pl-emoji">${{p.emoji}}</span>
      <span class="pl-name">${{p.name}}</span>
      <span class="pl-dot ${{stat}}"></span>
    `;
    item.addEventListener("click", () => selectPlant(i));
    list.appendChild(item);
  }});
}}

// ============================================================
// STATUS & LOADING
// ============================================================
function setStatus(ok, msg) {{
  document.getElementById("status-dot").className = "status-dot" + (ok ? " ok" : "");
  document.getElementById("status-text").textContent = msg;
}}

function hideLoading() {{
  document.getElementById("loading").classList.add("hidden");
}}

// ============================================================
// BILD: Warte auf natürliche Größe für korrektes Layout
// ============================================================
const floorImg = document.getElementById("floor-img");

function onImageReady() {{
  // Canvas auf Bildgröße bringen
  const canvas = getCanvas();
  const W = floorImg.naturalWidth  || 610;
  const H = floorImg.naturalHeight || 630;
  canvas.style.width  = W + "px";
  canvas.style.height = H + "px";
  // Skalierung für kleine Bildschirme
  const area = document.getElementById("map-area");
  const aW = area.clientWidth  - 40;
  const aH = area.clientHeight - 40;
  const scale = Math.min(1, aW / W, aH / H);
  getCanvas().style.transform = `translate(-50%, -50%) scale(${{scale}})`;
}}

floorImg.addEventListener("load", onImageReady);
if (floorImg.complete) onImageReady();

window.addEventListener("resize", onImageReady);

// ============================================================
// START
// ============================================================
loadPlants();
</script>
</body>
</html>
"""

# Höhe dynamisch: volle Viewport-Höhe minus Header-Overhead von Streamlit
components.html(html_app, height=820, scrolling=False)
