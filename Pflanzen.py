import streamlit as st
import streamlit.components.v1 as components
import json, math

# ============================================================
# KONFIGURATION
# ============================================================
st.set_page_config(layout="wide", page_title="Pflanzen-Planer Pro", page_icon="🌿")

st.markdown("""
<style>
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  .stApp { background: #FCFAF7; }
</style>
""", unsafe_allow_html=True)

SHEET_ID  = "1cbOPNq-CrYrin-U0OkUJ5AE2AWF6Ba7RqIHlVOtUCK0"
CSV_URL   = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
GITHUB_BASE = "https://raw.githubusercontent.com/simondereck1-hue/Pflanzen-bersicht/main"

LAT_DEG = 48.9
LON_DEG = 9.3

def building_north_azimuth(sx, sy, nx, ny):
    dx = nx - sx; dy = ny - sy
    return math.degrees(math.atan2(dx, -dy)) % 360

EG_BNA  = building_north_azimuth(1233, 775, 1267, 771)
OG1_BNA = building_north_azimuth(1221, 768, 1255, 703)
OG2_BNA = building_north_azimuth(1267, 744, 1293, 691)

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

html_app = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #F8F7F4;
  --surface: rgba(255,255,255,0.88);
  --surface-solid: #FFFFFF;
  --surface-2: #F1F8E9;
  --surface-3: #E8F5E9;
  --surface-db: #FAFBFC;
  --border: rgba(45,71,57,0.08);
  --border-2: rgba(45,71,57,0.15);
  --border-db: rgba(45,71,57,0.1);
  --accent: #7CB342;
  --accent-dim: rgba(124,179,66,0.13);
  --accent-glow: rgba(124,179,66,0.32);
  --accent-dark: #558B2F;
  --warn: #E2A76F;
  --warn-dim: rgba(226,167,111,0.14);
  --warn-dark: #B5712A;
  --danger: #E05858;
  --danger-dim: rgba(224,88,88,0.12);
  --danger-dark: #B03030;
  --dli-color: #5C9BD6;
  --dli-dim: rgba(92,155,214,0.14);
  --ok: #52A97A;
  --ok-dim: rgba(82,169,122,0.12);
  --text: #1E3328;
  --text-2: #2D4739;
  --muted: #5E8070;
  --muted2: #8EAD9D;
  --mono: 'JetBrains Mono', monospace;
  --r: 12px; --rs: 8px; --rx: 18px;
  --transition: 0.25s cubic-bezier(0.34,1.4,0.64,1);
  --sidebar-w: 320px;
  --header-h: 60px; --tab-h: 52px;
  --shadow-sm: 0 1px 4px rgba(30,51,40,0.06);
  --shadow-md: 0 4px 16px rgba(30,51,40,0.08);
  --shadow-lg: 0 8px 32px rgba(30,51,40,0.1);
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;overflow:hidden}}
body{{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);display:flex;flex-direction:column;}}
button{{font-family:inherit;cursor:pointer;border:none;background:none;color:inherit}}
input,select{{font-family:inherit;}}
select{{appearance:none;}}

/* ── HEADER ── */
#header{{
  height:var(--header-h);background:rgba(255,255,255,0.96);
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border-db);
  box-shadow:0 1px 0 rgba(255,255,255,0.8),var(--shadow-sm);
  display:flex;align-items:center;padding:0 20px;gap:10px;flex-shrink:0;z-index:200;
}}
.logo{{font-family:'Syne',sans-serif;font-weight:800;font-size:17px;color:var(--accent-dark);letter-spacing:-.4px;display:flex;align-items:center;gap:8px;}}
.logo-pip{{width:8px;height:8px;border-radius:50%;background:var(--accent);box-shadow:0 0 8px var(--accent-glow);}}
.header-divider{{width:1px;height:20px;background:var(--border-2);margin:0 4px;}}
.header-meta{{display:flex;align-items:center;gap:10px;margin-left:auto}}
.sun-chip{{
  display:flex;align-items:center;gap:7px;font-size:12px;font-weight:600;color:var(--text-2);
  background:var(--surface-solid);border:1px solid var(--border-db);border-radius:99px;
  padding:5px 14px;box-shadow:var(--shadow-sm);
}}
.sun-dot{{width:7px;height:7px;border-radius:50%;background:var(--warn);box-shadow:0 0 8px var(--warn);flex-shrink:0}}
.sync-chip{{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:600;color:var(--muted);padding:5px 12px;border:1px solid var(--border);border-radius:99px;background:var(--surface-solid);box-shadow:var(--shadow-sm);}}
.sync-dot{{width:7px;height:7px;border-radius:50%;background:var(--muted2);transition:background .4s,box-shadow .4s}}
.sync-dot.ok{{background:var(--accent);box-shadow:0 0 8px var(--accent)}}
.sync-dot.syncing{{background:var(--warn);box-shadow:0 0 8px var(--warn);animation:blink 1s infinite;}}
.sync-dot.error{{background:var(--danger);}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}

/* ── TABS ── */
#tabs{{
  height:var(--tab-h);background:transparent;
  display:flex;align-items:center;padding:0 20px;gap:6px;flex-shrink:0;z-index:150;
  border-bottom:1px solid var(--border);
  background:rgba(255,255,255,0.6);backdrop-filter:blur(10px);
}}
.tab{{
  padding:8px 20px;font-size:13px;font-weight:600;color:var(--muted);
  border-radius:var(--rs);cursor:pointer;border:1px solid transparent;
  transition:all .2s ease;position:relative;
}}
.tab:hover{{color:var(--text-2);background:rgba(255,255,255,0.7);}}
.tab.active{{color:var(--accent-dark);background:var(--surface-solid);border-color:var(--border-db);box-shadow:var(--shadow-sm);}}
.tab.active::after{{content:'';position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:24px;height:2px;background:var(--accent);border-radius:2px 2px 0 0;}}
.tab-badge{{
  display:inline-flex;align-items:center;justify-content:center;
  min-width:18px;height:18px;padding:0 5px;margin-left:6px;
  font-size:10px;font-weight:700;border-radius:99px;
  background:var(--danger);color:#fff;
}}

/* ── MAIN ── */
#main{{display:flex;flex:1;overflow:hidden;position:relative;gap:0;}}

/* ── SIDEBARS ── */
#left-sidebar{{
  width:var(--sidebar-w);background:rgba(255,255,255,0.97);
  border-right:1px solid var(--border-db);
  display:flex;flex-direction:column;overflow:hidden;flex-shrink:0;
  box-shadow:1px 0 0 rgba(255,255,255,0.5);
}}
#right-sidebar{{
  width:var(--sidebar-w);background:rgba(255,255,255,0.97);
  border-left:1px solid var(--border-db);
  display:flex;flex-direction:column;overflow:hidden;flex-shrink:0;
}}
#left-sidebar.hidden,#right-sidebar.hidden{{display:none}}

.sidebar-header{{
  padding:16px 16px 12px;font-family:'Syne',sans-serif;font-weight:700;font-size:12px;
  color:var(--muted);letter-spacing:.08em;text-transform:uppercase;
  border-bottom:1px solid var(--border);flex-shrink:0;display:flex;align-items:center;gap:8px;
}}
.sidebar-header span{{flex:1}}
.inv-search{{
  margin:10px 12px;padding:8px 14px;background:var(--surface-db);border:1px solid var(--border-db);
  border-radius:var(--rs);color:var(--text);font-size:13px;width:calc(100% - 24px);
  transition:border-color .2s,box-shadow .2s;
}}
.inv-search::placeholder{{color:var(--muted2)}}
.inv-search:focus{{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);}}
.inv-group{{padding:8px 0 2px}}
.inv-group-label{{
  padding:3px 16px 6px;font-size:10px;font-weight:700;color:var(--muted2);
  text-transform:uppercase;letter-spacing:.1em;
}}
.inv-item{{
  display:flex;align-items:center;gap:10px;padding:8px 16px;cursor:pointer;
  transition:background .15s;user-select:none;border-left:2px solid transparent;
}}
.inv-item:hover{{background:var(--surface-db);}}
.inv-item.dragging-source{{opacity:.35;}}
.inv-item.selected{{background:var(--accent-dim);border-left-color:var(--accent);}}
.inv-item.placed-elsewhere{{opacity:.55}}
.inv-emoji{{font-size:18px;width:26px;text-align:center;background:var(--surface-2);border-radius:6px;padding:3px;flex-shrink:0;}}
.inv-name{{font-size:13px;font-weight:500;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.inv-badge{{font-size:10px;padding:3px 8px;border-radius:99px;font-weight:600;background:var(--surface-2);color:var(--muted);white-space:nowrap}}
.inv-badge.placed-badge{{background:var(--accent-dim);border:1px solid var(--accent-glow);color:var(--accent-dark)}}
.inv-floor-switcher{{
  margin:auto 12px 12px;padding:4px;
  background:var(--surface-db);border:1px solid var(--border-db);border-radius:var(--r);
  display:flex;gap:3px;flex-shrink:0;
}}
.floor-btn{{flex:1;padding:8px 6px;font-size:12px;font-weight:700;border-radius:var(--rs);transition:all .2s;color:var(--muted)}}
.floor-btn:hover{{background:var(--surface-solid);color:var(--text);}}
.floor-btn.active{{background:var(--accent);color:#fff;box-shadow:0 2px 8px var(--accent-glow);}}

/* ── MAP AREA ── */
#map-area{{
  flex:1;position:relative;overflow:hidden;
  background:radial-gradient(ellipse at 50% 50%,rgba(124,179,66,.04) 0%,transparent 70%);
}}
#map-canvas{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);border-radius:10px;}}
#floor-img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;pointer-events:none;user-select:none;opacity:0.95;}}
#light-canvas{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:.6;mix-blend-mode:multiply;}}
#map-canvas.drag-over{{outline:2px dashed var(--accent);outline-offset:6px;border-radius:12px;background:rgba(124,179,66,0.04);}}

.map-controls{{
  position:absolute;top:14px;right:14px;z-index:100;
  display:flex;gap:8px;align-items:center;
}}
.map-ctrl-btn{{
  background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);
  border:1px solid var(--border-db);border-radius:var(--rs);
  padding:6px 12px;font-size:11px;font-weight:700;color:var(--muted);
  cursor:pointer;transition:all .2s;box-shadow:var(--shadow-sm);display:flex;align-items:center;gap:6px;
}}
.map-ctrl-btn:hover{{color:var(--text);background:rgba(255,255,255,1);}}
.map-ctrl-btn.active{{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 2px 8px var(--accent-glow);}}
.toggle-knob{{width:28px;height:16px;border-radius:8px;background:var(--muted2);position:relative;transition:background .2s;display:inline-block;}}
.toggle-knob.on{{background:var(--accent);}}
.toggle-knob::after{{content:'';position:absolute;top:2px;left:2px;width:12px;height:12px;border-radius:50%;background:#fff;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.2);}}
.toggle-knob.on::after{{transform:translateX(12px);}}

/* ── PLANT PINS ── */
.plant-pin{{position:absolute;display:flex;flex-direction:column;align-items:center;cursor:grab;user-select:none;touch-action:none;z-index:10;}}
.plant-pin:hover{{z-index:50;}}
.plant-pin.dragging{{cursor:grabbing;z-index:100;}}
.plant-pin.active .pin-bubble{{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim),var(--shadow-md);transform:scale(1.12);}}
.plant-pin.highlight-pulse .pin-bubble{{animation:hPulse 1.5s ease-in-out 3}}
@keyframes hPulse{{0%,100%{{box-shadow:0 0 0 0 var(--accent-glow)}}50%{{box-shadow:0 0 0 12px rgba(124,179,66,0)}}}}
.pin-bubble{{width:42px;height:42px;border-radius:50%;background:rgba(255,255,255,0.95);border:2px solid var(--accent-glow);display:flex;align-items:center;justify-content:center;font-size:20px;transition:all .3s cubic-bezier(.34,1.4,.64,1);box-shadow:var(--shadow-md);}}
.plant-pin:hover .pin-bubble{{transform:scale(1.15);box-shadow:0 6px 20px rgba(124,179,66,0.22);border-color:var(--accent);}}
.plant-pin.dragging .pin-bubble{{transform:scale(1.08) translateY(-4px);box-shadow:0 10px 26px rgba(124,179,66,0.28);}}
.pin-indicator{{width:8px;height:8px;border-radius:50%;margin-top:4px;background:var(--muted2);border:2px solid #fff;transition:background .3s;}}
.pin-indicator.ideal{{background:var(--accent);box-shadow:0 0 6px var(--accent)}}
.pin-indicator.ok{{background:var(--warn);box-shadow:0 0 6px var(--warn)}}
.pin-indicator.bad{{background:var(--danger);box-shadow:0 0 6px var(--danger)}}
.pin-label{{font-size:10px;font-weight:700;color:var(--text);margin-top:3px;white-space:nowrap;max-width:70px;overflow:hidden;text-overflow:ellipsis;text-align:center;background:rgba(255,255,255,0.88);padding:2px 7px;border-radius:6px;box-shadow:var(--shadow-sm);}}
.pin-light-badge{{font-size:9px;font-weight:700;padding:1px 7px;border-radius:99px;margin-top:2px;background:rgba(255,255,255,0.9);color:var(--muted);font-family:var(--mono);}}

/* ── RIGHT SIDEBAR ── */
#rsb-empty{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;color:var(--muted);padding:28px;text-align:center}}
#rsb-empty .empty-icon{{font-size:48px;opacity:.4;}}
#rsb-detail{{flex:1;display:none;flex-direction:column;overflow-y:auto;padding:0;}}
#rsb-detail.visible{{display:flex}}
#rsb-detail::-webkit-scrollbar{{width:4px}}
#rsb-detail::-webkit-scrollbar-thumb{{background:var(--border-2);border-radius:2px}}

.detail-img-wrap{{width:100%;height:140px;overflow:hidden;position:relative;background:var(--surface-2);flex-shrink:0;}}
.detail-img-wrap img{{width:100%;height:100%;object-fit:cover;}}
.detail-img-fallback{{width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:56px;opacity:.3;}}
.detail-body{{padding:18px;display:flex;flex-direction:column;gap:16px;}}

.plant-hdr{{display:flex;align-items:flex-start;gap:12px;}}
.big-emoji{{font-size:36px;flex-shrink:0;line-height:1;background:var(--surface-db);padding:10px;border-radius:var(--rs);border:1px solid var(--border);}}
.plant-hdr-text h2{{font-family:'Syne',sans-serif;font-size:19px;font-weight:700;line-height:1.2;color:var(--text);}}
.plant-hdr-text .botanical{{font-size:11px;color:var(--muted);font-style:italic;margin-top:2px;}}
.floor-tag{{display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:99px;font-size:10px;font-weight:700;background:var(--surface-db);color:var(--muted);margin-top:7px;border:1px solid var(--border);}}

/* DLI Panel */
.dli-panel{{background:linear-gradient(135deg,rgba(92,155,214,0.07),rgba(124,179,66,0.05));border:1px solid rgba(92,155,214,0.2);border-radius:var(--r);padding:14px;}}
.dli-panel-title{{font-size:10px;font-weight:700;color:var(--dli-color);text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;}}
.dli-score-row{{display:flex;align-items:baseline;gap:6px;margin-bottom:10px;}}
.dli-score-val{{font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:var(--text);}}
.dli-score-unit{{font-size:12px;color:var(--muted);}}
.dli-bar-track{{height:6px;border-radius:3px;background:rgba(45,71,57,0.08);overflow:hidden;margin-bottom:6px;}}
.dli-bar-fill{{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--dli-dim),var(--dli-color));transition:width .8s cubic-bezier(.34,1.4,.64,1);}}
.dli-live-row{{display:flex;align-items:center;gap:6px;padding:6px 10px;background:rgba(255,255,255,0.65);border-radius:var(--rs);border:1px solid var(--border);}}
.dli-live-dot{{width:5px;height:5px;border-radius:50%;background:var(--warn);animation:blink 2s infinite;flex-shrink:0;}}
.dli-live-text{{font-size:11px;font-weight:600;color:var(--text);flex:1;}}

/* Score badge */
.score-badge{{border-radius:var(--r);padding:12px 14px;display:flex;align-items:center;gap:12px;background:var(--surface-solid);border:1px solid var(--border);}}
.score-badge .sc-icon{{font-size:24px}}
.score-badge .sc-text h3{{font-family:'Syne',sans-serif;font-size:14px;font-weight:700}}
.score-badge .sc-text p{{font-size:12px;color:var(--muted);margin-top:2px;line-height:1.4}}
.score-badge.ideal{{border-color:var(--accent-glow);background:rgba(124,179,66,0.04);}}
.score-badge.ideal .sc-text h3{{color:var(--accent-dark)}}
.score-badge.ok{{border-color:rgba(226,167,111,0.4);}}
.score-badge.ok .sc-text h3{{color:var(--warn-dark)}}
.score-badge.bad{{border-color:rgba(224,88,88,0.3);}}
.score-badge.bad .sc-text h3{{color:var(--danger-dark)}}

.light-bar-wrap{{display:flex;flex-direction:column;gap:8px;background:var(--surface-db);padding:12px;border-radius:var(--r);border:1px solid var(--border);}}
.lbw-label{{display:flex;justify-content:space-between;font-size:12px;font-weight:600;color:var(--text)}}
.lbw-track{{height:10px;border-radius:5px;background:rgba(45,71,57,0.06);position:relative;overflow:hidden}}
.lbw-fill{{height:100%;border-radius:5px;background:linear-gradient(90deg,var(--accent-glow),var(--accent));transition:width .6s cubic-bezier(.34,1.4,.64,1)}}
.lbw-needle{{position:absolute;top:-2px;bottom:-2px;width:3px;background:#fff;border-radius:2px;box-shadow:0 0 3px rgba(0,0,0,.2);}}

.astro-panel{{background:var(--surface-db);border:1px solid var(--border);border-radius:var(--r);padding:12px;}}
.astro-title{{font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px}}
.astro-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;}}
.astro-cell{{background:var(--surface-solid);border-radius:var(--rs);padding:10px;border:1px solid var(--border);}}
.astro-cell-lbl{{font-size:9px;font-weight:700;color:var(--muted2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px}}
.astro-cell-val{{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:var(--text)}}
.astro-cell-unit{{font-size:11px;color:var(--muted);margin-left:2px}}
.window-chips{{display:flex;gap:5px;flex-wrap:wrap}}
.win-chip{{font-size:10px;font-weight:600;padding:3px 8px;border-radius:99px;background:var(--surface-db);border:1px solid var(--border);color:var(--muted);}}
.win-chip.hit{{background:var(--warn-dim);border-color:rgba(226,167,111,.4);color:var(--warn-dark);}}

.data-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.dc{{background:var(--surface-db);border:1px solid var(--border);border-radius:var(--rs);padding:12px;}}
.dc-lbl{{font-size:9px;font-weight:700;color:var(--muted2);text-transform:uppercase;letter-spacing:.07em;margin-bottom:4px}}
.dc-val{{font-family:'Syne',sans-serif;font-size:19px;font-weight:700;color:var(--text)}}
.dc-unit{{font-size:11px;color:var(--muted);margin-left:3px}}
.detail-extra-row{{background:var(--surface-db);border:1px solid var(--border);border-radius:var(--rs);padding:10px 12px;}}
.detail-extra-lbl{{font-size:9px;font-weight:700;color:var(--muted2);text-transform:uppercase;letter-spacing:.07em;margin-bottom:3px}}
.detail-extra-val{{font-size:12px;font-weight:500;color:var(--text);line-height:1.5;}}
.action-row{{display:flex;gap:8px;}}
.act-btn{{flex:1;padding:10px;border-radius:var(--rs);font-size:12px;font-weight:700;transition:all .2s;border:1px solid var(--border);background:var(--surface-db);color:var(--text);}}
.act-btn:hover{{background:var(--surface-solid);box-shadow:var(--shadow-sm);transform:translateY(-1px);}}
.act-btn.primary{{background:var(--accent);border-color:var(--accent);color:#fff;}}
.act-btn.primary:hover{{background:var(--accent-dark);box-shadow:0 3px 10px var(--accent-glow);}}
.act-btn.danger-btn{{border-color:rgba(224,88,88,0.3);color:var(--danger-dark)}}
.act-btn.danger-btn:hover{{background:var(--danger-dim);}}

/* ── LIBRARY VIEW ── */
#library-view{{display:none;flex:1;overflow:hidden;flex-direction:column;}}
#library-view.active{{display:flex}}

/* Library toolbar */
.lib-toolbar{{
  display:flex;align-items:center;gap:10px;padding:14px 20px;
  background:rgba(255,255,255,0.97);border-bottom:1px solid var(--border-db);
  flex-shrink:0;flex-wrap:wrap;box-shadow:var(--shadow-sm);
}}
.lib-toolbar-title{{font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:var(--text);flex-shrink:0;}}
.lib-toolbar-sub{{font-size:12px;color:var(--muted);margin-left:2px;}}
.lib-toolbar-spacer{{flex:1;}}
.lib-search-wrap{{position:relative;flex-shrink:0;}}
.lib-search-wrap::before{{content:'🔍';position:absolute;left:12px;top:50%;transform:translateY(-50%);font-size:13px;pointer-events:none;}}
.lib-search{{
  padding:8px 14px 8px 34px;background:var(--surface-db);border:1px solid var(--border-db);
  border-radius:var(--rs);color:var(--text);font-size:13px;width:220px;
  transition:all .2s;
}}
.lib-search::placeholder{{color:var(--muted2)}}
.lib-search:focus{{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);width:260px;}}

/* Filter bar */
.lib-filter-bar{{
  display:flex;align-items:center;gap:8px;padding:10px 20px;
  background:var(--surface-db);border-bottom:1px solid var(--border);flex-shrink:0;flex-wrap:wrap;
}}
.filter-label{{font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;flex-shrink:0;}}
.filter-select-wrap{{position:relative;}}
.filter-select-wrap::after{{content:'▾';position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:10px;color:var(--muted);pointer-events:none;}}
.filter-select{{
  padding:6px 28px 6px 11px;background:var(--surface-solid);border:1px solid var(--border-db);
  border-radius:var(--rs);color:var(--text);font-size:12px;font-weight:600;
  cursor:pointer;transition:all .2s;min-width:130px;
}}
.filter-select:focus{{outline:none;border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-dim);}}
.filter-select:hover{{border-color:var(--accent-glow);}}

.sort-bar{{display:flex;align-items:center;gap:6px;margin-left:auto;}}
.sort-btn{{
  padding:5px 12px;font-size:11px;font-weight:700;border-radius:var(--rs);
  border:1px solid var(--border-db);background:var(--surface-solid);color:var(--muted);
  cursor:pointer;transition:all .2s;display:flex;align-items:center;gap:4px;
}}
.sort-btn:hover{{color:var(--text);border-color:var(--accent-glow);}}
.sort-btn.active{{background:var(--accent-dim);border-color:var(--accent-glow);color:var(--accent-dark);}}
.sort-arrow{{font-size:9px;transition:transform .2s;}}

.filter-chip{{
  display:flex;align-items:center;gap:5px;padding:4px 10px;border-radius:99px;
  font-size:11px;font-weight:700;background:var(--accent-dim);border:1px solid var(--accent-glow);
  color:var(--accent-dark);cursor:pointer;
}}
.filter-chip:hover{{background:rgba(124,179,66,.22);}}
.filter-chip-x{{font-size:13px;line-height:1;margin-left:2px;}}

.lib-results-bar{{
  padding:8px 20px;font-size:11px;font-weight:600;color:var(--muted);
  background:var(--surface-db);border-bottom:1px solid var(--border);flex-shrink:0;
  display:flex;align-items:center;gap:12px;
}}

/* Library grid */
.lib-grid-wrap{{flex:1;overflow-y:auto;padding:20px;}}
.lib-grid-wrap::-webkit-scrollbar{{width:6px}}
.lib-grid-wrap::-webkit-scrollbar-thumb{{background:var(--border-2);border-radius:3px}}
.lib-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;}}

/* Premium Library Card */
.lib-card{{
  background:var(--surface-solid);border:1px solid var(--border-db);border-radius:var(--rx);
  display:flex;flex-direction:column;overflow:hidden;
  transition:all .22s ease;cursor:default;
  box-shadow:var(--shadow-sm);
}}
.lib-card:hover{{border-color:var(--accent-glow);box-shadow:var(--shadow-lg);transform:translateY(-3px);}}
.lib-card-img{{width:100%;height:160px;overflow:hidden;position:relative;background:var(--surface-2);flex-shrink:0;}}
.lib-card-img img{{width:100%;height:100%;object-fit:cover;transition:transform .5s ease;}}
.lib-card:hover .lib-card-img img{{transform:scale(1.05);}}
.lib-card-img-fallback{{width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:64px;opacity:.3;}}
.lib-card-img-overlay{{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(to top,rgba(30,51,40,.65),transparent);padding:14px;}}
.lib-card-name{{font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.3);}}
.lib-card-botanical{{font-size:11px;color:rgba(255,255,255,.72);font-style:italic;margin-top:1px;}}
.lib-card-body{{padding:14px 16px;display:flex;flex-direction:column;gap:12px;flex:1;}}
.lib-card-row1{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}}
.lib-card-loc{{display:flex;align-items:center;gap:5px;font-size:11px;font-weight:600;color:var(--muted);margin-left:auto;}}
.lib-card-loc-dot{{width:5px;height:5px;border-radius:50%;background:var(--muted2);flex-shrink:0}}
.lib-card-loc-dot.placed{{background:var(--accent);box-shadow:0 0 5px var(--accent);}}
.lib-status-chip{{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:99px;font-size:11px;font-weight:700;}}
.lib-status-chip.ideal{{background:var(--accent-dim);color:var(--accent-dark);border:1px solid var(--accent-glow);}}
.lib-status-chip.ok{{background:var(--warn-dim);color:var(--warn-dark);border:1px solid rgba(226,167,111,.35);}}
.lib-status-chip.bad{{background:var(--danger-dim);color:var(--danger-dark);border:1px solid rgba(224,88,88,.3);}}
.lib-status-chip.none{{background:var(--surface-db);color:var(--muted);border:1px solid var(--border)}}

/* Metric row */
.lib-metrics{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;}}
.lib-metric{{background:var(--surface-db);border:1px solid var(--border);border-radius:var(--rs);padding:8px 10px;}}
.lib-metric-lbl{{font-size:9px;font-weight:700;color:var(--muted2);text-transform:uppercase;letter-spacing:.07em;margin-bottom:2px;}}
.lib-metric-val{{font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:var(--text);}}
.lib-metric-unit{{font-size:10px;color:var(--muted);}}

/* Light bar */
.lib-light-bar-wrap{{display:flex;flex-direction:column;gap:4px;}}
.lib-light-header{{display:flex;justify-content:space-between;font-size:11px;font-weight:600;color:var(--muted);}}
.lib-light-track{{height:6px;border-radius:3px;background:rgba(45,71,57,0.07);overflow:hidden;position:relative;}}
.lib-light-fill{{height:100%;border-radius:3px;transition:width .6s cubic-bezier(.34,1.4,.64,1)}}
.lib-light-score{{font-family:'Syne',sans-serif;font-size:13px;font-weight:700;}}

/* Besonderheit */
.lib-besonderheit{{border-left:2px solid var(--accent-glow);padding:6px 10px;font-size:12px;color:var(--muted);line-height:1.5;background:var(--surface-db);border-radius:0 var(--rs) var(--rs) 0;}}
.lib-besonderheit strong{{font-size:9px;font-weight:700;color:var(--accent-dark);text-transform:uppercase;letter-spacing:.07em;display:block;margin-bottom:2px;}}

.lib-card-footer{{padding:0 16px 14px;}}
.show-on-map-btn{{
  width:100%;padding:9px;border-radius:var(--rs);font-size:12px;font-weight:700;
  background:var(--surface-db);border:1px solid var(--border-db);color:var(--text);
  transition:all .2s;
}}
.show-on-map-btn:hover{{background:var(--accent-dim);border-color:var(--accent-glow);color:var(--accent-dark);}}

/* ── CARE VIEW — DATABASE DASHBOARD ── */
#care-view{{display:none;flex:1;overflow:hidden;flex-direction:column;}}
#care-view.active{{display:flex}}

/* Care toolbar */
.care-toolbar{{
  display:flex;align-items:center;gap:12px;padding:14px 20px;
  background:rgba(255,255,255,0.97);border-bottom:1px solid var(--border-db);
  flex-shrink:0;flex-wrap:wrap;box-shadow:var(--shadow-sm);
}}
.care-toolbar-title{{font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:var(--text);}}
.care-kpi-bar{{display:flex;gap:8px;margin-left:auto;flex-wrap:wrap;}}
.care-kpi{{
  display:flex;align-items:center;gap:6px;padding:5px 12px;
  border-radius:var(--rs);font-size:11px;font-weight:700;
  border:1px solid var(--border);background:var(--surface-db);cursor:pointer;
  transition:all .2s;
}}
.care-kpi:hover{{box-shadow:var(--shadow-sm);}}
.care-kpi.kpi-overdue{{background:var(--danger-dim);border-color:rgba(224,88,88,.25);color:var(--danger-dark);}}
.care-kpi.kpi-today{{background:var(--warn-dim);border-color:rgba(226,167,111,.3);color:var(--warn-dark);}}
.care-kpi.kpi-soon{{background:var(--surface-2);border-color:var(--accent-glow);color:var(--accent-dark);}}
.care-kpi.kpi-ok{{background:var(--ok-dim);border-color:rgba(82,169,122,.25);color:#267a50;}}
.care-kpi-num{{font-family:'Syne',sans-serif;font-size:16px;font-weight:800;}}
.care-action-btn{{
  padding:8px 16px;font-size:12px;font-weight:700;border-radius:var(--rs);
  border:1px solid var(--border-db);background:var(--surface-solid);color:var(--text);
  transition:all .2s;box-shadow:var(--shadow-sm);
}}
.care-action-btn:hover{{background:var(--surface-db);}}
.care-action-btn.primary{{background:var(--accent);border-color:var(--accent);color:#fff;}}
.care-action-btn.primary:hover{{background:var(--accent-dark);box-shadow:0 2px 8px var(--accent-glow);}}

/* Care sub-nav */
.care-subnav{{
  display:flex;align-items:center;gap:0;padding:0 20px;
  border-bottom:1px solid var(--border-db);flex-shrink:0;
  background:rgba(255,255,255,0.9);
}}
.care-subnav-btn{{
  padding:10px 18px;font-size:12px;font-weight:700;color:var(--muted);
  border-bottom:2px solid transparent;cursor:pointer;transition:all .2s;
  display:flex;align-items:center;gap:6px;
}}
.care-subnav-btn:hover{{color:var(--text);}}
.care-subnav-btn.active{{color:var(--accent-dark);border-bottom-color:var(--accent);}}

/* Care panes */
.care-pane{{display:none;flex:1;overflow-y:auto;padding:20px;flex-direction:column;gap:14px;}}
.care-pane.active{{display:flex}}
.care-pane::-webkit-scrollbar{{width:6px}}
.care-pane::-webkit-scrollbar-thumb{{background:var(--border-2);border-radius:3px}}

/* Care section header */
.care-section-hdr{{
  display:flex;align-items:center;gap:10px;padding:0 0 8px;
  border-bottom:1px solid var(--border);margin-bottom:4px;flex-shrink:0;
}}
.care-section-title{{font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:var(--text);}}
.care-section-badge{{
  padding:2px 8px;border-radius:99px;font-size:10px;font-weight:700;
  background:var(--danger-dim);color:var(--danger-dark);border:1px solid rgba(224,88,88,.2);
}}
.care-section-badge.warn{{background:var(--warn-dim);color:var(--warn-dark);border-color:rgba(226,167,111,.3);}}
.care-section-badge.ok{{background:var(--ok-dim);color:#267a50;border-color:rgba(82,169,122,.25);}}

/* Care table */
.care-table{{
  background:var(--surface-solid);border:1px solid var(--border-db);border-radius:var(--r);
  overflow:hidden;box-shadow:var(--shadow-sm);
}}
.care-table-head{{
  display:grid;grid-template-columns:2fr 1.2fr 1.2fr 1fr 1fr auto;
  gap:0;background:var(--surface-db);border-bottom:1px solid var(--border-db);
}}
.care-table-head-cell{{
  padding:8px 14px;font-size:10px;font-weight:700;color:var(--muted2);
  text-transform:uppercase;letter-spacing:.08em;
}}
.care-row{{
  display:grid;grid-template-columns:2fr 1.2fr 1.2fr 1fr 1fr auto;
  gap:0;align-items:center;border-bottom:1px solid var(--border);
  transition:background .15s;
}}
.care-row:last-child{{border-bottom:none}}
.care-row:hover{{background:var(--surface-db);}}
.care-row.overdue{{background:rgba(224,88,88,.04);}}
.care-row.overdue:hover{{background:rgba(224,88,88,.07);}}
.care-row.today{{background:rgba(226,167,111,.05);}}
.care-row.today:hover{{background:rgba(226,167,111,.09);}}
.care-cell{{padding:10px 14px;font-size:13px;}}

/* Plant name cell */
.care-plant-cell{{display:flex;align-items:center;gap:10px;padding:10px 14px;}}
.care-thumb{{width:36px;height:36px;border-radius:var(--rs);overflow:hidden;flex-shrink:0;background:var(--surface-2);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;}}
.care-thumb img{{width:100%;height:100%;object-fit:cover;}}
.care-thumb-emoji{{font-size:18px;}}
.care-plant-name{{font-weight:600;font-size:13px;color:var(--text);}}
.care-plant-loc{{font-size:10px;color:var(--muted);margin-top:1px;}}

/* Progress ring */
.ring-wrap{{display:flex;align-items:center;justify-content:center;padding:8px 14px;}}
.ring-svg{{width:44px;height:44px;}}
.ring-bg{{fill:none;stroke:rgba(45,71,57,0.08);stroke-width:4;}}
.ring-fill{{fill:none;stroke-width:4;stroke-linecap:round;transform:rotate(-90deg);transform-origin:22px 22px;transition:stroke-dashoffset .8s cubic-bezier(.34,1.4,.64,1),stroke .4s;}}
.ring-text{{font-family:'Syne',sans-serif;font-size:10px;font-weight:700;fill:var(--text);text-anchor:middle;dominant-baseline:middle;}}

/* Status badge in table */
.care-status-badge{{
  display:inline-flex;align-items:center;gap:4px;padding:3px 8px;border-radius:99px;
  font-size:10px;font-weight:700;white-space:nowrap;
}}
.care-status-badge.overdue{{background:var(--danger-dim);color:var(--danger-dark);border:1px solid rgba(224,88,88,.25);}}
.care-status-badge.today{{background:var(--warn-dim);color:var(--warn-dark);border:1px solid rgba(226,167,111,.3);}}
.care-status-badge.soon{{background:var(--surface-2);color:var(--accent-dark);border:1px solid var(--accent-glow);}}
.care-status-badge.ok{{background:var(--ok-dim);color:#267a50;border:1px solid rgba(82,169,122,.25);}}

/* Action buttons in table */
.care-action-cell{{padding:6px 10px;display:flex;gap:5px;}}
.care-btn-water{{
  padding:5px 10px;font-size:11px;font-weight:700;border-radius:var(--rs);
  border:1px solid rgba(100,181,246,.4);color:#1565C0;background:rgba(100,181,246,.08);
  transition:all .2s;white-space:nowrap;
}}
.care-btn-water:hover{{background:rgba(100,181,246,.16);box-shadow:0 2px 6px rgba(100,181,246,.15);}}
.care-btn-water:active{{transform:scale(0.96);}}
.care-btn-fert{{
  padding:5px 10px;font-size:11px;font-weight:700;border-radius:var(--rs);
  border:1px solid var(--accent-glow);color:var(--accent-dark);background:var(--accent-dim);
  transition:all .2s;white-space:nowrap;
}}
.care-btn-fert:hover{{background:rgba(124,179,66,.22);box-shadow:0 2px 6px var(--accent-glow);}}
.care-btn-fert:active{{transform:scale(0.96);}}
.care-btn-syncing{{opacity:.6;pointer-events:none;}}

/* Calendar */
.calendar-wrap{{background:var(--surface-solid);border:1px solid var(--border-db);border-radius:var(--r);overflow:hidden;box-shadow:var(--shadow-sm);}}
.cal-nav{{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid var(--border);}}
.cal-nav-title{{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:var(--text);}}
.cal-nav-btn{{width:30px;height:30px;border-radius:50%;border:1px solid var(--border-db);background:var(--surface-db);color:var(--text);font-size:14px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all .2s;}}
.cal-nav-btn:hover{{background:var(--surface-solid);box-shadow:var(--shadow-sm);}}
.cal-grid{{display:grid;grid-template-columns:repeat(7,1fr);}}
.cal-day-hdr{{padding:8px;text-align:center;font-size:10px;font-weight:700;color:var(--muted2);text-transform:uppercase;letter-spacing:.06em;background:var(--surface-db);border-bottom:1px solid var(--border);}}
.cal-cell{{min-height:76px;padding:8px 6px;border-right:1px solid var(--border);border-bottom:1px solid var(--border);position:relative;transition:background .15s;}}
.cal-cell:nth-child(7n){{border-right:none;}}
.cal-cell:nth-last-child(-n+7){{border-bottom:none;}}
.cal-cell.other-month .cal-day-num{{color:var(--muted2);opacity:.4;}}
.cal-cell.today{{background:rgba(124,179,66,.04);}}
.cal-cell.today .cal-day-num{{background:var(--accent);color:#fff;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;box-shadow:0 1px 6px var(--accent-glow);}}
.cal-day-num{{font-size:12px;font-weight:600;color:var(--text);margin-bottom:4px;width:22px;height:22px;display:flex;align-items:center;justify-content:center;}}
.cal-events{{display:flex;flex-direction:column;gap:2px;}}
.cal-ev{{font-size:9px;font-weight:700;padding:1px 5px;border-radius:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.cal-ev.water{{background:rgba(100,181,246,.15);color:#1565C0;}}
.cal-ev.fertilize{{background:var(--accent-dim);color:var(--accent-dark);}}
.cal-ev.due-water{{background:rgba(100,181,246,.28);color:#1565C0;border:1px solid rgba(100,181,246,.4);}}
.cal-ev.due-fertilize{{background:rgba(124,179,66,.22);color:var(--accent-dark);border:1px solid var(--accent-glow);}}

/* History */
.history-list{{background:var(--surface-solid);border:1px solid var(--border-db);border-radius:var(--r);overflow:hidden;box-shadow:var(--shadow-sm);}}
.history-hdr{{padding:12px 16px;border-bottom:1px solid var(--border);font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:var(--text);display:flex;align-items:center;gap:8px;}}
.history-hdr-count{{font-family:'DM Sans',sans-serif;font-size:11px;color:var(--muted);font-weight:500;margin-left:auto;}}
.history-entry{{display:flex;align-items:center;gap:12px;padding:10px 16px;border-bottom:1px solid var(--border);font-size:12px;transition:background .15s;}}
.history-entry:last-child{{border-bottom:none}}
.history-entry:hover{{background:var(--surface-db);}}
.history-icon-wrap{{width:28px;height:28px;border-radius:var(--rs);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}}
.history-icon-wrap.water{{background:rgba(100,181,246,.12);}}
.history-icon-wrap.fertilize{{background:var(--accent-dim);}}
.history-text{{flex:1;font-weight:600;color:var(--text);}}
.history-time{{font-size:11px;color:var(--muted);font-family:var(--mono);}}
.history-sync-status{{font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;}}
.history-sync-status.synced{{background:var(--ok-dim);color:#267a50;}}
.history-sync-status.local{{background:var(--warn-dim);color:var(--warn-dark);}}

/* Care empty state */
.care-empty{{text-align:center;padding:40px 20px;color:var(--muted);background:var(--surface-solid);border:1px dashed var(--border-2);border-radius:var(--r);}}
.care-empty-icon{{font-size:40px;margin-bottom:10px;opacity:.4}}

/* ── TOAST & TOOLTIP ── */
#tooltip{{position:fixed;z-index:500;pointer-events:none;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border:1px solid var(--border-2);border-radius:var(--rs);padding:8px 12px;font-size:11px;font-weight:600;color:var(--text);box-shadow:var(--shadow-md);opacity:0;transition:opacity .12s;max-width:220px;}}
#tooltip.visible{{opacity:1}}
#save-toast{{position:fixed;bottom:20px;right:20px;z-index:999;background:var(--surface-solid);border:1px solid var(--border-db);border-radius:var(--r);padding:12px 18px;font-size:13px;font-weight:600;color:var(--text);box-shadow:var(--shadow-lg);transform:translateY(24px);opacity:0;transition:all .35s cubic-bezier(.34,1.4,.64,1);display:flex;align-items:center;gap:8px;min-width:200px;}}
#save-toast.show{{transform:translateY(0);opacity:1}}
#save-toast.error-toast{{border-color:rgba(224,88,88,.3);background:var(--danger-dim);color:var(--danger-dark);}}

/* ── LOADING ── */
#loading{{position:fixed;inset:0;z-index:9999;background:var(--bg);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;transition:opacity .5s,visibility .5s;}}
#loading.hidden{{opacity:0;visibility:hidden}}
#loading .ld-icon{{font-size:48px;animation:pulse 2s ease-in-out infinite}}
#loading p{{font-size:14px;font-weight:600;color:var(--muted)}}
@keyframes pulse{{0%,100%{{transform:scale(1);opacity:.6}}50%{{transform:scale(1.08);opacity:1}}}}
</style>
</head>
<body>

<div id="loading"><div class="ld-icon">🌿</div><p>Pflanzen-Datenbank wird geladen…</p></div>
<div id="tooltip"></div>
<div id="save-toast" id="save-toast"><span id="toast-icon">💾</span><span id="toast-msg">Gespeichert</span></div>

<!-- HEADER -->
<div id="header">
  <div class="logo"><div class="logo-pip"></div>Pflanzen-Planer Pro</div>
  <span style="font-size:11px;font-weight:600;color:var(--muted)" id="month-label"></span>
  <div class="header-meta">
    <div class="sun-chip"><div class="sun-dot"></div><span id="sun-label">Berechne Sonnenstand…</span></div>
    <div class="sync-chip"><div class="sync-dot" id="sdot"></div><span id="stext">Verbinden…</span></div>
  </div>
</div>

<!-- TABS -->
<div id="tabs">
  <button class="tab active" data-tab="planer" onclick="switchTab('planer')">🗺️ Grundriss-Planer</button>
  <button class="tab" data-tab="library" onclick="switchTab('library')">📚 Pflanzenbibliothek</button>
  <button class="tab" data-tab="care" onclick="switchTab('care')">🌱 Pflege-Dashboard <span class="tab-badge" id="care-badge" style="display:none">0</span></button>
</div>

<!-- MAIN -->
<div id="main">

  <!-- LEFT SIDEBAR -->
  <div id="left-sidebar">
    <div class="sidebar-header"><span>🪴 Inventar</span><span id="inv-count" style="font-size:10px;background:var(--surface-2);padding:2px 8px;border-radius:99px;font-weight:700;color:var(--muted)"></span></div>
    <input class="inv-search" id="inv-search" type="text" placeholder="Suchen…" oninput="filterInventory(this.value)">
    <div id="inv-list" style="flex:1;overflow-y:auto"></div>
    <div class="inv-floor-switcher">
      <button class="floor-btn active" onclick="setFloor('EG')" id="fbtn-EG">EG</button>
      <button class="floor-btn" onclick="setFloor('1. OG')" id="fbtn-1. OG">1.OG</button>
      <button class="floor-btn" onclick="setFloor('2. OG')" id="fbtn-2. OG">2.OG</button>
    </div>
  </div>

  <!-- MAP AREA -->
  <div id="map-area">
    <div class="map-controls">
      <button class="map-ctrl-btn" id="dli-btn" onclick="toggleDLIMode()">
        <span class="toggle-knob" id="dli-knob"></span>
        DLI-Modus
      </button>
    </div>
    <div id="map-canvas">
      <img id="floor-img" src="" alt="Grundriss" draggable="false"
           onerror="this.src='https://placehold.co/1100x600/F8F7F4/7CB342?text=Grundriss+nicht+gefunden'">
      <canvas id="light-canvas"></canvas>
    </div>
  </div>

  <!-- LIBRARY VIEW -->
  <div id="library-view">
    <div class="lib-toolbar">
      <div>
        <div class="lib-toolbar-title">📚 Pflanzenbibliothek</div>
        <div class="lib-toolbar-sub" id="lib-sub-label"></div>
      </div>
      <div class="lib-toolbar-spacer"></div>
      <div class="lib-search-wrap">
        <input class="lib-search" id="lib-search" type="text" placeholder="Pflanze suchen…" oninput="onLibFilterChange()">
      </div>
    </div>
    <div class="lib-filter-bar">
      <span class="filter-label">Filter:</span>

      <div class="filter-select-wrap">
        <select class="filter-select" id="filter-licht" onchange="onLibFilterChange()">
          <option value="">☀️ Lichtbedarf</option>
          <option value="low">🌑 Wenig (1–4)</option>
          <option value="mid">⛅ Mittel (5–7)</option>
          <option value="high">☀️ Viel (8–10)</option>
        </select>
      </div>

      <div class="filter-select-wrap">
        <select class="filter-select" id="filter-giess" onchange="onLibFilterChange()">
          <option value="">💧 Gießhäufigkeit</option>
          <option value="rare">🌵 Selten (>10 Tage)</option>
          <option value="normal">🌿 Normal (4–10 Tage)</option>
          <option value="frequent">💧 Häufig (1–3 Tage)</option>
        </select>
      </div>

      <div class="filter-select-wrap">
        <select class="filter-select" id="filter-placement" onchange="onLibFilterChange()">
          <option value="">📍 Platzierung</option>
          <option value="placed">Platziert</option>
          <option value="unplaced">Im Inventar</option>
        </select>
      </div>

      <div id="active-chips" style="display:flex;gap:6px;flex-wrap:wrap;"></div>

      <div class="sort-bar">
        <span class="filter-label">Sort:</span>
        <button class="sort-btn active" id="sort-name" onclick="setSort('name')">Name <span class="sort-arrow" id="arr-name">↑</span></button>
        <button class="sort-btn" id="sort-licht" onclick="setSort('licht')">Licht <span class="sort-arrow" id="arr-licht">↑</span></button>
        <button class="sort-btn" id="sort-giess" onclick="setSort('giess')">Gießen <span class="sort-arrow" id="arr-giess">↑</span></button>
      </div>
    </div>
    <div class="lib-results-bar" id="lib-results-bar">Lädt…</div>
    <div class="lib-grid-wrap"><div class="lib-grid" id="lib-grid"></div></div>
  </div>

  <!-- CARE VIEW -->
  <div id="care-view">
    <div class="care-toolbar">
      <div class="care-toolbar-title">🌱 Pflege-Dashboard</div>
      <div class="care-kpi-bar">
        <div class="care-kpi kpi-overdue" onclick="switchCarePane('tasks')" id="kpi-overdue"><span class="care-kpi-num" id="kpi-overdue-n">0</span> Überfällig</div>
        <div class="care-kpi kpi-today" onclick="switchCarePane('tasks')" id="kpi-today"><span class="care-kpi-num" id="kpi-today-n">0</span> Heute</div>
        <div class="care-kpi kpi-soon" onclick="switchCarePane('tasks')" id="kpi-soon"><span class="care-kpi-num" id="kpi-soon-n">0</span> Diese Woche</div>
        <div class="care-kpi kpi-ok" onclick="switchCarePane('tasks')" id="kpi-ok"><span class="care-kpi-num" id="kpi-ok-n">0</span> Versorgt</div>
      </div>
      <div style="display:flex;gap:8px;margin-left:8px;">
        <button class="care-action-btn" onclick="waterAllDue()">💧 Alle fälligen gießen</button>
        <button class="care-action-btn primary" onclick="syncCareFromSheets()">🔄 Sync</button>
      </div>
    </div>

    <div class="care-subnav">
      <button class="care-subnav-btn active" id="subnav-tasks" onclick="switchCarePane('tasks')">📋 Fällige Aufgaben</button>
      <button class="care-subnav-btn" id="subnav-calendar" onclick="switchCarePane('calendar')">📅 Kalender</button>
      <button class="care-subnav-btn" id="subnav-history" onclick="switchCarePane('history')">🕐 Pflege-Historie</button>
    </div>

    <!-- Tasks pane -->
    <div class="care-pane active" id="care-pane-tasks">
      <div id="care-overdue-block"></div>
      <div id="care-today-block"></div>
      <div id="care-soon-block"></div>
      <div id="care-ok-block"></div>
    </div>

    <!-- Calendar pane -->
    <div class="care-pane" id="care-pane-calendar">
      <div class="calendar-wrap">
        <div class="cal-nav">
          <button class="cal-nav-btn" onclick="changeCalMonth(-1)">‹</button>
          <span class="cal-nav-title" id="cal-month-title"></span>
          <button class="cal-nav-btn" onclick="changeCalMonth(1)">›</button>
        </div>
        <div class="cal-grid" id="cal-grid"></div>
      </div>
    </div>

    <!-- History pane -->
    <div class="care-pane" id="care-pane-history">
      <div id="history-list-wrap"></div>
    </div>
  </div>

  <!-- RIGHT SIDEBAR -->
  <div id="right-sidebar">
    <div id="rsb-empty">
      <div class="empty-icon">🪴</div>
      <p style="font-size:13px;line-height:1.6;color:var(--muted);font-weight:500;">Klicke auf eine Pflanze<br>für Details &amp; Pflegehinweise.</p>
    </div>
    <div id="rsb-detail"></div>
  </div>

</div>

<script>
// ============================================================
// KONSTANTEN
// ============================================================
const CSV_URL     = "{CSV_URL}";
const GITHUB_BASE = "{GITHUB_BASE}";
const FLOOR_DATA  = {FLOOR_DATA_JSON};
const LAT_RAD     = {LAT_DEG} * Math.PI / 180;
const LON_DEG_VAL = {LON_DEG};

const PLANT_EMOJIS = ["🌿","🌱","🪴","🌺","🌸","🌻","🌵","🎋","🌴","🌳","🍀","☘️","🌾","🌼","💐","🫧","🪷"];
const MONTHS_DE    = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];
const DAYS_DE      = ["So","Mo","Di","Mi","Do","Fr","Sa"];
const NOW          = new Date();
const NOW_MONTH    = NOW.getMonth();

const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx9Vf0xJ4gJPFt6j3SaQQjW2PKT29upU-UxmyoioOEs_upOXVA0MgKGmu17yZQm0uuM/exec";

// ============================================================
// STATE
// ============================================================
let plants          = [];
let positions       = {{}};
let careData        = {{}};   // plantIdx -> {{lastWatered, lastFertilized, syncedW, syncedF}}
let careHistory     = [];
let activePIdx      = null;
let currentFloor    = "EG";
let currentTab      = "planer";
let currentCarePane = "tasks";
let dragSrcIdx      = null;
let inventoryFilter = "";
let saveTimeout     = null;
let sunState        = {{ azimuth:180, elevation:0, factor:0 }};
let dliMode         = false;
let dliCache        = {{}};

// Library filter/sort state
let libFilter = {{ search:"", licht:"", giess:"", placement:"" }};
let libSort   = {{ key:"name", dir:1 }};

// Calendar state
let calMonth = NOW_MONTH;
let calYear  = NOW.getFullYear();

// ============================================================
// UTILITY
// ============================================================
const $ = id => document.getElementById(id);
const setStatus = (state, msg) => {{
  const dot = $("sdot"), txt = $("stext");
  dot.className = "sync-dot " + state;
  txt.textContent = msg;
}};

function showTooltip(msg, x, y) {{
  const t=$("tooltip"); t.textContent=msg;
  t.style.left=(x+14)+"px"; t.style.top=(y+14)+"px";
  t.classList.add("visible");
}}
function hideTooltip() {{ $("tooltip").classList.remove("visible"); }}

function showToast(msg, type="ok", dur=2600) {{
  const toast = $("save-toast");
  const icons = {{ok:"✅", sync:"☁️", error:"⚠️", warn:"💾"}};
  $("toast-icon").textContent = icons[type]||"✅";
  $("toast-msg").textContent = msg;
  toast.className = "show" + (type==="error"?" error-toast":"");
  setTimeout(()=>toast.className="", dur);
}}

$("month-label").textContent = MONTHS_DE[NOW_MONTH]+" "+NOW.getFullYear();

// ============================================================
// SUN PHYSICS
// ============================================================
function calcSunPosition(date) {{
  const JD = date/86400000+2440587.5, n=JD-2451545.0;
  const L=(280.460+0.9856474*n)%360;
  const g=((357.528+0.9856003*n)%360)*Math.PI/180;
  const lam=(L+1.915*Math.sin(g)+0.020*Math.sin(2*g))*Math.PI/180;
  const eps=(23.439-0.0000004*n)*Math.PI/180;
  const sinDec=Math.sin(eps)*Math.sin(lam), dec=Math.asin(sinDec);
  const RA=Math.atan2(Math.cos(eps)*Math.sin(lam),Math.cos(lam));
  const GMST=(6.697375+0.0657098242*n+(date.getUTCHours()+(date.getUTCMinutes()+date.getUTCSeconds()/60)/60))%24;
  const LMST=(GMST*15+LON_DEG_VAL)%360;
  const HA=(LMST-RA*180/Math.PI)*Math.PI/180;
  const sinElev=Math.sin(LAT_RAD)*Math.sin(dec)+Math.cos(LAT_RAD)*Math.cos(dec)*Math.cos(HA);
  const elev=Math.asin(sinElev), elevDeg=elev*180/Math.PI;
  const cosAz=(Math.sin(dec)-Math.sin(elev)*Math.sin(LAT_RAD))/(Math.cos(elev)*Math.cos(LAT_RAD));
  const azBase=Math.acos(Math.max(-1,Math.min(1,cosAz)))*180/Math.PI;
  const az=Math.sin(HA)>0?360-azBase:azBase;
  let airmass=1;
  if(elevDeg>0) airmass=1/(Math.sin(elev)+0.50572*Math.pow(elevDeg+6.07995,-1.6364));
  const transmit=elevDeg>0?Math.pow(0.7,Math.pow(airmass,0.678)):0;
  return {{azimuth:az,elevation:elevDeg,transmittance:transmit,factor:transmit}};
}}

function skyDiffuse(e){{if(e<=-6)return 0;if(e<=0)return .05;return .10+.05*Math.min(1,e/30);}}
function windowAzimuth(side,bna){{const m={{"N":0,"E":90,"S":180,"W":270}};return(bna+(m[side]??180))%360;}}
function directSunFactor(wa,sa,e){{if(e<=0)return 0;const d=Math.abs(((wa-sa+540)%360)-180);const c=Math.cos(d*Math.PI/180);return c<=0?0:c*Math.sin(e*Math.PI/180);}}
function roomPenetrationFactor(e){{if(e<=0)return 0;return 1-(Math.max(5,Math.min(80,e))-5)/80;}}

const WIN_SAMPLES=7;
function segmentsIntersect(ax,ay,bx,by,cx,cy,dx,dy){{
  const d=(bx-ax)*(dy-cy)-(by-ay)*(dx-cx);
  if(Math.abs(d)<1e-9)return false;
  const t=((cx-ax)*(dy-cy)-(cy-ay)*(dx-cx))/d;
  const u=((cx-ax)*(by-ay)-(cy-ay)*(bx-ax))/d;
  const eps=1e-6;return t>eps&&t<1-eps&&u>eps&&u<1-eps;
}}
function isBlocked(ax,ay,bx,by,segs){{for(const s of segs){{if(segmentsIntersect(ax,ay,bx,by,s.x1,s.y1,s.x2,s.y2))return true;}}return false;}}
function px2rel(px,p1,p2){{return(px-p1)/(p2-p1);}}

function computeLichtFull(px,py,floor){{
  const fd=FLOOR_DATA[floor],fw=fd.floorX2-fd.floorX1,fh=fd.floorY2-fd.floorY1;
  const realW=fd.realW,realH=fd.realH,bldAz=fd.buildingNorthAzimuth||0;
  const pAX=fd.floorX1+px*fw,pAY=fd.floorY1+py*fh;
  const m=4;if(pAX<fd.floorX1-m||pAX>fd.floorX2+m||pAY<fd.floorY1-m||pAY>fd.floorY2+m)return{{score:1,components:{{}},windowHits:[]}};
  const sunElevDeg=sunState.elevation,sunAzDeg=sunState.azimuth,sunDirect=sunState.factor,skyDiff=skyDiffuse(sunElevDeg),wallRef=0.15;
  let totalIllum=0;const windowHits=[];
  for(const w of fd.windows){{
    const winAz=windowAzimuth(w.side,bldAz);
    let winContrib=0,samplesVis=0,totalSamp=0,bestInc=0;
    for(let s=0;s<WIN_SAMPLES;s++){{
      const t=WIN_SAMPLES===1?.5:s/(WIN_SAMPLES-1);
      const sAX=w.x1+t*(w.x2-w.x1),sAY=w.y1+t*(w.y2-w.y1);
      totalSamp++;
      if(isBlocked(pAX,pAY,sAX,sAY,fd.walls))continue;
      if(isBlocked(pAX,pAY,sAX,sAY,fd.outerWalls))continue;
      samplesVis++;
      const dxM=(px-px2rel(sAX,fd.floorX1,fd.floorX2))*realW,dyM=(py-px2rel(sAY,fd.floorY1,fd.floorY2))*realH;
      const distM=Math.sqrt(dxM*dxM+dyM*dyM);
      const incF=directSunFactor(winAz,sunAzDeg,sunElevDeg);
      bestInc=Math.max(bestInc,incF);
      const kD=0.2+0.6*(1-roomPenetrationFactor(sunElevDeg));
      winContrib+=incF*sunDirect/(1+kD*distM*distM)+skyDiff/(1+0.3*distM);
    }}
    if(totalSamp>0){{
      const wl=Math.sqrt((w.x2-w.x1)**2+(w.y2-w.y1)**2);
      const iv=Math.abs(w.x2-w.x1)<Math.abs(w.y2-w.y1);
      const wm=Math.min(3,iv?(wl/fh)*realH:(wl/fw)*realW);
      totalIllum+=winContrib/totalSamp*wm;
    }}
    windowHits.push({{side:w.side,winAz:winAz.toFixed(0),incFactor:bestInc.toFixed(2),visRatio:(samplesVis/totalSamp).toFixed(2),occluded:samplesVis===0}});
  }}
  totalIllum*=(1+wallRef);
  const score=Math.min(10,Math.max(1,Math.round(totalIllum*22*10)/10));
  return{{score,components:{{totalIllum,skyDiff,sunDirect}},windowHits}};
}}
function computeLicht(px,py,floor){{return computeLichtFull(px,py,floor).score;}}
function getLichtStatus(ist,soll){{return ist>=soll?"ideal":ist>=soll-2?"ok":"bad";}}
const STATUS_CFG={{
  ideal:{{icon:"🌟",label:"Idealer Standort",desc:"Ausreichend Licht für diese Pflanze.",cls:"ideal"}},
  ok:   {{icon:"⛅",label:"Akzeptabler Standort",desc:"Etwas weniger als optimal, aber tolerierbar.",cls:"ok"}},
  bad:  {{icon:"🌑",label:"Zu dunkel",desc:"Bitte näher ans Fenster stellen.",cls:"bad"}},
}};

// DLI
function computeDLI(px,py,floor){{
  const d=new Date(),y=d.getFullYear(),mo=d.getMonth(),dy=d.getDate();
  let sum=0,w=0;
  for(let h=0;h<24;h++){{
    const dt=new Date(Date.UTC(y,mo,dy,h-1,0,0));
    const sun=calcSunPosition(dt);
    if(sun.elevation<=0)continue;
    const sv={{...sunState}};sunState=sun;
    const s=computeLichtFull(px,py,floor).score;
    sunState=sv;
    const wt=Math.sin(sun.elevation*Math.PI/180);
    sum+=s*wt;w+=wt;
  }}
  return w===0?1:Math.min(10,Math.max(1,Math.round(sum/w*10)/10));
}}
let dliScheduled=false;
function scheduleDLI(floor){{
  if(dliScheduled)return;dliScheduled=true;
  requestAnimationFrame(()=>{{
    dliScheduled=false;if(!dliMode)return;
    const step=0.05,cache={{}};
    for(let ry=0;ry<=1.01;ry+=step)for(let rx=0;rx<=1.01;rx+=step)
      cache[`${{rx.toFixed(2)}},${{ry.toFixed(2)}}`]=computeDLI(rx,ry,floor);
    dliCache[floor]=cache;drawLightMap();
  }});
}}
function getDLI(px,py,floor){{
  if(!dliCache[floor])return null;
  const step=0.05,rx=Math.round(px/step)*step,ry=Math.round(py/step)*step;
  return dliCache[floor]?.[`${{rx.toFixed(2)}},${{ry.toFixed(2)}}`]??null;
}}
function toggleDLIMode(){{
  dliMode=!dliMode;
  $("dli-knob").classList.toggle("on",dliMode);
  $("dli-btn").classList.toggle("active",dliMode);
  if(dliMode){{showToast("DLI-Berechnung läuft…","warn",3000);scheduleDLI(currentFloor);}}
  else drawLightMap();
  render();
}}

function updateSunInfo(){{
  const now=new Date();sunState=calcSunPosition(now);
  const e=sunState.elevation.toFixed(1),a=sunState.azimuth.toFixed(0);
  $("sun-label").textContent=sunState.elevation>0
    ?`☀️ ${"{"}e{"}"}° Elev · ${"{"}a{"}"}° Az · ${"{"}(sunState.factor*100).toFixed(0){"}"}%`
    :`🌙 Sonne unter Horizont (${"{"}e{"}"}°)`;
}}

// Light Map
function drawLightMap(){{
  const img=$("floor-img"),canvas=$("light-canvas");
  if(!img.naturalWidth)return;
  canvas.width=img.naturalWidth;canvas.height=img.naturalHeight;
  canvas.style.width=img.naturalWidth+"px";canvas.style.height=img.naturalHeight+"px";
  const ctx=canvas.getContext("2d"),fd=FLOOR_DATA[currentFloor];
  const fw=fd.floorX2-fd.floorX1,fh=fd.floorY2-fd.floorY1,step=20;
  ctx.clearRect(0,0,canvas.width,canvas.height);
  for(let iy=fd.floorY1;iy<=fd.floorY2;iy+=step){{
    for(let ix=fd.floorX1;ix<=fd.floorX2;ix+=step){{
      const rx=(ix-fd.floorX1)/fw,ry=(iy-fd.floorY1)/fh;
      if(dliMode){{
        const lv=getDLI(rx,ry,currentFloor)??computeLicht(rx,ry,currentFloor);
        const a=(lv/10)*.26;
        ctx.fillStyle=`rgba(${{Math.round(92+lv/10*50)}},${{Math.round(155+lv/10*28)}},${{Math.round(214-lv/10*48)}},${{a.toFixed(3)}})`;
      }}else{{
        const lv=computeLicht(rx,ry,currentFloor);
        const a=(lv/10)*.22,r=Math.round(lv/10*251),g=222,b=Math.round((1-lv/10)*128+74);
        ctx.fillStyle=`rgba(${{r}},${{g}},${{b}},${{a.toFixed(3)}})`;
      }}
      ctx.fillRect(ix,iy,step,step);
    }}
  }}
}}

function onImageReady(){{
  const img=$("floor-img"),cvs=$("map-canvas");
  const W=img.naturalWidth||1100,H=img.naturalHeight||600;
  cvs.style.width=W+"px";cvs.style.height=H+"px";
  const area=$("map-area"),scale=Math.min(1,(area.clientWidth-40)/W,(area.clientHeight-40)/H);
  cvs.style.transform=`translate(-50%,-50%) scale(${{scale}})`;
}}
$("floor-img").addEventListener("load",()=>{{onImageReady();drawLightMap();render();}});
window.addEventListener("resize",onImageReady);

// ============================================================
// PLANT IMAGE
// ============================================================
function getPlantImageUrl(name){{
  return `${{GITHUB_BASE}}/${{name.replace(/\s+/g,"%20")}}.png`;
}}
function imgTag(name,emoji,cls,style){{
  const url=getPlantImageUrl(name);
  return `<img src="${{url}}" class="${{cls}}" style="${{style||''}}"
    onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
  <div style="display:none;width:100%;height:100%;align-items:center;justify-content:center;font-size:48px;opacity:.3;">${{emoji}}</div>`;
}}

// ============================================================
// CSV LOAD & PARSE
// ============================================================
async function loadPlants(){{
  setStatus("syncing","Lade Daten…");
  try{{
    const res=await fetch(CSV_URL);
    if(!res.ok)throw new Error("HTTP "+res.status);
    plants=parseCSV(await res.text());
    setStatus("ok",plants.length+" Pflanzen geladen");
  }}catch(e){{
    console.warn("CSV-Fehler:",e);
    plants=[
      {{id:0,name:"Monstera Deliciosa",botanisch:"Monstera deliciosa",licht:7,giessen:"3",dungen:"4",umtopfen:"Alle 2 Jahre",luftfeuchtigkeit:"60–80%",besprühen:"Wöchentlich",besonderheit:"Bekannt für ihre spektakulären Blattlöcher.",emoji:"🌿",giessAll:{{}},duengAll:{{}}}},
      {{id:1,name:"Sukkulente",botanisch:"Echeveria spp.",licht:9,giessen:"14",dungen:"30",umtopfen:"Alle 3 Jahre",luftfeuchtigkeit:"30–50%",besprühen:"Nie",besonderheit:"Speichert Wasser in Blättern.",emoji:"🌵",giessAll:{{}},duengAll:{{}}}},
    ];
    setStatus("error","Offline-Modus");
  }}
  plants.forEach((p,i)=>{{if(!p.emoji)p.emoji=PLANT_EMOJIS[i%PLANT_EMOJIS.length];}});
  $("inv-count").textContent=plants.length;
  loadPositionsLocal();
  loadCareData();
  renderInventory();
  renderLibrary();
  setFloor(currentFloor);
  $("loading").classList.add("hidden");
  updateSunInfo();
  renderCare();
  renderCalendar();
  updateDueBadge();
  setInterval(()=>{{updateSunInfo();drawLightMap();render();updateDueBadge();}},60000);
}}

function parseCSV(text){{
  const lines=text.trim().split("\n");
  const headers=lines[0].split(",").map(h=>h.trim().replace(/"/g,""));
  const col=(...cands)=>{{
    for(const c of cands){{const i=headers.findIndex(h=>h.toLowerCase().includes(c.toLowerCase()));if(i>=0)return i;}}
    return -1;
  }};
  const colName=col("Pflanze","Name","name");
  const colBot =col("Botanischer","botanisch");
  const colLicht=col("Lichtbedarf");
  const colUmtopf=col("Umtopfen");
  const colLuft=col("Luftfeuchtigkeit","Optimale Luftfeu");
  const colBespr=col("Besprühen","Bespruehen");
  const colBesond=col("Besonderheit");
  const giessAll={{}},duengAll={{}};
  MONTHS_DE.forEach(m=>{{
    giessAll[m]=col("Gießen_"+m,"Giessen_"+m);
    duengAll[m]=col("Düngen_"+m,"Dunegen_"+m,"Duengen_"+m);
  }});
  const monthName=MONTHS_DE[NOW_MONTH];
  const colG=giessAll[monthName],colD=duengAll[monthName];
  const sc=(cols,idx)=>idx>=0?(cols[idx]||"").trim().replace(/^"|"$/g,""):"";

  return lines.slice(1).filter(l=>l.trim()).map((line,i)=>{{
    const cols=splitCSVLine(line);
    const obj={{
      id:i,
      name:           sc(cols,colName)||"Pflanze "+(i+1),
      botanisch:      sc(cols,colBot),
      licht:          parseFloat(sc(cols,colLicht))||5,
      giessen:        sc(cols,colG)||"—",
      dungen:         sc(cols,colD)||"—",
      umtopfen:       sc(cols,colUmtopf)||"—",
      luftfeuchtigkeit:sc(cols,colLuft),
      besprühen:      sc(cols,colBespr),
      besonderheit:   sc(cols,colBesond),
      emoji:          PLANT_EMOJIS[i%PLANT_EMOJIS.length],
      giessAll:{{}}, duengAll:{{}},
    }};
    MONTHS_DE.forEach(m=>{{
      obj.giessAll[m]=giessAll[m]>=0?sc(cols,giessAll[m]):"—";
      obj.duengAll[m]=duengAll[m]>=0?sc(cols,duengAll[m]):"—";
    }});
    return obj;
  }});
}}
function splitCSVLine(line){{
  const res=[];let cur="",inQ=false;
  for(const ch of line){{if(ch==='"'){{inQ=!inQ;continue}}if(ch===','&&!inQ){{res.push(cur.trim());cur="";continue}}cur+=ch;}}
  res.push(cur.trim());return res;
}}

// ============================================================
// PERSISTENZ
// ============================================================
function savePositionsLocal(){{
  try{{localStorage.setItem("pflanzen_positions_v2",JSON.stringify(positions));}}catch(e){{}}
}}
function loadPositionsLocal(){{
  try{{const r=localStorage.getItem("pflanzen_positions_v2");if(r)positions=JSON.parse(r);}}catch(e){{positions={{}};}}
}}
function saveCareLocal(){{
  try{{
    localStorage.setItem("pflanzen_care_v2",JSON.stringify(careData));
    localStorage.setItem("pflanzen_hist_v2",JSON.stringify(careHistory.slice(0,200)));
  }}catch(e){{}}
}}
function loadCareData(){{
  try{{
    const rc=localStorage.getItem("pflanzen_care_v2");if(rc)careData=JSON.parse(rc);
    const rh=localStorage.getItem("pflanzen_hist_v2");if(rh)careHistory=JSON.parse(rh);
  }}catch(e){{careData={{}};careHistory=[];}}
}}

// ============================================================
// ★ GOOGLE SHEETS BIDIREKTIONALE SYNC
// ============================================================
async function savePositionsToSheets(){{
  savePositionsLocal();
  const payload=Object.entries(positions).map(([idx,pos])=>
    ({{type:"position",idx:parseInt(idx),floor:pos.floor,x:pos.x,y:pos.y}}));
  await pushToSheets(payload,"positions");
}}

async function saveCareToSheets(plantIdx,careType,isoTime){{
  // Sofort lokal speichern
  saveCareLocal();
  const payload=[{{
    type:"care",
    idx:plantIdx,
    careType:careType,        // "water" | "fertilize"
    timestamp:isoTime,
    plantName:plants[plantIdx]?.name||"",
  }}];
  const ok=await pushToSheets(payload,"care");
  if(ok){{
    if(!careData[plantIdx])careData[plantIdx]={{}};
    if(careType==="water") careData[plantIdx].syncedW=true;
    else                   careData[plantIdx].syncedF=true;
    saveCareLocal();
    // Mark history entry as synced
    const hEntry=careHistory.find(h=>h.plantIdx===plantIdx&&h.type===careType&&h.time===isoTime);
    if(hEntry)hEntry.synced=true;
  }}
  return ok;
}}

async function pushToSheets(payload,context){{
  if(!APPS_SCRIPT_URL)return false;
  try{{
    await fetch(APPS_SCRIPT_URL,{{
      method:"POST",mode:"no-cors",
      headers:{{"Content-Type":"application/json"}},
      body:JSON.stringify({{payload,context}}),
    }});
    return true;
  }}catch(e){{
    console.warn("Sheets sync failed:",e);
    return false;
  }}
}}

// Sync care timestamps BACK from Sheets (read)
async function syncCareFromSheets(){{
  setStatus("syncing","Synchronisiere mit Sheets…");
  try{{
    // Try to fetch care data from sheets via CSV
    // The sheet may have lastWatered/lastFertilized columns per plant
    // We re-fetch the CSV which might have been updated
    const res=await fetch(CSV_URL+"&bustcache="+Date.now());
    if(!res.ok)throw new Error("HTTP "+res.status);
    const text=await res.text();
    const lines=text.trim().split("\n");
    const headers=lines[0].split(",").map(h=>h.trim().replace(/"/g,""));
    const colName=headers.findIndex(h=>h.toLowerCase().includes("pflanze")||h.toLowerCase().includes("name"));
    const colLW  =headers.findIndex(h=>h.toLowerCase().includes("lastwatered")||h.toLowerCase().includes("gegossen_am"));
    const colLF  =headers.findIndex(h=>h.toLowerCase().includes("lastfertilized")||h.toLowerCase().includes("gedungt_am"));

    if(colLW>=0||colLF>=0){{
      lines.slice(1).filter(l=>l.trim()).forEach((line,i)=>{{
        const cols=splitCSVLine(line);
        const nameFromSheet=(cols[colName]||"").trim();
        const pIdx=plants.findIndex(p=>p.name===nameFromSheet||p.id===i);
        if(pIdx<0)return;
        if(!careData[pIdx])careData[pIdx]={{}};
        if(colLW>=0&&cols[colLW]&&cols[colLW].trim()&&cols[colLW].trim()!=="—"){{
          const sheetDate=new Date(cols[colLW].trim());
          if(!isNaN(sheetDate)){{
            const existing=careData[pIdx].lastWatered?new Date(careData[pIdx].lastWatered):null;
            if(!existing||sheetDate>existing)careData[pIdx].lastWatered=sheetDate.toISOString();
          }}
        }}
        if(colLF>=0&&cols[colLF]&&cols[colLF].trim()&&cols[colLF].trim()!=="—"){{
          const sheetDate=new Date(cols[colLF].trim());
          if(!isNaN(sheetDate)){{
            const existing=careData[pIdx].lastFertilized?new Date(careData[pIdx].lastFertilized):null;
            if(!existing||sheetDate>existing)careData[pIdx].lastFertilized=sheetDate.toISOString();
          }}
        }}
      }});
      saveCareLocal();
      setStatus("ok","Synchronisiert ✓");
      showToast("Pflege-Daten aus Sheets geladen","sync");
    }}else{{
      setStatus("ok","Verbunden");
      showToast("Keine Pflege-Zeitstempel in Sheets gefunden","warn");
    }}
  }}catch(e){{
    setStatus("error","Sync fehlgeschlagen");
    showToast("Sync-Fehler: "+e.message,"error");
  }}
  renderCare();
  updateDueBadge();
}}

function debouncedSave(){{
  if(saveTimeout)clearTimeout(saveTimeout);
  saveTimeout=setTimeout(savePositionsToSheets,900);
}}

// ============================================================
// ★ SAISONALE PFLEGE-LOGIK
// ============================================================
function parseInterval(val){{
  if(!val||val==="—"||String(val).trim()==="")return null;
  const n=parseFloat(String(val).replace(",","."));
  return isNaN(n)||n<=0?null:n;
}}

/**
 * Gibt das aktuell gültige Intervall (in Tagen) für den angegebenen Monat zurück.
 * Fallback-Kette: Monatswert → nächster verfügbarer Monat → globalwert → null
 */
function getIntervalForMonth(plant,type,monthIdx){{
  const monthName=MONTHS_DE[monthIdx];
  const allMap=type==="water"?plant.giessAll:plant.duengAll;
  // 1. Direkt im angegebenen Monat
  let v=allMap[monthName];
  if(parseInterval(v)!==null)return parseInterval(v);
  // 2. Fallback: suche nächsten definierten Monat (zyklisch)
  for(let d=1;d<12;d++){{
    const m2=MONTHS_DE[(monthIdx+d)%12];
    v=allMap[m2];
    if(parseInterval(v)!==null)return parseInterval(v);
  }}
  // 3. Fallback: globaler Wert (p.giessen / p.dungen)
  return parseInterval(type==="water"?plant.giessen:plant.dungen);
}}

function getCareStatus(plantIdx,type){{
  const p=plants[plantIdx];
  if(!p)return null;
  const now=new Date();
  const intervalDays=getIntervalForMonth(p,type,now.getMonth());
  if(!intervalDays)return null;

  const cd=careData[plantIdx]||{{}};
  const lastStr=type==="water"?cd.lastWatered:cd.lastFertilized;
  const lastDate=lastStr?new Date(lastStr):null;

  let nextDate,overdueDays=0,pct=0,elapsedDays=0;

  if(lastDate&&!isNaN(lastDate)){{
    nextDate=new Date(lastDate.getTime()+intervalDays*86400000);
    const diffMs=now-nextDate;
    overdueDays=Math.max(0,Math.floor(diffMs/86400000));
    elapsedDays=(now-lastDate)/86400000;
    pct=Math.max(0,Math.min(100,Math.round((1-elapsedDays/intervalDays)*100)));
  }}else{{
    nextDate=new Date(now.getTime()-86400000);
    overdueDays=1;pct=0;elapsedDays=intervalDays+1;
  }}

  // Urgency: overdue / today / soon(3d) / ok
  let urgency="ok";
  if(overdueDays>0)urgency="overdue";
  else{{
    const daysUntil=Math.ceil((nextDate-now)/86400000);
    if(daysUntil===0)urgency="today";
    else if(daysUntil<=3)urgency="soon";
  }}

  return{{nextDate,overdueDays,intervalDays,pct,elapsedDays,urgency,lastDate}};
}}

function formatRel(date){{
  const d=Math.round((date-new Date())/86400000);
  if(d<-1)return`${{Math.abs(d)}} Tage überfällig`;
  if(d===-1)return"Gestern fällig";
  if(d===0)return"Heute fällig";
  if(d===1)return"Morgen";
  if(d<=7)return`In ${{d}} Tagen`;
  return date.toLocaleDateString("de-DE",{{day:"2-digit",month:"2-digit"}});
}}
function formatAbs(iso){{
  if(!iso)return"—";
  const d=new Date(iso);
  if(isNaN(d))return"—";
  return d.toLocaleDateString("de-DE",{{day:"2-digit",month:"2-digit",year:"numeric"}})+" "+d.toLocaleTimeString("de-DE",{{hour:"2-digit",minute:"2-digit"}});
}}

// ============================================================
// PROGRESS RING SVG
// ============================================================
function makeRing(pct,urgency){{
  const r=18,circ=2*Math.PI*r;
  const offset=circ*(1-pct/100);
  const color=urgency==="overdue"?"var(--danger)":urgency==="today"?"var(--warn)":urgency==="soon"?"var(--accent)":"var(--ok)";
  return `<svg class="ring-svg" viewBox="0 0 44 44">
    <circle class="ring-bg" cx="22" cy="22" r="${{r}}"/>
    <circle class="ring-fill" cx="22" cy="22" r="${{r}}"
      stroke="${{color}}" stroke-dasharray="${{circ.toFixed(2)}}" stroke-dashoffset="${{offset.toFixed(2)}}"/>
    <text class="ring-text" x="22" y="22">${{pct}}%</text>
  </svg>`;
}}

// ============================================================
// TAB SWITCHING
// ============================================================
function switchTab(tab){{
  currentTab=tab;
  document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("active",t.dataset.tab===tab));
  const isPlaner=tab==="planer",isLib=tab==="library",isCare=tab==="care";
  $("left-sidebar").classList.toggle("hidden",!isPlaner);
  $("right-sidebar").classList.toggle("hidden",!isPlaner);
  $("map-area").style.display=isPlaner?"block":"none";
  $("library-view").classList.toggle("active",isLib);
  $("care-view").classList.toggle("active",isCare);
  if(isLib)renderLibrary();
  if(isCare){{renderCare();renderCalendar();}}
}}

function switchCarePane(pane){{
  currentCarePane=pane;
  ["tasks","calendar","history"].forEach(p=>{{
    $("care-pane-"+p).classList.toggle("active",p===pane);
    $("subnav-"+p).classList.toggle("active",p===pane);
  }});
  if(pane==="calendar")renderCalendar();
  if(pane==="history")renderHistory();
  if(pane==="tasks")renderCareTasks();
}}

// ============================================================
// FLOOR
// ============================================================
function setFloor(floor){{
  currentFloor=floor;
  ["EG","1. OG","2. OG"].forEach(f=>{{const b=$("fbtn-"+f);if(b)b.classList.toggle("active",f===floor);}});
  const fi=$("floor-img");fi.src=FLOOR_DATA[floor].url;
  fi.onload=()=>{{onImageReady();drawLightMap();render();}};
  if(fi.complete&&fi.naturalWidth){{onImageReady();drawLightMap();render();}}
  render();renderInventory();
  if(activePIdx!==null)renderDetail(activePIdx);
  if(dliMode)scheduleDLI(floor);
}}

// ============================================================
// RENDER PINS
// ============================================================
function render(){{
  const canvas=$("map-canvas"),img=$("floor-img");
  const W=img.naturalWidth||1100,H=img.naturalHeight||600;
  canvas.style.width=W+"px";canvas.style.height=H+"px";
  canvas.querySelectorAll(".plant-pin").forEach(el=>el.remove());
  plants.forEach((p,i)=>{{
    const pos=positions[i];if(!pos||pos.floor!==currentFloor)return;
    const ist=dliMode?(getDLI(pos.x,pos.y,currentFloor)??computeLicht(pos.x,pos.y,currentFloor)):computeLicht(pos.x,pos.y,currentFloor);
    const stat=getLichtStatus(ist,p.licht);
    const pin=document.createElement("div");
    pin.className="plant-pin"+(activePIdx===i?" active":"");
    pin.dataset.idx=i;
    pin.style.transform=`translate(${{Math.round(pos.x*W-21)}}px,${{Math.round(pos.y*H-21)}}px)`;
    pin.innerHTML=`<div class="pin-bubble">${{p.emoji}}</div><div class="pin-indicator ${{stat}}"></div><div class="pin-label">${{p.name.split(" ")[0]}}</div><div class="pin-light-badge">${{ist}}/10</div>`;
    setupPinDrag(pin,i);
    pin.addEventListener("click",e=>{{e.stopPropagation();selectPlant(i);}});
    pin.addEventListener("mousemove",e=>showTooltip(`${{p.name}} · Licht: ${{ist}}/10 · Bedarf: ${{p.licht}}/10`,e.clientX,e.clientY));
    pin.addEventListener("mouseleave",hideTooltip);
    canvas.appendChild(pin);
  }});
}}

function selectPlant(idx){{
  activePIdx=activePIdx===idx?null:idx;
  render();
  if(activePIdx!==null)renderDetail(activePIdx);else showEmptyDetail();
  renderInventory();
}}
function showEmptyDetail(){{$("rsb-empty").style.display="";$("rsb-detail").classList.remove("visible");}}

// ============================================================
// RENDER DETAIL
// ============================================================
function renderDetail(idx){{
  const p=plants[idx],pos=positions[idx];
  const floor=pos?pos.floor:currentFloor;
  const lf=pos?computeLichtFull(pos.x,pos.y,floor):null;
  const liveScore=lf?lf.score:null;
  const dliScore=pos?getDLI(pos.x,pos.y,floor):null;
  const primary=dliMode&&dliScore?dliScore:liveScore;
  const stat=primary?getLichtStatus(primary,p.licht):null;
  const sc=stat?STATUS_CFG[stat]:null;

  $("rsb-empty").style.display="none";
  const det=$("rsb-detail");det.classList.add("visible");
  const imgUrl=getPlantImageUrl(p.name);
  const coordsHTML=pos?`<div style="font-size:11px;color:var(--muted);margin-top:4px;font-family:var(--mono);">${{(pos.x*100).toFixed(1)}}% · ${{(pos.y*100).toFixed(1)}}%</div><span class="floor-tag">📍 ${{pos.floor}}</span>`:`<span class="floor-tag">📦 Im Inventar</span>`;

  let dliHTML="";
  if(pos){{
    const dv=dliScore??null,lv=liveScore??null;
    const night=sunState.elevation<=-6;
    dliHTML=`<div class="dli-panel">
      <div class="dli-panel-title">📊 Daily Light Integral</div>
      <div class="dli-score-row"><span class="dli-score-val">${{dv??'—'}}</span><span class="dli-score-unit">/ 10 Tages-Ø</span></div>
      <div class="dli-bar-track"><div class="dli-bar-fill" style="width:${{dv?(dv/10*100).toFixed(0):0}}%"></div></div>
      <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);font-weight:600;margin-bottom:8px;"><span>Tagesmittel</span><span>Bedarf: ${{p.licht}}/10</span></div>
      <div class="dli-live-row"><div class="dli-live-dot"></div><span class="dli-live-text">${{night?"🌙 Nacht":"☀️ Live: "+(lv??'—')+"/10"}}</span></div>
      ${{!dv?'<div style="font-size:10px;color:var(--muted);text-align:center;margin-top:6px;">DLI-Modus aktivieren</div>':''}}
    </div>`;
  }}

  let astroHTML="";
  if(lf){{
    const wc=lf.windowHits.map(w=>{{
      const bright=!w.occluded&&parseFloat(w.incFactor)>.2;
      return `<span class="win-chip ${{bright?"hit":""}}">${{w.side}}${{w.occluded?" ✗":bright?" ☀️":""}}</span>`;
    }}).join("");
    const night=sunState.elevation<=-6,dawn=sunState.elevation<=0&&!night;
    astroHTML=`<div class="astro-panel">
      <div class="astro-title">☀️ Live-Lichtanalyse</div>
      <div class="astro-grid">
        <div class="astro-cell"><div class="astro-cell-lbl">Elevation</div><div class="astro-cell-val">${{sunState.elevation.toFixed(1)}}<span class="astro-cell-unit">°</span></div></div>
        <div class="astro-cell"><div class="astro-cell-lbl">Azimut</div><div class="astro-cell-val">${{sunState.azimuth.toFixed(0)}}<span class="astro-cell-unit">°</span></div></div>
        <div class="astro-cell"><div class="astro-cell-lbl">Direkt</div><div class="astro-cell-val">${{(lf.components.sunDirect*100).toFixed(0)}}<span class="astro-cell-unit">%</span></div></div>
        <div class="astro-cell"><div class="astro-cell-lbl">Himmel</div><div class="astro-cell-val">${{(lf.components.skyDiff*100/0.15).toFixed(0)}}<span class="astro-cell-unit">%</span></div></div>
      </div>
      <div class="window-chips">${{wc}}</div>
    </div>`;
  }}

  const bar=stat==='ideal'?'var(--accent)':stat==='ok'?'var(--warn)':'var(--danger)';
  const lightHTML=primary?`
    <div class="score-badge ${{sc.cls}}"><div class="sc-icon">${{sc.icon}}</div><div class="sc-text"><h3>${{sc.label}}</h3><p>${{sc.desc}}</p></div></div>
    <div class="light-bar-wrap">
      <div class="lbw-label"><span>💡 Lichtwert</span><span>${{primary}} / 10</span></div>
      <div class="lbw-track"><div class="lbw-fill" style="width:${{(primary/10*100).toFixed(1)}}%;background:linear-gradient(90deg,var(--accent-glow),${{bar}})"></div><div class="lbw-needle" style="left:${{(p.licht/10*100).toFixed(1)}}%"></div></div>
      <div class="lbw-label"><span style="color:var(--muted)">Bedarf: ${{p.licht}}/10</span><span style="color:var(--muted)">Verfügbar: ${{primary}}/10</span></div>
    </div>
    ${{dliHTML}}${{astroHTML}}
  `:`<div style="font-size:13px;color:var(--muted);background:var(--surface-db);border-radius:var(--r);padding:16px;text-align:center;border:1px solid var(--border);">${{dliHTML||'Auf Karte platzieren für Lichtanalyse.'}}</div>`;

  const extras=[
    p.luftfeuchtigkeit?`<div class="detail-extra-row"><div class="detail-extra-lbl">💧 Luftfeuchtigkeit</div><div class="detail-extra-val">${{p.luftfeuchtigkeit}}</div></div>`:"",
    p.besprühen?`<div class="detail-extra-row"><div class="detail-extra-lbl">🌫️ Besprühen</div><div class="detail-extra-val">${{p.besprühen}}</div></div>`:"",
    p.besonderheit?`<div class="detail-extra-row"><div class="detail-extra-lbl">💡 Besonderheit</div><div class="detail-extra-val">${{p.besonderheit}}</div></div>`:"",
  ].filter(Boolean).join("");

  det.innerHTML=`
    <div class="detail-img-wrap">
      <img src="${{imgUrl}}" style="width:100%;height:100%;object-fit:cover;" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="detail-img-fallback" style="display:none">${{p.emoji}}</div>
    </div>
    <div class="detail-body">
      <div class="plant-hdr">
        <div class="big-emoji">${{p.emoji}}</div>
        <div class="plant-hdr-text"><h2>${{p.name}}</h2>${{p.botanisch?`<div class="botanical">${{p.botanisch}}</div>`:''}}${{coordsHTML}}</div>
      </div>
      ${{lightHTML}}
      <div class="data-grid">
        <div class="dc"><div class="dc-lbl">💧 Gießen (${{MONTHS_DE[NOW_MONTH]}})</div><div class="dc-val">${{p.giessen||"—"}}<span class="dc-unit">Tage</span></div></div>
        <div class="dc"><div class="dc-lbl">🌿 Düngen (${{MONTHS_DE[NOW_MONTH]}})</div><div class="dc-val">${{p.dungen||"—"}}</div></div>
        <div class="dc"><div class="dc-lbl">☀️ Lichtbedarf</div><div class="dc-val">${{p.licht}}<span class="dc-unit">/ 10</span></div></div>
        <div class="dc"><div class="dc-lbl">🪴 Umtopfen</div><div class="dc-val" style="font-size:14px;">${{p.umtopfen||"—"}}</div></div>
      </div>
      ${{extras?`<div style="display:flex;flex-direction:column;gap:8px;">${{extras}}</div>`:""}}
      <div class="action-row">
        <button class="act-btn primary" onclick="selectPlant(${{idx}})">✓ Schließen</button>
        ${{pos?`<button class="act-btn danger-btn" onclick="removePlant(${{idx}})">🗑️</button>`:""}}
      </div>
    </div>
  `;
}}

function removePlant(idx){{
  delete positions[idx];activePIdx=null;debouncedSave();
  render();renderInventory();showEmptyDetail();
}}

// ============================================================
// INVENTORY
// ============================================================
function renderInventory(){{
  const list=$("inv-list"),filter=inventoryFilter.toLowerCase();
  const avail=[],here=[],other=[];
  plants.forEach((p,i)=>{{
    if(filter&&!p.name.toLowerCase().includes(filter))return;
    const pos=positions[i];
    if(!pos)avail.push(i);else if(pos.floor===currentFloor)here.push(i);else other.push(i);
  }});
  list.innerHTML="";
  const makeGroup=(label,indices,isPlaced,isOther)=>{{
    if(!indices.length)return;
    const grp=document.createElement("div");grp.className="inv-group";
    grp.innerHTML=`<div class="inv-group-label">${{label}} (${{indices.length}})</div>`;
    indices.forEach(i=>{{
      const p=plants[i],item=document.createElement("div");
      let cls="inv-item";if(activePIdx===i)cls+=" selected";if(isOther)cls+=" placed-elsewhere";
      item.className=cls;item.dataset.pidx=i;
      item.innerHTML=`<span class="inv-emoji">${{p.emoji}}</span><span class="inv-name">${{p.name}}</span>
        ${{isPlaced?`<span class="inv-badge placed-badge">📍 ${{positions[i]?.floor||""}}</span>`:`<span class="inv-badge">Verfügbar</span>`}}`;
      item.addEventListener("click",()=>{{
        activePIdx=i;
        if(positions[i]&&positions[i].floor!==currentFloor)setFloor(positions[i].floor);
        render();renderInventory();renderDetail(i);
      }});
      if(!isPlaced){{
        item.draggable=true;
        item.addEventListener("dragstart",e=>{{dragSrcIdx=i;e.dataTransfer.effectAllowed="move";setTimeout(()=>item.classList.add("dragging-source"),0);}});
        item.addEventListener("dragend",()=>{{item.classList.remove("dragging-source");dragSrcIdx=null;}});
      }}
      grp.appendChild(item);
    }});
    list.appendChild(grp);
  }};
  makeGroup("🟢 Verfügbar",avail,false,false);
  makeGroup("📍 Hier platziert",here,true,false);
  makeGroup("🔵 Anderes OG",other,true,true);
}}
function filterInventory(val){{inventoryFilter=val;renderInventory();}}

// Drop & Drag
const mapArea=$("map-area");
mapArea.addEventListener("dragover",e=>{{e.preventDefault();e.dataTransfer.dropEffect="move";$("map-canvas").classList.add("drag-over");}});
mapArea.addEventListener("dragleave",()=>$("map-canvas").classList.remove("drag-over"));
mapArea.addEventListener("drop",e=>{{
  e.preventDefault();$("map-canvas").classList.remove("drag-over");
  if(dragSrcIdx===null)return;
  const img=$("floor-img"),W=img.naturalWidth||1100,H=img.naturalHeight||600;
  const scale=parseFloat($("map-canvas").style.transform.match(/scale\(([^)]+)\)/)?.[1]||1);
  const area=$("map-area"),cX=area.clientWidth/2-W*scale/2,cY=area.clientHeight/2-H*scale/2;
  positions[dragSrcIdx]={{floor:currentFloor,x:Math.max(0,Math.min(1,(e.clientX-cX)/(W*scale))),y:Math.max(0,Math.min(1,(e.clientY-cY)/(H*scale)))}};
  activePIdx=dragSrcIdx;dragSrcIdx=null;debouncedSave();
  render();renderInventory();renderDetail(activePIdx);
}});
$("map-area").addEventListener("click",()=>{{activePIdx=null;render();renderInventory();showEmptyDetail();}});

function setupPinDrag(pin,idx){{
  let sX,sY,sPX,sPY,drag=false;
  function getWH(){{const img=$("floor-img"),W=img.naturalWidth||1100,H=img.naturalHeight||600,r=img.getBoundingClientRect();return{{W,H,scX:W/r.width,scY:H/r.height}};}}
  pin.addEventListener("pointerdown",e=>{{if(e.button&&e.button!==0)return;e.preventDefault();e.stopPropagation();drag=true;pin.classList.add("dragging");pin.setPointerCapture(e.pointerId);sX=e.clientX;sY=e.clientY;sPX=positions[idx].x;sPY=positions[idx].y;}});
  pin.addEventListener("pointermove",e=>{{
    if(!drag)return;e.preventDefault();
    const {{W,H,scX,scY}}=getWH();
    positions[idx].x=Math.max(0,Math.min(1,sPX+(e.clientX-sX)*scX/W));
    positions[idx].y=Math.max(0,Math.min(1,sPY+(e.clientY-sY)*scY/H));
    pin.style.transform=`translate(${{Math.round(positions[idx].x*W-21)}}px,${{Math.round(positions[idx].y*H-21)}}px)`;
    const ist=computeLicht(positions[idx].x,positions[idx].y,currentFloor);
    pin.querySelector(".pin-indicator").className="pin-indicator "+getLichtStatus(ist,plants[idx].licht);
    pin.querySelector(".pin-light-badge").textContent=ist+"/10";
    if(activePIdx===idx)renderDetail(idx);
  }});
  pin.addEventListener("pointerup",e=>{{if(!drag)return;drag=false;pin.classList.remove("dragging");debouncedSave();render();if(activePIdx===idx)renderDetail(idx);}});
  pin.addEventListener("pointercancel",()=>{{drag=false;pin.classList.remove("dragging");}});
}}

// ============================================================
// ★ LIBRARY — Smart Filter & Sort
// ============================================================
function onLibFilterChange(){{
  libFilter.search=($("lib-search").value||"").toLowerCase();
  libFilter.licht=$("filter-licht").value;
  libFilter.giess=$("filter-giess").value;
  libFilter.placement=$("filter-placement").value;
  renderLibrary();
}}

function setSort(key){{
  if(libSort.key===key)libSort.dir*=-1;
  else{{libSort.key=key;libSort.dir=1;}}
  ["name","licht","giess"].forEach(k=>{{
    $("sort-"+k).classList.toggle("active",k===key);
    $("arr-"+k).textContent=libSort.key===k?(libSort.dir===1?"↑":"↓"):"↑";
  }});
  renderLibrary();
}}

function filterAndSortPlants(){{
  let result=plants.map((p,i)=>{{{{return{{p,i}};}}}});

  // Text search
  if(libFilter.search)result=result.filter(({{{p}}})=>p.name.toLowerCase().includes(libFilter.search)||(p.botanisch||"").toLowerCase().includes(libFilter.search));

  // Licht filter
  if(libFilter.licht){{
    result=result.filter(({{{p}}})=>{{
      const l=p.licht;
      return libFilter.licht==="low"?l<=4:libFilter.licht==="mid"?l>=5&&l<=7:l>=8;
    }});
  }}

  // Giess filter
  if(libFilter.giess){{
    result=result.filter(({{{p}}})=>{{
      const g=getIntervalForMonth(p,"water",NOW_MONTH);
      if(g===null)return libFilter.giess==="rare";
      return libFilter.giess==="rare"?g>10:libFilter.giess==="normal"?g>=4&&g<=10:g<4;
    }});
  }}

  // Placement filter
  if(libFilter.placement){{
    result=result.filter(({{{i}}})=>{{
      const placed=!!positions[i];
      return libFilter.placement==="placed"?placed:!placed;
    }});
  }}

  // Sort
  result.sort((a,b)=>{{
    let va,vb;
    if(libSort.key==="name"){{va=a.p.name.toLowerCase();vb=b.p.name.toLowerCase();return va<vb?-libSort.dir:va>vb?libSort.dir:0;}}
    if(libSort.key==="licht"){{va=a.p.licht;vb=b.p.licht;}}
    if(libSort.key==="giess"){{va=getIntervalForMonth(a.p,"water",NOW_MONTH)??9999;vb=getIntervalForMonth(b.p,"water",NOW_MONTH)??9999;}}
    return(va-vb)*libSort.dir;
  }});
  return result;
}}

function renderActiveChips(){{
  const wrap=$("active-chips");wrap.innerHTML="";
  const labels={{licht:{{low:"Licht: Wenig",mid:"Licht: Mittel",high:"Licht: Viel"}},giess:{{rare:"Gießen: Selten",normal:"Gießen: Normal",frequent:"Gießen: Häufig"}},placement:{{placed:"Platziert",unplaced:"Im Inventar"}}}};
  ["licht","giess","placement"].forEach(k=>{{
    if(!libFilter[k])return;
    const label=labels[k][libFilter[k]]||libFilter[k];
    const chip=document.createElement("div");chip.className="filter-chip";
    chip.innerHTML=`${{label}} <span class="filter-chip-x">×</span>`;
    chip.addEventListener("click",()=>{{libFilter[k]="";$("filter-"+k).value="";onLibFilterChange();}});
    wrap.appendChild(chip);
  }});
}}

function renderLibrary(){{
  const result=filterAndSortPlants();
  renderActiveChips();

  const placed=Object.keys(positions).length;
  $("lib-sub-label").textContent=`${{plants.length}} Pflanzen · ${{placed}} platziert · ${{MONTHS_DE[NOW_MONTH]}}`;
  $("lib-results-bar").textContent=`${{result.length}} von ${{plants.length}} Pflanzen${{result.length!==plants.length?" (gefiltert)":""}} · Sortiert nach ${{libSort.key==="name"?"Name":libSort.key==="licht"?"Lichtbedarf":"Gießhäufigkeit"}} ${{libSort.dir===1?"↑":"↓"}}`;

  const grid=$("lib-grid");grid.innerHTML="";
  result.forEach(({{{p,i}}})=>{{
    const pos=positions[i];
    const lf=pos?computeLichtFull(pos.x,pos.y,pos.floor):null;
    const ist=lf?lf.score:null;
    const stat=ist?getLichtStatus(ist,p.licht):null;
    const bar=stat==="ideal"?"var(--accent)":stat==="ok"?"var(--warn)":"var(--danger)";
    const lightPct=ist?(ist/10*100).toFixed(0):0;
    const floorLabel=pos?`📍 ${{pos.floor}}`:"📦 Im Inventar";
    const giessInt=getIntervalForMonth(p,"water",NOW_MONTH);

    let statusChip="";
    if(stat){{
      const cfg={{ideal:"✅ Optimal",ok:"⚠️ Akzeptabel",bad:"❌ Zu dunkel"}};
      statusChip=`<span class="lib-status-chip ${{stat}}">${{cfg[stat]}}</span>`;
    }}else{{
      statusChip=`<span class="lib-status-chip none">📦 Nicht platziert</span>`;
    }}

    const imgUrl=getPlantImageUrl(p.name);
    const card=document.createElement("div");
    card.className="lib-card";
    card.innerHTML=`
      <div class="lib-card-img">
        <img src="${{imgUrl}}" alt="${{p.name}}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="lib-card-img-fallback" style="display:none">${{p.emoji}}</div>
        <div class="lib-card-img-overlay">
          <div class="lib-card-name">${{p.name}}</div>
          ${{p.botanisch?`<div class="lib-card-botanical">${{p.botanisch}}</div>`:""}}
        </div>
      </div>
      <div class="lib-card-body">
        <div class="lib-card-row1">
          ${{statusChip}}
          <div class="lib-card-loc" style="margin-left:auto">
            <div class="lib-card-loc-dot ${{pos?"placed":""}}"></div>${{floorLabel}}
          </div>
        </div>
        <div class="lib-metrics">
          <div class="lib-metric">
            <div class="lib-metric-lbl">☀️ Licht</div>
            <div class="lib-metric-val">${{p.licht}}<span class="lib-metric-unit">/10</span></div>
          </div>
          <div class="lib-metric">
            <div class="lib-metric-lbl">💧 Gießen</div>
            <div class="lib-metric-val">${{giessInt??p.giessen||"—"}}<span class="lib-metric-unit">Tage</span></div>
          </div>
          <div class="lib-metric">
            <div class="lib-metric-lbl">🌿 Düngen</div>
            <div class="lib-metric-val">${{getIntervalForMonth(p,"fertilize",NOW_MONTH)??p.dungen||"—"}}</div>
          </div>
        </div>
        ${{ist?`<div class="lib-light-bar-wrap">
          <div class="lib-light-header"><span>Licht verfügbar</span><span class="lib-light-score" style="color:${{bar}}">${{ist}}/10</span></div>
          <div class="lib-light-track"><div class="lib-light-fill" style="width:${{lightPct}}%;background:linear-gradient(90deg,var(--accent-glow),${{bar}})"></div></div>
        </div>`:"" }}
        ${{p.besonderheit?`<div class="lib-besonderheit"><strong>💡 Besonderheit</strong>${{p.besonderheit}}</div>`:""}}
        ${{p.luftfeuchtigkeit||p.besprühen?`<div style="display:flex;gap:8px;flex-wrap:wrap;font-size:12px;color:var(--muted);">
          ${{p.luftfeuchtigkeit?`<span>💧 ${{p.luftfeuchtigkeit}}</span>`:""}}
          ${{p.besprühen?`<span>🌫️ Besprühen: <strong style="color:var(--text)">${{p.besprühen}}</strong></span>`:""}}
        </div>`:"" }}
      </div>
      <div class="lib-card-footer">
        <button class="show-on-map-btn" data-pidx="${{i}}">🗺️ Auf Karte zeigen</button>
      </div>
    `;
    card.querySelector(".show-on-map-btn").addEventListener("click",()=>{{
      const pp=positions[i];if(pp)setFloor(pp.floor);
      switchTab("planer");
      setTimeout(()=>{{activePIdx=i;render();renderDetail(i);const pin=$("map-canvas").querySelector(`[data-idx="${{i}}"]`);if(pin){{pin.classList.add("highlight-pulse");setTimeout(()=>pin.classList.remove("highlight-pulse"),4500);}}}},120);
    }});
    grid.appendChild(card);
  }});
}}

// ============================================================
// ★ CARE DASHBOARD
// ============================================================
function updateDueBadge(){{
  let overdue=0;
  plants.forEach((_,i)=>{{
    const ws=getCareStatus(i,"water"),fs=getCareStatus(i,"fertilize");
    if((ws&&ws.urgency==="overdue")||(fs&&fs.urgency==="overdue"))overdue++;
  }});
  const badge=$("care-badge");
  badge.style.display=overdue>0?"inline-flex":"none";
  badge.textContent=overdue;
}}

function buildCareBuckets(){{
  const overdue=[],today=[],soon=[],ok=[];
  plants.forEach((p,i)=>{{
    const ws=getCareStatus(i,"water"),fs=getCareStatus(i,"fertilize");
    const urg=ws?.urgency==="overdue"||fs?.urgency==="overdue"?"overdue":
               ws?.urgency==="today"||fs?.urgency==="today"?"today":
               ws?.urgency==="soon"||fs?.urgency==="soon"?"soon":"ok";
    const entry={{idx:i,ws,fs,urg}};
    if(urg==="overdue")overdue.push(entry);
    else if(urg==="today")today.push(entry);
    else if(urg==="soon")soon.push(entry);
    else ok.push(entry);
  }});
  return{{overdue,today,soon,ok}};
}}

function renderCare(){{
  updateDueBadge();
  if(currentCarePane==="tasks")renderCareTasks();
  else if(currentCarePane==="calendar")renderCalendar();
  else renderHistory();
}}

function renderCareTasks(){{
  const buckets=buildCareBuckets();
  // Update KPIs
  $("kpi-overdue-n").textContent=buckets.overdue.length;
  $("kpi-today-n").textContent=buckets.today.length;
  $("kpi-soon-n").textContent=buckets.soon.length;
  $("kpi-ok-n").textContent=buckets.ok.length;

  renderCareBlock("care-overdue-block","⚠️ Überfällig",buckets.overdue,"danger");
  renderCareBlock("care-today-block","🟡 Heute fällig",buckets.today,"warn");
  renderCareBlock("care-soon-block","📅 Diese Woche",buckets.soon,"ok");
  renderCareBlock("care-ok-block","✅ Versorgt",buckets.ok,"ok",true);
}}

function renderCareBlock(elId,title,entries,badge,collapsed){{
  const el=$(elId);if(!el)return;
  if(entries.length===0){{el.innerHTML="";return;}}
  const badgeCls=badge==="danger"?"care-section-badge":badge==="warn"?"care-section-badge warn":"care-section-badge ok";
  const tableHTML=makeCareTable(entries,collapsed);
  el.innerHTML=`
    <div class="care-section-hdr">
      <div class="care-section-title">${{title}}</div>
      <span class="${{badgeCls}}">${{entries.length}} Pflanze${{entries.length!==1?"n":""}}</span>
    </div>
    ${{tableHTML}}
  `;
}}

function makeCareTable(entries,compact){{
  if(entries.length===0)return"";
  const rowsHTML=entries.map(e=>makeCareRow(e,compact)).join("");
  return `
    <div class="care-table">
      <div class="care-table-head">
        <div class="care-table-head-cell">Pflanze</div>
        <div class="care-table-head-cell">💧 Gießen</div>
        <div class="care-table-head-cell">🌿 Düngen</div>
        <div class="care-table-head-cell">Wasser %</div>
        <div class="care-table-head-cell">Dünger %</div>
        <div class="care-table-head-cell">Aktionen</div>
      </div>
      ${{rowsHTML}}
    </div>
  `;
}}

function makeCareRow(entry,compact){{
  const {{idx,ws,fs,urg}}=entry,p=plants[idx],cd=careData[idx]||{{}};
  const imgUrl=getPlantImageUrl(p.name);
  const pos=positions[idx];

  // Water status cell
  const wCell=ws?`<span class="care-status-badge ${{ws.urgency}}">${{formatRel(ws.nextDate)}}</span>`:`<span style="color:var(--muted2);font-size:12px;">—</span>`;
  const fCell=fs?`<span class="care-status-badge ${{fs.urgency}}">${{formatRel(fs.nextDate)}}</span>`:`<span style="color:var(--muted2);font-size:12px;">—</span>`;

  // Progress rings
  const wRing=ws?makeRing(ws.pct,ws.urgency):`<div style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;color:var(--muted2);font-size:12px;">—</div>`;
  const fRing=fs?makeRing(fs.pct,fs.urgency):`<div style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;color:var(--muted2);font-size:12px;">—</div>`;

  const rowCls="care-row"+(urg==="overdue"?" overdue":urg==="today"?" today":"");

  return `
    <div class="${{rowCls}}" id="care-row-${{idx}}">
      <div class="care-plant-cell">
        <div class="care-thumb">
          <img src="${{imgUrl}}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
          <div class="care-thumb-emoji" style="display:none">${{p.emoji}}</div>
        </div>
        <div>
          <div class="care-plant-name">${{p.name}}</div>
          <div class="care-plant-loc">${{pos?"📍 "+pos.floor:"📦 Inventar"}}</div>
        </div>
      </div>
      <div class="care-cell">${{wCell}}</div>
      <div class="care-cell">${{fCell}}</div>
      <div class="ring-wrap">${{wRing}}</div>
      <div class="ring-wrap">${{fRing}}</div>
      <div class="care-action-cell">
        ${{ws?`<button class="care-btn-water" id="wb-${{idx}}" onclick="doWater(${{idx}})">💧</button>`:"" }}
        ${{fs?`<button class="care-btn-fert" id="fb-${{idx}}" onclick="doFertilize(${{idx}})">🌿</button>`:"" }}
      </div>
    </div>
  `;
}}

// ============================================================
// ★ CARE ACTIONS — Sofort-Sync mit Google Sheets
// ============================================================
async function doWater(plantIdx){{
  const now=new Date().toISOString();
  if(!careData[plantIdx])careData[plantIdx]={{}};
  careData[plantIdx].lastWatered=now;
  careData[plantIdx].syncedW=false;
  careHistory.unshift({{type:"water",plantIdx,name:plants[plantIdx].name,emoji:plants[plantIdx].emoji,time:now,synced:false}});
  saveCareLocal();

  // Optimistic UI update
  const wb=$("wb-"+plantIdx);if(wb){{wb.classList.add("care-btn-syncing");wb.textContent="⏳";}}

  renderCare();renderCalendar();updateDueBadge();
  showToast(`💧 ${{plants[plantIdx].name}} gegossen`,"ok");

  // Async sync to sheets
  const ok=await saveCareToSheets(plantIdx,"water",now);
  setStatus(ok?"ok":"error",ok?"Synchronisiert ✓":"Lokal gespeichert");
  if(ok)showToast(`☁️ Gegossen & synchronisiert`,"sync");
  renderHistory();
}}

async function doFertilize(plantIdx){{
  const now=new Date().toISOString();
  if(!careData[plantIdx])careData[plantIdx]={{}};
  careData[plantIdx].lastFertilized=now;
  careData[plantIdx].syncedF=false;
  careHistory.unshift({{type:"fertilize",plantIdx,name:plants[plantIdx].name,emoji:plants[plantIdx].emoji,time:now,synced:false}});
  saveCareLocal();

  const fb=$("fb-"+plantIdx);if(fb){{fb.classList.add("care-btn-syncing");fb.textContent="⏳";}}

  renderCare();renderCalendar();updateDueBadge();
  showToast(`🌿 ${{plants[plantIdx].name}} gedüngt`,"ok");

  const ok=await saveCareToSheets(plantIdx,"fertilize",now);
  setStatus(ok?"ok":"error",ok?"Synchronisiert ✓":"Lokal gespeichert");
  if(ok)showToast(`☁️ Gedüngt & synchronisiert`,"sync");
  renderHistory();
}}

async function waterAllDue(){{
  setStatus("syncing","Gieße alle fälligen…");
  let count=0;
  const tasks=[];
  plants.forEach((p,i)=>{{
    const ws=getCareStatus(i,"water");
    if(ws&&(ws.urgency==="overdue"||ws.urgency==="today")){{
      const now=new Date().toISOString();
      if(!careData[i])careData[i]={{}};
      careData[i].lastWatered=now;
      careHistory.unshift({{type:"water",plantIdx:i,name:p.name,emoji:p.emoji,time:now,synced:false}});
      tasks.push(saveCareToSheets(i,"water",now));
      count++;
    }}
  }});
  saveCareLocal();
  const results=await Promise.all(tasks);
  const allOk=results.every(Boolean);
  setStatus(allOk?"ok":"error",allOk?"Alle synchronisiert":"Teils lokal gespeichert");
  renderCare();renderCalendar();updateDueBadge();
  showToast(`💧 ${{count}} Pflanzen gegossen${{allOk?" & synchronisiert":""}}`,allOk?"sync":"warn");
  renderHistory();
}}

// ============================================================
// CALENDAR
// ============================================================
function changeCalMonth(d){{
  calMonth+=d;if(calMonth>11){{calMonth=0;calYear++;}}if(calMonth<0){{calMonth=11;calYear--;}}
  renderCalendar();
}}

function renderCalendar(){{
  const titleEl=$("cal-month-title");if(titleEl)titleEl.textContent=MONTHS_DE[calMonth]+" "+calYear;
  const grid=$("cal-grid");if(!grid)return;
  let html=DAYS_DE.map(d=>`<div class="cal-day-hdr">${{d}}</div>`).join("");
  const first=new Date(calYear,calMonth,1),last=new Date(calYear,calMonth+1,0);
  const startDow=first.getDay(),total=last.getDate();
  const prevLast=new Date(calYear,calMonth,0).getDate();
  for(let d=startDow-1;d>=0;d--)html+=`<div class="cal-cell other-month"><div class="cal-day-num">${{prevLast-d}}</div></div>`;

  // Collect events
  const evByDay={{}};
  careHistory.forEach(h=>{{
    const d=new Date(h.time);
    if(d.getMonth()===calMonth&&d.getFullYear()===calYear){{
      const day=d.getDate();
      if(!evByDay[day])evByDay[day]=[];
      evByDay[day].push({{type:h.type,name:h.name}});
    }}
  }});
  plants.forEach((p,i)=>{{
    ["water","fertilize"].forEach(type=>{{
      const s=getCareStatus(i,type);if(!s)return;
      const nd=s.nextDate;
      if(nd.getMonth()===calMonth&&nd.getFullYear()===calYear){{
        const day=nd.getDate();if(!evByDay[day])evByDay[day]=[];
        evByDay[day].push({{type:"due-"+type,name:p.name}});
      }}
    }});
  }});

  const todayD=NOW.getDate(),todayM=NOW.getMonth(),todayY=NOW.getFullYear();
  for(let d=1;d<=total;d++){{
    const isToday=d===todayD&&calMonth===todayM&&calYear===todayY;
    const evs=evByDay[d]||[];
    const evHTML=evs.slice(0,3).map(e=>{{
      const cls=e.type==="water"?"water":e.type==="fertilize"?"fertilize":e.type==="due-water"?"due-water":"due-fertilize";
      const icon=e.type.includes("water")?"💧":"🌿";
      return `<div class="cal-ev ${{cls}}">${{icon}} ${{e.name}}</div>`;
    }}).join("")+(evs.length>3?`<div class="cal-ev" style="color:var(--muted2)">+${{evs.length-3}}</div>`:"");
    html+=`<div class="cal-cell${{isToday?" today":""}}"}<div class="cal-day-num">${{d}}</div><div class="cal-events">${{evHTML}}</div></div>`;
  }}

  const used=startDow+total,rem=(7-used%7)%7;
  for(let d=1;d<=rem;d++)html+=`<div class="cal-cell other-month"><div class="cal-day-num">${{d}}</div></div>`;
  grid.innerHTML=html;
}}

// ============================================================
// HISTORY
// ============================================================
function renderHistory(){{
  const wrap=$("history-list-wrap");if(!wrap)return;
  if(!careHistory.length){{
    wrap.innerHTML=`<div class="care-empty"><div class="care-empty-icon">📋</div><p style="font-size:14px;font-weight:500">Noch keine Aktionen aufgezeichnet.</p></div>`;
    return;
  }}
  const rows=careHistory.slice(0,100).map(h=>{{
    const icon=h.type==="water"?"💧":"🌿";
    const label=h.type==="water"?"gegossen":"gedüngt";
    const synced=h.synced;
    return `<div class="history-entry">
      <div class="history-icon-wrap ${{h.type}}">${{icon}}</div>
      <span class="history-text">${{h.emoji}} ${{h.name}} ${{label}}</span>
      <span class="history-time">${{formatAbs(h.time)}}</span>
      <span class="history-sync-status ${{synced?"synced":"local"}}">${{synced?"☁️ Sync":"💾 Lokal"}}</span>
    </div>`;
  }}).join("");
  wrap.innerHTML=`<div class="history-list">
    <div class="history-hdr">📋 Pflege-Historie <span class="history-hdr-count">${{careHistory.length}} Einträge</span></div>
    ${{rows}}
  </div>`;
}}

// ============================================================
// BOOT
// ============================================================
// Initialize UI
switchCarePane("tasks");
loadPlants();
</script>
</body>
</html>"""

components.html(html_app, height=900, scrolling=False)
