import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# KONFIGURATION
# ============================================================
st.set_page_config(layout="wide", page_title="Pflanzen-Planer Pro", page_icon="🌿")

st.markdown("""
<style>
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  .stApp { background: #0f1117; }
</style>
""", unsafe_allow_html=True)

SHEET_ID  = "1cbOPNq-CrYrin-U0OkUJ5AE2AWF6Ba7RqIHlVOtUCK0"
CSV_URL   = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
GITHUB_BASE = "https://raw.githubusercontent.com/simondereck1-hue/Pflanzen-bersicht/main"

# ============================================================
# FLOOR METADATA  (aus Maße.docx)
# ============================================================
FLOOR_DATA = {
    "EG": {
        "url": f"{GITHUB_BASE}/EG.png",
        "imgW": 1312, "imgH": 808,
        "floorX1": 170, "floorY1": 5, "floorX2": 1100, "floorY2": 570,
        "realW": 10, "realH": 6,
        "windows": [
            {"x1":170,"y1":95,  "x2":170, "y2":470, "side":"W"},
            {"x1":900,"y1":570, "x2":1000,"y2":570, "side":"S"},
            {"x1":1100,"y1":340,"x2":1100,"y2":530, "side":"E"},
            {"x1":1100,"y1":33, "x2":1100,"y2":100, "side":"E"},
        ],
        "walls": [
            {"x1":750,"y1":270,"x2":1100,"y2":270},
            {"x1":760,"y1":5,  "x2":760, "y2":170},
            {"x1":520,"y1":5,  "x2":520, "y2":170},
        ],
    },
    "1. OG": {
        "url": f"{GITHUB_BASE}/1.%20OG.png",
        "imgW": 1300, "imgH": 800,
        "floorX1": 110, "floorY1": 0, "floorX2": 1150, "floorY2": 620,
        "realW": 10, "realH": 6,
        "windows": [
            {"x1":110,"y1":110,"x2":110,"y2":175,"side":"W"},
            {"x1":110,"y1":315,"x2":110,"y2":515,"side":"W"},
            {"x1":590,"y1":620,"x2":740,"y2":620,"side":"S"},
            {"x1":1150,"y1":405,"x2":1150,"y2":580,"side":"E"},
            {"x1":1150,"y1":210,"x2":1150,"y2":335,"side":"E"},
        ],
        "walls": [
            {"x1":510,"y1":310,"x2":510,"y2":620},
            {"x1":510,"y1":310,"x2":790,"y2":310},
            {"x1":790,"y1":310,"x2":790,"y2":375},
            {"x1":790,"y1":375,"x2":1150,"y2":375},
            {"x1":790,"y1":0,  "x2":790,"y2":200},
            {"x1":510,"y1":0,  "x2":510,"y2":200},
        ],
    },
    "2. OG": {
        "url": f"{GITHUB_BASE}/2.%20OG.png",
        "imgW": 1348, "imgH": 784,
        "floorX1": 210, "floorY1": 10, "floorX2": 1100, "floorY2": 580,
        "realW": 10, "realH": 6,
        "windows": [
            {"x1":210,"y1":210,"x2":210,"y2":375,"side":"W"},
            {"x1":630,"y1":580,"x2":770,"y2":580,"side":"S"},
        ],
        "walls": [
            {"x1":560,"y1":280,"x2":560,"y2":580},
            {"x1":560,"y1":280,"x2":1100,"y2":280},
            {"x1":800,"y1":10, "x2":800,"y2":180},
            {"x1":560,"y1":10, "x2":560,"y2":180},
        ],
    },
}

import json
FLOOR_DATA_JSON = json.dumps(FLOOR_DATA)

# ============================================================
# HTML / JS APP
# ============================================================
html_app = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>
/* ── TOKENS ── */
:root {{
  --bg:#0f1117; --surface:#171b26; --surface-2:#1e2433; --surface-3:#232940;
  --border:rgba(255,255,255,0.07); --border-2:rgba(255,255,255,0.12);
  --accent:#4ade80; --accent-dim:rgba(74,222,128,0.12); --accent-glow:rgba(74,222,128,0.35);
  --warn:#fbbf24; --warn-dim:rgba(251,191,36,0.12);
  --danger:#f87171; --danger-dim:rgba(248,113,113,0.12);
  --text:#f0f4f8; --muted:#6b7a99; --muted2:#4a5568;
  --r:12px; --rs:8px; --rx:16px;
  --transition:.22s cubic-bezier(.4,0,.2,1);
  --sidebar-w:300px;
  --header-h:52px; --tab-h:46px;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;overflow:hidden}}
body{{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);display:flex;flex-direction:column}}
button{{font-family:inherit;cursor:pointer;border:none;background:none;color:inherit}}
input,select{{font-family:inherit}}

/* ── HEADER ── */
#header{{
  height:var(--header-h);background:var(--surface);border-bottom:1px solid var(--border);
  display:flex;align-items:center;padding:0 20px;gap:10px;flex-shrink:0;z-index:200;
}}
.logo{{font-family:'Syne',sans-serif;font-weight:800;font-size:17px;color:var(--accent);letter-spacing:-.5px}}
.logo-sep{{color:var(--border-2);font-size:20px}}
.status-wrap{{margin-left:auto;display:flex;align-items:center;gap:8px;font-size:12px;color:var(--muted)}}
.sdot{{width:7px;height:7px;border-radius:50%;background:var(--muted);transition:background .3s}}
.sdot.ok{{background:var(--accent);box-shadow:0 0 8px var(--accent)}}

/* ── TABS ── */
#tabs{{
  height:var(--tab-h);background:var(--surface);border-bottom:1px solid var(--border);
  display:flex;align-items:flex-end;padding:0 20px;gap:4px;flex-shrink:0;z-index:150;
}}
.tab{{
  padding:10px 18px;font-size:13px;font-weight:500;color:var(--muted);
  border-radius:var(--rs) var(--rs) 0 0;cursor:pointer;
  border:1px solid transparent;border-bottom:none;transition:all var(--transition);
  position:relative;bottom:-1px;
}}
.tab:hover{{color:var(--text);background:var(--surface-2)}}
.tab.active{{color:var(--accent);background:var(--bg);border-color:var(--border);border-bottom:1px solid var(--bg)}}
.tab-icon{{margin-right:7px}}

/* ── MAIN ── */
#main{{display:flex;flex:1;overflow:hidden;position:relative}}

/* ── LEFT SIDEBAR (Inventory) ── */
#left-sidebar{{
  width:var(--sidebar-w);background:var(--surface);border-right:1px solid var(--border);
  display:flex;flex-direction:column;overflow:hidden;flex-shrink:0;
}}
#left-sidebar.hidden{{display:none}}
.sidebar-header{{
  padding:16px 16px 12px;font-family:'Syne',sans-serif;font-weight:700;font-size:13px;
  color:var(--muted);text-transform:uppercase;letter-spacing:.08em;
  border-bottom:1px solid var(--border);flex-shrink:0;display:flex;align-items:center;gap:8px;
}}
.sidebar-header span{{flex:1}}
.inv-search{{
  margin:10px 12px;padding:8px 12px;background:var(--surface-2);border:1px solid var(--border);
  border-radius:var(--rs);color:var(--text);font-size:13px;width:calc(100% - 24px);
}}
.inv-search::placeholder{{color:var(--muted)}}
.inv-search:focus{{outline:none;border-color:var(--accent)}}

.inv-group{{padding:8px 0}}
.inv-group-label{{
  padding:4px 14px 6px;font-size:11px;color:var(--muted2);text-transform:uppercase;letter-spacing:.07em
}}
.inv-item{{
  display:flex;align-items:center;gap:9px;padding:8px 14px;cursor:grab;
  transition:background var(--transition);user-select:none;
}}
.inv-item:hover{{background:var(--surface-2)}}
.inv-item.dragging-source{{opacity:.4}}
.inv-item.placed{{opacity:.55;cursor:default}}
.inv-item.placed:hover{{background:transparent}}
.inv-emoji{{font-size:18px;width:24px;text-align:center}}
.inv-name{{font-size:13px;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.inv-badge{{
  font-size:10px;padding:2px 7px;border-radius:99px;
  background:var(--surface-3);color:var(--muted);white-space:nowrap
}}
.inv-badge.placed-badge{{background:var(--accent-dim);color:var(--accent)}}
.inv-floor-switcher{{
  margin:auto 14px 14px;padding:6px 10px;
  background:var(--surface-2);border:1px solid var(--border);border-radius:var(--r);
  display:flex;gap:6px;flex-shrink:0
}}
.floor-btn{{
  flex:1;padding:7px 4px;font-size:12px;font-weight:500;
  border-radius:var(--rs);transition:all var(--transition);color:var(--muted)
}}
.floor-btn:hover{{background:var(--surface-3);color:var(--text)}}
.floor-btn.active{{background:var(--accent-dim);color:var(--accent);border:1px solid var(--accent-glow)}}

/* ── MAP AREA ── */
#map-area{{
  flex:1;position:relative;overflow:hidden;
  background:radial-gradient(ellipse at 20% 50%,rgba(74,222,128,.04) 0%,transparent 60%),var(--bg);
}}
#map-canvas{{
  position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%);
}}
#floor-img{{
  position:absolute;inset:0;width:100%;height:100%;
  object-fit:contain;pointer-events:none;user-select:none;opacity:.9;
}}
/* Light overlay canvas */
#light-canvas{{
  position:absolute;inset:0;width:100%;height:100%;
  pointer-events:none;opacity:.55;
}}
/* Drop zone highlight */
#map-canvas.drag-over{{
  outline:2px dashed var(--accent);outline-offset:4px;
}}

/* ── PLANT PINS ── */
.plant-pin{{
  position:absolute;display:flex;flex-direction:column;align-items:center;
  cursor:grab;user-select:none;touch-action:none;z-index:10;
  transition:transform var(--transition),filter var(--transition);
}}
.plant-pin:hover{{z-index:50;filter:drop-shadow(0 4px 16px rgba(74,222,128,.5))}}
.plant-pin.dragging{{cursor:grabbing;z-index:100;transition:none;filter:drop-shadow(0 8px 24px rgba(74,222,128,.7))}}
.plant-pin.active .pin-bubble{{background:var(--accent);color:#0f1117;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-glow)}}
.plant-pin.highlight-pulse .pin-bubble{{animation:highlightPulse 1.5s ease-in-out 3}}
@keyframes highlightPulse{{0%,100%{{box-shadow:0 0 0 0 var(--accent-glow)}}50%{{box-shadow:0 0 0 12px rgba(74,222,128,0)}}}}
.pin-bubble{{
  width:40px;height:40px;border-radius:50%;background:var(--surface-2);
  border:2px solid rgba(74,222,128,.35);display:flex;align-items:center;justify-content:center;
  font-size:19px;transition:all var(--transition);box-shadow:0 2px 12px rgba(0,0,0,.4);
}}
.pin-indicator{{width:8px;height:8px;border-radius:50%;margin-top:3px;background:var(--muted);transition:background .3s}}
.pin-indicator.ideal{{background:var(--accent);box-shadow:0 0 6px var(--accent)}}
.pin-indicator.ok{{background:var(--warn);box-shadow:0 0 6px var(--warn)}}
.pin-indicator.bad{{background:var(--danger);box-shadow:0 0 6px var(--danger)}}
.pin-label{{font-size:10px;color:var(--muted);margin-top:3px;white-space:nowrap;max-width:72px;overflow:hidden;text-overflow:ellipsis;text-align:center}}
.pin-light-badge{{
  font-size:9px;padding:1px 5px;border-radius:99px;margin-top:2px;
  background:var(--surface-2);color:var(--muted);font-variant-numeric:tabular-nums;
}}

/* ── RIGHT SIDEBAR (Detail) ── */
#right-sidebar{{
  width:var(--sidebar-w);background:var(--surface);border-left:1px solid var(--border);
  display:flex;flex-direction:column;overflow:hidden;flex-shrink:0;
}}
#right-sidebar.hidden{{display:none}}
#rsb-empty{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;color:var(--muted);padding:24px;text-align:center}}
#rsb-empty .empty-icon{{font-size:44px;opacity:.35}}
#rsb-detail{{flex:1;display:none;flex-direction:column;overflow-y:auto;padding:20px;gap:16px}}
#rsb-detail.visible{{display:flex}}
#rsb-detail::-webkit-scrollbar{{width:4px}}
#rsb-detail::-webkit-scrollbar-thumb{{background:var(--border);border-radius:2px}}

/* Detail components */
.plant-hdr{{display:flex;align-items:flex-start;gap:12px}}
.big-emoji{{font-size:38px;flex-shrink:0;line-height:1}}
.plant-hdr-text h2{{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;line-height:1.2}}
.coords-row{{font-size:11px;color:var(--muted);margin-top:4px;font-variant-numeric:tabular-nums}}
.floor-tag{{
  display:inline-block;padding:2px 8px;border-radius:99px;font-size:11px;
  background:var(--surface-2);color:var(--muted);margin-top:4px;
}}
.score-badge{{border-radius:var(--r);padding:13px;display:flex;align-items:center;gap:12px;background:var(--surface-2)}}
.score-badge .sc-icon{{font-size:24px}}
.score-badge .sc-text h3{{font-family:'Syne',sans-serif;font-size:14px;font-weight:600}}
.score-badge .sc-text p{{font-size:12px;color:var(--muted);margin-top:2px;line-height:1.4}}
.score-badge.ideal{{border:1px solid rgba(74,222,128,.3);background:var(--accent-dim)}}
.score-badge.ideal .sc-text h3{{color:var(--accent)}}
.score-badge.ok{{border:1px solid rgba(251,191,36,.3);background:var(--warn-dim)}}
.score-badge.ok .sc-text h3{{color:var(--warn)}}
.score-badge.bad{{border:1px solid rgba(248,113,113,.3);background:var(--danger-dim)}}
.score-badge.bad .sc-text h3{{color:var(--danger)}}

.light-bar-wrap{{display:flex;flex-direction:column;gap:7px}}
.lbw-label{{display:flex;justify-content:space-between;font-size:12px;color:var(--muted)}}
.lbw-track{{height:6px;border-radius:3px;background:var(--surface-2);position:relative;overflow:hidden}}
.lbw-fill{{height:100%;border-radius:3px;background:var(--accent);transition:width .5s cubic-bezier(.4,0,.2,1)}}
.lbw-needle{{position:absolute;top:0;bottom:0;width:2px;background:rgba(255,255,255,.5);border-radius:1px}}

.data-grid{{display:grid;grid-template-columns:1fr 1fr;gap:9px}}
.dc{{background:var(--surface-2);border:1px solid var(--border);border-radius:var(--rs);padding:13px}}
.dc-lbl{{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:5px}}
.dc-val{{font-family:'Syne',sans-serif;font-size:20px;font-weight:700}}
.dc-unit{{font-size:12px;font-weight:400;color:var(--muted);margin-left:3px}}

.care-row{{
  background:var(--surface-2);border:1px solid var(--border);border-radius:var(--rs);padding:13px;
  display:flex;flex-direction:column;gap:5px
}}
.care-row-lbl{{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}}
.care-row-val{{font-size:13px;line-height:1.5}}

.action-row{{display:flex;gap:8px;margin-top:4px}}
.act-btn{{
  flex:1;padding:9px;border-radius:var(--rs);font-size:12px;font-weight:500;
  transition:all var(--transition);border:1px solid var(--border);background:var(--surface-2);color:var(--muted);
}}
.act-btn:hover{{background:var(--surface-3);color:var(--text)}}
.act-btn.primary{{background:var(--accent-dim);border-color:var(--accent-glow);color:var(--accent)}}
.act-btn.primary:hover{{background:rgba(74,222,128,.25)}}
.act-btn.danger-btn{{background:var(--danger-dim);border-color:rgba(248,113,113,.3);color:var(--danger)}}
.act-btn.danger-btn:hover{{background:rgba(248,113,113,.2)}}

/* ── LIBRARY VIEW ── */
#library-view{{display:none;flex:1;overflow-y:auto;padding:24px;flex-direction:column;gap:16px}}
#library-view.active{{display:flex}}
#library-view::-webkit-scrollbar{{width:4px}}
#library-view::-webkit-scrollbar-thumb{{background:var(--border);border-radius:2px}}
.lib-header{{display:flex;align-items:center;gap:12px;flex-shrink:0}}
.lib-header h2{{font-family:'Syne',sans-serif;font-size:20px;font-weight:700}}
.lib-search{{
  margin-left:auto;padding:8px 14px;background:var(--surface-2);border:1px solid var(--border);
  border-radius:var(--r);color:var(--text);font-size:13px;width:220px;
}}
.lib-search::placeholder{{color:var(--muted)}}
.lib-search:focus{{outline:none;border-color:var(--accent)}}
.lib-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}}
.lib-card{{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:18px;display:flex;flex-direction:column;gap:12px;
  transition:border-color var(--transition),box-shadow var(--transition);
}}
.lib-card:hover{{border-color:var(--border-2);box-shadow:0 4px 24px rgba(0,0,0,.3)}}
.lib-card-top{{display:flex;align-items:center;gap:12px}}
.lib-card-emoji{{font-size:30px}}
.lib-card-name{{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;line-height:1.2}}
.lib-card-floor{{font-size:11px;color:var(--muted);margin-top:3px}}
.lib-card-chips{{display:flex;gap:6px;flex-wrap:wrap}}
.chip{{
  font-size:11px;padding:3px 9px;border-radius:99px;
  background:var(--surface-2);color:var(--muted);border:1px solid var(--border)
}}
.chip.accent-chip{{background:var(--accent-dim);color:var(--accent);border-color:var(--accent-glow)}}
.lib-card-divider{{height:1px;background:var(--border)}}
.lib-care-row{{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted)}}
.lib-care-val{{color:var(--text);font-weight:500}}
.show-on-map-btn{{
  width:100%;padding:9px;border-radius:var(--rs);font-size:12px;font-weight:500;
  background:var(--surface-2);border:1px solid var(--border);color:var(--muted);
  transition:all var(--transition);
}}
.show-on-map-btn:hover{{background:var(--accent-dim);border-color:var(--accent-glow);color:var(--accent)}}

/* ── LOADING ── */
#loading{{
  position:fixed;inset:0;z-index:9999;background:var(--bg);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;
  transition:opacity .4s,visibility .4s;
}}
#loading.hidden{{opacity:0;visibility:hidden}}
#loading .ld-icon{{font-size:44px;animation:pulse 1.5s ease-in-out infinite}}
#loading p{{font-size:14px;color:var(--muted)}}
@keyframes pulse{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}

/* ── TOOLTIP ── */
#tooltip{{
  position:fixed;z-index:500;pointer-events:none;
  background:var(--surface-3);border:1px solid var(--border-2);
  border-radius:var(--rs);padding:8px 12px;font-size:12px;
  box-shadow:0 4px 20px rgba(0,0,0,.4);opacity:0;transition:opacity .15s;
  max-width:200px;
}}
#tooltip.visible{{opacity:1}}

::-webkit-scrollbar{{width:4px;height:4px}}
::-webkit-scrollbar-thumb{{background:var(--border);border-radius:2px}}
</style>
</head>
<body>

<div id="loading"><div class="ld-icon">🌿</div><p>Pflanzendaten werden geladen…</p></div>
<div id="tooltip"></div>

<!-- HEADER -->
<div id="header">
  <span class="logo">🌿 Pflanzen-Planer Pro</span>
  <span class="logo-sep">|</span>
  <span style="font-size:13px;color:var(--muted)" id="month-label"></span>
  <div class="status-wrap">
    <div class="sdot" id="sdot"></div>
    <span id="stext">Verbinden…</span>
  </div>
</div>

<!-- TABS -->
<div id="tabs">
  <button class="tab active" data-tab="planer" onclick="switchTab('planer')">
    <span class="tab-icon">🗺️</span>Grundriss-Planer
  </button>
  <button class="tab" data-tab="library" onclick="switchTab('library')">
    <span class="tab-icon">📚</span>Pflanzen-Bibliothek
  </button>
</div>

<!-- MAIN -->
<div id="main">

  <!-- LEFT SIDEBAR -->
  <div id="left-sidebar">
    <div class="sidebar-header">
      <span>🪴 Inventar</span>
      <span id="inv-count" style="font-size:11px;background:var(--surface-2);padding:2px 7px;border-radius:99px;font-weight:400"></span>
    </div>
    <input class="inv-search" id="inv-search" type="text" placeholder="Suchen…" oninput="filterInventory(this.value)">
    <div id="inv-list" style="flex:1;overflow-y:auto"></div>
    <div class="inv-floor-switcher">
      <button class="floor-btn active" onclick="setFloor('EG')" id="fbtn-EG">EG</button>
      <button class="floor-btn" onclick="setFloor('1. OG')" id="fbtn-1. OG">1.OG</button>
      <button class="floor-btn" onclick="setFloor('2. OG')" id="fbtn-2. OG">2.OG</button>
    </div>
  </div>

  <!-- MAP AREA (Planer) -->
  <div id="map-area" style="flex:1;position:relative;overflow:hidden;background:radial-gradient(ellipse at 20% 50%,rgba(74,222,128,.04) 0%,transparent 60%),var(--bg)">
    <div id="map-canvas">
      <img id="floor-img" src="" alt="Grundriss" draggable="false"
           onerror="this.src='https://placehold.co/1100x600/171b26/4ade80?text=Grundriss+nicht+gefunden'">
      <canvas id="light-canvas"></canvas>
    </div>
  </div>

  <!-- LIBRARY VIEW -->
  <div id="library-view">
    <div class="lib-header">
      <h2>🌱 Pflanzen-Bibliothek</h2>
      <input class="lib-search" id="lib-search" type="text" placeholder="🔍 Pflanze suchen…" oninput="filterLibrary(this.value)">
    </div>
    <div class="lib-grid" id="lib-grid"></div>
  </div>

  <!-- RIGHT SIDEBAR -->
  <div id="right-sidebar">
    <div id="rsb-empty">
      <div class="empty-icon">🪴</div>
      <p style="font-size:13px;line-height:1.6;color:var(--muted)">Klicke auf eine Pflanze<br>für Details &amp; Pflegehinweise.</p>
    </div>
    <div id="rsb-detail"></div>
  </div>

</div><!-- /main -->

<script>
// ============================================================
// KONSTANTEN & FLOOR DATA
// ============================================================
const CSV_URL   = "{CSV_URL}";
const FLOOR_DATA = {FLOOR_DATA_JSON};
const PLANT_EMOJIS = ["🌿","🌱","🪴","🌺","🌸","🌻","🌵","🎋","🌴","🌳","🍀","☘️","🌾","🌼","💐","🫧","🌏","🌙","✨","🪷"];
const MONTHS_DE = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];
const NOW_MONTH = new Date().getMonth(); // 0-based

// ============================================================
// STATE
// ============================================================
let plants        = [];          // all plants
let positions     = {{}};          // plantIdx -> {{floor, x, y}} (relative 0-1 on img)
let activePIdx    = null;
let currentFloor  = "EG";
let currentTab    = "planer";
let dragSrcIdx    = null;        // inventory drag source
let inventoryFilter = "";
let libraryFilter   = "";

// ============================================================
// UTILITY
// ============================================================
const $ = id => document.getElementById(id);

function setStatus(ok, msg) {{
  $("sdot").className = "sdot" + (ok?" ok":"");
  $("stext").textContent = msg;
}}

function showTooltip(msg, x, y) {{
  const t = $("tooltip");
  t.textContent = msg;
  t.style.left = (x+12)+"px";
  t.style.top  = (y+12)+"px";
  t.classList.add("visible");
}}
function hideTooltip() {{ $("tooltip").classList.remove("visible"); }}

// ============================================================
// MONTH LABEL
// ============================================================
$("month-label").textContent = MONTHS_DE[NOW_MONTH] + " " + new Date().getFullYear();

// ============================================================
// CSV LOAD
// ============================================================
async function loadPlants() {{
  setStatus(false, "Lade Daten…");
  try {{
    const res = await fetch(CSV_URL);
    if (!res.ok) throw new Error("HTTP "+res.status);
    const text = await res.text();
    plants = parseCSV(text);
    setStatus(true, plants.length+" Pflanzen geladen");
  }} catch(e) {{
    console.warn("CSV-Fehler:", e);
    plants = [
      {{name:"Monstera Deliciosa",licht:7,giessen:3,dungen:4,umtopfen:"Alle 2 Jahre",info:"Robuste Zimmerpflanze, indirektes Licht",emoji:"🌿"}},
      {{name:"Sukkulente",licht:9,giessen:14,dungen:8,umtopfen:"Alle 3 Jahre",info:"Sehr genügsam, viel Sonne",emoji:"🌵"}},
      {{name:"Farn",licht:3,giessen:2,dungen:3,umtopfen:"Jährlich",info:"Schattig & feucht",emoji:"🌿"}},
      {{name:"Orchidee",licht:6,giessen:10,dungen:6,umtopfen:"Alle 2 Jahre",info:"Indirektes Licht, wenig Wasser",emoji:"🌺"}},
    ];
    setStatus(false,"Offline-Modus");
  }}

  plants.forEach((p,i) => {{ if(!p.emoji) p.emoji = PLANT_EMOJIS[i%PLANT_EMOJIS.length]; }});

  $("inv-count").textContent = plants.length;
  renderInventory();
  renderLibrary();
  setFloor(currentFloor);
  $("loading").classList.add("hidden");
}}

// ============================================================
// CSV PARSE
// ============================================================
function parseCSV(text) {{
  const lines   = text.trim().split("\\n");
  const headers = lines[0].split(",").map(h=>h.trim().replace(/"/g,""));

  const col = (candidates) => {{
    for(const c of candidates) {{
      const idx = headers.findIndex(h=>h.toLowerCase().includes(c.toLowerCase()));
      if(idx>=0) return idx;
    }}
    return -1;
  }};

  const colName    = col(["Pflanze","Name","name"]);
  const colLicht   = col(["Lichtbedarf"]);
  const colUmtopf  = col(["Umtopfen"]);

  // Gießen/Düngen für aktuellen Monat
  const monthName  = MONTHS_DE[NOW_MONTH];
  const colGiess   = col(["Gießen_"+monthName,"Giessen_"+monthName]);
  const colDueng   = col(["Düngen_"+monthName,"Dunegen_"+monthName,"Dunken_"+monthName]);

  // Alle Gieß/Düng-Spalten für Bibliothek
  const giessAll = {{}};
  const duengAll = {{}};
  MONTHS_DE.forEach(m => {{
    giessAll[m] = col(["Gießen_"+m,"Giessen_"+m]);
    duengAll[m] = col(["Düngen_"+m,"Dunegen_"+m]);
  }});

  return lines.slice(1).filter(l=>l.trim()).map((line,i)=>{{
    const cols = splitCSVLine(line);
    const obj  = {{
      id:      i,
      name:    colName>=0 ? (cols[colName]||"Pflanze "+(i+1)) : "Pflanze "+(i+1),
      licht:   colLicht>=0 ? (parseFloat(cols[colLicht])||5) : 5,
      giessen: colGiess>=0 ? (cols[colGiess]||"—") : "—",
      dungen:  colDueng>=0 ? (cols[colDueng]||"—") : "—",
      umtopfen:colUmtopf>=0? (cols[colUmtopf]||"—") : "—",
      emoji:   PLANT_EMOJIS[i%PLANT_EMOJIS.length],
      giessAll:{{}}, duengAll:{{}},
    }};
    MONTHS_DE.forEach(m=>{{
      obj.giessAll[m] = giessAll[m]>=0 ? (cols[giessAll[m]]||"—") : "—";
      obj.duengAll[m] = duengAll[m]>=0 ? (cols[duengAll[m]]||"—") : "—";
    }});
    return obj;
  }});
}}

function splitCSVLine(line) {{
  const result=[]; let cur="",inQ=false;
  for(const ch of line) {{
    if(ch==='"'){{inQ=!inQ;continue}}
    if(ch===','&&!inQ){{result.push(cur.trim());cur="";continue}}
    cur+=ch;
  }}
  result.push(cur.trim()); return result;
}}

// ============================================================
// TAB SWITCHING
// ============================================================
function switchTab(tab) {{
  currentTab = tab;
  document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("active",t.dataset.tab===tab));

  const isPlaner  = tab==="planer";
  $("left-sidebar").classList.toggle("hidden", !isPlaner);
  $("right-sidebar").classList.toggle("hidden", !isPlaner);
  $("map-area").style.display      = isPlaner ? "block" : "none";
  $("library-view").classList.toggle("active", !isPlaner);

  if(!isPlaner) renderLibrary();
}}

// ============================================================
// FLOOR SWITCHING
// ============================================================
function setFloor(floor) {{
  currentFloor = floor;

  // Update floor buttons
  ["EG","1. OG","2. OG"].forEach(f=>{{
    const btn = $("fbtn-"+f);
    if(btn) btn.classList.toggle("active", f===floor);
  }});

  const fd  = FLOOR_DATA[floor];
  const img = $("floor-img");
  img.src   = fd.url;
  img.onload = () => {{ onImageReady(); drawLightMap(); render(); }};
  if(img.complete && img.naturalWidth) {{ onImageReady(); drawLightMap(); render(); }}
  render();
  renderInventory();
  if(activePIdx!==null) renderDetail(activePIdx);
}}

// ============================================================
// LIGHT ENGINE
// ============================================================
function px2rel(px, p1, p2) {{ return (px-p1)/(p2-p1); }}

function windowMidpoints(floor) {{
  const fd = FLOOR_DATA[floor];
  return fd.windows.map(w=>{{
    const mx = (w.x1+w.x2)/2;
    const my = (w.y1+w.y2)/2;
    return {{
      rx: px2rel(mx, fd.floorX1, fd.floorX2),
      ry: px2rel(my, fd.floorY1, fd.floorY2),
      len: Math.sqrt((w.x2-w.x1)**2+(w.y2-w.y1)**2),
    }};
  }});
}}

function segmentsIntersect(ax,ay,bx,by, cx,cy,dx,dy) {{
  const denom = (bx-ax)*(dy-cy)-(by-ay)*(dx-cx);
  if(Math.abs(denom)<1e-10) return false;
  const t = ((cx-ax)*(dy-cy)-(cy-ay)*(dx-cx))/denom;
  const u = ((cx-ax)*(by-ay)-(cy-ay)*(bx-ax))/denom;
  return t>=0&&t<=1&&u>=0&&u<=1;
}}

function isOccluded(px,py, wx,wy, floor) {{
  const fd   = FLOOR_DATA[floor];
  const imgW = fd.imgW; const imgH = fd.imgH;
  const fx1  = fd.floorX1; const fy1 = fd.floorY1;
  const fx2  = fd.floorX2; const fy2 = fd.floorY2;

  // Convert rel (0-1 on floor) → absolute pixel
  const toAbsX = r => fx1 + r*(fx2-fx1);
  const toAbsY = r => fy1 + r*(fy2-fy1);

  const pAbsX = toAbsX(px); const pAbsY = toAbsY(py);
  const wAbsX = toAbsX(wx); const wAbsY = toAbsY(wy);

  for(const wall of fd.walls) {{
    if(segmentsIntersect(pAbsX,pAbsY,wAbsX,wAbsY, wall.x1,wall.y1,wall.x2,wall.y2)) return true;
  }}
  return false;
}}

function computeLicht(px, py, floor) {{
  const fd   = FLOOR_DATA[floor];
  const pxM  = fd.realW; const pyM = fd.realH; // 10m × 6m
  let total   = 0;

  for(const w of fd.windows) {{
    const wx = px2rel((w.x1+w.x2)/2, fd.floorX1, fd.floorX2);
    const wy = px2rel((w.y1+w.y2)/2, fd.floorY1, fd.floorY2);

    if(isOccluded(px,py,wx,wy,floor)) continue;

    // Distance in metres
    const dxM = (px-wx)*pxM;
    const dyM = (py-wy)*pyM;
    const distM = Math.sqrt(dxM*dxM+dyM*dyM);

    // Window size contribution (normalised)
    const winSizePx = Math.sqrt((w.x2-w.x1)**2+(w.y2-w.y1)**2);
    const winFactor  = Math.min(1, winSizePx/200);

    // Quadratic falloff
    total += winFactor / (1 + 0.35*distM*distM);
  }}

  return Math.min(10, Math.max(1, Math.round(total*40*10)/10));
}}

function getLichtStatus(ist, soll) {{
  if(ist>=soll)      return "ideal";
  if(ist>=soll-2)    return "ok";
  return "bad";
}}

const STATUS_CFG = {{
  ideal:{{icon:"🌟",label:"Idealer Standort",desc:"Ausreichend Licht für diese Pflanze.",cls:"ideal"}},
  ok:   {{icon:"⛅",label:"Akzeptabler Standort",desc:"Etwas weniger als optimal, aber tolerierbar.",cls:"ok"}},
  bad:  {{icon:"🌑",label:"Zu dunkel",desc:"Bitte näher ans Fenster stellen.",cls:"bad"}},
}};

// ============================================================
// LIGHT MAP (Canvas overlay)
// ============================================================
function drawLightMap() {{
  const img    = $("floor-img");
  const canvas = $("light-canvas");
  if(!img.naturalWidth) return;
  canvas.width  = img.naturalWidth;
  canvas.height = img.naturalHeight;
  canvas.style.width  = img.naturalWidth+"px";
  canvas.style.height = img.naturalHeight+"px";

  const ctx  = canvas.getContext("2d");
  const fd   = FLOOR_DATA[currentFloor];
  const fw   = fd.floorX2 - fd.floorX1;
  const fh   = fd.floorY2 - fd.floorY1;
  const step = 16; // pixel grid step

  for(let iy=0; iy<img.naturalHeight; iy+=step) {{
    for(let ix=0; ix<img.naturalWidth; ix+=step) {{
      // Only draw inside floor bounds
      if(ix<fd.floorX1||ix>fd.floorX2||iy<fd.floorY1||iy>fd.floorY2) continue;
      const rx = (ix-fd.floorX1)/fw;
      const ry = (iy-fd.floorY1)/fh;
      const lv = computeLicht(rx,ry,currentFloor);
      const alpha = (lv/10)*0.28;
      ctx.fillStyle = `rgba(74,222,128,${{alpha.toFixed(3)}})`;
      ctx.fillRect(ix,iy,step,step);
    }}
  }}
}}

// ============================================================
// IMAGE READY
// ============================================================
function onImageReady() {{
  const img    = $("floor-img");
  const canvas = $("map-canvas");
  const W      = img.naturalWidth  || 1100;
  const H      = img.naturalHeight || 600;
  canvas.style.width  = W+"px";
  canvas.style.height = H+"px";
  const area   = $("map-area");
  const aW     = area.clientWidth-40;
  const aH     = area.clientHeight-40;
  const scale  = Math.min(1, aW/W, aH/H);
  canvas.style.transform = `translate(-50%,-50%) scale(${{scale}})`;
}}
$("floor-img").addEventListener("load", ()=>{{onImageReady();drawLightMap();render();}});
window.addEventListener("resize", onImageReady);

// ============================================================
// RENDER PINS
// ============================================================
function render() {{
  const canvas = $("map-canvas");
  const img    = $("floor-img");
  const W      = img.naturalWidth  || 1100;
  const H      = img.naturalHeight || 600;
  canvas.style.width  = W+"px";
  canvas.style.height = H+"px";

  canvas.querySelectorAll(".plant-pin").forEach(el=>el.remove());

  plants.forEach((p,i)=>{{
    const pos = positions[i];
    if(!pos || pos.floor !== currentFloor) return;

    const ist  = computeLicht(pos.x, pos.y, currentFloor);
    const stat = getLichtStatus(ist, p.licht);

    const pin  = document.createElement("div");
    pin.className = "plant-pin"+(activePIdx===i?" active":"");
    pin.dataset.idx = i;

    const tx = Math.round(pos.x*W - 20);
    const ty = Math.round(pos.y*H - 20);
    pin.style.transform = `translate(${{tx}}px,${{ty}}px)`;

    pin.innerHTML = `
      <div class="pin-bubble">${{p.emoji}}</div>
      <div class="pin-indicator ${{stat}}"></div>
      <div class="pin-label">${{p.name.split(" ")[0]}}</div>
      <div class="pin-light-badge">${{ist}}/10</div>
    `;

    setupPinDrag(pin, i);
    pin.addEventListener("click", e=>{{e.stopPropagation();selectPlant(i);}});
    pin.addEventListener("mousemove", e=>showTooltip(`${{p.name}} · Licht: ${{ist}}/10 · Bedarf: ${{p.licht}}/10`,e.clientX,e.clientY));
    pin.addEventListener("mouseleave", hideTooltip);

    canvas.appendChild(pin);
  }});
}}

// ============================================================
// SELECT PLANT
// ============================================================
function selectPlant(idx) {{
  activePIdx = (activePIdx===idx) ? null : idx;
  render();
  if(activePIdx!==null) renderDetail(activePIdx);
  else showEmptyDetail();
}}

function showEmptyDetail() {{
  $("rsb-empty").style.display = "";
  $("rsb-detail").classList.remove("visible");
}}

// ============================================================
// RENDER DETAIL (Right Sidebar)
// ============================================================
function renderDetail(idx) {{
  const p   = plants[idx];
  const pos = positions[idx];
  const ist = pos ? computeLicht(pos.x, pos.y, currentFloor) : null;
  const stat= ist ? getLichtStatus(ist, p.licht) : null;
  const sc  = stat ? STATUS_CFG[stat] : null;
  const fd  = FLOOR_DATA[currentFloor];

  $("rsb-empty").style.display = "none";
  const det = $("rsb-detail");
  det.classList.add("visible");

  const coordsHTML = pos
    ? `<div class="coords-row">Rel. ${{(pos.x*100).toFixed(1)}}% · ${{(pos.y*100).toFixed(1)}}%</div>
       <span class="floor-tag">📍 ${{pos.floor}}</span>`
    : `<span class="floor-tag">📦 Im Inventar</span>`;

  const lightHTML = ist ? `
    <div class="score-badge ${{sc.cls}}">
      <div class="sc-icon">${{sc.icon}}</div>
      <div class="sc-text"><h3>${{sc.label}}</h3><p>${{sc.desc}}</p></div>
    </div>
    <div class="light-bar-wrap">
      <div class="lbw-label"><span>💡 Licht</span><span>${{ist}} / 10</span></div>
      <div class="lbw-track">
        <div class="lbw-fill" style="width:${{(ist/10*100).toFixed(1)}}%;background:${{stat==='ideal'?'var(--accent)':stat==='ok'?'var(--warn)':'var(--danger)'}}"></div>
        <div class="lbw-needle" style="left:${{(p.licht/10*100).toFixed(1)}}%"></div>
      </div>
      <div class="lbw-label"><span style="color:var(--muted)">Bedarf: ${{p.licht}}/10</span><span style="color:var(--muted)">Verfügbar: ${{ist}}/10</span></div>
    </div>
  ` : `<div style="font-size:13px;color:var(--muted);background:var(--surface-2);border-radius:var(--rs);padding:13px">Pflanze auf Karte platzieren, um Lichtwert zu berechnen.</div>`;

  const removeHTML = pos
    ? `<button class="act-btn danger-btn" onclick="removePlant(${{idx}})">🗑️ Entfernen</button>`
    : "";

  det.innerHTML = `
    <div class="plant-hdr">
      <div class="big-emoji">${{p.emoji}}</div>
      <div class="plant-hdr-text">
        <h2>${{p.name}}</h2>
        ${{coordsHTML}}
      </div>
    </div>
    ${{lightHTML}}
    <div class="data-grid">
      <div class="dc">
        <div class="dc-lbl">💧 Gießen (${{MONTHS_DE[NOW_MONTH]}})</div>
        <div class="dc-val">${{p.giessen||"—"}}<span class="dc-unit">Tage</span></div>
      </div>
      <div class="dc">
        <div class="dc-lbl">🌿 Düngen (${{MONTHS_DE[NOW_MONTH]}})</div>
        <div class="dc-val">${{p.dungen||"—"}}<span class="dc-unit"></span></div>
      </div>
      <div class="dc">
        <div class="dc-lbl">☀️ Lichtbedarf</div>
        <div class="dc-val">${{p.licht}}<span class="dc-unit">/ 10</span></div>
      </div>
      <div class="dc">
        <div class="dc-lbl">🪴 Umtopfen</div>
        <div class="dc-val" style="font-size:13px;padding-top:4px">${{p.umtopfen||"—"}}</div>
      </div>
    </div>
    <div class="action-row">
      <button class="act-btn primary" onclick="selectPlant(${{idx}})">✓ Schließen</button>
      ${{removeHTML}}
    </div>
  `;
}}

function removePlant(idx) {{
  delete positions[idx];
  activePIdx = null;
  render();
  renderInventory();
  showEmptyDetail();
}}

// ============================================================
// RENDER INVENTORY (Left Sidebar)
// ============================================================
function renderInventory() {{
  const list    = $("inv-list");
  const filter  = inventoryFilter.toLowerCase();

  const available  = [];
  const placedHere = [];
  const otherFloor = [];

  plants.forEach((p,i)=>{{
    if(filter && !p.name.toLowerCase().includes(filter)) return;
    const pos = positions[i];
    if(!pos) available.push(i);
    else if(pos.floor===currentFloor) placedHere.push(i);
    else otherFloor.push(i);
  }});

  list.innerHTML = "";

  const makeGroup = (label, indices, placed) => {{
    if(!indices.length) return;
    const grp = document.createElement("div");
    grp.className = "inv-group";
    grp.innerHTML = `<div class="inv-group-label">${{label}} (${{indices.length}})</div>`;
    indices.forEach(i=>{{
      const p    = plants[i];
      const item = document.createElement("div");
      item.className = "inv-item"+(placed?" placed":"");
      item.dataset.pidx = i;
      const badgeHtml = placed
        ? `<span class="inv-badge placed-badge">📍 ${{positions[i]?.floor||""}}</span>`
        : `<span class="inv-badge">Verfügbar</span>`;
      item.innerHTML = `
        <span class="inv-emoji">${{p.emoji}}</span>
        <span class="inv-name">${{p.name}}</span>
        ${{badgeHtml}}
      `;
      if(!placed) {{
        item.draggable = true;
        item.addEventListener("dragstart", e=>{{
          dragSrcIdx = i;
          e.dataTransfer.effectAllowed = "move";
          setTimeout(()=>item.classList.add("dragging-source"),0);
        }});
        item.addEventListener("dragend", ()=>{{
          item.classList.remove("dragging-source");
          dragSrcIdx = null;
        }});
        item.addEventListener("click", ()=>{{activePIdx=i;render();renderDetail(i);}});
      }}
      grp.appendChild(item);
    }});
    list.appendChild(grp);
  }};

  makeGroup("🟢 Verfügbar",  available,  false);
  makeGroup("📍 Hier platziert", placedHere, true);
  makeGroup("🔵 Anderes Stockwerk", otherFloor, true);
}}

function filterInventory(val) {{
  inventoryFilter = val;
  renderInventory();
}}

// ============================================================
// DROP ONTO MAP
// ============================================================
const mapArea = $("map-area");
mapArea.addEventListener("dragover", e=>{{
  e.preventDefault(); e.dataTransfer.dropEffect="move";
  $("map-canvas").classList.add("drag-over");
}});
mapArea.addEventListener("dragleave", ()=>$("map-canvas").classList.remove("drag-over"));
mapArea.addEventListener("drop", e=>{{
  e.preventDefault();
  $("map-canvas").classList.remove("drag-over");
  if(dragSrcIdx===null) return;

  const img   = $("floor-img");
  const W     = img.naturalWidth  || 1100;
  const H     = img.naturalHeight || 600;
  const area  = $("map-area");
  const aW    = area.clientWidth;  const aH = area.clientHeight;
  const scale = parseFloat($("map-canvas").style.transform.match(/scale\(([^)]+)\)/)?.[1]||1);

  // Canvas is centered via translate(-50%,-50%) + scale
  const cX = aW/2 - W*scale/2;
  const cY = aH/2 - H*scale/2;
  const rx  = Math.max(0, Math.min(1, (e.clientX - cX)/(W*scale)));
  const ry  = Math.max(0, Math.min(1, (e.clientY - cY)/(H*scale)));

  positions[dragSrcIdx] = {{floor:currentFloor, x:rx, y:ry}};
  activePIdx = dragSrcIdx;
  dragSrcIdx = null;

  render();
  renderInventory();
  renderDetail(activePIdx);
}});

// ============================================================
// PIN DRAG (move placed plants)
// ============================================================
function setupPinDrag(pin, idx) {{
  let startX,startY,startPX,startPY,dragging=false;

  function getWH() {{
    const img = $("floor-img");
    const W   = img.naturalWidth  || 1100;
    const H   = img.naturalHeight || 600;
    const rect= img.getBoundingClientRect();
    return {{W,H,scaleX:W/rect.width,scaleY:H/rect.height}};
  }}

  pin.addEventListener("pointerdown", e=>{{
    if(e.button!==0&&e.button!==undefined) return;
    e.preventDefault(); e.stopPropagation();
    dragging=true; pin.classList.add("dragging"); pin.setPointerCapture(e.pointerId);
    startX=e.clientX; startY=e.clientY;
    startPX=positions[idx].x; startPY=positions[idx].y;
  }});

  pin.addEventListener("pointermove", e=>{{
    if(!dragging) return; e.preventDefault();
    const {{W,H,scaleX,scaleY}} = getWH();
    positions[idx].x = Math.max(0,Math.min(1, startPX+(e.clientX-startX)*scaleX/W));
    positions[idx].y = Math.max(0,Math.min(1, startPY+(e.clientY-startY)*scaleY/H));
    const tx=Math.round(positions[idx].x*W-20);
    const ty=Math.round(positions[idx].y*H-20);
    pin.style.transform=`translate(${{tx}}px,${{ty}}px)`;
    // live light update
    const ist = computeLicht(positions[idx].x, positions[idx].y, currentFloor);
    const stat= getLichtStatus(ist, plants[idx].licht);
    pin.querySelector(".pin-indicator").className="pin-indicator "+stat;
    pin.querySelector(".pin-light-badge").textContent=ist+"/10";
    if(activePIdx===idx) renderDetail(idx);
  }});

  pin.addEventListener("pointerup", e=>{{
    if(!dragging) return;
    dragging=false; pin.classList.remove("dragging");
    render();
    if(activePIdx===idx) renderDetail(idx);
  }});
  pin.addEventListener("pointercancel",e=>{{dragging=false;pin.classList.remove("dragging")}});
}}

// ============================================================
// LIBRARY VIEW
// ============================================================
function renderLibrary() {{
  const grid   = $("lib-grid");
  const filter = libraryFilter.toLowerCase();
  grid.innerHTML = "";

  plants.filter(p=>!filter||p.name.toLowerCase().includes(filter)).forEach((p,i)=>{{
    const pos    = positions[i];
    const floorTag = pos ? `📍 ${{pos.floor}}` : "📦 Inventar";
    const ist    = pos ? computeLicht(pos.x,pos.y,pos.floor) : null;
    const stat   = ist ? getLichtStatus(ist, p.licht) : null;

    const card = document.createElement("div");
    card.className = "lib-card";
    card.innerHTML = `
      <div class="lib-card-top">
        <span class="lib-card-emoji">${{p.emoji}}</span>
        <div>
          <div class="lib-card-name">${{p.name}}</div>
          <div class="lib-card-floor">${{floorTag}}</div>
        </div>
      </div>
      <div class="lib-card-chips">
        <span class="chip">☀️ Licht ${{p.licht}}/10</span>
        ${{stat ? `<span class="chip ${{stat==="ideal"?"accent-chip":""}}">
          ${{stat==="ideal"?"✅ Optimal":stat==="ok"?"⚠️ Ok":"❌ Zu dunkel"}}
        </span>` : ""}}
        <span class="chip">💧 ${{p.giessen||"—"}} Tage</span>
      </div>
      <div class="lib-card-divider"></div>
      <div class="lib-care-row">💧 Gießen <strong class="lib-care-val">&nbsp;${{p.giessen||"—"}}&nbsp;</strong>·
        🌿 Düngen <strong class="lib-care-val">&nbsp;${{p.dungen||"—"}}&nbsp;</strong>
        <span style="margin-left:2px;color:var(--muted);font-size:11px">(${{MONTHS_DE[NOW_MONTH]}})</span>
      </div>
      <button class="show-on-map-btn" data-pidx="${{i}}">🗺️ Auf Karte zeigen</button>
    `;

    card.querySelector(".show-on-map-btn").addEventListener("click",()=>{{
      const ppos = positions[i];
      if(ppos) setFloor(ppos.floor);
      switchTab("planer");
      setTimeout(()=>{{
        activePIdx=i;
        render();
        renderDetail(i);
        // highlight pulse
        const pin = $("map-canvas").querySelector(`[data-idx="${{i}}"]`);
        if(pin) {{pin.classList.add("highlight-pulse");setTimeout(()=>pin.classList.remove("highlight-pulse"),4500);}}
      }},120);
    }});

    grid.appendChild(card);
  }});
}}

function filterLibrary(val) {{
  libraryFilter = val;
  renderLibrary();
}}

// ============================================================
// CLICK OUTSIDE → DESELECT
// ============================================================
$("map-area").addEventListener("click",()=>{{activePIdx=null;render();showEmptyDetail();}});

// ============================================================
// BOOT
// ============================================================
loadPlants();
</script>
</body>
</html>"""

components.html(html_app, height=900, scrolling=False)
