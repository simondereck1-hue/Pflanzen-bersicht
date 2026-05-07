import streamlit as st
import streamlit.components.v1 as components
import json, math
import pandas as pd

# ============================================================
# KONFIGURATION
# ============================================================
st.set_page_config(layout="wide", page_title="Plant Management System", page_icon="🌿")

st.markdown("""
<style>
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  .stApp { background: #0D1117; }
</style>
""", unsafe_allow_html=True)

SHEET_ID  = "1cbOPNq-CrYrin-U0OkUJ5AE2AWF6Ba7RqIHlVOtUCK0"
CSV_URL   = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

GITHUB_BASE = "https://raw.githubusercontent.com/simondereck1-hue/Pflanzen-bersicht/main"

# ============================================================
# STANDORT: Rielingshausen (71672)
# ============================================================
LAT_DEG = 48.9
LON_DEG = 9.3

# ============================================================
# GEBÄUDEAUSRICHTUNG
# ============================================================
def building_north_azimuth(sx, sy, nx, ny):
    dx = nx - sx
    dy = ny - sy
    az = math.degrees(math.atan2(dx, -dy)) % 360
    return az

EG_BNA   = building_north_azimuth(1233, 775, 1267, 771)
OG1_BNA  = building_north_azimuth(1221, 768, 1255, 703)
OG2_BNA  = building_north_azimuth(1267, 744, 1293, 691)

FLOOR_DATA = {
    "EG": {
        "url": f"{GITHUB_BASE}/EG.png",
        "imgW": 1312, "imgH": 808,
        "floorX1": 170, "floorY1": 5, "floorX2": 1100, "floorY2": 570,
        "realW": 10, "realH": 6,
        "buildingNorthAzimuth": EG_BNA,
        "outerWalls": [
            {"x1":170,"y1":5,   "x2":170,"y2":95},
            {"x1":170,"y1":470, "x2":170,"y2":570},
            {"x1":170,"y1":570, "x2":900,"y2":570},
            {"x1":1000,"y1":570,"x2":1100,"y2":570},
            {"x1":1100,"y1":570,"x2":1100,"y2":530},
            {"x1":1100,"y1":340,"x2":1100,"y2":100},
            {"x1":1100,"y1":33, "x2":1100,"y2":5},
            {"x1":1100,"y1":5,  "x2":170,"y2":5},
        ],
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
        "buildingNorthAzimuth": OG1_BNA,
        "outerWalls": [
            {"x1":110,"y1":0,   "x2":110,"y2":110},
            {"x1":110,"y1":175, "x2":110,"y2":315},
            {"x1":110,"y1":515, "x2":110,"y2":620},
            {"x1":110,"y1":620, "x2":590,"y2":620},
            {"x1":740,"y1":620, "x2":1150,"y2":620},
            {"x1":1150,"y1":620,"x2":1150,"y2":580},
            {"x1":1150,"y1":405,"x2":1150,"y2":335},
            {"x1":1150,"y1":210,"x2":1150,"y2":0},
            {"x1":1150,"y1":0,  "x2":110,"y2":0},
        ],
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
        "buildingNorthAzimuth": OG2_BNA,
        "outerWalls": [
            {"x1":210,"y1":10,  "x2":210,"y2":210},
            {"x1":210,"y1":375, "x2":210,"y2":580},
            {"x1":210,"y1":580, "x2":630,"y2":580},
            {"x1":770,"y1":580, "x2":1100,"y2":580},
            {"x1":1100,"y1":580,"x2":1100,"y2":10},
            {"x1":1100,"y1":10, "x2":210,"y2":10},
        ],
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
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ── DATABASE DARK THEME TOKENS ── */
:root {{
  --bg: #0D1117;
  --surface: #161B22;
  --surface-2: #21262D;
  --surface-3: #30363D;
  --border: rgba(48, 54, 61, 0.8);
  --border-2: rgba(48, 54, 61, 1);
  --accent: #3FB950;
  --accent-dim: rgba(63, 185, 80, 0.12);
  --accent-glow: rgba(63, 185, 80, 0.3);
  --accent-dark: #2EA043;
  --warn: #D29922;
  --warn-dim: rgba(210, 153, 34, 0.12);
  --warn-bright: #E3B341;
  --danger: #F85149;
  --danger-dim: rgba(248, 81, 73, 0.12);
  --danger-bright: #FF6B6B;
  --blue: #58A6FF;
  --blue-dim: rgba(88, 166, 255, 0.12);
  --purple: #BC8CFF;
  --text: #E6EDF3;
  --text-2: #8B949E;
  --text-3: #6E7681;
  --r: 8px; --rs: 6px; --rx: 12px;
  --transition: 0.2s ease;
  --sidebar-w: 320px;
  --header-h: 56px; --tab-h: 48px;
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Inter', sans-serif;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;overflow:hidden}}
body{{
  font-family: var(--font-sans);
  background: var(--bg);
  color: var(--text);
  display:flex;flex-direction:column;
  font-size: 13px;
}}
button{{font-family:inherit;cursor:pointer;border:none;background:none;color:inherit}}
input,select{{font-family:inherit}}
::-webkit-scrollbar{{width:6px;height:6px}}
::-webkit-scrollbar-track{{background:var(--surface)}}
::-webkit-scrollbar-thumb{{background:var(--surface-3);border-radius:3px}}
::-webkit-scrollbar-thumb:hover{{background:#484F58}}

/* ── HEADER ── */
#header{{
  height:var(--header-h);background:var(--surface);
  border-bottom:1px solid var(--border-2);
  display:flex;align-items:center;padding:0 20px;gap:12px;flex-shrink:0;z-index:200;
}}
.logo{{font-family:var(--font-mono);font-weight:700;font-size:15px;color:var(--accent);letter-spacing:-.3px;display:flex;align-items:center;gap:8px;}}
.logo-tag{{font-size:11px;padding:2px 8px;border-radius:4px;background:var(--accent-dim);border:1px solid var(--accent-glow);color:var(--accent);font-weight:600;letter-spacing:.05em;}}
.header-sep{{width:1px;height:24px;background:var(--border-2);margin:0 4px;}}
.header-meta{{display:flex;align-items:center;gap:12px;margin-left:auto}}
.sun-info{{
  display:flex;align-items:center;gap:8px;font-size:12px;font-weight:500;color:var(--text-2);
  background:var(--surface-2);border:1px solid var(--border);border-radius:6px;
  padding:5px 12px;font-family:var(--font-mono);
}}
.sun-dot{{width:7px;height:7px;border-radius:50%;background:var(--warn-bright);box-shadow:0 0 8px var(--warn);flex-shrink:0}}
.status-wrap{{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--text-2);font-weight:500;font-family:var(--font-mono);}}
.sdot{{width:7px;height:7px;border-radius:50%;background:var(--text-3);transition:background .3s}}
.sdot.ok{{background:var(--accent);box-shadow:0 0 8px var(--accent-dark)}}
.sdot.syncing{{background:var(--blue);animation:sdot-blink 1s infinite;}}
@keyframes sdot-blink{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}

/* ── TABS ── */
#tabs{{
  height:var(--tab-h);background:var(--surface);
  border-bottom:1px solid var(--border-2);
  display:flex;align-items:center;padding:0 20px;gap:2px;flex-shrink:0;z-index:150;
}}
.tab{{
  padding:8px 18px;font-size:13px;font-weight:500;color:var(--text-2);
  border-radius:6px;cursor:pointer;
  transition:all var(--transition);display:flex;align-items:center;gap:7px;
  position:relative;
}}
.tab:hover{{color:var(--text);background:var(--surface-2);}}
.tab.active{{color:var(--text);background:var(--surface-2);}}
.tab.active::after{{content:'';position:absolute;bottom:-9px;left:0;right:0;height:2px;background:var(--accent);border-radius:1px 1px 0 0;}}
.tab-badge{{
  font-size:10px;font-weight:700;padding:1px 6px;border-radius:99px;
  background:var(--danger-dim);color:var(--danger-bright);border:1px solid rgba(248,81,73,0.25);
  font-family:var(--font-mono);
}}
.tab-badge.warn{{background:var(--warn-dim);color:var(--warn-bright);border-color:rgba(210,153,34,0.25);}}
.tab-badge.ok{{background:var(--accent-dim);color:var(--accent);border-color:var(--accent-glow);display:none;}}

/* ── MAIN ── */
#main{{display:flex;flex:1;overflow:hidden;position:relative;background:var(--bg);}}

/* ── SIDEBARS ── */
#left-sidebar, #right-sidebar{{
  width:var(--sidebar-w);background:var(--surface);
  border-right:1px solid var(--border-2);
  display:flex;flex-direction:column;overflow:hidden;flex-shrink:0;
}}
#right-sidebar{{border-right:none;border-left:1px solid var(--border-2);}}
#left-sidebar.hidden, #right-sidebar.hidden{{display:none}}

.sidebar-header{{
  padding:14px 16px 12px;font-weight:600;font-size:12px;
  color:var(--text-2);letter-spacing:.06em;text-transform:uppercase;
  border-bottom:1px solid var(--border);flex-shrink:0;display:flex;align-items:center;gap:8px;
}}
.sidebar-header span{{flex:1;color:var(--text)}}
.sb-count{{
  font-size:11px;padding:2px 8px;border-radius:99px;
  background:var(--surface-2);border:1px solid var(--border);
  color:var(--text-2);font-family:var(--font-mono);
}}
.inv-search{{
  margin:12px;padding:8px 12px;background:var(--surface-2);border:1px solid var(--border-2);
  border-radius:var(--r);color:var(--text);font-size:13px;width:calc(100% - 24px);
  transition: border-color .2s, box-shadow .2s;
}}
.inv-search::placeholder{{color:var(--text-3)}}
.inv-search:focus{{outline:none;border-color:var(--accent);box-shadow: 0 0 0 3px var(--accent-dim);}}

.inv-group{{padding:4px 0}}
.inv-group-label{{
  padding:8px 16px 6px;font-size:11px;font-weight:600;color:var(--text-3);
  text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;
}}
.inv-group-label::after{{content:'';flex:1;height:1px;background:var(--border);margin-left:4px;}}
.inv-item{{
  display:flex;align-items:center;gap:10px;padding:8px 16px;cursor:pointer;
  transition:all var(--transition);user-select:none;
}}
.inv-item:hover{{background:var(--surface-2);}}
.inv-item.dragging-source{{opacity:.3; transform: scale(0.98);}}
.inv-item.selected{{background:var(--accent-dim);}}
.inv-item.placed-elsewhere{{opacity:.55}}
.inv-emoji{{font-size:18px;width:26px;text-align:center}}
.inv-name{{font-size:13px;font-weight:500;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--text)}}
.inv-badge{{
  font-size:10px;padding:2px 8px;border-radius:99px;font-weight:600;
  background:var(--surface-2);color:var(--text-3);border:1px solid var(--border);
  font-family:var(--font-mono);white-space:nowrap
}}
.inv-badge.placed-badge{{background:var(--accent-dim);border-color:var(--accent-glow);color:var(--accent)}}
.inv-floor-switcher{{
  margin:auto 12px 12px;padding:4px;
  background:var(--surface-2);border:1px solid var(--border-2);border-radius:var(--rx);
  display:flex;gap:3px;flex-shrink:0;
}}
.floor-btn{{
  flex:1;padding:8px 6px;font-size:12px;font-weight:600;
  border-radius:8px;transition:all var(--transition);color:var(--text-2);font-family:var(--font-mono);
}}
.floor-btn:hover{{background:var(--surface-3);color:var(--text)}}
.floor-btn.active{{background:var(--accent);color:#0D1117;box-shadow:0 2px 8px var(--accent-dim);}}

/* ── MAP AREA ── */
#map-area{{
  flex:1;position:relative;overflow:hidden;background:var(--bg);
}}
#map-canvas{{
  position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%);
  border-radius: 8px;
}}
#floor-img{{
  position:absolute;inset:0;width:100%;height:100%;
  object-fit:contain;pointer-events:none;user-select:none;opacity:0.95;
}}
#light-canvas{{
  position:absolute;inset:0;width:100%;height:100%;
  pointer-events:none;opacity:.65; mix-blend-mode: screen;
}}
#map-canvas.drag-over{{
  outline:2px dashed var(--accent);outline-offset:4px; border-radius: 10px;
}}

/* DLI Toggle */
.dli-toggle-wrap{{
  position:absolute;top:14px;right:14px;z-index:100;
  display:flex;gap:8px;align-items:center;
  background:var(--surface);border:1px solid var(--border-2);border-radius:8px;padding:6px 12px;
}}
.dli-toggle-label{{font-size:11px;font-weight:600;color:var(--text-2);font-family:var(--font-mono);}}
.dli-toggle{{
  width:34px;height:18px;border-radius:9px;background:var(--surface-3);
  position:relative;cursor:pointer;transition:background .3s;border:none;
}}
.dli-toggle.on{{background:var(--blue);}}
.dli-toggle::after{{
  content:'';position:absolute;top:2px;left:2px;width:14px;height:14px;
  border-radius:50%;background:#fff;transition:transform .3s;
}}
.dli-toggle.on::after{{transform:translateX(16px);}}

/* ── PLANT PINS ── */
.plant-pin{{
  position:absolute;display:flex;flex-direction:column;align-items:center;
  cursor:grab;user-select:none;touch-action:none;z-index:10;
  transition:transform 0.1s;
}}
.plant-pin:hover{{z-index:50;}}
.plant-pin.dragging{{cursor:grabbing;z-index:100;}}
.plant-pin.active .pin-bubble{{background:var(--surface-2);border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim), 0 6px 20px rgba(0,0,0,0.5);transform:scale(1.12);}}
.plant-pin.highlight-pulse .pin-bubble{{animation:highlightPulse 1.5s ease-in-out 3}}
@keyframes highlightPulse{{0%,100%{{box-shadow:0 0 0 0 var(--accent-glow)}}50%{{box-shadow:0 0 0 14px rgba(63,185,80,0)}}}}
.pin-bubble{{
  width:42px;height:42px;border-radius:50%;background:var(--surface);
  border:2px solid var(--border-2);display:flex;align-items:center;justify-content:center;
  font-size:20px;transition:transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow:0 4px 12px rgba(0,0,0,0.4);
}}
.plant-pin:hover .pin-bubble{{transform:scale(1.15);box-shadow:0 6px 20px rgba(63,185,80,0.2);border-color:var(--accent);}}
.plant-pin.dragging .pin-bubble{{transform:scale(1.08) translateY(-4px);}}
.pin-indicator{{width:8px;height:8px;border-radius:50%;margin-top:4px;background:var(--text-3);transition:background .3s;border:1px solid var(--bg);}}
.pin-indicator.ideal{{background:var(--accent);}}
.pin-indicator.ok{{background:var(--warn-bright);}}
.pin-indicator.bad{{background:var(--danger-bright);}}
.pin-label{{
  font-size:10px;font-weight:600;color:var(--text);margin-top:3px;white-space:nowrap;
  max-width:80px;overflow:hidden;text-overflow:ellipsis;text-align:center;
  background:rgba(22,27,34,0.9);padding:2px 7px;border-radius:4px;
  border:1px solid var(--border);
}}
.pin-light-badge{{
  font-size:9px;font-weight:700;padding:1px 6px;border-radius:4px;margin-top:2px;
  background:var(--surface-2);color:var(--text-2);border:1px solid var(--border);
  font-family:var(--font-mono);
}}

/* ── FULL-SCREEN VIEWS ── */
#library-view, #care-view{{
  position:absolute;inset:0;background:var(--bg);
  display:none;flex-direction:column;overflow:hidden;z-index:90;
}}
#library-view.active, #care-view.active{{display:flex;}}

/* ── LIBRARY VIEW ── */
.lib-toolbar{{
  padding:16px 20px 12px;background:var(--surface);border-bottom:1px solid var(--border-2);
  display:flex;align-items:center;gap:12px;flex-shrink:0;flex-wrap:wrap;
}}
.lib-toolbar-title{{
  font-weight:700;font-size:15px;color:var(--text);margin-right:4px;
}}
.lib-toolbar-sub{{font-size:12px;color:var(--text-3);font-family:var(--font-mono);}}
.lib-filters{{display:flex;align-items:center;gap:8px;flex:1;flex-wrap:wrap;}}
.lib-search{{
  padding:7px 12px;background:var(--surface-2);border:1px solid var(--border-2);
  border-radius:var(--r);color:var(--text);font-size:13px;min-width:180px;
  transition:border-color .2s;
}}
.lib-search::placeholder{{color:var(--text-3)}}
.lib-search:focus{{outline:none;border-color:var(--accent);}}
.lib-select{{
  padding:7px 10px;background:var(--surface-2);border:1px solid var(--border-2);
  border-radius:var(--r);color:var(--text);font-size:12px;cursor:pointer;
  transition:border-color .2s;appearance:none;padding-right:24px;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%238B949E'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 8px center;
}}
.lib-select:focus{{outline:none;border-color:var(--accent);}}
.lib-sort-btn{{
  padding:7px 12px;background:var(--surface-2);border:1px solid var(--border-2);
  border-radius:var(--r);color:var(--text-2);font-size:12px;cursor:pointer;
  transition:all var(--transition);font-weight:500;white-space:nowrap;
}}
.lib-sort-btn.active{{border-color:var(--accent);color:var(--accent);background:var(--accent-dim);}}
.lib-sort-btn:hover{{border-color:var(--text-3);color:var(--text);}}
.lib-results-bar{{
  padding:8px 20px;background:var(--surface);border-bottom:1px solid var(--border);
  font-size:11px;color:var(--text-3);font-family:var(--font-mono);display:flex;align-items:center;gap:12px;flex-shrink:0;
}}
.lib-filter-tag{{
  display:inline-flex;align-items:center;gap:5px;padding:2px 8px;border-radius:4px;
  background:var(--accent-dim);border:1px solid var(--accent-glow);color:var(--accent);
  font-size:10px;font-weight:600;cursor:pointer;transition:all var(--transition);
}}
.lib-filter-tag:hover{{background:rgba(248,81,73,0.1);border-color:rgba(248,81,73,0.3);color:var(--danger-bright);}}
.lib-grid{{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:1px;background:var(--border-2);
  overflow-y:auto;flex:1;
}}
.lib-card{{
  background:var(--surface);display:flex;flex-direction:column;
  transition:background var(--transition);cursor:pointer;
}}
.lib-card:hover{{background:var(--surface-2);}}
.lib-card-img{{
  position:relative;height:160px;overflow:hidden;background:var(--surface-2);flex-shrink:0;
}}
.lib-card-img img{{width:100%;height:100%;object-fit:cover;opacity:.8;transition:opacity var(--transition);}}
.lib-card:hover .lib-card-img img{{opacity:.95;}}
.lib-card-img-fallback{{display:flex;align-items:center;justify-content:center;width:100%;height:100%;font-size:52px;opacity:.3;}}
.lib-card-img-overlay{{
  position:absolute;bottom:0;left:0;right:0;
  background:linear-gradient(transparent,rgba(13,17,23,0.95));padding:16px 14px 12px;
}}
.lib-card-name{{font-weight:700;font-size:14px;color:var(--text)}}
.lib-card-botanical{{font-size:11px;color:var(--text-2);font-style:italic;margin-top:2px}}
.lib-card-body{{padding:14px;flex:1;display:flex;flex-direction:column;gap:10px;}}
.lib-card-top-row{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}}
.lib-status-chip{{
  font-size:11px;font-weight:600;padding:2px 8px;border-radius:4px;
  background:var(--surface-2);color:var(--text-3);border:1px solid var(--border);
}}
.lib-status-chip.ideal{{background:var(--accent-dim);color:var(--accent);border-color:var(--accent-glow);}}
.lib-status-chip.ok{{background:var(--warn-dim);color:var(--warn-bright);border-color:rgba(210,153,34,0.3);}}
.lib-status-chip.bad{{background:var(--danger-dim);color:var(--danger-bright);border-color:rgba(248,81,73,0.3);}}
.lib-card-loc{{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--text-2);font-family:var(--font-mono);}}
.lib-card-loc-dot{{width:6px;height:6px;border-radius:50%;background:var(--text-3);}}
.lib-card-loc-dot.placed{{background:var(--accent);}}

/* Metrics row in library card */
.lib-metrics-row{{
  display:grid;grid-template-columns:repeat(3,1fr);gap:8px;
}}
.lib-metric{{
  background:var(--surface-2);border:1px solid var(--border);border-radius:6px;
  padding:8px 10px;
}}
.lib-metric-lbl{{font-size:10px;color:var(--text-3);font-weight:500;margin-bottom:3px;}}
.lib-metric-val{{font-size:15px;font-weight:700;color:var(--text);font-family:var(--font-mono);display:flex;align-items:baseline;gap:3px;}}
.lib-metric-unit{{font-size:10px;color:var(--text-3);font-weight:500;}}

/* Light bar in library */
.lib-light-row{{display:flex;align-items:center;gap:8px;}}
.lib-light-bar-wrap{{flex:1}}
.lib-light-bar-track{{height:4px;background:var(--surface-3);border-radius:2px;overflow:hidden;}}
.lib-light-bar-fill{{height:100%;border-radius:2px;transition:width 1s ease;}}
.lib-light-labels{{display:flex;justify-content:space-between;font-size:10px;color:var(--text-3);margin-top:3px;font-family:var(--font-mono);}}
.lib-light-score{{font-size:13px;font-weight:700;font-family:var(--font-mono);min-width:36px;text-align:right;}}
.lib-divider{{height:1px;background:var(--border);margin:2px 0;}}
.lib-besonderheit{{
  background:var(--surface-2);border:1px solid var(--border);border-left:2px solid var(--purple);
  border-radius:6px;padding:10px 12px;font-size:12px;color:var(--text-2);line-height:1.5;
}}
.lib-besonderheit-lbl{{font-size:10px;font-weight:700;color:var(--purple);margin-bottom:4px;text-transform:uppercase;letter-spacing:.05em;}}
.lib-humidity-row{{display:flex;align-items:center;gap:5px;font-size:12px;color:var(--text-2);}}
.lib-humidity-badge{{background:var(--blue-dim);border:1px solid rgba(88,166,255,0.25);color:var(--blue);padding:1px 7px;border-radius:4px;font-size:11px;font-family:var(--font-mono);font-weight:600;}}
.lib-card-footer{{
  padding:10px 14px;border-top:1px solid var(--border);flex-shrink:0;
  display:flex;gap:8px;
}}
.show-on-map-btn{{
  flex:1;padding:7px 12px;font-size:12px;font-weight:600;
  border:1px solid var(--border-2);border-radius:6px;
  background:var(--surface-2);color:var(--text-2);
  transition:all var(--transition);
}}
.show-on-map-btn:hover{{border-color:var(--accent);color:var(--accent);background:var(--accent-dim);}}
.show-on-map-btn.care-btn-lib{{border-color:var(--blue-dim);color:var(--blue);}}
.show-on-map-btn.care-btn-lib:hover{{border-color:var(--blue);background:var(--blue-dim);}}
.lib-no-results{{
  grid-column:1/-1;text-align:center;padding:60px;color:var(--text-3);
}}
.lib-no-results-icon{{font-size:40px;margin-bottom:12px;opacity:.4;}}

/* ── RIGHT SIDEBAR (Detail) ── */
#rsb-empty{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;color:var(--text-3);padding:24px;text-align:center}}
#rsb-empty .empty-icon{{font-size:44px;opacity:.3;}}
#rsb-detail{{flex:1;display:none;flex-direction:column;overflow-y:auto;}}
#rsb-detail.visible{{display:flex}}

.detail-img-wrap{{
  position:relative;height:160px;overflow:hidden;background:var(--surface-2);flex-shrink:0;
}}
.detail-img-wrap img{{width:100%;height:100%;object-fit:cover;opacity:.85;}}
.detail-img-overlay{{
  position:absolute;inset:0;background:linear-gradient(transparent 40%,var(--surface) 100%);
}}
.plant-hdr{{padding:14px 16px 10px;display:flex;gap:12px;align-items:flex-start;}}
.big-emoji{{font-size:28px;}}
.plant-hdr-text h2{{font-size:15px;font-weight:700;color:var(--text);line-height:1.3;}}
.botanical{{font-size:11px;color:var(--text-3);font-style:italic;margin-top:2px;}}
.plant-hdr-text .coords{{font-size:10px;color:var(--text-3);margin-top:4px;font-family:var(--font-mono);}}

.score-badge{{
  margin:0 16px 12px;padding:10px 14px;border-radius:8px;border:1px solid var(--border);
  background:var(--surface-2);display:flex;align-items:center;gap:10px;
}}
.score-badge.ideal{{border-color:rgba(63,185,80,.3);background:rgba(63,185,80,.06);}}
.score-badge.ok{{border-color:rgba(210,153,34,.3);background:rgba(210,153,34,.06);}}
.score-badge.bad{{border-color:rgba(248,81,73,.3);background:rgba(248,81,73,.06);}}
.sc-icon{{font-size:20px;}}
.sc-text h3{{font-size:13px;font-weight:600;color:var(--text);}}
.sc-text p{{font-size:11px;color:var(--text-2);margin-top:2px;}}

.light-bar-wrap{{margin:0 16px 12px;}}
.lbw-label{{display:flex;justify-content:space-between;font-size:11px;color:var(--text-3);margin-bottom:5px;font-family:var(--font-mono);}}
.lbw-track{{height:6px;background:var(--surface-3);border-radius:3px;overflow:hidden;position:relative;}}
.lbw-fill{{height:100%;border-radius:3px;transition:width 1s ease;}}
.lbw-needle{{position:absolute;top:-2px;bottom:-2px;width:2px;background:var(--text-3);border-radius:1px;}}

.data-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 16px 12px;}}
.dc{{background:var(--surface-2);border:1px solid var(--border);border-radius:8px;padding:10px 12px;}}
.dc-lbl{{font-size:10px;color:var(--text-3);font-weight:500;margin-bottom:4px;}}
.dc-val{{font-size:18px;font-weight:700;font-family:var(--font-mono);color:var(--text);display:flex;align-items:baseline;gap:3px;}}
.dc-unit{{font-size:10px;color:var(--text-3);font-weight:500;}}

.detail-extra-row{{display:flex;gap:8px;padding:0 16px 8px;align-items:flex-start;}}
.detail-extra-lbl{{font-size:11px;font-weight:600;color:var(--text-3);min-width:140px;}}
.detail-extra-val{{font-size:12px;color:var(--text-2);}}

.astro-panel{{
  margin:0 16px 12px;background:var(--surface-2);border:1px solid var(--border);
  border-radius:8px;padding:12px;
}}
.astro-title{{font-size:11px;font-weight:700;color:var(--text-2);margin-bottom:10px;text-transform:uppercase;letter-spacing:.05em;}}
.astro-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:10px;}}
.astro-cell{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:8px 10px;}}
.astro-cell-lbl{{font-size:10px;color:var(--text-3);margin-bottom:3px;}}
.astro-cell-val{{font-size:16px;font-weight:700;color:var(--text);font-family:var(--font-mono);}}
.astro-cell-unit{{font-size:11px;color:var(--text-3);}}
.window-chips{{display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;}}
.win-chip{{font-size:10px;padding:2px 8px;border-radius:4px;background:var(--surface);border:1px solid var(--border);color:var(--text-3);font-family:var(--font-mono);}}
.win-chip.hit{{background:rgba(210,153,34,.1);border-color:rgba(210,153,34,.3);color:var(--warn-bright);}}

.action-row{{display:flex;gap:8px;padding:12px 16px 16px;}}
.act-btn{{
  flex:1;padding:9px 14px;font-size:13px;font-weight:600;border-radius:var(--r);
  border:1px solid var(--border-2);background:var(--surface-2);color:var(--text-2);
  transition:all var(--transition);
}}
.act-btn:hover{{background:var(--surface-3);color:var(--text);border-color:var(--text-3);}}
.act-btn.primary{{border-color:var(--accent-glow);color:var(--accent);background:var(--accent-dim);}}
.act-btn.primary:hover{{background:rgba(63,185,80,.2);}}
.act-btn.danger-btn{{border-color:rgba(248,81,73,.3);color:var(--danger);background:var(--danger-dim);}}
.act-btn.danger-btn:hover{{background:rgba(248,81,73,.2);}}

/* DLI detail */
.dli-detail{{
  margin:0 16px 12px;background:var(--blue-dim);border:1px solid rgba(88,166,255,0.25);
  border-radius:8px;padding:12px;
}}
.dli-detail-lbl{{font-size:10px;font-weight:700;color:var(--blue);margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em;}}
.dli-bar-wrap{{display:flex;align-items:center;gap:8px;}}
.dli-bar-track{{flex:1;height:6px;background:var(--surface-3);border-radius:3px;overflow:hidden;}}
.dli-bar-fill{{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--blue-dim),var(--blue));transition:width 1s ease;}}
.dli-score-val{{font-size:16px;font-weight:700;font-family:var(--font-mono);color:var(--blue);}}

/* ── CARE VIEW ── */
.care-header{{
  padding:14px 20px 12px;background:var(--surface);border-bottom:1px solid var(--border-2);
  display:flex;align-items:center;gap:14px;flex-shrink:0;flex-wrap:wrap;
}}
.care-header-title{{font-weight:700;font-size:15px;color:var(--text);}}
.care-header-sub{{font-size:12px;color:var(--text-3);font-family:var(--font-mono);}}
.care-header-actions{{display:flex;gap:8px;margin-left:auto;flex-wrap:wrap;}}
.care-mass-btn{{
  padding:7px 14px;font-size:12px;font-weight:600;border-radius:6px;
  border:1px solid var(--border-2);background:var(--surface-2);color:var(--text-2);
  transition:all var(--transition);
}}
.care-mass-btn:hover{{border-color:var(--text-3);color:var(--text);background:var(--surface-3);}}
.care-mass-btn.primary{{border-color:var(--accent-glow);color:var(--accent);background:var(--accent-dim);}}
.care-mass-btn.primary:hover{{background:rgba(63,185,80,.2);}}
.care-mass-btn.danger{{border-color:rgba(88,166,255,0.3);color:var(--blue);background:var(--blue-dim);}}

.care-subtabs{{
  display:flex;background:var(--surface);border-bottom:1px solid var(--border-2);
  padding:0 20px;gap:2px;flex-shrink:0;
}}
.care-subtab{{
  padding:8px 16px;font-size:12px;font-weight:500;color:var(--text-2);
  border-radius:6px;cursor:pointer;transition:all var(--transition);position:relative;
  display:flex;align-items:center;gap:6px;
}}
.care-subtab:hover{{color:var(--text);background:var(--surface-2);}}
.care-subtab.active{{color:var(--text);}}
.care-subtab.active::after{{content:'';position:absolute;bottom:-1px;left:0;right:0;height:2px;background:var(--accent);border-radius:1px;}}

/* Sync indicator */
.sync-badge{{
  font-size:10px;padding:2px 8px;border-radius:4px;font-family:var(--font-mono);font-weight:600;
  background:var(--accent-dim);border:1px solid var(--accent-glow);color:var(--accent);
  display:flex;align-items:center;gap:5px;
}}
.sync-badge.syncing{{background:var(--blue-dim);border-color:rgba(88,166,255,0.3);color:var(--blue);animation:sdot-blink 1s infinite;}}
.sync-badge.error{{background:var(--danger-dim);border-color:rgba(248,81,73,0.25);color:var(--danger-bright);}}

/* Care panes */
#care-calendar-pane, #care-status-pane, #care-history-pane{{
  flex:1;overflow-y:auto;padding:16px 20px;display:none;flex-direction:column;gap:16px;
}}
#care-calendar-pane.active, #care-status-pane.active, #care-history-pane.active{{display:flex;}}

/* Calendar */
.calendar-wrap{{
  background:var(--surface);border:1px solid var(--border-2);border-radius:var(--rx);overflow:hidden;
  max-width:900px;
}}
.calendar-nav{{
  display:flex;align-items:center;padding:14px 16px;border-bottom:1px solid var(--border);
}}
.calendar-nav-btn{{
  padding:6px 12px;border-radius:6px;border:1px solid var(--border-2);background:var(--surface-2);
  color:var(--text-2);font-size:16px;cursor:pointer;transition:all var(--transition);
}}
.calendar-nav-btn:hover{{background:var(--surface-3);color:var(--text);}}
.calendar-nav-title{{flex:1;text-align:center;font-weight:700;font-size:14px;color:var(--text);font-family:var(--font-mono);}}
.cal-grid{{display:grid;grid-template-columns:repeat(7,1fr);border-top:1px solid var(--border);}}
.cal-header-row{{
  display:grid;grid-template-columns:repeat(7,1fr);
  border-bottom:1px solid var(--border);
}}
.cal-header-cell{{
  padding:8px 10px;text-align:center;font-size:11px;font-weight:600;
  color:var(--text-3);text-transform:uppercase;letter-spacing:.06em;background:var(--surface-2);
}}
.cal-cell{{
  padding:8px 10px;min-height:80px;border-right:1px solid var(--border);
  border-bottom:1px solid var(--border);background:var(--bg);transition:background var(--transition);
}}
.cal-cell:nth-child(7n){{border-right:none;}}
.cal-cell.other-month{{opacity:.35;background:var(--surface);}}
.cal-cell.today{{background:rgba(63,185,80,0.04);}}
.cal-cell.today .cal-day-num{{
  background:var(--accent);color:#0D1117;width:24px;height:24px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-weight:700;font-family:var(--font-mono);
}}
.cal-day-num{{font-size:12px;font-weight:600;color:var(--text-2);margin-bottom:4px;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-family:var(--font-mono);}}
.cal-events{{display:flex;flex-direction:column;gap:2px;}}
.cal-event{{
  font-size:10px;font-weight:600;padding:2px 5px;border-radius:3px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}}
.cal-event.water{{background:var(--blue-dim);color:var(--blue);}}
.cal-event.fertilize{{background:var(--accent-dim);color:var(--accent);}}
.cal-event.due-water{{background:rgba(88,166,255,0.2);color:var(--blue);border:1px solid rgba(88,166,255,0.25);}}
.cal-event.due-fertilize{{background:rgba(63,185,80,0.18);color:var(--accent);border:1px solid var(--accent-glow);}}

/* Care Dashboard — Section Titles */
.care-section-title{{
  font-size:12px;font-weight:700;color:var(--text-2);text-transform:uppercase;
  letter-spacing:.06em;display:flex;align-items:center;gap:10px;margin-bottom:2px;
}}
.care-section-title .care-badge{{
  font-family:var(--font-mono);font-size:10px;font-weight:700;padding:2px 8px;
  border-radius:4px;background:var(--danger-dim);color:var(--danger-bright);border:1px solid rgba(248,81,73,0.25);
  text-transform:none;letter-spacing:0;
}}
.care-section-title .care-badge.warn{{background:var(--warn-dim);color:var(--warn-bright);border-color:rgba(210,153,34,0.25);}}
.care-section-title .care-badge.ok{{background:var(--accent-dim);color:var(--accent);border-color:var(--accent-glow);}}

/* Pflege-Karten */
.care-card{{
  background:var(--surface);border:1px solid var(--border-2);border-radius:var(--rx);
  display:flex;align-items:center;gap:14px;
  transition:all var(--transition);position:relative;overflow:hidden;
}}
.care-card-stripe{{
  width:3px;height:100%;background:var(--accent);flex-shrink:0;align-self:stretch;min-height:80px;
  border-radius:0;
}}
.care-card.overdue .care-card-stripe{{background:var(--danger-bright);}}
.care-card.soon .care-card-stripe{{background:var(--warn-bright);}}
.care-card.done .care-card-stripe{{background:var(--surface-3);}}
.care-card:hover{{background:var(--surface-2);}}
.care-card-inner{{display:flex;align-items:center;gap:14px;flex:1;padding:14px 16px 14px 0;}}

/* Care card plant thumbnail */
.care-card-thumb{{
  width:46px;height:46px;border-radius:8px;overflow:hidden;flex-shrink:0;
  background:var(--surface-2);border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;
}}
.care-card-thumb img{{width:100%;height:100%;object-fit:cover;}}
.care-card-thumb-emoji{{font-size:24px;}}
.care-card-info{{flex:1;min-width:0}}
.care-card-name{{font-weight:700;font-size:14px;color:var(--text);margin-bottom:4px;}}
.care-card-meta{{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-bottom:8px;}}
.care-chip{{
  font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;
  background:var(--surface-2);color:var(--text-2);border:1px solid var(--border);font-family:var(--font-mono);
}}
.care-chip.overdue{{background:var(--danger-dim);color:var(--danger-bright);border-color:rgba(248,81,73,0.3);}}
.care-chip.soon{{background:var(--warn-dim);color:var(--warn-bright);border-color:rgba(210,153,34,0.25);}}
.care-chip.ok{{background:var(--accent-dim);color:var(--accent);border-color:var(--accent-glow);}}

/* Progress bars — rings style */
.care-progress-wrap{{display:flex;flex-direction:column;gap:5px;margin-bottom:6px;}}
.care-progress-row{{display:flex;align-items:center;gap:7px;}}
.care-progress-icon{{font-size:11px;flex-shrink:0;width:14px;}}
.care-progress-track{{flex:1;height:4px;border-radius:2px;background:var(--surface-3);overflow:hidden;}}
.care-progress-fill{{height:100%;border-radius:2px;transition:width 1s ease;}}
.care-progress-fill.water{{background:linear-gradient(90deg,rgba(88,166,255,.4),var(--blue));}}
.care-progress-fill.fertilize{{background:linear-gradient(90deg,var(--accent-dim),var(--accent));}}
.care-progress-pct{{font-size:10px;font-weight:700;color:var(--text-3);min-width:28px;text-align:right;font-family:var(--font-mono);}}

/* Circle progress for overdue section */
.care-circles{{display:flex;gap:12px;margin-bottom:8px;}}
.care-circle-wrap{{display:flex;flex-direction:column;align-items:center;gap:4px;}}
.care-circle{{position:relative;width:44px;height:44px;}}
.care-circle svg{{transform:rotate(-90deg);}}
.care-circle-bg{{fill:none;stroke:var(--surface-3);stroke-width:4;}}
.care-circle-fill{{fill:none;stroke-width:4;stroke-linecap:round;transition:stroke-dashoffset 1s ease;}}
.care-circle-fill.water{{stroke:var(--blue);}}
.care-circle-fill.water.urgent{{stroke:var(--danger-bright);}}
.care-circle-fill.fertilize{{stroke:var(--accent);}}
.care-circle-fill.fertilize.urgent{{stroke:var(--warn-bright);}}
.care-circle-label{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;font-family:var(--font-mono);color:var(--text-2);}}
.care-circle-sub{{font-size:9px;color:var(--text-3);font-weight:500;text-align:center;max-width:52px;}}

.care-card-actions{{display:flex;flex-direction:column;gap:6px;flex-shrink:0;padding-right:14px;}}
.care-btn{{
  padding:7px 12px;font-size:11px;font-weight:700;border-radius:6px;
  border:1px solid var(--border-2);background:var(--surface-2);color:var(--text-2);
  transition:all var(--transition);cursor:pointer;white-space:nowrap;
  font-family:var(--font-mono);
}}
.care-btn:hover{{background:var(--surface-3);}}
.care-btn:active{{transform:scale(0.97);}}
.care-btn.water{{border-color:rgba(88,166,255,0.35);color:var(--blue);background:var(--blue-dim);}}
.care-btn.water:hover{{background:rgba(88,166,255,0.2);box-shadow:0 2px 8px rgba(88,166,255,0.15);}}
.care-btn.fertilize{{border-color:var(--accent-glow);color:var(--accent);background:var(--accent-dim);}}
.care-btn.fertilize:hover{{background:rgba(63,185,80,.2);}}
.care-btn.syncing{{opacity:.7;pointer-events:none;}}

/* Historie */
.care-history{{
  background:var(--surface);border:1px solid var(--border-2);border-radius:var(--rx);
  overflow:hidden;
}}
.care-history-header{{
  padding:12px 16px;border-bottom:1px solid var(--border);
  font-size:12px;font-weight:700;color:var(--text-2);text-transform:uppercase;letter-spacing:.06em;
  display:flex;align-items:center;gap:10px;background:var(--surface-2);
}}
.history-entry{{
  display:flex;align-items:center;gap:12px;padding:10px 16px;
  border-bottom:1px solid var(--border);font-size:12px;
  transition:background .2s;
}}
.history-entry:last-child{{border-bottom:none}}
.history-entry:hover{{background:var(--surface-2);}}
.history-icon{{font-size:14px;flex-shrink:0;}}
.history-text{{flex:1;color:var(--text);font-weight:500;}}
.history-sub{{font-size:11px;color:var(--text-3);margin-top:2px;font-family:var(--font-mono);}}
.history-badge{{
  font-size:10px;padding:2px 7px;border-radius:4px;font-family:var(--font-mono);font-weight:600;
  flex-shrink:0;
}}
.history-badge.synced{{background:var(--accent-dim);color:var(--accent);border:1px solid var(--accent-glow);}}
.history-badge.local{{background:var(--surface-2);color:var(--text-3);border:1px solid var(--border);}}
.history-time{{font-size:11px;color:var(--text-3);font-family:var(--font-mono);white-space:nowrap;}}

.care-empty{{
  text-align:center;padding:40px;color:var(--text-3);
  background:var(--surface);border:1px dashed var(--border-2);border-radius:var(--rx);
}}
.care-empty .ce-icon{{font-size:40px;margin-bottom:10px;opacity:.3;display:block}}
.care-empty p{{font-size:13px;font-weight:500;line-height:1.6;}}

/* ── TOAST & TOOLTIP ── */
#tooltip{{
  position:fixed;z-index:500;pointer-events:none;
  background:var(--surface-2);border:1px solid var(--border-2);
  border-radius:6px;padding:8px 12px;font-size:12px;font-weight:500;color:var(--text);
  box-shadow:0 8px 20px rgba(0,0,0,0.5);opacity:0;transition:opacity .15s;
  max-width:220px;font-family:var(--font-mono);
}}
#tooltip.visible{{opacity:1}}

#save-toast{{
  position:fixed;bottom:20px;right:20px;z-index:999;
  background:var(--surface-2);border:1px solid var(--border-2);
  border-radius:8px;padding:12px 18px;font-size:13px;font-weight:600;color:var(--text);
  box-shadow:0 8px 24px rgba(0,0,0,0.5);
  transform:translateY(20px);opacity:0;
  transition:all .3s ease;
  display:flex;align-items:center;gap:10px;font-family:var(--font-mono);
}}
#save-toast.show{{transform:translateY(0);opacity:1}}
#save-toast.success{{border-color:var(--accent-glow);}}
#save-toast.error{{border-color:rgba(248,81,73,.3);}}
#save-toast.info{{border-color:rgba(88,166,255,.3);}}

/* ── LOADING ── */
#loading{{
  position:fixed;inset:0;z-index:9999;background:var(--bg);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;
  transition:opacity .5s,visibility .5s;
}}
#loading.hidden{{opacity:0;visibility:hidden}}
#loading .ld-icon{{font-size:44px;animation:pulse 2s ease-in-out infinite}}
#loading p{{font-size:14px;font-weight:500;color:var(--text-2);font-family:var(--font-mono);}}
.ld-bar{{width:200px;height:2px;background:var(--surface-3);border-radius:1px;overflow:hidden;}}
.ld-bar-fill{{height:100%;background:var(--accent);border-radius:1px;animation:ldFill 2s ease infinite;}}
@keyframes ldFill{{0%{{width:0%}}100%{{width:100%}}}}
@keyframes pulse{{0%,100%{{transform:scale(1);opacity:.5}}50%{{transform:scale(1.08);opacity:1}}}}
</style>
</head>
<body>

<div id="loading">
  <div class="ld-icon">🌿</div>
  <p>Plant Management System wird geladen…</p>
  <div class="ld-bar"><div class="ld-bar-fill"></div></div>
</div>
<div id="tooltip"></div>
<div id="save-toast">💾 <span id="toast-msg">Gespeichert</span></div>

<!-- HEADER -->
<div id="header">
  <span class="logo">🌿 PlantOS <span class="logo-tag">v7</span></span>
  <div class="header-sep"></div>
  <span style="font-size:12px;font-weight:500;color:var(--text-2);font-family:var(--font-mono)" id="month-label"></span>
  <div class="header-meta">
    <div class="sun-info">
      <div class="sun-dot"></div>
      <span id="sun-label">☀ Berechne…</span>
    </div>
    <div id="sync-badge" class="sync-badge" style="display:none">⟳ Sync</div>
    <div class="status-wrap">
      <div class="sdot" id="sdot"></div>
      <span id="stext">Verbinden…</span>
    </div>
  </div>
</div>

<!-- TABS -->
<div id="tabs">
  <button class="tab active" data-tab="planer" onclick="switchTab('planer')">
    🗺 Grundriss-Planer
  </button>
  <button class="tab" data-tab="library" onclick="switchTab('library')">
    📚 Pflanzen-Bibliothek
  </button>
  <button class="tab" data-tab="care" onclick="switchTab('care')">
    🌱 Care Dashboard
    <span class="tab-badge" id="care-tab-badge" style="display:none">0</span>
  </button>
</div>

<!-- MAIN -->
<div id="main">

  <!-- LEFT SIDEBAR -->
  <div id="left-sidebar">
    <div class="sidebar-header">
      <span>Inventar</span>
      <span class="sb-count" id="inv-count">0</span>
    </div>
    <input class="inv-search" id="inv-search" type="text" placeholder="Pflanze suchen…" oninput="filterInventory(this.value)">
    <div id="inv-list" style="flex:1;overflow-y:auto"></div>
    <div class="inv-floor-switcher">
      <button class="floor-btn active" onclick="setFloor('EG')" id="fbtn-EG">EG</button>
      <button class="floor-btn" onclick="setFloor('1. OG')" id="fbtn-1. OG">1.OG</button>
      <button class="floor-btn" onclick="setFloor('2. OG')" id="fbtn-2. OG">2.OG</button>
    </div>
  </div>

  <!-- MAP AREA -->
  <div id="map-area">
    <div class="dli-toggle-wrap">
      <span class="dli-toggle-label">DLI-Modus</span>
      <button class="dli-toggle" id="dli-toggle-btn" onclick="toggleDLIMode()"></button>
    </div>
    <div id="map-canvas">
      <img id="floor-img" src="" alt="Grundriss" draggable="false"
           onerror="this.src='https://placehold.co/1100x600/161B22/3FB950?text=Grundriss+nicht+gefunden'">
      <canvas id="light-canvas"></canvas>
    </div>
  </div>

  <!-- LIBRARY VIEW -->
  <div id="library-view">
    <div class="lib-toolbar">
      <div>
        <div class="lib-toolbar-title">📚 Pflanzen-Bibliothek</div>
        <div class="lib-toolbar-sub" id="lib-sub-label">–</div>
      </div>
      <div class="lib-filters">
        <input class="lib-search" id="lib-search" type="text" placeholder="🔍 Name suchen…" oninput="onLibraryFilterChange()">
        <select class="lib-select" id="lib-filter-light" onchange="onLibraryFilterChange()">
          <option value="">☀ Lichtbedarf</option>
          <option value="low">Schattig (1–4)</option>
          <option value="mid">Halbschattig (5–7)</option>
          <option value="high">Sonnig (8–10)</option>
        </select>
        <select class="lib-select" id="lib-filter-water" onchange="onLibraryFilterChange()">
          <option value="">💧 Gießhäufigkeit</option>
          <option value="rare">Selten (14+ Tage)</option>
          <option value="mid">Mittel (7–13 Tage)</option>
          <option value="frequent">Häufig (1–6 Tage)</option>
        </select>
        <select class="lib-select" id="lib-sort" onchange="onLibraryFilterChange()">
          <option value="name">Sortieren: Name A→Z</option>
          <option value="name-desc">Sortieren: Name Z→A</option>
          <option value="licht">Sortieren: Lichtbedarf ↑</option>
          <option value="licht-desc">Sortieren: Lichtbedarf ↓</option>
          <option value="giessen">Sortieren: Gießintervall ↑</option>
          <option value="giessen-desc">Sortieren: Gießintervall ↓</option>
        </select>
        <button class="lib-sort-btn" id="lib-reset-btn" onclick="resetLibraryFilters()" style="display:none">✕ Filter zurücksetzen</button>
      </div>
    </div>
    <div class="lib-results-bar" id="lib-results-bar">
      <span id="lib-results-count">–</span>
      <span id="lib-active-filters"></span>
    </div>
    <div class="lib-grid" id="lib-grid"></div>
  </div>

  <!-- CARE VIEW -->
  <div id="care-view">
    <div class="care-header">
      <div>
        <div class="care-header-title">🌱 Care Dashboard</div>
        <div class="care-header-sub" id="care-sub-label">Lade Pflegedaten…</div>
      </div>
      <div class="care-header-actions">
        <button class="care-mass-btn" onclick="waterAllDue()">💧 Alle fälligen gießen</button>
        <button class="care-mass-btn danger" onclick="syncAllFromSheets()">⟳ Sheets laden</button>
        <button class="care-mass-btn primary" onclick="refreshCare()">↻ Aktualisieren</button>
      </div>
    </div>

    <!-- Sub-tabs -->
    <div class="care-subtabs">
      <button class="care-subtab active" id="subtab-due" onclick="switchCareSubtab('due')">🔴 Fällige Aufgaben</button>
      <button class="care-subtab" id="subtab-all" onclick="switchCareSubtab('all')">📋 Alle Pflanzen</button>
      <button class="care-subtab" id="subtab-calendar" onclick="switchCareSubtab('calendar')">📅 Kalender</button>
      <button class="care-subtab" id="subtab-history" onclick="switchCareSubtab('history')">🕐 Pflege-Historie</button>
    </div>

    <!-- Due pane -->
    <div id="care-due-pane" class="active">
      <div id="care-overdue-section"></div>
      <div id="care-soon-section"></div>
    </div>

    <!-- All pane -->
    <div id="care-all-pane">
      <div id="care-all-section"></div>
    </div>

    <!-- Calendar pane -->
    <div id="care-calendar-pane">
      <div class="calendar-wrap">
        <div class="cal-header-row" id="cal-header-row"></div>
        <div class="calendar-nav">
          <button class="calendar-nav-btn" onclick="changeCalMonth(-1)">‹</button>
          <span class="calendar-nav-title" id="cal-month-title"></span>
          <button class="calendar-nav-btn" onclick="changeCalMonth(1)">›</button>
        </div>
        <div class="cal-grid" id="cal-grid"></div>
      </div>
    </div>

    <!-- History pane -->
    <div id="care-history-pane">
      <div id="care-history-section"></div>
    </div>
  </div>

  <!-- RIGHT SIDEBAR -->
  <div id="right-sidebar">
    <div id="rsb-empty">
      <div class="empty-icon">🪴</div>
      <p style="font-size:13px;line-height:1.6;color:var(--text-3);font-weight:500;">Pflanze auswählen<br>für Details &amp; Analyse</p>
    </div>
    <div id="rsb-detail"></div>
  </div>

</div><!-- /main -->

<script>
// ============================================================
// KONSTANTEN & FLOOR DATA
// ============================================================
const CSV_URL     = "{CSV_URL}";
const SHEET_ID    = "{SHEET_ID}";
const GITHUB_BASE = "{GITHUB_BASE}";
const FLOOR_DATA  = {FLOOR_DATA_JSON};
const LAT_RAD     = {LAT_DEG} * Math.PI / 180;
const LON_DEG_VAL = {LON_DEG};

const PLANT_EMOJIS = ["🌿","🌱","🪴","🌺","🌸","🌻","🌵","🎋","🌴","🌳","🍀","☘️","🌾","🌼","💐","🫧","🌏","🌙","✨","🪷"];
const MONTHS_DE    = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];
const DAYS_DE      = ["So","Mo","Di","Mi","Do","Fr","Sa"];
const NOW          = new Date();
const NOW_MONTH    = NOW.getMonth();

// ============================================================
// STATE
// ============================================================
let plants          = [];
let positions       = {{}};
let careData        = {{}};    // keyed by plant idx: {{lastWatered, lastFertilized, syncedAt}}
let careHistory     = [];
let activePIdx      = null;
let currentFloor    = "EG";
let currentTab      = "planer";
let currentCareSubtab = "due";
let dragSrcIdx      = null;
let inventoryFilter = "";
let libraryFilter   = "";
let libFilterLight  = "";
let libFilterWater  = "";
let libSort         = "name";
let saveTimeout     = null;
let sunState        = {{ azimuth:180, elevation:0, factor:0 }};
let dliMode         = false;
let dliCache        = {{}};
let calMonth        = NOW_MONTH;
let calYear         = NOW.getFullYear();
let syncInProgress  = false;

// ============================================================
// UTILITY
// ============================================================
const $ = id => document.getElementById(id);

function setStatus(ok, msg) {{
  $("sdot").className = "sdot"+(ok?" ok":"");
  $("stext").textContent = msg;
}}

function showSyncBadge(state) {{
  const badge = $("sync-badge");
  badge.style.display = "flex";
  badge.className = "sync-badge" + (state==="syncing" ? " syncing" : state==="error" ? " error" : "");
  badge.textContent = state==="syncing" ? "⟳ Syncing…" : state==="error" ? "✕ Sync-Fehler" : "✓ Synced";
  if(state !== "syncing") setTimeout(()=>{{ badge.style.display="none"; }}, 3000);
}}

function showTooltip(msg, x, y) {{
  const t = $("tooltip");
  t.textContent = msg;
  t.style.left = (x+16)+"px";
  t.style.top  = (y+16)+"px";
  t.classList.add("visible");
}}
function hideTooltip() {{ $("tooltip").classList.remove("visible"); }}

function showToast(msg, type='success', dur=2500) {{
  $("toast-msg").textContent = msg;
  const el = $("save-toast");
  el.className = "show " + type;
  clearTimeout(el._t);
  el._t = setTimeout(()=>el.classList.remove("show"), dur);
}}

$("month-label").textContent = MONTHS_DE[NOW_MONTH]+" "+NOW.getFullYear();

// ============================================================
// ASTRONOMISCHE LICHTSIMULATION
// ============================================================
function calcSunPosition(date) {{
  const JD = date / 86400000 + 2440587.5;
  const n  = JD - 2451545.0;
  const L  = (280.460 + 0.9856474*n) % 360;
  const g  = ((357.528 + 0.9856003*n) % 360) * Math.PI/180;
  const lam= (L + 1.915*Math.sin(g) + 0.020*Math.sin(2*g)) * Math.PI/180;
  const eps = (23.439 - 0.0000004*n) * Math.PI/180;
  const sinDec = Math.sin(eps)*Math.sin(lam);
  const dec    = Math.asin(sinDec);
  const RA     = Math.atan2(Math.cos(eps)*Math.sin(lam), Math.cos(lam));
  const ut = (date % 86400000) / 3600000;
  const GMST = (6.697375 + 0.0657098242*n + ut) % 24;
  const LST  = (GMST + LON_DEG_VAL/15) % 24;
  const HA   = (LST*15 - RA*180/Math.PI) * Math.PI/180;
  const sinAlt= Math.sin(LAT_RAD)*sinDec + Math.cos(LAT_RAD)*Math.cos(dec)*Math.cos(HA);
  const alt  = Math.asin(Math.max(-1,Math.min(1,sinAlt)));
  const cosAz= (sinDec - Math.sin(LAT_RAD)*sinAlt)/(Math.cos(LAT_RAD)*Math.cos(alt));
  let az     = Math.acos(Math.max(-1,Math.min(1,cosAz))) * 180/Math.PI;
  if(Math.sin(HA)>0) az = 360-az;
  return {{ elevation: alt*180/Math.PI, azimuth: az }};
}}

function skyDiffuse(elevDeg) {{
  const e = Math.max(0, elevDeg);
  return 0.05 + 0.10 * Math.min(e/90, 1);
}}

function updateSunInfo() {{
  const s = calcSunPosition(Date.now());
  const factor = Math.max(0, Math.sin(s.elevation*Math.PI/180));
  sunState = {{ azimuth: s.azimuth, elevation: s.elevation, factor }};
  const risen = s.elevation > 0;
  $("sun-label").textContent = risen
    ? `☀ Az:${{s.azimuth.toFixed(0)}}° El:${{s.elevation.toFixed(1)}}°`
    : `🌙 El:${{s.elevation.toFixed(1)}}°`;
}}

const WIN_SAMPLES = 5;

function windowAzimuth(side, buildingNorthAzimuth) {{
  const map = {{ N:0, NE:45, E:90, SE:135, S:180, SW:225, W:270, NW:315 }};
  const base = map[side] ?? 0;
  return (buildingNorthAzimuth + base) % 360;
}}

function directSunFactor(winAzDeg, sunAzDeg, sunElevDeg) {{
  if(sunElevDeg<=0) return 0;
  let diff = Math.abs(winAzDeg - sunAzDeg) % 360;
  if(diff>180) diff = 360-diff;
  if(diff>90)  return 0;
  return Math.cos(diff*Math.PI/180) * Math.sin(sunElevDeg*Math.PI/180);
}}

function roomPenetrationFactor(sunElevDeg, side, buildingNorthAzimuth) {{
  const winAz = windowAzimuth(side, buildingNorthAzimuth);
  let solarAngle = (buildingNorthAzimuth - winAz + 180) % 360;
  if(solarAngle>180) solarAngle=360-solarAngle;
  if(sunElevDeg<=0) return 0;
  return Math.max(0, Math.cos(solarAngle*Math.PI/180)) * Math.cos(sunElevDeg*Math.PI/180);
}}

function isBlockedByInnerWall(px,py,wx,wy,fd) {{
  for(const wall of fd.walls) {{
    if(segmentsIntersect(px,py,wx,wy,wall.x1,wall.y1,wall.x2,wall.y2)) return true;
  }}
  return false;
}}

function isBlockedByOuterWall(px,py,wx,wy,fd) {{
  for(const wall of fd.outerWalls) {{
    if(segmentsIntersect(px,py,wx,wy,wall.x1,wall.y1,wall.x2,wall.y2)) return true;
  }}
  return false;
}}

function cross2D(ax,ay,bx,by) {{ return ax*by-ay*bx; }}

function segmentsIntersect(ax,ay,bx,by,cx,cy,dx,dy) {{
  const d1x=bx-ax, d1y=by-ay, d2x=dx-cx, d2y=dy-cy;
  const denom=cross2D(d1x,d1y,d2x,d2y);
  if(Math.abs(denom)<1e-9) return false;
  const t=cross2D(cx-ax,cy-ay,d2x,d2y)/denom;
  const u=cross2D(cx-ax,cy-ay,d1x,d1y)/denom;
  return t>1e-6&&t<1-1e-6&&u>1e-6&&u<1-1e-6;
}}

// DLI Cache
function getDLIScore(rx,ry,floor) {{
  if(!dliCache[floor]) return null;
  const key=`${{Math.round(rx*20)}},${{Math.round(ry*20)}}`;
  return dliCache[floor].get(key) ?? null;
}}

let dliComputeTimer=null;
function scheduleDLICompute(floor) {{
  if(dliComputeTimer) clearTimeout(dliComputeTimer);
  dliComputeTimer=setTimeout(()=>computeDLIForFloor(floor),100);
}}

function computeDLIForFloor(floor) {{
  const fd=FLOOR_DATA[floor];
  const fw=fd.floorX2-fd.floorX1, fh=fd.floorY2-fd.floorY1;
  if(!dliCache[floor]) dliCache[floor]=new Map();
  const cache=dliCache[floor];
  const totalDLI=12*3600;
  const steps=12;
  const now=Date.now();
  const startOfDay=now - (now%(86400000)) - 4*3600000;
  for(let iy=0;iy<=20;iy++) {{
    for(let ix=0;ix<=20;ix++) {{
      const rx=ix/20, ry=iy/20;
      const pAX=fd.floorX1+rx*fw, pAY=fd.floorY1+ry*fh;
      if(pAX<fd.floorX1||pAX>fd.floorX2||pAY<fd.floorY1||pAY>fd.floorY2) continue;
      let sum=0;
      for(let s=0;s<steps;s++) {{
        const t=(s+0.5)/steps;
        const ts=startOfDay+t*86400000;
        const sp=calcSunPosition(ts);
        const fac=Math.max(0,Math.sin(sp.elevation*Math.PI/180));
        const tmpState={{azimuth:sp.azimuth,elevation:sp.elevation,factor:fac}};
        const origState=sunState;
        sunState=tmpState;
        const score=computeLicht(rx,ry,floor);
        sunState=origState;
        sum+=score*(1/steps);
      }}
      const dliScore=Math.min(10,Math.max(1,Math.round(sum*10)/10));
      cache.set(`${{ix}},${{iy}}`,dliScore);
    }}
  }}
  drawLightMap();
}}

function toggleDLIMode() {{
  dliMode=!dliMode;
  $("dli-toggle-btn").classList.toggle("on",dliMode);
  if(dliMode) scheduleDLICompute(currentFloor);
  drawLightMap(); render();
}}

function px2rel(px,p1,p2) {{ return (px-p1)/(p2-p1); }}

function computeLichtFull(px,py,floor) {{
  const fd=FLOOR_DATA[floor];
  const fw=fd.floorX2-fd.floorX1, fh=fd.floorY2-fd.floorY1;
  const realW=fd.realW, realH=fd.realH;
  const bldAz=fd.buildingNorthAzimuth||0;
  const pAX=fd.floorX1+px*fw, pAY=fd.floorY1+py*fh;
  const margin=4;
  if(pAX<fd.floorX1-margin||pAX>fd.floorX2+margin||pAY<fd.floorY1-margin||pAY>fd.floorY2+margin) {{
    return {{score:1,components:{{}},windowHits:[]}};
  }}
  const sunElevDeg=sunState.elevation, sunAzDeg=sunState.azimuth, sunDirect=sunState.factor;
  const skyDiff=skyDiffuse(sunElevDeg);
  const wallReflectance=0.15;
  let totalIlluminance=0;
  const windowHits=[];
  for(const w of fd.windows) {{
    const winAz=windowAzimuth(w.side,bldAz);
    let winContrib=0,samplesVisible=0,totalSamples=0,bestIncFactor=0;
    for(let s=0;s<WIN_SAMPLES;s++) {{
      const t=WIN_SAMPLES===1?0.5:s/(WIN_SAMPLES-1);
      const sAX=w.x1+t*(w.x2-w.x1), sAY=w.y1+t*(w.y2-w.y1);
      totalSamples++;
      if(isBlockedByInnerWall(pAX,pAY,sAX,sAY,fd)) continue;
      if(isBlockedByOuterWall(pAX,pAY,sAX,sAY,fd)) continue;
      samplesVisible++;
      const dxM=(px-px2rel(sAX,fd.floorX1,fd.floorX2))*realW;
      const dyM=(py-px2rel(sAY,fd.floorY1,fd.floorY2))*realH;
      const distM=Math.sqrt(dxM*dxM+dyM*dyM);
      const incFactor=directSunFactor(winAz,sunAzDeg,sunElevDeg);
      bestIncFactor=Math.max(bestIncFactor,incFactor);
      const penetration=roomPenetrationFactor(sunElevDeg,w.side,bldAz);
      const kDirect=0.2+0.6*(1-penetration);
      const directContrib=incFactor*sunDirect/(1+kDirect*distM*distM);
      const kDiffuse=0.3;
      const diffuseContrib=skyDiff/(1+kDiffuse*distM);
      winContrib+=directContrib+diffuseContrib;
    }}
    if(totalSamples>0) {{
      const avgContrib=winContrib/totalSamples;
      const winPxLen=Math.sqrt((w.x2-w.x1)**2+(w.y2-w.y1)**2);
      const isVertical=Math.abs(w.x2-w.x1)<Math.abs(w.y2-w.y1);
      const winMeter=isVertical?(winPxLen/fh)*realH:(winPxLen/fw)*realW;
      const winSizeFactor=Math.min(3,winMeter)/1.0;
      totalIlluminance+=avgContrib*winSizeFactor;
    }}
    windowHits.push({{side:w.side,winAz:winAz.toFixed(0),incFactor:bestIncFactor.toFixed(2),visRatio:(samplesVisible/totalSamples).toFixed(2),occluded:samplesVisible===0}});
  }}
  totalIlluminance*=(1+wallReflectance);
  const scaleFactor=22;
  const score=Math.min(10,Math.max(1,Math.round(totalIlluminance*scaleFactor*10)/10));
  return {{score,components:{{totalIlluminance,skyDiff,sunDirect}},windowHits}};
}}

function computeLicht(px,py,floor) {{ return computeLichtFull(px,py,floor).score; }}

function getLichtStatus(ist,soll) {{
  if(ist>=soll) return "ideal";
  if(ist>=soll-2) return "ok";
  return "bad";
}}

const STATUS_CFG = {{
  ideal:{{icon:"🟢",label:"Idealer Standort",desc:"Ausreichend Licht für diese Pflanze.",cls:"ideal"}},
  ok:   {{icon:"🟡",label:"Akzeptabler Standort",desc:"Etwas weniger als optimal.",cls:"ok"}},
  bad:  {{icon:"🔴",label:"Zu dunkel",desc:"Bitte näher ans Fenster stellen.",cls:"bad"}},
}};

// ============================================================
// LIGHT MAP
// ============================================================
function drawLightMap() {{
  const img=document.getElementById("floor-img");
  const canvas=$("light-canvas");
  if(!img.naturalWidth) return;
  canvas.width=img.naturalWidth; canvas.height=img.naturalHeight;
  canvas.style.width=img.naturalWidth+"px"; canvas.style.height=img.naturalHeight+"px";
  const ctx=canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const fd=FLOOR_DATA[currentFloor];
  const fw=fd.floorX2-fd.floorX1, fh=fd.floorY2-fd.floorY1;
  const step=20;
  for(let iy=fd.floorY1;iy<=fd.floorY2;iy+=step) {{
    for(let ix=fd.floorX1;ix<=fd.floorX2;ix+=step) {{
      const rx=(ix-fd.floorX1)/fw, ry=(iy-fd.floorY1)/fh;
      let lv;
      if(dliMode) {{
        const cached=getDLIScore(rx,ry,currentFloor);
        lv=cached!==null?cached:computeLicht(rx,ry,currentFloor);
        const alpha=(lv/10)*0.22;
        const r=Math.round(50+(lv/10)*40);
        const g=Math.round(120+(lv/10)*46);
        const b=Math.round(220-(lv/10)*40);
        ctx.fillStyle=`rgba(${{r}},${{g}},${{b}},${{alpha.toFixed(3)}})`;
      }} else {{
        lv=computeLicht(rx,ry,currentFloor);
        const alpha=(lv/10)*0.2;
        const g=Math.round(140+(lv/10)*75);
        ctx.fillStyle=`rgba(63,${{g}},80,${{alpha.toFixed(3)}})`;
      }}
      ctx.fillRect(ix,iy,step,step);
    }}
  }}
}}

// ============================================================
// IMAGE READY
// ============================================================
function onImageReady() {{
  const img=$("floor-img");
  const cvs=$("map-canvas");
  const W=img.naturalWidth||1100, H=img.naturalHeight||600;
  cvs.style.width=W+"px"; cvs.style.height=H+"px";
  const area=$("map-area");
  const scale=Math.min(1,(area.clientWidth-40)/W,(area.clientHeight-40)/H);
  cvs.style.transform=`translate(-50%,-50%) scale(${{scale}})`;
}}
$("floor-img").addEventListener("load",()=>{{onImageReady();drawLightMap();render();}});
window.addEventListener("resize",onImageReady);

// ============================================================
// PLANT IMAGE URL
// ============================================================
function getPlantImageUrl(plantName) {{
  const safeName=plantName.replace(/\s+/g,'%20');
  return `${{GITHUB_BASE}}/${{safeName}}.png`;
}}

// ============================================================
// CSV LOAD
// ============================================================
async function loadPlants() {{
  setStatus(false,"Lade Daten…");
  try {{
    const res=await fetch(CSV_URL);
    if(!res.ok) throw new Error("HTTP "+res.status);
    const text=await res.text();
    plants=parseCSV(text);
    setStatus(true,plants.length+" Pflanzen geladen");
  }} catch(e) {{
    console.warn("CSV-Fehler:",e);
    plants=[
      {{name:"Monstera Deliciosa",botanisch:"Monstera deliciosa",licht:7,giessen:3,dungen:4,umtopfen:"Alle 2 Jahre",info:"Robuste Zimmerpflanze",emoji:"🌿",luftfeuchtigkeit:"60-80%",besprühen:"Ja",besonderheit:"Bekannt für spektakuläre Blattlöcher.",giessAll:{{}},duengAll:{{}}}},
      {{name:"Sukkulente",botanisch:"Echeveria spp.",licht:9,giessen:14,dungen:8,umtopfen:"Alle 3 Jahre",info:"Viel Sonne",emoji:"🌵",luftfeuchtigkeit:"30-50%",besprühen:"Nein",besonderheit:"Speichert Wasser in Blättern.",giessAll:{{}},duengAll:{{}}}},
    ];
    setStatus(false,"Offline-Modus");
  }}
  plants.forEach((p,i)=>{{ if(!p.emoji) p.emoji=PLANT_EMOJIS[i%PLANT_EMOJIS.length]; }});
  $("inv-count").textContent=plants.length;
  loadPositionsLocal();
  loadCareData();
  // Try to load care data from sheets
  await syncCareFromSheets();
  renderInventory();
  renderLibrary();
  setFloor(currentFloor);
  $("loading").classList.add("hidden");
  updateSunInfo();
  renderCare();
  setInterval(()=>{{updateSunInfo();drawLightMap();render();}},60000);
  updateCareBadge();
}}

// ============================================================
// CSV PARSE
// ============================================================
function parseCSV(text) {{
  const lines=text.trim().split("\\n");
  const headers=lines[0].split(",").map(h=>h.trim().replace(/"/g,""));
  const col=(cands)=>{{
    for(const c of cands) {{
      const idx=headers.findIndex(h=>h.toLowerCase().includes(c.toLowerCase()));
      if(idx>=0) return idx;
    }}
    return -1;
  }};
  const colName=col(["Pflanze","Name","name"]);
  const colBotanisch=col(["Botanischer","botanisch","Botanisch"]);
  const colLicht=col(["Lichtbedarf"]);
  const colUmtopf=col(["Umtopfen"]);
  const colLuft=col(["Luftfeuchtigkeit","Optimale Luftfeu","luftfeucht"]);
  const colBespr=col(["Besprühen","Bespruhen","besprühen"]);
  const colBesond=col(["Besonderheit","besonderheit"]);
  const monthName=MONTHS_DE[NOW_MONTH];
  const colGiess=col(["Gießen_"+monthName,"Giessen_"+monthName]);
  const colDueng=col(["Düngen_"+monthName,"Dunegen_"+monthName,"Düngen_"+monthName]);
  const giessAll={{}}, duengAll={{}};
  MONTHS_DE.forEach(m=>{{
    giessAll[m]=col(["Gießen_"+m,"Giessen_"+m]);
    duengAll[m]=col(["Düngen_"+m,"Dunegen_"+m,"Düngen_"+m]);
  }});
  // Care timestamp columns
  const colLastWatered=col(["lastWatered","last_watered","LastWatered"]);
  const colLastFertilized=col(["lastFertilized","last_fertilized","LastFertilized"]);

  return lines.slice(1).filter(l=>l.trim()).map((line,i)=>{{
    const cols=splitCSVLine(line);
    const safeCol=(idx)=>idx>=0?(cols[idx]||"").trim().replace(/"/g,""):"";
    const obj={{
      id:i,
      name:safeCol(colName)||"Pflanze "+(i+1),
      botanisch:safeCol(colBotanisch),
      licht:parseFloat(safeCol(colLicht))||5,
      giessen:colGiess>=0?(safeCol(colGiess)||"—"):"—",
      dungen:colDueng>=0?(safeCol(colDueng)||"—"):"—",
      umtopfen:safeCol(colUmtopf)||"—",
      luftfeuchtigkeit:safeCol(colLuft)||"",
      besprühen:safeCol(colBespr)||"",
      besonderheit:safeCol(colBesond)||"",
      emoji:PLANT_EMOJIS[i%PLANT_EMOJIS.length],
      giessAll:{{}},duengAll:{{}},
      // Care timestamps from CSV (may be overridden by local/sheets)
      csvLastWatered:colLastWatered>=0?safeCol(colLastWatered):"",
      csvLastFertilized:colLastFertilized>=0?safeCol(colLastFertilized):"",
    }};
    MONTHS_DE.forEach(m=>{{
      obj.giessAll[m]=giessAll[m]>=0?(safeCol(giessAll[m])||"—"):"—";
      obj.duengAll[m]=duengAll[m]>=0?(safeCol(duengAll[m])||"—"):"—";
    }});
    return obj;
  }});
}}

function splitCSVLine(line) {{
  const res=[]; let cur="",inQ=false;
  for(const ch of line) {{
    if(ch==='"'){{inQ=!inQ;continue}}
    if(ch===','&&!inQ){{res.push(cur.trim());cur="";continue}}
    cur+=ch;
  }}
  res.push(cur.trim()); return res;
}}

// ============================================================
// PERSISTENZ — LOCAL STORAGE
// ============================================================
function savePositionsLocal() {{
  try {{ localStorage.setItem("pflanzen_positions_v2",JSON.stringify(positions)); }} catch(e) {{}}
}}
function loadPositionsLocal() {{
  try {{
    const raw=localStorage.getItem("pflanzen_positions_v2");
    if(raw) positions=JSON.parse(raw);
  }} catch(e) {{ positions={{}}; }}
}}
function saveCareData() {{
  try {{
    localStorage.setItem("pflanzen_care_v2",JSON.stringify(careData));
    localStorage.setItem("pflanzen_history_v2",JSON.stringify(careHistory.slice(0,200)));
  }} catch(e) {{}}
}}
function loadCareData() {{
  try {{
    const rc=localStorage.getItem("pflanzen_care_v2");
    if(rc) careData=JSON.parse(rc);
    const rh=localStorage.getItem("pflanzen_history_v2");
    if(rh) careHistory=JSON.parse(rh);
    // Merge CSV timestamps if no local data exists
    plants.forEach((p,i)=>{{
      if(!careData[i]) careData[i]={{}};
      const cd=careData[i];
      if(!cd.lastWatered && p.csvLastWatered) {{
        const d=new Date(p.csvLastWatered);
        if(!isNaN(d.getTime())) cd.lastWatered=d.toISOString();
      }}
      if(!cd.lastFertilized && p.csvLastFertilized) {{
        const d=new Date(p.csvLastFertilized);
        if(!isNaN(d.getTime())) cd.lastFertilized=d.toISOString();
      }}
    }});
  }} catch(e) {{ careData={{}}; careHistory=[]; }}
}}

// ============================================================
// GOOGLE APPS SCRIPT URL
// ============================================================
const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx9Vf0xJ4gJPFt6j3SaQQjW2PKT29upU-UxmyoioOEs_upOXVA0MgKGmu17yZQm0uuM/exec";

// ============================================================
// SHEETS SYNC — Positionen speichern
// ============================================================
async function savePositionsToSheets() {{
  savePositionsLocal();
  if(!APPS_SCRIPT_URL) return;
  const payload=Object.entries(positions).map(([idx,pos])=>{{
    return {{action:"savePosition",idx:parseInt(idx),floor:pos.floor,x:pos.x,y:pos.y}};
  }});
  try {{
    await fetch(APPS_SCRIPT_URL,{{method:"POST",mode:"no-cors",headers:{{"Content-Type":"application/json"}},body:JSON.stringify(payload)}});
    showToast("☁ Standorte synchronisiert","success");
  }} catch(e) {{
    showToast("💾 Lokal gespeichert","info");
  }}
}}

function debouncedSave() {{
  if(saveTimeout) clearTimeout(saveTimeout);
  saveTimeout=setTimeout(savePositionsToSheets,800);
}}

// ============================================================
// SHEETS SYNC — Care-Daten schreiben
// ============================================================
async function saveCareToSheets(plantIdx, type, timestamp) {{
  saveCareData();
  if(!APPS_SCRIPT_URL) return false;
  const p=plants[plantIdx];
  if(!p) return false;
  const payload={{
    action:"saveCare",
    idx:plantIdx,
    plantName:p.name,
    type:type,           // "water" | "fertilize"
    timestamp:timestamp,
    lastWatered:careData[plantIdx]?.lastWatered || "",
    lastFertilized:careData[plantIdx]?.lastFertilized || "",
  }};
  try {{
    showSyncBadge("syncing");
    $("sdot").className="sdot syncing";
    await fetch(APPS_SCRIPT_URL,{{method:"POST",mode:"no-cors",headers:{{"Content-Type":"application/json"}},body:JSON.stringify([payload])}});
    careData[plantIdx].syncedAt=new Date().toISOString();
    saveCareData();
    showSyncBadge("ok");
    $("sdot").className="sdot ok";
    return true;
  }} catch(e) {{
    console.warn("Sheets-Sync fehlgeschlagen:",e);
    showSyncBadge("error");
    $("sdot").className="sdot ok";
    return false;
  }}
}}

// ============================================================
// SHEETS SYNC — Care-Daten lesen
// ============================================================
async function syncCareFromSheets() {{
  if(!APPS_SCRIPT_URL || syncInProgress) return;
  syncInProgress=true;
  try {{
    showSyncBadge("syncing");
    const url=APPS_SCRIPT_URL+"?action=getCare&t="+Date.now();
    const res=await fetch(url,{{method:"GET",mode:"cors"}});
    if(!res.ok) throw new Error("HTTP "+res.status);
    const data=await res.json();
    // data expected: array of {{idx, lastWatered, lastFertilized}}
    if(Array.isArray(data)) {{
      data.forEach(entry=>{{
        const i=entry.idx;
        if(i===undefined||i===null) return;
        if(!careData[i]) careData[i]={{}};
        // Only update if sheets data is newer
        const sheetW=entry.lastWatered?new Date(entry.lastWatered):null;
        const sheetF=entry.lastFertilized?new Date(entry.lastFertilized):null;
        const localW=careData[i].lastWatered?new Date(careData[i].lastWatered):null;
        const localF=careData[i].lastFertilized?new Date(careData[i].lastFertilized):null;
        if(sheetW && (!localW || sheetW>localW)) {{
          careData[i].lastWatered=entry.lastWatered;
        }}
        if(sheetF && (!localF || sheetF>localF)) {{
          careData[i].lastFertilized=entry.lastFertilized;
        }}
      }});
      saveCareData();
      showSyncBadge("ok");
    }}
  }} catch(e) {{
    // Silently fail — sheets might not support GET yet
    showSyncBadge("ok");
  }} finally {{
    syncInProgress=false;
  }}
}}

async function syncAllFromSheets() {{
  showToast("⟳ Lade von Google Sheets…","info",4000);
  await syncCareFromSheets();
  renderCare();
  showToast("✓ Daten aktualisiert","success");
}}

// ============================================================
// TAB SWITCHING
// ============================================================
function switchTab(tab) {{
  currentTab=tab;
  document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("active",t.dataset.tab===tab));
  const isPlaner=tab==="planer";
  const isLibrary=tab==="library";
  const isCare=tab==="care";
  $("left-sidebar").classList.toggle("hidden",!isPlaner);
  $("right-sidebar").classList.toggle("hidden",!isPlaner);
  $("map-area").style.display=isPlaner?"block":"none";
  $("library-view").classList.toggle("active",isLibrary);
  $("care-view").classList.toggle("active",isCare);
  if(isLibrary) renderLibrary();
  if(isCare) renderCare();
}}

// ============================================================
// CARE SUB-TABS
// ============================================================
function switchCareSubtab(tab) {{
  currentCareSubtab=tab;
  ["due","all","calendar","history"].forEach(t=>{{
    const btn=$("subtab-"+t);
    if(btn) btn.classList.toggle("active",t===tab);
    const pane=$("care-"+t+"-pane");
    if(pane) pane.classList.toggle("active",t===tab);
  }});
  if(tab==="calendar") renderCalendar();
  if(tab==="history")  renderCareHistory();
  if(tab==="due")      renderCareDue();
  if(tab==="all")      renderCareAll();
}}

// ============================================================
// FLOOR SWITCHING
// ============================================================
function setFloor(floor) {{
  currentFloor=floor;
  ["EG","1. OG","2. OG"].forEach(f=>{{
    const btn=$("fbtn-"+f);
    if(btn) btn.classList.toggle("active",f===floor);
  }});
  const fd=$("floor-img");
  fd.src=FLOOR_DATA[floor].url;
  fd.onload=()=>{{onImageReady();drawLightMap();render();}};
  if(fd.complete&&fd.naturalWidth){{onImageReady();drawLightMap();render();}}
  render(); renderInventory();
  if(activePIdx!==null) renderDetail(activePIdx);
  if(dliMode) scheduleDLICompute(floor);
}}

// ============================================================
// RENDER PINS
// ============================================================
function render() {{
  const canvas=$("map-canvas");
  const img=$("floor-img");
  const W=img.naturalWidth||1100, H=img.naturalHeight||600;
  canvas.style.width=W+"px"; canvas.style.height=H+"px";
  canvas.querySelectorAll(".plant-pin").forEach(el=>el.remove());
  plants.forEach((p,i)=>{{
    const pos=positions[i];
    if(!pos||pos.floor!==currentFloor) return;
    const ist=dliMode?(getDLIScore(pos.x,pos.y,currentFloor)??computeLicht(pos.x,pos.y,currentFloor)):computeLicht(pos.x,pos.y,currentFloor);
    const stat=getLichtStatus(ist,p.licht);
    const pin=document.createElement("div");
    pin.className="plant-pin"+(activePIdx===i?" active":"");
    pin.dataset.idx=i;
    const tx=Math.round(pos.x*W-21), ty=Math.round(pos.y*H-21);
    pin.style.transform=`translate(${{tx}}px,${{ty}}px)`;
    pin.innerHTML=`
      <div class="pin-bubble">${{p.emoji}}</div>
      <div class="pin-indicator ${{stat}}"></div>
      <div class="pin-label">${{p.name}}</div>
      <div class="pin-light-badge">${{ist}}/10</div>
    `;
    pin.addEventListener("click",e=>{{e.stopPropagation();activePIdx=i;render();renderInventory();renderDetail(i);}});
    pin.addEventListener("mouseenter",e=>showTooltip(`${{p.name}} — ${{ist}}/10 Licht`,e.clientX,e.clientY));
    pin.addEventListener("mouseleave",hideTooltip);
    setupPinDrag(pin,i);
    canvas.appendChild(pin);
  }});
}}

// ============================================================
// DETAIL PANEL
// ============================================================
function showEmptyDetail() {{
  $("rsb-empty").style.display="flex";
  $("rsb-detail").classList.remove("visible");
  $("rsb-detail").innerHTML="";
}}

function renderDetail(idx) {{
  const p=plants[idx];
  if(!p) return;
  const det=$("rsb-detail");
  det.innerHTML="";
  det.classList.add("visible");
  $("rsb-empty").style.display="none";

  const pos=positions[idx];
  const lf=pos?computeLichtFull(pos.x,pos.y,pos.floor):null;
  const liveScore=lf?lf.score:null;
  const dliScore=pos?(getDLIScore(pos.x,pos.y,pos.floor||currentFloor)??null):null;
  const primaryScore=dliMode?dliScore:liveScore;
  const stat=primaryScore?getLichtStatus(primaryScore,p.licht):null;
  const sc=stat?STATUS_CFG[stat]:null;

  const imgUrl=getPlantImageUrl(p.name);
  const imgHTML=`
    <div class="detail-img-wrap">
      <img src="${{imgUrl}}" style="width:100%;height:100%;object-fit:cover;"
        onerror="this.style.display='none'">
      <div class="detail-img-overlay"></div>
    </div>
  `;

  const coordsHTML=pos?`<div class="coords">📍 ${{pos.floor}} · x:${{(pos.x*100).toFixed(1)}}% y:${{(pos.y*100).toFixed(1)}}%</div>`:'';

  // DLI panel
  let dliHTML="";
  if(dliScore&&dliMode) {{
    const dliPct=(dliScore/10*100).toFixed(1);
    dliHTML=`
      <div class="dli-detail">
        <div class="dli-detail-lbl">Tages-DLI (berechnet)</div>
        <div class="dli-bar-wrap">
          <div class="dli-bar-track"><div class="dli-bar-fill" style="width:${{dliPct}}%"></div></div>
          <div class="dli-score-val">${{dliScore}}</div>
        </div>
      </div>
    `;
  }}

  // Astro panel
  let astroHTML="";
  if(lf) {{
    const winChips=lf.windowHits.map(w=>{{
      const visRatio=parseFloat(w.visRatio||0);
      const bright=!w.occluded&&parseFloat(w.incFactor)>0.2;
      return `<span class="win-chip ${{bright?"hit":""}}">${{w.side}}${{w.occluded?" ✕":bright?" ☀":""}} (${{Math.round(visRatio*100)}}%)</span>`;
    }}).join("");
    const nightMode=sunState.elevation<=-6;
    const dawnMode=sunState.elevation<=0&&!nightMode;
    const timeLabel=nightMode?"🌙 Nacht":dawnMode?"🌅 Dämmerung":"☀ Tageslicht";
    astroHTML=`
      <div class="astro-panel">
        <div class="astro-title">Lichtanalyse · ${{timeLabel}}</div>
        <div class="astro-grid">
          <div class="astro-cell"><div class="astro-cell-lbl">Elevation</div><div class="astro-cell-val">${{sunState.elevation.toFixed(1)}}<span class="astro-cell-unit">°</span></div></div>
          <div class="astro-cell"><div class="astro-cell-lbl">Azimut</div><div class="astro-cell-val">${{sunState.azimuth.toFixed(0)}}<span class="astro-cell-unit">°</span></div></div>
          <div class="astro-cell"><div class="astro-cell-lbl">Direktsonne</div><div class="astro-cell-val">${{(lf.components.sunDirect*100).toFixed(0)}}<span class="astro-cell-unit">%</span></div></div>
          <div class="astro-cell"><div class="astro-cell-lbl">Himmelslicht</div><div class="astro-cell-val">${{(lf.components.skyDiff*100/0.15).toFixed(0)}}<span class="astro-cell-unit">%</span></div></div>
        </div>
        <div class="window-chips">${{winChips}}</div>
      </div>
    `;
  }}

  const barColor=stat==='ideal'?'var(--accent)':stat==='ok'?'var(--warn-bright)':'var(--danger-bright)';
  const scoreToShow=primaryScore||liveScore;
  const lightHTML=scoreToShow?`
    <div class="score-badge ${{sc.cls}}">
      <div class="sc-icon">${{sc.icon}}</div>
      <div class="sc-text"><h3>${{sc.label}}</h3><p>${{sc.desc}}</p></div>
    </div>
    <div class="light-bar-wrap">
      <div class="lbw-label"><span>Lichtwert</span><span>${{scoreToShow}} / 10</span></div>
      <div class="lbw-track">
        <div class="lbw-fill" style="width:${{(scoreToShow/10*100).toFixed(1)}}%;background:linear-gradient(90deg,var(--accent-dim),${{barColor}})"></div>
        <div class="lbw-needle" style="left:${{(p.licht/10*100).toFixed(1)}}%"></div>
      </div>
      <div class="lbw-label"><span style="color:var(--text-3)">Bedarf: ${{p.licht}}/10</span><span style="color:var(--text-3)">Verfügbar: ${{scoreToShow}}/10</span></div>
    </div>
    ${{dliHTML}}
    ${{astroHTML}}
  `:`
    ${{dliHTML||'<div style="font-size:12px;color:var(--text-3);background:var(--surface-2);border-radius:8px;padding:16px;margin:0 16px 12px;text-align:center;">Pflanze auf Karte platzieren für Lichtanalyse</div>'}}
  `;

  const removeHTML=pos?`<button class="act-btn danger-btn" onclick="removePlant(${{idx}})">🗑 Entfernen</button>`:"";
  const extraHTML=`
    <div style="padding:0 0 8px;">
      ${{p.luftfeuchtigkeit?`<div class="detail-extra-row"><div class="detail-extra-lbl">💧 Luftfeuchtigkeit</div><div class="detail-extra-val">${{p.luftfeuchtigkeit}}</div></div>`:''}}
      ${{p.besprühen?`<div class="detail-extra-row"><div class="detail-extra-lbl">🌫 Besprühen</div><div class="detail-extra-val">${{p.besprühen}}</div></div>`:''}}
      ${{p.besonderheit?`<div class="detail-extra-row"><div class="detail-extra-lbl">💡 Besonderheit</div><div class="detail-extra-val">${{p.besonderheit}}</div></div>`:''}}
    </div>
  `;

  det.innerHTML=`
    ${{imgHTML}}
    <div class="plant-hdr">
      <div class="big-emoji">${{p.emoji}}</div>
      <div class="plant-hdr-text">
        <h2>${{p.name}}</h2>
        ${{p.botanisch?`<div class="botanical">${{p.botanisch}}</div>`:''}}
        ${{coordsHTML}}
      </div>
    </div>
    ${{lightHTML}}
    <div class="data-grid">
      <div class="dc"><div class="dc-lbl">💧 Gießen (${{MONTHS_DE[NOW_MONTH]}})</div><div class="dc-val">${{p.giessen||"—"}}<span class="dc-unit">Tage</span></div></div>
      <div class="dc"><div class="dc-lbl">🌿 Düngen (${{MONTHS_DE[NOW_MONTH]}})</div><div class="dc-val">${{p.dungen||"—"}}</div></div>
      <div class="dc"><div class="dc-lbl">☀ Lichtbedarf</div><div class="dc-val">${{p.licht}}<span class="dc-unit">/ 10</span></div></div>
      <div class="dc"><div class="dc-lbl">🪴 Umtopfen</div><div class="dc-val" style="font-size:13px">${{p.umtopfen||"—"}}</div></div>
    </div>
    ${{extraHTML}}
    <div class="action-row">
      <button class="act-btn primary" onclick="selectPlant(${{idx}})">✓ OK</button>
      ${{removeHTML}}
    </div>
  `;
}}

function selectPlant(idx) {{
  activePIdx=null;
  render(); renderInventory(); showEmptyDetail();
}}

function removePlant(idx) {{
  delete positions[idx];
  activePIdx=null;
  debouncedSave();
  render(); renderInventory(); showEmptyDetail();
}}

// ============================================================
// RENDER INVENTORY
// ============================================================
function renderInventory() {{
  const list=$("inv-list");
  const filter=inventoryFilter.toLowerCase();
  const available=[],placedHere=[],otherFloor=[];
  plants.forEach((p,i)=>{{
    if(filter&&!p.name.toLowerCase().includes(filter)) return;
    const pos=positions[i];
    if(!pos) available.push(i);
    else if(pos.floor===currentFloor) placedHere.push(i);
    else otherFloor.push(i);
  }});
  list.innerHTML="";
  const makeGroup=(label,indices,isPlaced,isOther)=>{{
    if(!indices.length) return;
    const grp=document.createElement("div");
    grp.className="inv-group";
    grp.innerHTML=`<div class="inv-group-label">${{label}} (${{indices.length}})</div>`;
    indices.forEach(i=>{{
      const p=plants[i];
      const item=document.createElement("div");
      let cls="inv-item";
      if(activePIdx===i) cls+=" selected";
      if(isOther) cls+=" placed-elsewhere";
      item.className=cls;
      item.dataset.pidx=i;
      const badgeHtml=isPlaced?`<span class="inv-badge placed-badge">📍 ${{positions[i]?.floor||""}}</span>`:`<span class="inv-badge">Frei</span>`;
      item.innerHTML=`<span class="inv-emoji">${{p.emoji}}</span><span class="inv-name">${{p.name}}</span>${{badgeHtml}}`;
      item.addEventListener("click",()=>{{
        activePIdx=i;
        if(positions[i]&&positions[i].floor!==currentFloor) setFloor(positions[i].floor);
        render(); renderInventory(); renderDetail(i);
      }});
      if(!isPlaced) {{
        item.draggable=true;
        item.addEventListener("dragstart",e=>{{dragSrcIdx=i;e.dataTransfer.effectAllowed="move";setTimeout(()=>item.classList.add("dragging-source"),0);}});
        item.addEventListener("dragend",()=>{{item.classList.remove("dragging-source");dragSrcIdx=null;}});
      }}
      grp.appendChild(item);
    }});
    list.appendChild(grp);
  }};
  makeGroup("Verfügbar",available,false,false);
  makeGroup("Hier platziert",placedHere,true,false);
  makeGroup("Anderes OG",otherFloor,true,true);
}}

function filterInventory(val) {{ inventoryFilter=val; renderInventory(); }}

// ============================================================
// DROP ONTO MAP
// ============================================================
const mapArea=$("map-area");
mapArea.addEventListener("dragover",e=>{{e.preventDefault();e.dataTransfer.dropEffect="move";$("map-canvas").classList.add("drag-over");}});
mapArea.addEventListener("dragleave",()=>$("map-canvas").classList.remove("drag-over"));
mapArea.addEventListener("drop",e=>{{
  e.preventDefault(); $("map-canvas").classList.remove("drag-over");
  if(dragSrcIdx===null) return;
  const img=$("floor-img");
  const W=img.naturalWidth||1100, H=img.naturalHeight||600;
  const area=$("map-area");
  const scale=parseFloat($("map-canvas").style.transform.match(/scale\(([^)]+)\)/)?.[1]||1);
  const cX=area.clientWidth/2-W*scale/2, cY=area.clientHeight/2-H*scale/2;
  const rx=Math.max(0,Math.min(1,(e.clientX-cX)/(W*scale)));
  const ry=Math.max(0,Math.min(1,(e.clientY-cY)/(H*scale)));
  positions[dragSrcIdx]={{floor:currentFloor,x:rx,y:ry}};
  activePIdx=dragSrcIdx; dragSrcIdx=null;
  debouncedSave();
  render(); renderInventory(); renderDetail(activePIdx);
}});

// ============================================================
// PIN DRAG
// ============================================================
function setupPinDrag(pin,idx) {{
  let startX,startY,startPX,startPY,dragging=false;
  function getWH() {{
    const img=$("floor-img");
    const W=img.naturalWidth||1100, H=img.naturalHeight||600;
    const rect=img.getBoundingClientRect();
    return {{W,H,scaleX:W/rect.width,scaleY:H/rect.height}};
  }}
  pin.addEventListener("pointerdown",e=>{{
    if(e.button!==0&&e.button!==undefined) return;
    e.preventDefault(); e.stopPropagation();
    dragging=true; pin.classList.add("dragging"); pin.setPointerCapture(e.pointerId);
    startX=e.clientX; startY=e.clientY;
    startPX=positions[idx].x; startPY=positions[idx].y;
  }});
  pin.addEventListener("pointermove",e=>{{
    if(!dragging) return; e.preventDefault();
    const {{W,H,scaleX,scaleY}}=getWH();
    positions[idx].x=Math.max(0,Math.min(1,startPX+(e.clientX-startX)*scaleX/W));
    positions[idx].y=Math.max(0,Math.min(1,startPY+(e.clientY-startY)*scaleY/H));
    const tx=Math.round(positions[idx].x*W-21), ty=Math.round(positions[idx].y*H-21);
    pin.style.transform=`translate(${{tx}}px,${{ty}}px)`;
    const ist=computeLicht(positions[idx].x,positions[idx].y,currentFloor);
    const stat=getLichtStatus(ist,plants[idx].licht);
    pin.querySelector(".pin-indicator").className="pin-indicator "+stat;
    pin.querySelector(".pin-light-badge").textContent=ist+"/10";
    if(activePIdx===idx) renderDetail(idx);
  }});
  pin.addEventListener("pointerup",e=>{{
    if(!dragging) return;
    dragging=false; pin.classList.remove("dragging");
    debouncedSave();
    render();
    if(activePIdx===idx) renderDetail(idx);
  }});
  pin.addEventListener("pointercancel",()=>{{dragging=false;pin.classList.remove("dragging");}});
}}

// ============================================================
// LIBRARY — SMART FILTER & SORT
// ============================================================
function onLibraryFilterChange() {{
  libraryFilter=$("lib-search").value;
  libFilterLight=$("lib-filter-light").value;
  libFilterWater=$("lib-filter-water").value;
  libSort=$("lib-sort").value;
  renderLibrary();
}}

function resetLibraryFilters() {{
  $("lib-search").value="";
  $("lib-filter-light").value="";
  $("lib-filter-water").value="";
  $("lib-sort").value="name";
  libraryFilter=""; libFilterLight=""; libFilterWater=""; libSort="name";
  renderLibrary();
}}

function applyLibraryFiltersAndSort(list) {{
  const txt=libraryFilter.toLowerCase();
  // Filter
  let filtered=list.filter(p=>{{
    if(txt && !p.name.toLowerCase().includes(txt) && !(p.botanisch||"").toLowerCase().includes(txt)) return false;
    if(libFilterLight) {{
      const l=p.licht||5;
      if(libFilterLight==="low"&&l>4) return false;
      if(libFilterLight==="mid"&&(l<5||l>7)) return false;
      if(libFilterLight==="high"&&l<8) return false;
    }}
    if(libFilterWater) {{
      const days=parseIntervalDays(p.giessen);
      if(libFilterWater==="rare"&&(days===null||days<14)) return false;
      if(libFilterWater==="mid"&&(days===null||days<7||days>=14)) return false;
      if(libFilterWater==="frequent"&&(days===null||days>=7)) return false;
    }}
    return true;
  }});
  // Sort
  filtered.sort((a,b)=>{{
    switch(libSort) {{
      case "name": return a.name.localeCompare(b.name,"de");
      case "name-desc": return b.name.localeCompare(a.name,"de");
      case "licht": return (a.licht||0)-(b.licht||0);
      case "licht-desc": return (b.licht||0)-(a.licht||0);
      case "giessen": return (parseIntervalDays(a.giessen)||999)-(parseIntervalDays(b.giessen)||999);
      case "giessen-desc": return (parseIntervalDays(b.giessen)||999)-(parseIntervalDays(a.giessen)||999);
      default: return 0;
    }}
  }});
  return filtered;
}}

function renderLibrary() {{
  const grid=$("lib-grid");
  const filtered=applyLibraryFiltersAndSort(plants);
  const placed=Object.keys(positions).length;
  const hasFilters=libraryFilter||libFilterLight||libFilterWater;

  // Results bar
  $("lib-sub-label").textContent=`${{plants.length}} Pflanzen · ${{placed}} platziert · ${{MONTHS_DE[NOW_MONTH]}}`;
  $("lib-results-count").textContent=`${{filtered.length}} von ${{plants.length}} Einträgen`;

  // Active filter tags
  const filterTags=[];
  if(libraryFilter) filterTags.push(`"${{libraryFilter}}"`);
  if(libFilterLight) filterTags.push(libFilterLight==="low"?"☀ Schattig":libFilterLight==="mid"?"☀ Halbschattig":"☀ Sonnig");
  if(libFilterWater) filterTags.push(libFilterWater==="rare"?"💧 Selten":libFilterWater==="mid"?"💧 Mittel":"💧 Häufig");
  $("lib-active-filters").innerHTML=filterTags.map(t=>`<span class="lib-filter-tag" onclick="resetLibraryFilters()">${{t}} ✕</span>`).join("");

  const resetBtn=$("lib-reset-btn");
  if(resetBtn) resetBtn.style.display=hasFilters?"":"none";

  grid.innerHTML="";

  if(!filtered.length) {{
    grid.innerHTML=`<div class="lib-no-results"><div class="lib-no-results-icon">🔍</div><div style="font-size:14px;font-weight:600;color:var(--text-2)">Keine Pflanzen gefunden</div><div style="font-size:12px;color:var(--text-3);margin-top:6px">Filter anpassen oder zurücksetzen</div></div>`;
    return;
  }}

  filtered.forEach(p=>{{
    const i=plants.indexOf(p);
    const pos=positions[i];
    const lf=pos?computeLichtFull(pos.x,pos.y,pos.floor):null;
    const ist=lf?lf.score:null;
    const stat=ist?getLichtStatus(ist,p.licht):null;
    const floorLabel=pos?`📍 ${{pos.floor}}`:"📦 Inventar";
    const barColor=stat==='ideal'?'var(--accent)':stat==='ok'?'var(--warn-bright)':'var(--danger-bright)';
    const lightPct=ist?(ist/10*100).toFixed(1):0;

    let statusChip="";
    if(stat) {{
      const cfg={{ideal:{{cls:"ideal",lbl:"✓ Optimal"}},ok:{{cls:"ok",lbl:"~ Akzeptabel"}},bad:{{cls:"bad",lbl:"✕ Zu dunkel"}}}};
      const c=cfg[stat];
      statusChip=`<span class="lib-status-chip ${{c.cls}}">${{c.lbl}}</span>`;
    }} else {{
      statusChip=`<span class="lib-status-chip none">📦 Nicht platziert</span>`;
    }}

    const imgUrl=getPlantImageUrl(p.name);
    const besondHTML=p.besonderheit?`<div class="lib-besonderheit"><div class="lib-besonderheit-lbl">💡 Besonderheit</div>${{p.besonderheit}}</div>`:'';
    const humiHTML=(p.luftfeuchtigkeit||p.besprühen)?`
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        ${{p.luftfeuchtigkeit?`<div class="lib-humidity-row">💧 <span class="lib-humidity-badge">${{p.luftfeuchtigkeit}}</span></div>`:''}}
        ${{p.besprühen?`<div class="lib-humidity-row">🌫 Besprühen: <strong style="color:var(--text);margin-left:3px">${{p.besprühen}}</strong></div>`:''}}
      </div>
    `:'';

    const waterDays=parseIntervalDays(p.giessen);
    const fertDays=parseIntervalDays(p.dungen);

    const card=document.createElement("div");
    card.className="lib-card";
    card.innerHTML=`
      <div class="lib-card-img">
        <img src="${{imgUrl}}" alt="${{p.name}}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="lib-card-img-fallback" style="display:none">${{p.emoji}}</div>
        <div class="lib-card-img-overlay">
          <div class="lib-card-name">${{p.name}}</div>
          ${{p.botanisch?`<div class="lib-card-botanical">${{p.botanisch}}</div>`:''}}
        </div>
      </div>
      <div class="lib-card-body">
        <div class="lib-card-top-row">
          ${{statusChip}}
          <div class="lib-card-loc" style="margin-left:auto">
            <div class="lib-card-loc-dot ${{pos?"placed":""}}"></div>
            ${{floorLabel}}
          </div>
        </div>
        <div class="lib-metrics-row">
          <div class="lib-metric">
            <div class="lib-metric-lbl">☀ Lichtbedarf</div>
            <div class="lib-metric-val">${{p.licht}}<span class="lib-metric-unit">/ 10</span></div>
          </div>
          <div class="lib-metric">
            <div class="lib-metric-lbl">💧 Gießen</div>
            <div class="lib-metric-val">${{waterDays||"—"}}<span class="lib-metric-unit">${{waterDays?"d":""}}</span></div>
          </div>
          <div class="lib-metric">
            <div class="lib-metric-lbl">🌿 Düngen</div>
            <div class="lib-metric-val">${{fertDays||"—"}}<span class="lib-metric-unit">${{fertDays?"d":""}}</span></div>
          </div>
        </div>
        ${{ist?`
        <div class="lib-light-row">
          <div style="font-size:11px;color:var(--text-3);width:60px;font-family:var(--font-mono)">Licht</div>
          <div class="lib-light-bar-wrap">
            <div class="lib-light-bar-track">
              <div class="lib-light-bar-fill" style="width:${{lightPct}}%;background:linear-gradient(90deg,rgba(63,185,80,.3),${{barColor}})"></div>
            </div>
          </div>
          <div class="lib-light-score" style="color:${{barColor}}">${{ist}}/10</div>
        </div>
        `:''}
        ${{humiHTML}}
        ${{besondHTML}}
      </div>
      <div class="lib-card-footer">
        <button class="show-on-map-btn" data-pidx="${{i}}">🗺 Auf Karte</button>
        <button class="show-on-map-btn care-btn-lib" onclick="switchTab('care')">🌱 Pflege</button>
      </div>
    `;
    card.querySelector(".show-on-map-btn").addEventListener("click",()=>{{
      const ppos=positions[i];
      if(ppos) setFloor(ppos.floor);
      switchTab("planer");
      setTimeout(()=>{{
        activePIdx=i; render(); renderDetail(i);
        const pin=$("map-canvas").querySelector(`[data-idx="${{i}}"]`);
        if(pin){{pin.classList.add("highlight-pulse");setTimeout(()=>pin.classList.remove("highlight-pulse"),4500);}}
      }},120);
    }});
    grid.appendChild(card);
  }});
}}

// ============================================================
// CLICK OUTSIDE → DESELECT
// ============================================================
$("map-area").addEventListener("click",()=>{{activePIdx=null;render();renderInventory();showEmptyDetail();}});

// ============================================================
// CARE BADGE UPDATE
// ============================================================
function updateCareBadge() {{
  const now=new Date();
  let dueCount=0;
  plants.forEach((p,i)=>{{
    const ws=getCareStatus(i,'water');
    const fs=getCareStatus(i,'fertilize');
    if((ws&&ws.overdueDays>0)||(fs&&fs.overdueDays>0)) dueCount++;
  }});
  const badge=$("care-tab-badge");
  if(badge) {{
    badge.textContent=dueCount;
    badge.style.display=dueCount>0?"":"none";
    badge.className="tab-badge"+(dueCount>0?" ":"");
  }}
}}

// ============================================================
// KALENDER
// ============================================================
function changeCalMonth(d) {{
  calMonth+=d;
  if(calMonth<0){{calMonth=11;calYear--;}}
  if(calMonth>11){{calMonth=0;calYear++;}}
  renderCalendar();
}}

function renderCalendar() {{
  const title=$("cal-month-title");
  if(title) title.textContent=`${{MONTHS_DE[calMonth]}} ${{calYear}}`;
  const headerRow=$("cal-header-row");
  if(headerRow) headerRow.innerHTML=DAYS_DE.map(d=>`<div class="cal-header-cell">${{d}}</div>`).join("");
  const grid=$("cal-grid");
  if(!grid) return;
  const firstDay=new Date(calYear,calMonth,1);
  const totalDays=new Date(calYear,calMonth+1,0).getDate();
  const prevMonthDays=new Date(calYear,calMonth,0).getDate();
  let startDow=firstDay.getDay();
  let html="";
  for(let d=0;d<startDow;d++) html+=`<div class="cal-cell other-month"><div class="cal-day-num">${{prevMonthDays-startDow+d+1}}</div></div>`;
  const todayD=NOW.getDate(),todayM=NOW.getMonth(),todayY=NOW.getFullYear();
  const eventsByDay={{}};
  careHistory.forEach(h=>{{
    const d=new Date(h.time);
    if(d.getMonth()===calMonth&&d.getFullYear()===calYear) {{
      const day=d.getDate();
      if(!eventsByDay[day]) eventsByDay[day]=[];
      eventsByDay[day].push({{type:h.type,name:h.name,emoji:h.emoji}});
    }}
  }});
  plants.forEach((p,i)=>{{
    const ws=getCareStatus(i,'water');
    const fs=getCareStatus(i,'fertilize');
    [['water',ws],['fertilize',fs]].forEach(([type,status])=>{{
      if(!status) return;
      const nd=status.nextDate;
      if(nd.getMonth()===calMonth&&nd.getFullYear()===calYear) {{
        const day=nd.getDate();
        if(!eventsByDay[day]) eventsByDay[day]=[];
        eventsByDay[day].push({{type:'due-'+type,name:p.name,emoji:p.emoji}});
      }}
    }});
  }});
  for(let d=1;d<=totalDays;d++) {{
    const isToday=d===todayD&&calMonth===todayM&&calYear===todayY;
    const events=eventsByDay[d]||[];
    const evHTML=events.slice(0,3).map(e=>{{
      const cls=e.type==='water'?'water':e.type==='fertilize'?'fertilize':e.type==='due-water'?'due-water':'due-fertilize';
      const icon=e.type.includes('water')?'💧':'🌿';
      return `<div class="cal-event ${{cls}}">${{icon}} ${{e.name}}</div>`;
    }}).join("");
    const moreHTML=events.length>3?`<div class="cal-event" style="color:var(--text-3);background:transparent;">+${{events.length-3}}</div>`:"";
    html+=`<div class="cal-cell${{isToday?' today':''}}"><div class="cal-day-num">${{d}}</div><div class="cal-events">${{evHTML}}${{moreHTML}}</div></div>`;
  }}
  const cellsUsed=startDow+totalDays;
  const remaining=(7-(cellsUsed%7))%7;
  for(let d=1;d<=remaining;d++) html+=`<div class="cal-cell other-month"><div class="cal-day-num">${{d}}</div></div>`;
  grid.innerHTML=html;
}}

// ============================================================
// CARE STATUS LOGIC — Saisonale 12-Monate-Logik
// ============================================================
function parseIntervalDays(val) {{
  if(!val||val==="—"||String(val).trim()==="") return null;
  const n=parseFloat(String(val).replace(",","."));
  return isNaN(n)||n<=0?null:Math.round(n);
}}

function getMonthlyInterval(plantIdx, type) {{
  // Uses current month's value from the 12-month schema in Sheets
  const p=plants[plantIdx];
  if(!p) return null;
  const currentMonthName=MONTHS_DE[NOW_MONTH];
  let val;
  if(type==='water') {{
    val = p.giessAll&&p.giessAll[currentMonthName] !== undefined
      ? p.giessAll[currentMonthName]
      : p.giessen;
  }} else {{
    val = p.duengAll&&p.duengAll[currentMonthName] !== undefined
      ? p.duengAll[currentMonthName]
      : p.dungen;
  }}
  return parseIntervalDays(val);
}}

function getCareStatus(plantIdx, type) {{
  const intervalDays=getMonthlyInterval(plantIdx, type);
  if(!intervalDays) return null;

  const cd=careData[plantIdx]||{{}};
  const lastStr=type==='water'?cd.lastWatered:cd.lastFertilized;

  // Robust date parsing
  let lastDate=null;
  if(lastStr) {{
    const d=new Date(lastStr);
    if(!isNaN(d.getTime())) lastDate=d;
  }}

  const now=new Date();
  let nextDate,overdueDays=0,moisturePct=50;

  if(lastDate) {{
    nextDate=new Date(lastDate.getTime()+intervalDays*24*3600*1000);
    const diffMs=now-nextDate;
    overdueDays=Math.max(0,Math.floor(diffMs/(24*3600*1000)));
    const elapsed=(now-lastDate)/(1000*3600*24);
    moisturePct=Math.max(0,Math.min(100,Math.round((1-elapsed/intervalDays)*100)));
  }} else {{
    // Never cared for — treat as overdue since yesterday
    nextDate=new Date(now.getTime()-24*3600*1000);
    overdueDays=1;
    moisturePct=0;
  }}

  return {{nextDate,overdueDays,intervalDays,moisturePct,lastDate}};
}}

function formatRelDate(date) {{
  const now=new Date();
  const diffDays=Math.round((date-now)/(24*3600*1000));
  if(diffDays<-1) return `${{Math.abs(diffDays)}} Tage überfällig`;
  if(diffDays===-1) return "Gestern fällig";
  if(diffDays===0) return "Heute fällig";
  if(diffDays===1) return "Morgen";
  if(diffDays<=3) return `In ${{diffDays}} Tagen`;
  return date.toLocaleDateString("de-DE",{{day:"2-digit",month:"2-digit"}});
}}

function formatAbsDate(isoStr) {{
  if(!isoStr) return "—";
  const d=new Date(isoStr);
  if(isNaN(d.getTime())) return "Ungültiges Datum";
  return d.toLocaleDateString("de-DE",{{day:"2-digit",month:"2-digit",year:"numeric"}})
    +" "+d.toLocaleTimeString("de-DE",{{hour:"2-digit",minute:"2-digit"}});
}}

// ============================================================
// CARE ACTIONS — Sofort-Sync
// ============================================================
async function doWater(plantIdx) {{
  if(!careData[plantIdx]) careData[plantIdx]={{}};
  const now=new Date().toISOString();
  careData[plantIdx].lastWatered=now;
  careHistory.unshift({{type:'water',plantIdx,name:plants[plantIdx].name,emoji:plants[plantIdx].emoji,time:now,synced:false}});
  saveCareData();
  renderCare();
  updateCareBadge();
  showToast(`💧 ${{plants[plantIdx].name}} gegossen`,"success");
  // Async sync to Sheets
  const ok=await saveCareToSheets(plantIdx,'water',now);
  if(ok) {{
    careHistory[0].synced=true;
    saveCareData();
    if(currentCareSubtab==='history') renderCareHistory();
  }}
}}

async function doFertilize(plantIdx) {{
  if(!careData[plantIdx]) careData[plantIdx]={{}};
  const now=new Date().toISOString();
  careData[plantIdx].lastFertilized=now;
  careHistory.unshift({{type:'fertilize',plantIdx,name:plants[plantIdx].name,emoji:plants[plantIdx].emoji,time:now,synced:false}});
  saveCareData();
  renderCare();
  updateCareBadge();
  showToast(`🌿 ${{plants[plantIdx].name}} gedüngt`,"success");
  const ok=await saveCareToSheets(plantIdx,'fertilize',now);
  if(ok) {{
    careHistory[0].synced=true;
    saveCareData();
    if(currentCareSubtab==='history') renderCareHistory();
  }}
}}

async function waterAllDue() {{
  let count=0;
  const toSync=[];
  plants.forEach((p,i)=>{{
    const ws=getCareStatus(i,'water');
    if(ws&&ws.overdueDays>0) {{
      if(!careData[i]) careData[i]={{}};
      const now=new Date().toISOString();
      careData[i].lastWatered=now;
      careHistory.unshift({{type:'water',plantIdx:i,name:p.name,emoji:p.emoji,time:now,synced:false}});
      toSync.push({{idx:i,time:now}});
      count++;
    }}
  }});
  saveCareData();
  renderCare();
  updateCareBadge();
  showToast(`💧 ${{count}} Pflanzen gegossen`,"success");
  // Batch sync
  for(const s of toSync) await saveCareToSheets(s.idx,'water',s.time);
}}

function refreshCare() {{ renderCare(); updateCareBadge(); }}

function renderCare() {{
  if(currentCareSubtab==='calendar') renderCalendar();
  else if(currentCareSubtab==='due') renderCareDue();
  else if(currentCareSubtab==='all') renderCareAll();
  else if(currentCareSubtab==='history') renderCareHistory();
  renderCareStatusCounts();
}}

function renderCareStatusCounts() {{
  const now=new Date();
  const in3days=new Date(now.getTime()+3*24*3600*1000);
  let dueCount=0,soonCount=0;
  plants.forEach((p,i)=>{{
    const ws=getCareStatus(i,'water');
    const fs=getCareStatus(i,'fertilize');
    const wOver=ws&&ws.overdueDays>0;
    const fOver=fs&&fs.overdueDays>0;
    const wSoon=ws&&!wOver&&ws.nextDate<=in3days;
    const fSoon=fs&&!fOver&&fs.nextDate<=in3days;
    if(wOver||fOver) dueCount++;
    else if(wSoon||fSoon) soonCount++;
  }});
  $("care-sub-label").textContent=`${{plants.length}} Pflanzen · ${{dueCount}} fällig · ${{soonCount}} demnächst`;
}}

// ============================================================
// CARE DUE — Fällige Aufgaben
// ============================================================
function renderCareDue() {{
  const now=new Date();
  const in3days=new Date(now.getTime()+3*24*3600*1000);
  const overdueItems=[],soonItems=[];
  plants.forEach((p,i)=>{{
    const ws=getCareStatus(i,'water');
    const fs=getCareStatus(i,'fertilize');
    const wOver=ws&&ws.overdueDays>0;
    const fOver=fs&&fs.overdueDays>0;
    const wSoon=ws&&!wOver&&ws.nextDate<=in3days;
    const fSoon=fs&&!fOver&&fs.nextDate<=in3days;
    if(wOver||fOver) overdueItems.push({{idx:i,ws,fs}});
    else if(wSoon||fSoon) soonItems.push({{idx:i,ws,fs}});
  }});

  const overdueSection=$("care-overdue-section");
  if(overdueSection) {{
    if(overdueItems.length>0) {{
      overdueSection.innerHTML=`
        <div class="care-section-title">🔴 Überfällig / Heute fällig <span class="care-badge">${{overdueItems.length}} Pflanze${{overdueItems.length!==1?'n':''}}</span></div>
        ${{overdueItems.map(e=>makeCareCard(e.idx,e.ws,e.fs,'overdue')).join("")}}
      `;
    }} else {{
      overdueSection.innerHTML=`
        <div class="care-section-title">🔴 Überfällig <span class="care-badge ok">✓ Alles erledigt</span></div>
        <div class="care-empty"><span class="ce-icon">🎉</span><p>Alle Pflanzen sind versorgt!</p></div>
      `;
    }}
  }}

  const soonSection=$("care-soon-section");
  if(soonSection) {{
    if(soonItems.length>0) {{
      soonSection.innerHTML=`
        <div class="care-section-title" style="margin-top:12px">🟡 In den nächsten 3 Tagen <span class="care-badge warn">${{soonItems.length}} Pflanze${{soonItems.length!==1?'n':''}}</span></div>
        ${{soonItems.map(e=>makeCareCard(e.idx,e.ws,e.fs,'soon')).join("")}}
      `;
    }} else {{
      soonSection.innerHTML='';
    }}
  }}
}}

// ============================================================
// CARE ALL
// ============================================================
function renderCareAll() {{
  const now=new Date();
  const in3days=new Date(now.getTime()+3*24*3600*1000);
  const allSection=$("care-all-section");
  if(!allSection) return;

  // Grouped: overdue, soon, ok
  const groups={{overdue:[],soon:[],ok:[]}};
  plants.forEach((p,i)=>{{
    const ws=getCareStatus(i,'water');
    const fs=getCareStatus(i,'fertilize');
    const wOver=ws&&ws.overdueDays>0;
    const fOver=fs&&fs.overdueDays>0;
    const wSoon=ws&&!wOver&&ws.nextDate<=in3days;
    const fSoon=fs&&!fOver&&fs.nextDate<=in3days;
    if(wOver||fOver) groups.overdue.push({{idx:i,ws,fs}});
    else if(wSoon||fSoon) groups.soon.push({{idx:i,ws,fs}});
    else groups.ok.push({{idx:i,ws,fs}});
  }});

  let html='';
  if(groups.overdue.length) {{
    html+=`<div class="care-section-title">🔴 Überfällig <span class="care-badge">${{groups.overdue.length}}</span></div>`;
    html+=groups.overdue.map(e=>makeCareCard(e.idx,e.ws,e.fs,'overdue')).join('');
  }}
  if(groups.soon.length) {{
    html+=`<div class="care-section-title" style="margin-top:14px">🟡 Demnächst fällig <span class="care-badge warn">${{groups.soon.length}}</span></div>`;
    html+=groups.soon.map(e=>makeCareCard(e.idx,e.ws,e.fs,'soon')).join('');
  }}
  if(groups.ok.length) {{
    html+=`<div class="care-section-title" style="margin-top:14px">🟢 Versorgt <span class="care-badge ok">${{groups.ok.length}}</span></div>`;
    html+=groups.ok.map(e=>makeCareCard(e.idx,e.ws,e.fs,'ok')).join('');
  }}
  allSection.innerHTML=html;
}}

// ============================================================
// CARE CARD — mit Kreisdiagrammen und Fortschrittsbalken
// ============================================================
function makeCareCard(plantIdx, waterStatus, fertilizeStatus, variant) {{
  const p=plants[plantIdx];
  const cd=careData[plantIdx]||{{}};
  const wOver=waterStatus&&waterStatus.overdueDays>0;
  const fOver=fertilizeStatus&&fertilizeStatus.overdueDays>0;
  let cardCls="care-card"+(wOver||fOver?" overdue":variant==="soon"?" soon":variant==="ok"?" done":"");

  // Water chip
  let waterChip="";
  if(waterStatus) {{
    const cls=waterStatus.overdueDays>0?"overdue":waterStatus.nextDate<=new Date(Date.now()+3*86400000)?"soon":"ok";
    waterChip=`<span class="care-chip ${{cls}}">💧 ${{formatRelDate(waterStatus.nextDate)}}</span>`;
  }}

  // Fertilize chip
  let fertChip="";
  if(fertilizeStatus) {{
    const cls=fertilizeStatus.overdueDays>0?"overdue":fertilizeStatus.nextDate<=new Date(Date.now()+3*86400000)?"soon":"ok";
    fertChip=`<span class="care-chip ${{cls}}">🌿 ${{formatRelDate(fertilizeStatus.nextDate)}}</span>`;
  }}

  // Circle progress diagrams
  const R=18, C=2*Math.PI*R;
  let circlesHTML='';
  if(waterStatus) {{
    const pct=waterStatus.moisturePct;
    const urgent=wOver;
    const offset=C-(pct/100)*C;
    circlesHTML+=`
      <div class="care-circle-wrap">
        <div class="care-circle">
          <svg width="44" height="44" viewBox="0 0 44 44">
            <circle class="care-circle-bg" cx="22" cy="22" r="${{R}}"/>
            <circle class="care-circle-fill water${{urgent?' urgent':''}}" cx="22" cy="22" r="${{R}}"
              stroke-dasharray="${{C.toFixed(1)}}" stroke-dashoffset="${{offset.toFixed(1)}}"/>
          </svg>
          <div class="care-circle-label">${{pct}}%</div>
        </div>
        <div class="care-circle-sub">💧 Wasser</div>
      </div>
    `;
  }}
  if(fertilizeStatus) {{
    const pct=fertilizeStatus.moisturePct;
    const urgentF=fOver;
    const offset=C-(pct/100)*C;
    circlesHTML+=`
      <div class="care-circle-wrap">
        <div class="care-circle">
          <svg width="44" height="44" viewBox="0 0 44 44">
            <circle class="care-circle-bg" cx="22" cy="22" r="${{R}}"/>
            <circle class="care-circle-fill fertilize${{urgentF?' urgent':''}}" cx="22" cy="22" r="${{R}}"
              stroke-dasharray="${{C.toFixed(1)}}" stroke-dashoffset="${{offset.toFixed(1)}}"/>
          </svg>
          <div class="care-circle-label">${{pct}}%</div>
        </div>
        <div class="care-circle-sub">🌿 Dünger</div>
      </div>
    `;
  }}

  // Plant thumbnail
  const imgUrl=getPlantImageUrl(p.name);
  const thumbHTML=`
    <div class="care-card-thumb">
      <img src="${{imgUrl}}" style="width:100%;height:100%;object-fit:cover;"
        onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="care-card-thumb-emoji" style="display:none">${{p.emoji}}</div>
    </div>
  `;

  const lastW=cd.lastWatered?`Gegossen: ${{formatAbsDate(cd.lastWatered)}}`:"Noch nie gegossen";
  const lastF=cd.lastFertilized?`Gedüngt: ${{formatAbsDate(cd.lastFertilized)}}`:"Noch nie gedüngt";

  // Month label for seasonal logic
  const monthInterval=waterStatus?`Interval ${{MONTHS_DE[NOW_MONTH]}}: alle ${{waterStatus.intervalDays}} Tage`:'' ;

  return `
    <div class="${{cardCls}}">
      <div class="care-card-stripe"></div>
      <div class="care-card-inner">
        ${{thumbHTML}}
        <div class="care-card-info">
          <div class="care-card-name">${{p.name}}</div>
          <div class="care-card-meta">${{waterChip}}${{fertChip}}</div>
          <div class="care-circles">${{circlesHTML}}</div>
          <div style="font-size:10px;color:var(--text-3);font-family:var(--font-mono);display:flex;flex-direction:column;gap:2px;">
            <span>${{lastW}}</span>
            ${{fertilizeStatus?`<span>${{lastF}}</span>`:''}}
            ${{monthInterval?`<span style="color:var(--text-3);opacity:.7">${{monthInterval}}</span>`:''}}
          </div>
        </div>
        <div class="care-card-actions">
          ${{waterStatus?`<button class="care-btn water" id="wbtn-${{plantIdx}}" onclick="doWater(${{plantIdx}})">💧 Gegossen</button>`:''}}
          ${{fertilizeStatus?`<button class="care-btn fertilize" id="fbtn-c-${{plantIdx}}" onclick="doFertilize(${{plantIdx}})">🌿 Gedüngt</button>`:''}}
        </div>
      </div>
    </div>
  `;
}}

// ============================================================
// CARE HISTORY — aus lokalen + Sheets Daten
// ============================================================
function renderCareHistory() {{
  const histSection=$("care-history-section");
  if(!histSection) return;

  // Build combined history: from local actions + from sheets timestamps
  const allEntries=[...careHistory];

  // Add initial-load timestamps from care data (if not already in history)
  const existingKeys=new Set(careHistory.map(h=>`${{h.plantIdx}}-${{h.type}}-${{h.time}}`));
  plants.forEach((p,i)=>{{
    const cd=careData[i]||{{}};
    if(cd.lastWatered) {{
      const key=`${{i}}-water-${{cd.lastWatered}}`;
      if(!existingKeys.has(key)) {{
        allEntries.push({{type:'water',plantIdx:i,name:p.name,emoji:p.emoji,time:cd.lastWatered,synced:true,fromSheets:true}});
        existingKeys.add(key);
      }}
    }}
    if(cd.lastFertilized) {{
      const key=`${{i}}-fertilize-${{cd.lastFertilized}}`;
      if(!existingKeys.has(key)) {{
        allEntries.push({{type:'fertilize',plantIdx:i,name:p.name,emoji:p.emoji,time:cd.lastFertilized,synced:true,fromSheets:true}});
        existingKeys.add(key);
      }}
    }}
  }});

  // Sort by time descending
  allEntries.sort((a,b)=>new Date(b.time)-new Date(a.time));

  if(allEntries.length>0) {{
    const entries=allEntries.slice(0,80).map(h=>{{
      const icon=h.type==='water'?'💧':'🌿';
      const label=h.type==='water'?'gegossen':'gedüngt';
      const source=h.fromSheets?'sheets':h.synced?'synced':'local';
      const badge=source==='local'
        ?`<span class="history-badge local">lokal</span>`
        :`<span class="history-badge synced">☁ Sheets</span>`;
      return `
        <div class="history-entry">
          <span class="history-icon">${{icon}}</span>
          <div style="flex:1">
            <div class="history-text">${{h.emoji||'🌿'}} ${{h.name}} ${{label}}</div>
            <div class="history-sub">${{MONTHS_DE[new Date(h.time).getMonth()]}} ${{new Date(h.time).getFullYear()}} · ${{h.type==='water'?'💧 Wasser':'🌿 Dünger'}}</div>
          </div>
          ${{badge}}
          <span class="history-time">${{formatAbsDate(h.time)}}</span>
        </div>
      `;
    }}).join("");
    histSection.innerHTML=`
      <div class="care-history">
        <div class="care-history-header">
          📋 Pflege-Historie
          <span style="font-size:11px;font-weight:500;color:var(--text-3);margin-left:auto;font-family:var(--font-mono)">${{allEntries.length}} Einträge</span>
        </div>
        ${{entries}}
      </div>
    `;
  }} else {{
    histSection.innerHTML=`
      <div class="care-history">
        <div class="care-history-header">📋 Pflege-Historie</div>
        <div style="padding:32px;text-align:center;color:var(--text-3);font-size:13px;">Noch keine Aktionen aufgezeichnet.</div>
      </div>
    `;
  }}
}}

// ============================================================
// BOOT
// ============================================================
switchCareSubtab('due');
loadPlants();
</script>
</body>
</html>"""

components.html(html_app, height=920, scrolling=False)
