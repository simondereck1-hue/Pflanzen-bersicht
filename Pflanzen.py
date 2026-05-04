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
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<style>
/* ── TOKENS (Biophilic Palette) ── */
:root {{
  --bg: #FCFAF7;
  --surface: rgba(255, 255, 255, 0.85);
  --surface-solid: #FFFFFF;
  --surface-2: #F1F8E9;
  --surface-3: #E8F5E9;
  --border: rgba(45, 71, 57, 0.08);
  --border-2: rgba(45, 71, 57, 0.15);
  --accent: #7CB342;
  --accent-dim: rgba(124, 179, 66, 0.15);
  --accent-glow: rgba(124, 179, 66, 0.35);
  --accent-dark: #558B2F;
  --warn: #E2A76F;
  --warn-dim: rgba(226, 167, 111, 0.15);
  --danger: #E57373;
  --danger-dim: rgba(229, 115, 115, 0.15);
  --dli-color: #5C9BD6;
  --dli-dim: rgba(92, 155, 214, 0.15);
  --text: #2D4739;
  --muted: #688E7B;
  --muted2: #9EB5A8;
  --r: 16px; --rs: 12px; --rx: 24px;
  --transition: 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  --sidebar-w: 340px;
  --header-h: 68px; --tab-h: 56px;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;overflow:hidden}}
body{{
  font-family:'DM Sans',sans-serif;
  background: var(--bg);
  background-image: radial-gradient(circle at 0% 0%, rgba(241, 248, 233, 0.8) 0%, transparent 40%),
                    radial-gradient(circle at 100% 100%, rgba(232, 245, 233, 0.8) 0%, transparent 40%);
  color:var(--text);display:flex;flex-direction:column;
}}
button{{font-family:inherit;cursor:pointer;border:none;background:none;color:inherit}}
input,select{{font-family:inherit}}

/* ── HEADER ── */
#header{{
  height:var(--header-h);background:var(--surface);
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255,255,255,0.5);
  box-shadow: 0 4px 30px rgba(45, 71, 57, 0.04);
  display:flex;align-items:center;padding:0 24px;gap:12px;flex-shrink:0;z-index:200;
}}
.logo{{font-family:'Syne',sans-serif;font-weight:800;font-size:18px;color:var(--accent);letter-spacing:-.5px}}
.logo-sep{{color:var(--border-2);font-size:20px;font-weight:300;}}
.header-meta{{display:flex;align-items:center;gap:14px;margin-left:auto}}
.sun-info{{
  display:flex;align-items:center;gap:8px;font-size:13px;font-weight:500;color:var(--text);
  background:var(--surface-solid);border:1px solid var(--border);border-radius:99px;
  padding:6px 16px;box-shadow: 0 2px 10px rgba(45, 71, 57, 0.03);
}}
.sun-dot{{width:8px;height:8px;border-radius:50%;background:var(--warn);box-shadow:0 0 10px var(--warn);flex-shrink:0}}
.status-wrap{{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--muted);font-weight:500;}}
.sdot{{width:8px;height:8px;border-radius:50%;background:var(--muted2);transition:background .3s}}
.sdot.ok{{background:var(--accent);box-shadow:0 0 10px var(--accent)}}

/* ── TABS ── */
#tabs{{
  height:var(--tab-h);background:transparent;
  display:flex;align-items:center;justify-content:flex-start;padding:0 24px;gap:10px;flex-shrink:0;z-index:150;
  margin-top: 12px;
}}
.tab{{
  padding:12px 24px;font-size:14px;font-weight:600;color:var(--muted);
  border-radius:99px;cursor:pointer;
  background: rgba(255, 255, 255, 0.5); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border:1px solid var(--border);transition:all var(--transition);
  box-shadow: 0 2px 10px rgba(45, 71, 57, 0.02);
}}
.tab:hover{{color:var(--text);background:rgba(255, 255, 255, 0.9);transform:translateY(-2px);box-shadow: 0 6px 16px rgba(45, 71, 57, 0.05);}}
.tab.active{{color:var(--text);background:var(--surface-solid);border-color:var(--accent);box-shadow: 0 4px 16px var(--accent-dim);}}
.tab-icon{{margin-right:8px;font-size:16px;}}

/* ── MAIN ── */
#main{{display:flex;flex:1;overflow:hidden;position:relative;padding:0 16px 16px 16px;gap:16px;}}

/* ── SIDEBARS ── */
#left-sidebar, #right-sidebar{{
  width:var(--sidebar-w);background:var(--surface);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border:1px solid rgba(255,255,255,0.6);
  border-radius: var(--rx);
  box-shadow: 0 12px 40px rgba(45, 71, 57, 0.05);
  display:flex;flex-direction:column;overflow:hidden;flex-shrink:0;
}}
#left-sidebar.hidden, #right-sidebar.hidden{{display:none}}

.sidebar-header{{
  padding:20px 20px 16px;font-family:'Syne',sans-serif;font-weight:700;font-size:14px;
  color:var(--text);letter-spacing:.02em;
  border-bottom:1px solid var(--border);flex-shrink:0;display:flex;align-items:center;gap:8px;
}}
.sidebar-header span{{flex:1}}
.inv-search{{
  margin:16px;padding:10px 16px;background:var(--surface-solid);border:1px solid var(--border);
  border-radius:var(--r);color:var(--text);font-size:14px;width:calc(100% - 32px);
  box-shadow: inset 0 2px 4px rgba(45,71,57,0.02); transition: border-color .3s;
}}
.inv-search::placeholder{{color:var(--muted2)}}
.inv-search:focus{{outline:none;border-color:var(--accent);box-shadow: 0 0 0 3px var(--accent-dim);}}

.inv-group{{padding:12px 0 4px 0}}
.inv-group-label{{
  padding:4px 20px 8px;font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;
}}
.inv-item{{
  display:flex;align-items:center;gap:12px;padding:10px 20px;cursor:pointer;
  transition:all var(--transition);user-select:none; border-left: 3px solid transparent;
}}
.inv-item:hover{{background:rgba(255,255,255,0.5);}}
.inv-item.dragging-source{{opacity:.4; transform: scale(0.95);}}
.inv-item.selected{{background:var(--surface-solid);border-left:3px solid var(--accent);box-shadow: 0 4px 12px rgba(45,71,57,0.03);}}
.inv-item.placed-elsewhere{{opacity:.6}}
.inv-emoji{{font-size:20px;width:28px;text-align:center;background:var(--surface-2);border-radius:8px;padding:4px;}}
.inv-name{{font-size:14px;font-weight:500;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.inv-badge{{
  font-size:11px;padding:4px 10px;border-radius:99px;font-weight:600;
  background:var(--surface-3);color:var(--muted);white-space:nowrap
}}
.inv-badge.placed-badge{{background:var(--surface-solid);border: 1px solid var(--accent-glow);color:var(--accent)}}
.inv-floor-switcher{{
  margin:auto 16px 16px;padding:6px;
  background:var(--surface-solid);border:1px solid var(--border);border-radius:var(--rx);
  display:flex;gap:4px;flex-shrink:0; box-shadow: 0 4px 16px rgba(45,71,57,0.03);
}}
.floor-btn{{
  flex:1;padding:10px 8px;font-size:13px;font-weight:600;
  border-radius:var(--r);transition:all var(--transition);color:var(--muted)
}}
.floor-btn:hover{{background:var(--surface-2);color:var(--text)}}
.floor-btn.active{{background:var(--accent);color:#fff;box-shadow:0 4px 12px var(--accent-glow);}}

/* ── MAP AREA ── */
#map-area{{
  flex:1;position:relative;overflow:hidden;
  background:radial-gradient(ellipse at 50% 50%,rgba(124,179,66,.05) 0%,transparent 70%);
  border-radius: var(--rx);
  box-shadow: inset 0 0 30px rgba(45,71,57,0.02);
}}
#map-canvas{{
  position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%);
  border-radius: 12px;
}}
#floor-img{{
  position:absolute;inset:0;width:100%;height:100%;
  object-fit:contain;pointer-events:none;user-select:none;opacity:0.95;
}}
#light-canvas{{
  position:absolute;inset:0;width:100%;height:100%;
  pointer-events:none;opacity:.65; mix-blend-mode: multiply;
}}
#map-canvas.drag-over{{
  outline:3px dashed var(--accent);outline-offset:8px; border-radius: 16px;
  background: rgba(124,179,66,0.05);
}}

/* DLI Toggle */
.dli-toggle-wrap{{
  position:absolute;top:16px;right:16px;z-index:100;
  display:flex;gap:8px;align-items:center;
  background:rgba(255,255,255,0.9);backdrop-filter:blur(8px);
  border:1px solid var(--border);border-radius:99px;padding:6px 14px;
  box-shadow:0 4px 16px rgba(45,71,57,0.06);
}}
.dli-toggle-label{{font-size:12px;font-weight:600;color:var(--muted)}}
.dli-toggle{{
  width:36px;height:20px;border-radius:10px;background:var(--muted2);
  position:relative;cursor:pointer;transition:background .3s;border:none;
}}
.dli-toggle.on{{background:var(--dli-color);}}
.dli-toggle::after{{
  content:'';position:absolute;top:3px;left:3px;width:14px;height:14px;
  border-radius:50%;background:#fff;transition:transform .3s;
  box-shadow:0 1px 4px rgba(0,0,0,0.15);
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
.plant-pin.active .pin-bubble{{background:var(--surface-solid);border-color:var(--accent);box-shadow:0 0 0 4px var(--accent-dim), 0 8px 24px rgba(45,71,57,0.1);transform:scale(1.15);}}
.plant-pin.highlight-pulse .pin-bubble{{animation:highlightPulse 1.5s ease-in-out 3}}
@keyframes highlightPulse{{0%,100%{{box-shadow:0 0 0 0 var(--accent-glow)}}50%{{box-shadow:0 0 0 16px rgba(124,179,66,0)}}}}
.pin-bubble{{
  width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,0.9); backdrop-filter:blur(4px);
  border:2px solid var(--accent-glow);display:flex;align-items:center;justify-content:center;
  font-size:22px;transition:transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.4s;
  box-shadow:0 4px 16px rgba(45,71,57,0.08);
}}
.plant-pin:hover .pin-bubble{{transform:scale(1.2);box-shadow:0 8px 24px rgba(124,179,66,0.25);border-color:var(--accent);}}
.plant-pin.dragging .pin-bubble{{transform:scale(1.1) translateY(-5px);box-shadow:0 12px 30px rgba(124,179,66,0.3);}}
.pin-indicator{{width:10px;height:10px;border-radius:50%;margin-top:6px;background:var(--muted);transition:background .3s;border:2px solid #fff;}}
.pin-indicator.ideal{{background:var(--accent);box-shadow:0 0 8px var(--accent)}}
.pin-indicator.ok{{background:var(--warn);box-shadow:0 0 8px var(--warn)}}
.pin-indicator.bad{{background:var(--danger);box-shadow:0 0 8px var(--danger)}}
.pin-label{{
  font-size:11px;font-weight:600;color:var(--text);margin-top:4px;white-space:nowrap;
  max-width:80px;overflow:hidden;text-overflow:ellipsis;text-align:center;
  background:rgba(255,255,255,0.8);padding:3px 8px;border-radius:8px;backdrop-filter:blur(4px);
  box-shadow:0 2px 8px rgba(45,71,57,0.05);
}}
.pin-light-badge{{
  font-size:10px;font-weight:600;padding:2px 8px;border-radius:99px;margin-top:4px;
  background:var(--surface-solid);color:var(--muted);font-variant-numeric:tabular-nums;
  box-shadow:0 2px 6px rgba(45,71,57,0.04);
}}

/* ── RIGHT SIDEBAR (Detail) ── */
#rsb-empty{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;color:var(--muted);padding:32px;text-align:center}}
#rsb-empty .empty-icon{{font-size:54px;opacity:.5;filter:grayscale(0.5);}}
#rsb-detail{{flex:1;display:none;flex-direction:column;overflow-y:auto;padding:24px;gap:20px}}
#rsb-detail.visible{{display:flex}}
#rsb-detail::-webkit-scrollbar{{width:6px}}
#rsb-detail::-webkit-scrollbar-thumb{{background:var(--border-2);border-radius:3px}}

/* Detail Plant Image */
.detail-img-wrap{{
  width:100%;height:160px;border-radius:var(--rx);overflow:hidden;position:relative;
  background:var(--surface-2);border:1px solid var(--border);
  box-shadow:0 4px 16px rgba(45,71,57,0.04);
}}
.detail-img-wrap img{{width:100%;height:100%;object-fit:cover;}}
.detail-img-fallback{{
  width:100%;height:100%;display:flex;align-items:center;justify-content:center;
  font-size:64px;opacity:.4;
}}

.plant-hdr{{display:flex;align-items:flex-start;gap:16px}}
.big-emoji{{font-size:42px;flex-shrink:0;line-height:1;background:var(--surface-solid);padding:12px;border-radius:var(--r);box-shadow:0 4px 16px rgba(45,71,57,0.04);}}
.plant-hdr-text h2{{font-family:'Syne',sans-serif;font-size:22px;font-weight:700;line-height:1.2;color:var(--text);}}
.plant-hdr-text .botanical{{font-size:12px;color:var(--muted);font-style:italic;margin-top:3px;}}
.coords-row{{font-size:12px;color:var(--muted);margin-top:6px;font-variant-numeric:tabular-nums;font-weight:500;}}
.floor-tag{{
  display:inline-block;padding:4px 10px;border-radius:99px;font-size:11px;font-weight:600;
  background:var(--surface-solid);color:var(--text);margin-top:8px;border:1px solid var(--border);
  box-shadow:0 2px 8px rgba(45,71,57,0.02);
}}

/* DLI Score Panel */
.dli-panel{{
  background:linear-gradient(135deg, rgba(92,155,214,0.08) 0%, rgba(124,179,66,0.06) 100%);
  border:1px solid rgba(92,155,214,0.25);border-radius:var(--rx);padding:16px;
  display:flex;flex-direction:column;gap:12px;box-shadow:0 4px 16px rgba(92,155,214,0.06);
}}
.dli-panel-title{{font-size:11px;font-weight:700;color:var(--dli-color);text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;}}
.dli-score-row{{display:flex;align-items:baseline;gap:8px;}}
.dli-score-val{{font-family:'Syne',sans-serif;font-size:32px;font-weight:800;color:var(--text);}}
.dli-score-unit{{font-size:13px;color:var(--muted);font-weight:500;}}
.dli-bar-wrap{{display:flex;flex-direction:column;gap:6px;}}
.dli-bar-track{{height:8px;border-radius:4px;background:rgba(45,71,57,0.08);position:relative;overflow:hidden;}}
.dli-bar-fill{{height:100%;border-radius:4px;transition:width .8s cubic-bezier(.34,1.56,.64,1);background:linear-gradient(90deg,var(--dli-dim),var(--dli-color));}}
.dli-bar-labels{{display:flex;justify-content:space-between;font-size:11px;font-weight:600;color:var(--muted);}}
.dli-live-row{{display:flex;align-items:center;gap:8px;padding:8px 12px;background:rgba(255,255,255,0.7);border-radius:var(--rs);border:1px solid var(--border);}}
.dli-live-dot{{width:6px;height:6px;border-radius:50%;background:var(--warn);box-shadow:0 0 6px var(--warn);animation:pulse2 2s infinite;flex-shrink:0;}}
@keyframes pulse2{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.dli-live-text{{font-size:12px;font-weight:600;color:var(--text);flex:1;}}
.dli-live-val{{font-size:12px;font-weight:700;color:var(--muted);font-variant-numeric:tabular-nums;}}

.score-badge{{border-radius:var(--rx);padding:16px;display:flex;align-items:center;gap:16px;background:var(--surface-solid);box-shadow:0 4px 16px rgba(45,71,57,0.03);}}
.score-badge .sc-icon{{font-size:28px}}
.score-badge .sc-text h3{{font-family:'Syne',sans-serif;font-size:16px;font-weight:700}}
.score-badge .sc-text p{{font-size:13px;color:var(--muted);margin-top:4px;line-height:1.4}}
.score-badge.ideal{{border:1px solid var(--accent-glow);background:var(--surface-solid);}}
.score-badge.ideal .sc-text h3{{color:var(--accent)}}
.score-badge.ok{{border:1px solid rgba(226,167,111,0.4);background:var(--surface-solid);}}
.score-badge.ok .sc-text h3{{color:var(--warn)}}
.score-badge.bad{{border:1px solid rgba(229,115,115,0.4);background:var(--surface-solid);}}
.score-badge.bad .sc-text h3{{color:var(--danger)}}

.astro-panel{{
  background:var(--surface-solid);border:1px solid var(--border);border-radius:var(--rx);
  padding:16px;display:flex;flex-direction:column;gap:10px;box-shadow:0 4px 16px rgba(45,71,57,0.03);
}}
.astro-title{{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px}}
.astro-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.astro-cell{{background:var(--bg);border-radius:var(--r);padding:12px}}
.astro-cell-lbl{{font-size:10px;font-weight:600;color:var(--muted2);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px}}
.astro-cell-val{{font-family:'Syne',sans-serif;font-size:20px;font-weight:700;color:var(--text)}}
.astro-cell-unit{{font-size:12px;font-weight:500;color:var(--muted);margin-left:4px}}
.window-chips{{display:flex;gap:6px;flex-wrap:wrap}}
.win-chip{{
  font-size:11px;font-weight:600;padding:4px 10px;border-radius:99px;background:var(--bg);
  border:1px solid var(--border);color:var(--muted);
}}
.win-chip.hit{{background:var(--warn-dim);border-color:rgba(226,167,111,0.4);color:#d38e53;}}

.light-bar-wrap{{display:flex;flex-direction:column;gap:10px;background:var(--surface-solid);padding:16px;border-radius:var(--rx);border:1px solid var(--border);box-shadow:0 4px 16px rgba(45,71,57,0.03);}}
.lbw-label{{display:flex;justify-content:space-between;font-size:13px;font-weight:600;color:var(--text)}}
.lbw-track{{height:12px;border-radius:6px;background:rgba(45,71,57,0.05);position:relative;overflow:hidden}}
.lbw-fill{{height:100%;border-radius:6px;background:linear-gradient(90deg, var(--accent-glow), var(--accent));transition:width .8s cubic-bezier(.34, 1.56, .64, 1)}}
.lbw-needle{{position:absolute;top:-2px;bottom:-2px;width:4px;background:#fff;border-radius:2px;box-shadow:0 0 4px rgba(0,0,0,0.2);}}

.data-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.dc{{background:var(--surface-solid);border:1px solid var(--border);border-radius:var(--r);padding:16px;box-shadow:0 4px 16px rgba(45,71,57,0.02);}}
.dc-lbl{{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}}
.dc-val{{font-family:'Syne',sans-serif;font-size:22px;font-weight:700;color:var(--text)}}
.dc-unit{{font-size:13px;font-weight:500;color:var(--muted);margin-left:4px}}
/* Extra detail fields (humidity, besonderheit, besprühen) */
.detail-extra-row{{
  background:var(--surface-solid);border:1px solid var(--border);border-radius:var(--r);
  padding:14px 16px;display:flex;flex-direction:column;gap:4px;
  box-shadow:0 4px 16px rgba(45,71,57,0.02);
}}
.detail-extra-lbl{{font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;}}
.detail-extra-val{{font-size:13px;font-weight:500;color:var(--text);line-height:1.5;}}

.action-row{{display:flex;gap:10px;margin-top:8px}}
.act-btn{{
  flex:1;padding:12px;border-radius:var(--r);font-size:13px;font-weight:600;
  transition:all var(--transition);border:1px solid var(--border);background:var(--surface-solid);color:var(--text);
  box-shadow:0 2px 8px rgba(45,71,57,0.02);
}}
.act-btn:hover{{background:var(--bg);transform:translateY(-1px);box-shadow:0 4px 12px rgba(45,71,57,0.05);}}
.act-btn.primary{{background:var(--accent);border-color:var(--accent);color:#fff;}}
.act-btn.primary:hover{{background:#6aa335;box-shadow:0 4px 16px var(--accent-glow);}}
.act-btn.danger-btn{{background:var(--surface-solid);border-color:rgba(229,115,115,0.4);color:var(--danger)}}
.act-btn.danger-btn:hover{{background:var(--danger-dim);}}

/* ── LIBRARY VIEW ── */
#library-view{{display:none;flex:1;overflow-y:auto;padding:24px 32px;flex-direction:column;gap:24px}}
#library-view.active{{display:flex}}
#library-view::-webkit-scrollbar{{width:8px}}
#library-view::-webkit-scrollbar-thumb{{background:var(--border-2);border-radius:4px}}

.lib-header{{display:flex;align-items:center;gap:16px;flex-shrink:0;flex-wrap:wrap;background:var(--surface);padding:24px;border-radius:var(--rx);border:1px solid var(--border);backdrop-filter:blur(16px);box-shadow:0 8px 32px rgba(45,71,57,0.04);}}
.lib-header h2{{font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:var(--text);}}
.lib-header-sub{{font-size:14px;font-weight:500;color:var(--muted);margin-top:4px}}
.lib-search{{
  margin-left:auto;padding:12px 20px;background:var(--surface-solid);border:1px solid var(--border);
  border-radius:99px;color:var(--text);font-size:15px;width:300px;
  box-shadow:inset 0 2px 6px rgba(45,71,57,0.02);transition:all .3s;
}}
.lib-search::placeholder{{color:var(--muted2)}}
.lib-search:focus{{outline:none;border-color:var(--accent);box-shadow:0 0 0 4px var(--accent-dim);}}

.lib-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:24px;padding-bottom:32px;}}

/* Premium Library Card */
.lib-card{{
  background:var(--surface-solid);border:1px solid rgba(255,255,255,0.8);border-radius:var(--rx);
  display:flex;flex-direction:column;overflow:hidden;position:relative;
  transition:all var(--transition); cursor:default;
  box-shadow:0 8px 24px rgba(45,71,57,0.04);
}}
.lib-card:hover{{
  border-color:var(--accent-glow);
  box-shadow:0 20px 60px rgba(45,71,57,0.1);
  transform:translateY(-6px);
}}
.lib-card-img{{
  width:100%;height:180px;overflow:hidden;position:relative;
  background:linear-gradient(135deg,var(--surface-2),var(--surface-3));
  flex-shrink:0;
}}
.lib-card-img img{{
  width:100%;height:100%;object-fit:cover;transition:transform .6s ease;
}}
.lib-card:hover .lib-card-img img{{transform:scale(1.06);}}
.lib-card-img-fallback{{
  width:100%;height:100%;display:flex;align-items:center;justify-content:center;
  font-size:72px;opacity:.35;
}}
.lib-card-img-overlay{{
  position:absolute;bottom:0;left:0;right:0;
  background:linear-gradient(to top, rgba(45,71,57,0.6) 0%, transparent 100%);
  padding:16px;
}}
.lib-card-img-overlay .lib-card-name{{
  font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:#fff;
  text-shadow:0 2px 8px rgba(0,0,0,0.3);
}}
.lib-card-img-overlay .lib-card-botanical{{font-size:12px;color:rgba(255,255,255,0.75);font-style:italic;margin-top:2px;}}
.lib-card-body{{padding:20px;display:flex;flex-direction:column;gap:16px;}}

.lib-card-top-row{{display:flex;align-items:center;gap:12px;}}
.lib-card-loc{{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:500;color:var(--muted);}}
.lib-card-loc-dot{{width:6px;height:6px;border-radius:50%;background:var(--muted2);flex-shrink:0}}
.lib-card-loc-dot.placed{{background:var(--accent);box-shadow:0 0 6px var(--accent);}}

.lib-light-row{{display:flex;align-items:center;gap:12px;background:var(--bg);padding:12px 16px;border-radius:var(--r);}}
.lib-light-icon{{font-size:18px;flex-shrink:0}}
.lib-light-bar-wrap{{flex:1}}
.lib-light-bar-track{{height:8px;border-radius:4px;background:rgba(45,71,57,0.06);position:relative;overflow:hidden}}
.lib-light-bar-fill{{height:100%;border-radius:4px;transition:width .8s cubic-bezier(.34, 1.56, .64, 1)}}
.lib-light-labels{{display:flex;justify-content:space-between;font-size:11px;font-weight:600;color:var(--muted);margin-top:6px}}
.lib-light-score{{font-family:'Syne',sans-serif;font-size:16px;font-weight:700;min-width:44px;text-align:right;flex-shrink:0}}

.lib-divider{{height:1px;background:var(--border);margin:0}}

.lib-care-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.lib-care-cell{{background:var(--bg);border-radius:var(--rs);padding:10px 14px;display:flex;flex-direction:column;gap:4px;border:1px solid var(--border);}}
.lib-care-cell-lbl{{font-size:10px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}}
.lib-care-cell-val{{font-size:15px;font-weight:700;color:var(--text)}}
.lib-care-cell-unit{{font-size:11px;color:var(--muted);margin-left:3px;font-weight:500}}

/* Besonderheit field in library */
.lib-besonderheit{{
  background:linear-gradient(135deg,rgba(124,179,66,0.04),rgba(92,155,214,0.04));
  border:1px solid var(--border);border-radius:var(--rs);padding:12px 14px;
  font-size:13px;color:var(--text);line-height:1.5;font-style:italic;
  border-left:3px solid var(--accent-glow);
}}
.lib-besonderheit-lbl{{font-size:10px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;font-style:normal;}}

.lib-humidity-row{{display:flex;align-items:center;gap:10px;font-size:13px;color:var(--muted);font-weight:500;}}
.lib-humidity-badge{{
  padding:4px 10px;border-radius:99px;font-size:11px;font-weight:700;
  background:rgba(92,155,214,0.12);color:var(--dli-color);border:1px solid rgba(92,155,214,0.2);
}}

.lib-status-chip{{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:99px;font-size:12px;font-weight:600;}}
.lib-status-chip.ideal{{background:var(--surface-solid);color:var(--accent);border:1px solid var(--accent-glow);box-shadow:0 2px 8px var(--accent-dim);}}
.lib-status-chip.ok{{background:var(--surface-solid);color:#d38e53;border:1px solid rgba(226,167,111,0.4);box-shadow:0 2px 8px var(--warn-dim);}}
.lib-status-chip.bad{{background:var(--surface-solid);color:var(--danger);border:1px solid rgba(229,115,115,0.4);box-shadow:0 2px 8px var(--danger-dim);}}
.lib-status-chip.none{{background:var(--surface-solid);color:var(--muted);border:1px solid var(--border)}}

.lib-card-footer{{display:flex;align-items:center;gap:12px;padding:0 20px 20px;margin-top:auto;}}
.show-on-map-btn{{
  flex:1;padding:12px;border-radius:var(--r);font-size:13px;font-weight:600;
  background:var(--surface-solid);border:1px solid var(--border);color:var(--text);
  transition:all var(--transition);box-shadow:0 2px 8px rgba(45,71,57,0.02);
}}
.show-on-map-btn:hover{{background:var(--bg);border-color:var(--accent-glow);color:var(--accent);transform:translateY(-1px);box-shadow:0 4px 12px rgba(45,71,57,0.05);}}

/* ── PFLEGE-KALENDER VIEW ── */
#care-view{{display:none;flex:1;overflow-y:auto;padding:24px 32px;flex-direction:column;gap:20px}}
#care-view.active{{display:flex}}
#care-view::-webkit-scrollbar{{width:8px}}
#care-view::-webkit-scrollbar-thumb{{background:var(--border-2);border-radius:4px}}

.care-header{{
  display:flex;align-items:center;gap:16px;flex-shrink:0;flex-wrap:wrap;
  background:var(--surface);padding:24px;border-radius:var(--rx);border:1px solid var(--border);
  backdrop-filter:blur(16px);box-shadow:0 8px 32px rgba(45,71,57,0.04);
}}
.care-header h2{{font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:var(--text);}}
.care-header-sub{{font-size:14px;font-weight:500;color:var(--muted);margin-top:4px}}
.care-header-actions{{margin-left:auto;display:flex;gap:10px;align-items:center;flex-wrap:wrap;}}
.care-mass-btn{{
  padding:10px 20px;font-size:13px;font-weight:600;border-radius:99px;
  border:1px solid var(--border);background:var(--surface-solid);color:var(--text);
  transition:all var(--transition);box-shadow:0 2px 8px rgba(45,71,57,0.02);cursor:pointer;
}}
.care-mass-btn:hover{{background:var(--bg);border-color:var(--accent-glow);color:var(--accent);transform:translateY(-1px);}}
.care-mass-btn.primary{{background:var(--accent);border-color:var(--accent);color:#fff;}}
.care-mass-btn.primary:hover{{background:#6aa335;box-shadow:0 4px 16px var(--accent-glow);transform:translateY(-1px);}}

/* Care Sub-tabs */
.care-subtabs{{
  display:flex;gap:8px;background:var(--surface-solid);border:1px solid var(--border);
  border-radius:var(--rx);padding:6px;box-shadow:0 4px 16px rgba(45,71,57,0.03);flex-shrink:0;
}}
.care-subtab{{
  flex:1;padding:10px 20px;font-size:13px;font-weight:600;color:var(--muted);
  border-radius:var(--r);transition:all var(--transition);
}}
.care-subtab:hover{{color:var(--text);background:var(--surface-2);}}
.care-subtab.active{{background:var(--accent);color:#fff;box-shadow:0 4px 12px var(--accent-glow);}}

/* Calendar Grid */
#care-calendar-pane{{display:flex;flex-direction:column;gap:20px;}}
#care-status-pane{{display:none;flex-direction:column;gap:16px;}}

.calendar-wrap{{
  background:var(--surface-solid);border:1px solid var(--border);border-radius:var(--rx);
  overflow:hidden;box-shadow:0 8px 32px rgba(45,71,57,0.04);
}}
.calendar-nav{{
  display:flex;align-items:center;justify-content:space-between;padding:20px 24px;
  border-bottom:1px solid var(--border);
}}
.calendar-nav-title{{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:var(--text);}}
.calendar-nav-btn{{
  width:36px;height:36px;border-radius:50%;border:1px solid var(--border);
  background:var(--surface-solid);color:var(--text);font-size:16px;
  display:flex;align-items:center;justify-content:center;
  transition:all var(--transition);cursor:pointer;
}}
.calendar-nav-btn:hover{{background:var(--surface-2);border-color:var(--accent-glow);transform:scale(1.08);}}
.cal-grid{{display:grid;grid-template-columns:repeat(7,1fr);}}
.cal-day-header{{
  padding:12px 8px;text-align:center;font-size:11px;font-weight:700;color:var(--muted);
  text-transform:uppercase;letter-spacing:.06em;background:var(--bg);border-bottom:1px solid var(--border);
}}
.cal-cell{{
  min-height:90px;padding:10px 8px;border-right:1px solid var(--border);border-bottom:1px solid var(--border);
  position:relative;transition:background .2s;
}}
.cal-cell:nth-child(7n){{border-right:none;}}
.cal-cell:nth-last-child(-n+7){{border-bottom:none;}}
.cal-cell.other-month .cal-day-num{{color:var(--muted2);opacity:.5;}}
.cal-cell.today{{background:linear-gradient(135deg,rgba(124,179,66,0.06),rgba(124,179,66,0.02));}}
.cal-cell.today .cal-day-num{{
  background:var(--accent);color:#fff;width:28px;height:28px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-weight:700;
  box-shadow:0 2px 8px var(--accent-glow);
}}
.cal-day-num{{font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px;width:28px;height:28px;display:flex;align-items:center;justify-content:center;}}
.cal-events{{display:flex;flex-direction:column;gap:3px;}}
.cal-event{{
  font-size:10px;font-weight:600;padding:2px 6px;border-radius:4px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}}
.cal-event.water{{background:rgba(100,181,246,0.15);color:#1565C0;}}
.cal-event.fertilize{{background:var(--accent-dim);color:var(--accent-dark);}}
.cal-event.due-water{{background:rgba(100,181,246,0.3);color:#1565C0;border:1px solid rgba(100,181,246,0.4);}}
.cal-event.due-fertilize{{background:rgba(124,179,66,0.25);color:var(--accent-dark);border:1px solid var(--accent-glow);}}

/* Care Status Pane */
.care-section-title{{
  font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:var(--text);
  display:flex;align-items:center;gap:10px;margin-bottom:4px;
}}
.care-section-title .care-badge{{
  font-family:'DM Sans',sans-serif;font-size:12px;font-weight:600;padding:3px 10px;
  border-radius:99px;background:var(--danger-dim);color:var(--danger);border:1px solid rgba(229,115,115,0.3);
}}
.care-section-title .care-badge.warn{{background:var(--warn-dim);color:#c27a3e;border-color:rgba(226,167,111,0.3);}}
.care-section-title .care-badge.ok{{background:var(--surface-2);color:var(--accent);border-color:var(--accent-glow);}}

/* Pflege-Karten */
.care-card{{
  background:var(--surface-solid);border:1px solid var(--border);border-radius:var(--rx);
  padding:20px;display:flex;align-items:center;gap:16px;
  transition:all var(--transition);box-shadow:0 4px 16px rgba(45,71,57,0.03);
  position:relative;overflow:hidden;
}}
.care-card::before{{
  content:'';position:absolute;left:0;top:0;bottom:0;width:4px;
  background:var(--accent);border-radius:0;transition:background .3s;
}}
.care-card.overdue::before{{background:var(--danger);}}
.care-card.soon::before{{background:var(--warn);}}
.care-card.done::before{{background:var(--muted2);}}
.care-card:hover{{box-shadow:0 8px 32px rgba(45,71,57,0.07);transform:translateY(-1px);}}

/* Care card plant thumbnail */
.care-card-thumb{{
  width:52px;height:52px;border-radius:var(--r);overflow:hidden;flex-shrink:0;
  background:var(--surface-2);border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;
}}
.care-card-thumb img{{width:100%;height:100%;object-fit:cover;}}
.care-card-thumb-emoji{{font-size:26px;}}
.care-card-info{{flex:1;min-width:0}}
.care-card-name{{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:var(--text);margin-bottom:4px;}}
.care-card-meta{{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:10px;}}
.care-chip{{
  font-size:11px;font-weight:600;padding:3px 10px;border-radius:99px;
  background:var(--surface-2);color:var(--muted);border:1px solid var(--border);
}}
.care-chip.overdue{{background:var(--danger-dim);color:var(--danger);border-color:rgba(229,115,115,0.3);}}
.care-chip.soon{{background:var(--warn-dim);color:#c27a3e;border-color:rgba(226,167,111,0.3);}}
.care-chip.ok{{background:var(--surface-2);color:var(--accent);border-color:var(--accent-glow);}}

/* Progress bars for water and fertilizer */
.care-progress-wrap{{display:flex;flex-direction:column;gap:6px;margin-bottom:8px;}}
.care-progress-row{{display:flex;align-items:center;gap:8px;}}
.care-progress-icon{{font-size:12px;flex-shrink:0;width:16px;}}
.care-progress-track{{flex:1;height:5px;border-radius:3px;background:rgba(45,71,57,0.08);overflow:hidden;}}
.care-progress-fill{{height:100%;border-radius:3px;transition:width 1s cubic-bezier(.34,1.56,.64,1);}}
.care-progress-fill.water{{background:linear-gradient(90deg,rgba(100,181,246,0.5),#64B5F6);}}
.care-progress-fill.fertilize{{background:linear-gradient(90deg,var(--accent-dim),var(--accent));}}
.care-progress-pct{{font-size:10px;font-weight:700;color:var(--muted);min-width:30px;text-align:right;}}

.moisture-wrap{{display:flex;align-items:center;gap:8px;}}
.moisture-label{{font-size:11px;font-weight:600;color:var(--muted);min-width:64px;}}
.moisture-track{{flex:1;height:6px;border-radius:3px;background:rgba(45,71,57,0.08);overflow:hidden;}}
.moisture-fill{{height:100%;border-radius:3px;transition:width 1s cubic-bezier(.34,1.56,.64,1);}}

.care-card-actions{{display:flex;flex-direction:column;gap:8px;flex-shrink:0;}}
.care-btn{{
  padding:9px 16px;font-size:12px;font-weight:600;border-radius:var(--r);
  border:1px solid var(--border);background:var(--surface-solid);color:var(--text);
  transition:all var(--transition);cursor:pointer;white-space:nowrap;
  box-shadow:0 2px 8px rgba(45,71,57,0.02);
}}
.care-btn:hover{{background:var(--bg);transform:translateY(-1px);}}
.care-btn:active{{transform:scale(0.96);}}
.care-btn.water{{border-color:rgba(100,181,246,0.5);color:#1976d2;background:rgba(100,181,246,0.08);}}
.care-btn.water:hover{{background:rgba(100,181,246,0.15);box-shadow:0 4px 12px rgba(100,181,246,0.15);}}
.care-btn.fertilize{{border-color:var(--accent-glow);color:var(--accent);background:var(--surface-2);}}
.care-btn.fertilize:hover{{background:var(--surface-3);box-shadow:0 4px 12px var(--accent-dim);}}
.care-btn.done-btn{{opacity:.5;pointer-events:none;}}

/* Historie */
.care-history{{
  background:var(--surface-solid);border:1px solid var(--border);border-radius:var(--rx);
  overflow:hidden;box-shadow:0 4px 16px rgba(45,71,57,0.03);
}}
.care-history-header{{
  padding:16px 20px;border-bottom:1px solid var(--border);
  font-family:'Syne',sans-serif;font-size:14px;font-weight:700;color:var(--text);
  display:flex;align-items:center;gap:10px;
}}
.history-entry{{
  display:flex;align-items:center;gap:12px;padding:12px 20px;
  border-bottom:1px solid var(--border);font-size:13px;
  transition:background .2s;
}}
.history-entry:last-child{{border-bottom:none}}
.history-entry:hover{{background:var(--bg);}}
.history-icon{{font-size:16px;flex-shrink:0;}}
.history-text{{flex:1;color:var(--text);font-weight:500;}}
.history-time{{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;}}

.care-empty{{
  text-align:center;padding:48px 24px;color:var(--muted);
  background:var(--surface-solid);border:1px dashed var(--border-2);border-radius:var(--rx);
}}
.care-empty .ce-icon{{font-size:48px;margin-bottom:12px;opacity:.5}}
.care-empty p{{font-size:14px;font-weight:500;line-height:1.6;}}

/* ── TOAST & TOOLTIP ── */
#tooltip{{
  position:fixed;z-index:500;pointer-events:none;
  background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);border:1px solid var(--border-2);
  border-radius:var(--rs);padding:10px 14px;font-size:12px;font-weight:600;color:var(--text);
  box-shadow:0 8px 24px rgba(45,71,57,0.08);opacity:0;transition:opacity .15s;
  max-width:240px;
}}
#tooltip.visible{{opacity:1}}

#save-toast{{
  position:fixed;bottom:24px;right:24px;z-index:999;
  background:var(--surface-solid);border:1px solid var(--accent-glow);
  border-radius:var(--r);padding:14px 20px;font-size:14px;font-weight:600;color:var(--text);
  box-shadow:0 8px 32px rgba(124,179,66,0.15);
  transform:translateY(30px);opacity:0;
  transition:all .4s cubic-bezier(.34, 1.56, .64, 1);
  display:flex;align-items:center;gap:10px;
}}
#save-toast.show{{transform:translateY(0);opacity:1}}

/* ── LOADING ── */
#loading{{
  position:fixed;inset:0;z-index:9999;background:var(--bg);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;
  transition:opacity .6s,visibility .6s;
}}
#loading.hidden{{opacity:0;visibility:hidden}}
#loading .ld-icon{{font-size:54px;animation:pulse 2s ease-in-out infinite}}
#loading p{{font-size:16px;font-weight:500;color:var(--text)}}
@keyframes pulse{{0%,100%{{transform:scale(1);opacity:.6}}50%{{transform:scale(1.1);opacity:1}}}}
</style>
</head>
<body>

<div id="loading"><div class="ld-icon">🌿</div><p>Natürliches Umfeld wird geladen…</p></div>
<div id="tooltip"></div>
<div id="save-toast">💾 <span id="toast-msg">Gespeichert</span></div>

<!-- HEADER -->
<div id="header">
  <span class="logo">🌿 Pflanzen-Planer Pro</span>
  <span class="logo-sep">|</span>
  <span style="font-size:14px;font-weight:500;color:var(--text)" id="month-label"></span>
  <div class="header-meta">
    <div class="sun-info">
      <div class="sun-dot"></div>
      <span id="sun-label">Sonnenstand wird berechnet…</span>
    </div>
    <div class="status-wrap">
      <div class="sdot" id="sdot"></div>
      <span id="stext">Verbinden…</span>
    </div>
  </div>
</div>

<!-- TABS -->
<div id="tabs">
  <button class="tab active" data-tab="planer" onclick="switchTab('planer')">
    <span class="tab-icon">🗺️</span> Grundriss-Planer
  </button>
  <button class="tab" data-tab="library" onclick="switchTab('library')">
    <span class="tab-icon">📚</span> Pflanzen-Bibliothek
  </button>
  <button class="tab" data-tab="care" onclick="switchTab('care')">
    <span class="tab-icon">🌱</span> Pflege-Kalender
  </button>
</div>

<!-- MAIN -->
<div id="main">

  <!-- LEFT SIDEBAR -->
  <div id="left-sidebar">
    <div class="sidebar-header">
      <span>🪴 Inventar</span>
      <span id="inv-count" style="font-size:12px;background:var(--surface-2);color:var(--text);padding:4px 10px;border-radius:99px;font-weight:600"></span>
    </div>
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
    <div class="dli-toggle-wrap">
      <span class="dli-toggle-label">📊 DLI-Modus</span>
      <button class="dli-toggle" id="dli-toggle-btn" onclick="toggleDLIMode()"></button>
    </div>
    <div id="map-canvas">
      <img id="floor-img" src="" alt="Grundriss" draggable="false"
           onerror="this.src='https://placehold.co/1100x600/FCFAF7/7CB342?text=Grundriss+nicht+gefunden'">
      <canvas id="light-canvas"></canvas>
    </div>
  </div>

  <!-- LIBRARY VIEW -->
  <div id="library-view">
    <div class="lib-header">
      <div>
        <h2>🌱 Pflanzen-Bibliothek</h2>
        <div class="lib-header-sub" id="lib-sub-label"></div>
      </div>
      <input class="lib-search" id="lib-search" type="text" placeholder="🔍 Pflanze suchen…" oninput="filterLibrary(this.value)">
    </div>
    <div class="lib-grid" id="lib-grid"></div>
  </div>

  <!-- CARE VIEW -->
  <div id="care-view">
    <div class="care-header">
      <div>
        <h2>🌱 Pflege-Kalender</h2>
        <div class="care-header-sub" id="care-sub-label">Lade Pflegedaten…</div>
      </div>
      <div class="care-header-actions">
        <button class="care-mass-btn" onclick="waterAllDue()">💧 Alle fälligen gießen</button>
        <button class="care-mass-btn primary" onclick="refreshCare()">🔄 Aktualisieren</button>
      </div>
    </div>

    <!-- Sub-tabs -->
    <div class="care-subtabs">
      <button class="care-subtab active" id="subtab-calendar" onclick="switchCareSubtab('calendar')">📅 Kalender</button>
      <button class="care-subtab" id="subtab-status" onclick="switchCareSubtab('status')">📋 Pflege-Status</button>
      <button class="care-subtab" id="subtab-history" onclick="switchCareSubtab('history')">🕐 Historie</button>
    </div>

    <!-- Calendar pane -->
    <div id="care-calendar-pane">
      <div class="calendar-wrap">
        <div class="calendar-nav">
          <button class="calendar-nav-btn" onclick="changeCalMonth(-1)">‹</button>
          <span class="calendar-nav-title" id="cal-month-title"></span>
          <button class="calendar-nav-btn" onclick="changeCalMonth(1)">›</button>
        </div>
        <div class="cal-grid" id="cal-grid"></div>
      </div>
    </div>

    <!-- Status pane -->
    <div id="care-status-pane">
      <div id="care-overdue-section"></div>
      <div id="care-soon-section"></div>
      <div id="care-all-section"></div>
    </div>

    <!-- History pane -->
    <div id="care-history-pane" style="display:none">
      <div id="care-history-section"></div>
    </div>
  </div>

  <!-- RIGHT SIDEBAR -->
  <div id="right-sidebar">
    <div id="rsb-empty">
      <div class="empty-icon">🪴</div>
      <p style="font-size:14px;line-height:1.6;color:var(--muted);font-weight:500;">Klicke auf eine Pflanze<br>für Details &amp; Pflegehinweise.</p>
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
let careData        = {{}};
let careHistory     = [];
let activePIdx      = null;
let currentFloor    = "EG";
let currentTab      = "planer";
let currentCareSubtab = "calendar";
let dragSrcIdx      = null;
let inventoryFilter = "";
let libraryFilter   = "";
let saveTimeout     = null;
let sunState        = {{ azimuth:180, elevation:0, factor:0 }};
let dliMode         = false;      // DLI overlay vs. live overlay
let dliCache        = {{}};        // floor -> Map of "rx,ry" -> dliScore
let calMonth        = NOW_MONTH;
let calYear         = NOW.getFullYear();

// ============================================================
// UTILITY
// ============================================================
const $ = id => document.getElementById(id);

function setStatus(ok, msg) {{
  $("sdot").className = "sdot"+(ok?" ok":"");
  $("stext").textContent = msg;
}}

function showTooltip(msg, x, y) {{
  const t = $("tooltip");
  t.textContent = msg;
  t.style.left = (x+16)+"px";
  t.style.top  = (y+16)+"px";
  t.classList.add("visible");
}}
function hideTooltip() {{ $("tooltip").classList.remove("visible"); }}

function showToast(msg, dur=2200) {{
  $("toast-msg").textContent = msg;
  $("save-toast").classList.add("show");
  setTimeout(()=>$("save-toast").classList.remove("show"), dur);
}}

$("month-label").textContent = MONTHS_DE[NOW_MONTH]+" "+NOW.getFullYear();

// ============================================================
// ★ ASTRONOMISCHE LICHTSIMULATION
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

  const GMST = (6.697375 + 0.0657098242*n + (date.getUTCHours()+(date.getUTCMinutes()+date.getUTCSeconds()/60)/60)) % 24;
  const LMST = (GMST*15 + LON_DEG_VAL) % 360;
  const HA   = (LMST - RA*180/Math.PI) * Math.PI/180;

  const sinElev = Math.sin(LAT_RAD)*Math.sin(dec) + Math.cos(LAT_RAD)*Math.cos(dec)*Math.cos(HA);
  const elev    = Math.asin(sinElev);
  const cosAz   = (Math.sin(dec) - Math.sin(elev)*Math.sin(LAT_RAD)) / (Math.cos(elev)*Math.cos(LAT_RAD));
  const azBase  = Math.acos(Math.max(-1,Math.min(1,cosAz))) * 180/Math.PI;
  const az      = Math.sin(HA)>0 ? 360-azBase : azBase;

  const elevDeg = elev * 180/Math.PI;

  let airmass = 1;
  if(elevDeg > 0) airmass = 1 / (Math.sin(elev) + 0.50572*Math.pow(elevDeg+6.07995,-1.6364));

  const transmit = elevDeg > 0 ? Math.pow(0.7, Math.pow(airmass, 0.678)) : 0;

  return {{ azimuth:az, elevation:elevDeg, transmittance:transmit, factor:transmit }};
}}

// ============================================================
// ★ DLI (Daily Light Integral) SIMULATION
// Simuliert Sonnenverlauf in 1h-Schritten, berechnet gewichteten
// Tagesmittelwert (0-10) für jeden Punkt auf der Karte.
// ============================================================
function computeDLI(px, py, floor) {{
  const today = new Date();
  const year  = today.getFullYear();
  const month = today.getMonth();
  const day   = today.getDate();

  let sumScore   = 0;
  let weightSum  = 0;

  // Simuliere 24 Stunden in 1h-Schritten
  for(let h = 0; h < 24; h++) {{
    const dt = new Date(Date.UTC(year, month, day, h - 1, 0, 0)); // UTC offset ~-1 für MEZ
    const sun = calcSunPosition(dt);
    if(sun.elevation <= 0) continue; // Nacht überspringen

    // Speichere sunState temporär
    const savedState = {{...sunState}};
    sunState = sun;
    const score = computeLichtFull(px, py, floor).score;
    sunState = savedState;

    // Gewichtung nach Sonnenelevation (sin-Kurve = natürliche Tageskurve)
    const weight = Math.sin(sun.elevation * Math.PI / 180);
    sumScore  += score * weight;
    weightSum += weight;
  }}

  if(weightSum === 0) return 1; // Polarnacht / Sonderfälle
  return Math.min(10, Math.max(1, Math.round(sumScore / weightSum * 10) / 10));
}}

// DLI-Cache befüllen (asynchron, nach Frame)
let dliComputeScheduled = false;
function scheduleDLICompute(floor) {{
  if(dliComputeScheduled) return;
  dliComputeScheduled = true;
  requestAnimationFrame(()=>{{
    dliComputeScheduled = false;
    if(!dliMode) return;
    const fd   = FLOOR_DATA[floor];
    const step = 0.05; // 5% Schritte = 400 Punkte pro Etage
    const cache = {{}};
    for(let ry=0; ry<=1.01; ry+=step) {{
      for(let rx=0; rx<=1.01; rx+=step) {{
        const key = `${{rx.toFixed(2)}},${{ry.toFixed(2)}}`;
        cache[key] = computeDLI(rx, ry, floor);
      }}
    }}
    dliCache[floor] = cache;
    drawLightMap();
  }});
}}

function getDLIScore(px, py, floor) {{
  if(!dliCache[floor]) return null;
  // Finde nächsten Cache-Punkt
  const step = 0.05;
  const rx = Math.round(px / step) * step;
  const ry = Math.round(py / step) * step;
  const key = `${{rx.toFixed(2)}},${{ry.toFixed(2)}}`;
  return dliCache[floor]?.[key] ?? null;
}}

function toggleDLIMode() {{
  dliMode = !dliMode;
  const btn = $("dli-toggle-btn");
  btn.classList.toggle("on", dliMode);
  if(dliMode) {{
    showToast("📊 DLI-Modus: Tages-Durchschnitt wird berechnet…", 3000);
    scheduleDLICompute(currentFloor);
  }} else {{
    drawLightMap();
  }}
  render();
}}

// ============================================================
// ★ PHYSIKALISCH KORREKTE LICHTSIMULATION
// ============================================================
const WIN_SAMPLES = 7;

function skyDiffuse(sunElevDeg) {{
  if(sunElevDeg <= -6) return 0;
  if(sunElevDeg <= 0)  return 0.05;
  return 0.10 + 0.05 * Math.min(1, sunElevDeg / 30);
}}

function windowAzimuth(side, buildingNorthAzimuth) {{
  const sideOffset = {{"N":0,"E":90,"S":180,"W":270}};
  const offset = sideOffset[side] ?? 180;
  return (buildingNorthAzimuth + offset) % 360;
}}

function directSunFactor(winAz, sunAz, sunElevDeg) {{
  if(sunElevDeg <= 0) return 0;
  const diff    = Math.abs(((winAz - sunAz + 540) % 360) - 180);
  const cosHoriz = Math.cos(diff * Math.PI / 180);
  if(cosHoriz <= 0) return 0;
  const sinElev = Math.sin(sunElevDeg * Math.PI / 180);
  return cosHoriz * sinElev;
}}

function roomPenetrationFactor(sunElevDeg, winSide, buildingNorthAzimuth) {{
  if(sunElevDeg <= 0) return 0;
  const elev = Math.max(5, Math.min(80, sunElevDeg));
  return 1 - (elev - 5) / 80;
}}

function updateSunInfo() {{
  const now = new Date();
  sunState  = calcSunPosition(now);

  const elev = sunState.elevation.toFixed(1);
  const az   = sunState.azimuth.toFixed(0);
  if(sunState.elevation > 0) {{
    $("sun-label").textContent = `☀️ Elevation ${{elev}}° · Azimut ${{az}}° · Stärke ${{(sunState.factor*100).toFixed(0)}}%`;
  }} else {{
    $("sun-label").textContent = `🌙 Sonne unter Horizont (${{elev}}°)`;
  }}
}}

function segmentsIntersect(ax,ay,bx,by, cx,cy,dx,dy) {{
  const denom = (bx-ax)*(dy-cy)-(by-ay)*(dx-cx);
  if(Math.abs(denom)<1e-9) return false;
  const t = ((cx-ax)*(dy-cy)-(cy-ay)*(dx-cx))/denom;
  const u = ((cx-ax)*(by-ay)-(cy-ay)*(bx-ax))/denom;
  const eps = 1e-6;
  return t>eps && t<1-eps && u>eps && u<1-eps;
}}

function isBlockedByInnerWall(pAX, pAY, sAX, sAY, fd) {{
  for(const w of fd.walls) {{
    if(segmentsIntersect(pAX,pAY,sAX,sAY, w.x1,w.y1,w.x2,w.y2)) return true;
  }}
  return false;
}}

function isBlockedByOuterWall(pAX, pAY, sAX, sAY, fd) {{
  for(const seg of fd.outerWalls) {{
    if(segmentsIntersect(pAX,pAY,sAX,sAY, seg.x1,seg.y1,seg.x2,seg.y2)) return true;
  }}
  return false;
}}

function px2rel(px, p1, p2) {{ return (px-p1)/(p2-p1); }}

function computeLichtFull(px, py, floor) {{
  const fd    = FLOOR_DATA[floor];
  const fw    = fd.floorX2 - fd.floorX1;
  const fh    = fd.floorY2 - fd.floorY1;
  const realW = fd.realW;
  const realH = fd.realH;
  const bldAz = fd.buildingNorthAzimuth || 0;

  const pAX = fd.floorX1 + px * fw;
  const pAY = fd.floorY1 + py * fh;

  const margin = 4;
  if(pAX < fd.floorX1-margin || pAX > fd.floorX2+margin ||
     pAY < fd.floorY1-margin || pAY > fd.floorY2+margin) {{
    return {{ score:1, components:{{}}, windowHits:[] }};
  }}

  const sunElevDeg = sunState.elevation;
  const sunAzDeg   = sunState.azimuth;
  const sunDirect  = sunState.factor;
  const skyDiff    = skyDiffuse(sunElevDeg);
  const wallReflectance = 0.15;

  let totalIlluminance = 0;
  const windowHits = [];

  for(const w of fd.windows) {{
    const winAz = windowAzimuth(w.side, bldAz);
    let winContrib      = 0;
    let samplesVisible  = 0;
    let totalSamples    = 0;
    let bestIncFactor   = 0;

    for(let s=0; s<WIN_SAMPLES; s++) {{
      const t = WIN_SAMPLES===1 ? 0.5 : s/(WIN_SAMPLES-1);
      const sAX = w.x1 + t*(w.x2-w.x1);
      const sAY = w.y1 + t*(w.y2-w.y1);

      totalSamples++;

      if(isBlockedByInnerWall(pAX,pAY,sAX,sAY,fd)) continue;
      if(isBlockedByOuterWall(pAX,pAY,sAX,sAY,fd)) continue;

      samplesVisible++;

      const dxM   = (px - px2rel(sAX,fd.floorX1,fd.floorX2)) * realW;
      const dyM   = (py - px2rel(sAY,fd.floorY1,fd.floorY2)) * realH;
      const distM = Math.sqrt(dxM*dxM + dyM*dyM);

      const incFactor = directSunFactor(winAz, sunAzDeg, sunElevDeg);
      bestIncFactor = Math.max(bestIncFactor, incFactor);

      const penetration = roomPenetrationFactor(sunElevDeg, w.side, bldAz);
      const kDirect = 0.2 + 0.6*(1-penetration);
      const directContrib = incFactor * sunDirect / (1 + kDirect * distM * distM);

      const kDiffuse = 0.3;
      const diffuseContrib = skyDiff / (1 + kDiffuse * distM);

      winContrib += directContrib + diffuseContrib;
    }}

    if(totalSamples > 0) {{
      const avgContrib = winContrib / totalSamples;
      const winPxLen = Math.sqrt((w.x2-w.x1)**2 + (w.y2-w.y1)**2);
      const isVertical = Math.abs(w.x2-w.x1) < Math.abs(w.y2-w.y1);
      const winMeter = isVertical
        ? (winPxLen / fh) * realH
        : (winPxLen / fw) * realW;
      const winSizeFactor = Math.min(3, winMeter) / 1.0;
      totalIlluminance += avgContrib * winSizeFactor;
    }}

    windowHits.push({{
      side:       w.side,
      winAz:      winAz.toFixed(0),
      incFactor:  bestIncFactor.toFixed(2),
      visRatio:   (samplesVisible/totalSamples).toFixed(2),
      occluded:   samplesVisible === 0,
    }});
  }}

  totalIlluminance *= (1 + wallReflectance);

  const scaleFactor = 22;
  const score = Math.min(10, Math.max(1, Math.round(totalIlluminance * scaleFactor * 10) / 10));

  return {{
    score,
    components: {{ totalIlluminance, skyDiff, sunDirect }},
    windowHits,
  }};
}}

function computeLicht(px, py, floor) {{
  return computeLichtFull(px, py, floor).score;
}}

function getLichtStatus(ist, soll) {{
  if(ist>=soll)   return "ideal";
  if(ist>=soll-2) return "ok";
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
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const fd  = FLOOR_DATA[currentFloor];
  const fw  = fd.floorX2-fd.floorX1, fh = fd.floorY2-fd.floorY1;
  const step= 20;

  for(let iy=fd.floorY1; iy<=fd.floorY2; iy+=step) {{
    for(let ix=fd.floorX1; ix<=fd.floorX2; ix+=step) {{
      const rx=(ix-fd.floorX1)/fw, ry=(iy-fd.floorY1)/fh;
      let lv;
      if(dliMode) {{
        const cached = getDLIScore(rx, ry, currentFloor);
        lv = cached !== null ? cached : computeLicht(rx, ry, currentFloor);
        // DLI mode: blue tint
        const alpha = (lv/10)*0.28;
        const r = Math.round(92 + (lv/10)*50);
        const g = Math.round(155 + (lv/10)*30);
        const b = Math.round(214 - (lv/10)*50);
        ctx.fillStyle=`rgba(${{r}},${{g}},${{b}},${{alpha.toFixed(3)}})`;
      }} else {{
        lv = computeLicht(rx, ry, currentFloor);
        const alpha=(lv/10)*0.25;
        const r = Math.round(lv/10*251), g=222, b=Math.round((1-lv/10)*128+74);
        ctx.fillStyle=`rgba(${{r}},${{g}},${{b}},${{alpha.toFixed(3)}})`;
      }}
      ctx.fillRect(ix,iy,step,step);
    }}
  }}
}}

// ============================================================
// IMAGE READY
// ============================================================
function onImageReady() {{
  const img  = $("floor-img");
  const cvs  = $("map-canvas");
  const W    = img.naturalWidth||1100, H = img.naturalHeight||600;
  cvs.style.width=W+"px"; cvs.style.height=H+"px";
  const area = $("map-area");
  const scale= Math.min(1,(area.clientWidth-40)/W,(area.clientHeight-40)/H);
  cvs.style.transform=`translate(-50%,-50%) scale(${{scale}})`;
}}
$("floor-img").addEventListener("load",()=>{{onImageReady();drawLightMap();render();}});
window.addEventListener("resize",onImageReady);

// ============================================================
// PLANT IMAGE URL
// ============================================================
function getPlantImageUrl(plantName) {{
  const safeName = plantName.replace(/\s+/g, '%20');
  return `${{GITHUB_BASE}}/${{safeName}}.png`;
}}

function makePlantImgTag(plant, cls, style) {{
  const url = getPlantImageUrl(plant.name);
  const fallback = plant.emoji || '🌿';
  return `<img src="${{url}}" class="${{cls}}" style="${{style||''}}"
    onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
  <div style="display:none;width:100%;height:100%;align-items:center;justify-content:center;font-size:54px;opacity:.4;">${{fallback}}</div>`;
}}

// ============================================================
// CSV LOAD
// ============================================================
async function loadPlants() {{
  setStatus(false,"Lade Daten…");
  try {{
    const res = await fetch(CSV_URL);
    if(!res.ok) throw new Error("HTTP "+res.status);
    const text = await res.text();
    plants = parseCSV(text);
    setStatus(true, plants.length+" Pflanzen geladen");
  }} catch(e) {{
    console.warn("CSV-Fehler:",e);
    plants = [
      {{name:"Monstera Deliciosa",botanisch:"Monstera deliciosa",licht:7,giessen:3,dungen:4,umtopfen:"Alle 2 Jahre",info:"Robuste Zimmerpflanze",emoji:"🌿",luftfeuchtigkeit:"60-80%",besprühen:"Ja",besonderheit:"Bekannt für ihre spektakulären Blattlöcher.",giessAll:{{}},duengAll:{{}}}},
      {{name:"Sukkulente",botanisch:"Echeveria spp.",licht:9,giessen:14,dungen:8,umtopfen:"Alle 3 Jahre",info:"Viel Sonne",emoji:"🌵",luftfeuchtigkeit:"30-50%",besprühen:"Nein",besonderheit:"Speichert Wasser in Blättern – extrem pflegeleicht.",giessAll:{{}},duengAll:{{}}}},
    ];
    setStatus(false,"Offline-Modus");
  }}
  plants.forEach((p,i)=>{{ if(!p.emoji) p.emoji=PLANT_EMOJIS[i%PLANT_EMOJIS.length]; }});
  $("inv-count").textContent = plants.length;

  loadPositionsLocal();
  loadCareData();

  renderInventory();
  renderLibrary();
  setFloor(currentFloor);
  $("loading").classList.add("hidden");
  updateSunInfo();
  renderCalendar();
  setInterval(()=>{{ updateSunInfo(); drawLightMap(); render(); }}, 60000);
}}

// ============================================================
// CSV PARSE — erweitert mit neuen Spalten
// ============================================================
function parseCSV(text) {{
  const lines   = text.trim().split("\\n");
  const headers = lines[0].split(",").map(h=>h.trim().replace(/"/g,""));
  const col = (cands) => {{
    for(const c of cands) {{
      const idx=headers.findIndex(h=>h.toLowerCase().includes(c.toLowerCase()));
      if(idx>=0) return idx;
    }}
    return -1;
  }};

  const colName      = col(["Pflanze","Name","name"]);
  const colBotanisch = col(["Botanischer","botanisch","Botanisch"]);
  const colLicht     = col(["Lichtbedarf"]);
  const colUmtopf    = col(["Umtopfen"]);
  const colLuft      = col(["Luftfeuchtigkeit","Optimale Luftfeu","luftfeucht"]);
  const colBespr     = col(["Besprühen","Bespruhen","besprühen"]);
  const colBesond    = col(["Besonderheit","besonderheit"]);

  const monthName = MONTHS_DE[NOW_MONTH];
  const colGiess  = col(["Gießen_"+monthName,"Giessen_"+monthName]);
  const colDueng  = col(["Düngen_"+monthName,"Dunegen_"+monthName,"Düngen_"+monthName]);
  const giessAll={{}}, duengAll={{}};
  MONTHS_DE.forEach(m=>{{
    giessAll[m]=col(["Gießen_"+m,"Giessen_"+m]);
    duengAll[m]=col(["Düngen_"+m,"Dunegen_"+m,"Düngen_"+m]);
  }});

  return lines.slice(1).filter(l=>l.trim()).map((line,i)=>{{
    const cols=splitCSVLine(line);
    const safeCol = (idx) => idx>=0 ? (cols[idx]||"").trim().replace(/"/g,"") : "";

    const obj={{
      id:i,
      name:          safeCol(colName) || "Pflanze "+(i+1),
      botanisch:     safeCol(colBotanisch),
      licht:         parseFloat(safeCol(colLicht))||5,
      giessen:       colGiess>=0 ? (safeCol(colGiess)||"—") : "—",
      dungen:        colDueng>=0 ? (safeCol(colDueng)||"—") : "—",
      umtopfen:      safeCol(colUmtopf)||"—",
      luftfeuchtigkeit: safeCol(colLuft)||"",
      besprühen:     safeCol(colBespr)||"",
      besonderheit:  safeCol(colBesond)||"",
      emoji:         PLANT_EMOJIS[i%PLANT_EMOJIS.length],
      giessAll:{{}}, duengAll:{{}},
    }};
    MONTHS_DE.forEach(m=>{{
      obj.giessAll[m] = giessAll[m]>=0 ? (safeCol(giessAll[m])||"—") : "—";
      obj.duengAll[m] = duengAll[m]>=0 ? (safeCol(duengAll[m])||"—") : "—";
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
// ★ PERSISTENZ
// ============================================================
function savePositionsLocal() {{
  try {{ localStorage.setItem("pflanzen_positions_v2", JSON.stringify(positions)); }}
  catch(e) {{ console.warn("localStorage write failed:", e); }}
}}

function loadPositionsLocal() {{
  try {{
    const raw = localStorage.getItem("pflanzen_positions_v2");
    if(raw) positions = JSON.parse(raw);
  }} catch(e) {{ positions = {{}}; }}
}}

function saveCareData() {{
  try {{
    localStorage.setItem("pflanzen_care_v1", JSON.stringify(careData));
    localStorage.setItem("pflanzen_history_v1", JSON.stringify(careHistory.slice(0,100)));
  }} catch(e) {{ console.warn("care save failed:", e); }}
}}

function loadCareData() {{
  try {{
    const rc = localStorage.getItem("pflanzen_care_v1");
    if(rc) careData = JSON.parse(rc);
    const rh = localStorage.getItem("pflanzen_history_v1");
    if(rh) careHistory = JSON.parse(rh);
  }} catch(e) {{ careData={{}}; careHistory=[]; }}
}}

const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx9Vf0xJ4gJPFt6j3SaQQjW2PKT29upU-UxmyoioOEs_upOXVA0MgKGmu17yZQm0uuM/exec";

async function savePositionsToSheets() {{
  savePositionsLocal();
  if(!APPS_SCRIPT_URL) return;
  const payload = Object.entries(positions).map(([idx,pos])=>{{
    return {{ idx:parseInt(idx), floor:pos.floor, x:pos.x, y:pos.y }};
  }});
  try {{
    await fetch(APPS_SCRIPT_URL, {{
      method:"POST", mode:"no-cors",
      headers:{{"Content-Type":"application/json"}},
      body: JSON.stringify(payload),
    }});
    showToast("☁️ Synchronisiert");
  }} catch(e) {{
    showToast("💾 Lokal gespeichert");
  }}
}}

function debouncedSave() {{
  if(saveTimeout) clearTimeout(saveTimeout);
  saveTimeout = setTimeout(savePositionsToSheets, 800);
}}

// ============================================================
// TAB SWITCHING
// ============================================================
function switchTab(tab) {{
  currentTab=tab;
  document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("active",t.dataset.tab===tab));
  const isPlaner = tab==="planer";
  const isLibrary= tab==="library";
  const isCare   = tab==="care";
  $("left-sidebar").classList.toggle("hidden",!isPlaner);
  $("right-sidebar").classList.toggle("hidden",!isPlaner);
  $("map-area").style.display=isPlaner?"block":"none";
  $("library-view").classList.toggle("active",isLibrary);
  $("care-view").classList.toggle("active",isCare);
  if(isLibrary) renderLibrary();
  if(isCare) {{ renderCare(); renderCalendar(); }}
}}

// ============================================================
// CARE SUB-TABS
// ============================================================
function switchCareSubtab(tab) {{
  currentCareSubtab = tab;
  ["calendar","status","history"].forEach(t=>{{
    $("subtab-"+t).classList.toggle("active", t===tab);
  }});
  $("care-calendar-pane").style.display = tab==="calendar" ? "flex" : "none";
  $("care-status-pane").style.display   = tab==="status"   ? "flex" : "none";
  $("care-history-pane").style.display  = tab==="history"  ? "block" : "none";
  if(tab==="calendar") renderCalendar();
  if(tab==="status")   renderCareStatus();
  if(tab==="history")  renderCareHistory();
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
  render();
  renderInventory();
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
    const ist = dliMode
      ? (getDLIScore(pos.x, pos.y, currentFloor) ?? computeLicht(pos.x,pos.y,currentFloor))
      : computeLicht(pos.x,pos.y,currentFloor);
    const stat=getLichtStatus(ist,p.licht);
    const pin=document.createElement("div");
    pin.className="plant-pin"+(activePIdx===i?" active":"");
    pin.dataset.idx=i;
    const tx=Math.round(pos.x*W-23), ty=Math.round(pos.y*H-23);
    pin.style.transform=`translate(${{tx}}px,${{ty}}px)`;
    const modeLabel = dliMode ? "DLI" : "Live";
    pin.innerHTML=`
      <div class="pin-bubble">${{p.emoji}}</div>
      <div class="pin-indicator ${{stat}}"></div>
      <div class="pin-label">${{p.name.split(" ")[0]}}</div>
      <div class="pin-light-badge">${{ist}}/10</div>
    `;
    setupPinDrag(pin,i);
    pin.addEventListener("click",e=>{{e.stopPropagation();selectPlant(i);}});
    pin.addEventListener("mousemove",e=>showTooltip(`${{p.name}} · ${{modeLabel}}: ${{ist}}/10 · Bedarf: ${{p.licht}}/10`,e.clientX,e.clientY));
    pin.addEventListener("mouseleave",hideTooltip);
    canvas.appendChild(pin);
  }});
}}

// ============================================================
// SELECT PLANT
// ============================================================
function selectPlant(idx) {{
  activePIdx=(activePIdx===idx)?null:idx;
  render();
  if(activePIdx!==null) renderDetail(activePIdx);
  else showEmptyDetail();
  renderInventory();
}}
function showEmptyDetail() {{
  $("rsb-empty").style.display="";
  $("rsb-detail").classList.remove("visible");
}}

// ============================================================
// ★ RENDER DETAIL (mit DLI + neuen Feldern + Bild)
// ============================================================
function renderDetail(idx) {{
  const p  =plants[idx];
  const pos=positions[idx];
  const floor=pos?pos.floor:currentFloor;
  const lf = pos ? computeLichtFull(pos.x,pos.y,floor) : null;
  const liveScore = lf ? lf.score : null;

  // DLI Score
  const dliScore = pos ? getDLIScore(pos.x, pos.y, floor) : null;
  const primaryScore = dliMode && dliScore ? dliScore : liveScore;

  const stat=primaryScore?getLichtStatus(primaryScore,p.licht):null;
  const sc  =stat?STATUS_CFG[stat]:null;

  $("rsb-empty").style.display="none";
  const det=$("rsb-detail");
  det.classList.add("visible");

  // Plant image header
  const imgUrl = getPlantImageUrl(p.name);
  const imgHTML = `
    <div class="detail-img-wrap">
      <img src="${{imgUrl}}" style="width:100%;height:100%;object-fit:cover;"
        onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="detail-img-fallback" style="display:none">${{p.emoji}}</div>
    </div>
  `;

  const coordsHTML=pos
    ?`<div class="coords-row">Rel. ${{(pos.x*100).toFixed(1)}}% · ${{(pos.y*100).toFixed(1)}}%</div>
      <span class="floor-tag">📍 ${{pos.floor}}</span>`
    :`<span class="floor-tag">📦 Im Inventar</span>`;

  // DLI Panel
  let dliHTML = "";
  if(pos) {{
    const hasCache = dliScore !== null;
    const dliVal   = hasCache ? dliScore : "—";
    const dliPct   = hasCache ? ((dliScore/10)*100).toFixed(0) : 0;
    const liveVal  = liveScore !== null ? liveScore : "—";
    const nightMode = sunState.elevation <= -6;
    const liveLabel = nightMode ? "🌙 Nacht (kein Tageslicht)" : `${{"☀️"}} Live-Score ${{liveVal}}/10`;

    dliHTML = `
      <div class="dli-panel">
        <div class="dli-panel-title">📊 Daily Light Integral</div>
        <div class="dli-score-row">
          <span class="dli-score-val">${{dliVal}}</span>
          <span class="dli-score-unit">/ 10 Tages-Ø</span>
        </div>
        <div class="dli-bar-wrap">
          <div class="dli-bar-track">
            <div class="dli-bar-fill" style="width:${{dliPct}}%"></div>
          </div>
          <div class="dli-bar-labels">
            <span>Tagesmittel</span>
            <span>Bedarf: ${{p.licht}}/10</span>
          </div>
        </div>
        <div class="dli-live-row">
          <div class="dli-live-dot"></div>
          <span class="dli-live-text">${{liveLabel}}</span>
        </div>
        ${{!hasCache ? '<div style="font-size:11px;color:var(--muted);text-align:center;margin-top:4px;">DLI-Modus aktivieren für Tagesberechnung</div>' : ''}}
      </div>
    `;
  }}

  // Astro panel
  let astroHTML="";
  if(lf) {{
    const winChips=lf.windowHits.map(w=>{{
      const visRatio = parseFloat(w.visRatio||0);
      const bright = !w.occluded && parseFloat(w.incFactor)>0.2;
      const partialLabel = visRatio>0&&visRatio<1 ? ` (${{Math.round(visRatio*100)}}%)` : "";
      return `<span class="win-chip ${{bright?"hit":""}}">
        ${{w.side}}${{w.occluded?" (verdeckt)": bright?" ☀️":""}}${{partialLabel}}
      </span>`;
    }}).join("");

    const nightMode = sunState.elevation <= -6;
    const dawnMode  = sunState.elevation <= 0 && !nightMode;
    const timeLabel = nightMode ? "🌙 Nacht" : dawnMode ? "🌅 Dämmerung" : "☀️ Tageslicht";
    const skyPct    = (lf.components.skyDiff * 100 / 0.15).toFixed(0);
    const dirPct    = (lf.components.sunDirect * 100).toFixed(0);

    astroHTML=`
      <div class="astro-panel">
        <div class="astro-title">☀️ Lichtanalyse (Live)</div>
        <div class="astro-grid">
          <div class="astro-cell">
            <div class="astro-cell-lbl">Elevation</div>
            <div class="astro-cell-val">${{sunState.elevation.toFixed(1)}}<span class="astro-cell-unit">°</span></div>
          </div>
          <div class="astro-cell">
            <div class="astro-cell-lbl">Azimut</div>
            <div class="astro-cell-val">${{sunState.azimuth.toFixed(0)}}<span class="astro-cell-unit">°</span></div>
          </div>
          <div class="astro-cell">
            <div class="astro-cell-lbl">Direkt. Sonne</div>
            <div class="astro-cell-val">${{dirPct}}<span class="astro-cell-unit">%</span></div>
          </div>
          <div class="astro-cell">
            <div class="astro-cell-lbl">Himmelslicht</div>
            <div class="astro-cell-val">${{skyPct}}<span class="astro-cell-unit">%</span></div>
          </div>
        </div>
        <div style="font-size:11px;font-weight:600;color:var(--muted);margin-top:4px">${{timeLabel}} · Fenster-Sichtbarkeit:</div>
        <div class="window-chips">${{winChips}}</div>
      </div>
    `;
  }}

  const barColor = stat==='ideal' ? 'var(--accent)' : stat==='ok' ? 'var(--warn)' : 'var(--danger)';
  const scoreToShow = primaryScore || liveScore;
  const lightHTML=scoreToShow?`
    <div class="score-badge ${{sc.cls}}">
      <div class="sc-icon">${{sc.icon}}</div>
      <div class="sc-text"><h3>${{sc.label}}</h3><p>${{sc.desc}}</p></div>
    </div>
    <div class="light-bar-wrap">
      <div class="lbw-label"><span>💡 Lichtwert</span><span>${{scoreToShow}} / 10</span></div>
      <div class="lbw-track">
        <div class="lbw-fill" style="width:${{(scoreToShow/10*100).toFixed(1)}}%;background:linear-gradient(90deg, var(--accent-glow), ${{barColor}})"></div>
        <div class="lbw-needle" style="left:${{(p.licht/10*100).toFixed(1)}}%"></div>
      </div>
      <div class="lbw-label"><span style="color:var(--muted);font-weight:500;">Bedarf: ${{p.licht}}/10</span><span style="color:var(--muted);font-weight:500;">Verfügbar: ${{scoreToShow}}/10</span></div>
    </div>
    ${{dliHTML}}
    ${{astroHTML}}
  `:`
    ${{dliHTML || '<div style="font-size:14px;font-weight:500;color:var(--muted);background:var(--surface-solid);border-radius:var(--rx);padding:20px;text-align:center;box-shadow:0 4px 16px rgba(45,71,57,0.02);border:1px solid var(--border);">Pflanze auf Karte platzieren, um Lichtwert zu berechnen.</div>'}}
  `;

  const removeHTML=pos?`<button class="act-btn danger-btn" onclick="removePlant(${{idx}})">🗑️ Entfernen</button>`:"";

  // Extra fields
  const extraHTML = `
    <div style="display:flex;flex-direction:column;gap:10px;">
      ${{p.luftfeuchtigkeit ? `<div class="detail-extra-row"><div class="detail-extra-lbl">💧 Opt. Luftfeuchtigkeit</div><div class="detail-extra-val">${{p.luftfeuchtigkeit}}</div></div>` : ''}}
      ${{p.besprühen ? `<div class="detail-extra-row"><div class="detail-extra-lbl">🌫️ Besprühen</div><div class="detail-extra-val">${{p.besprühen}}</div></div>` : ''}}
      ${{p.besonderheit ? `<div class="detail-extra-row"><div class="detail-extra-lbl">💡 Besonderheit</div><div class="detail-extra-val">${{p.besonderheit}}</div></div>` : ''}}
    </div>
  `;

  det.innerHTML=`
    ${{imgHTML}}
    <div class="plant-hdr">
      <div class="big-emoji">${{p.emoji}}</div>
      <div class="plant-hdr-text">
        <h2>${{p.name}}</h2>
        ${{p.botanisch ? `<div class="botanical">${{p.botanisch}}</div>` : ''}}
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
        <div class="dc-val" style="font-size:14px;padding-top:4px">${{p.umtopfen||"—"}}</div>
      </div>
    </div>
    ${{extraHTML}}
    <div class="action-row">
      <button class="act-btn primary" onclick="selectPlant(${{idx}})">✓ Schließen</button>
      ${{removeHTML}}
    </div>
  `;
}}

function removePlant(idx) {{
  delete positions[idx];
  activePIdx=null;
  debouncedSave();
  render(); renderInventory(); showEmptyDetail();
}}

// ============================================================
// ★ RENDER INVENTORY
// ============================================================
function renderInventory() {{
  const list  =$("inv-list");
  const filter=inventoryFilter.toLowerCase();
  const available=[], placedHere=[], otherFloor=[];

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
      if(isOther)        cls+=" placed-elsewhere";
      item.className=cls;
      item.dataset.pidx=i;

      const badgeHtml=isPlaced
        ?`<span class="inv-badge placed-badge">📍 ${{positions[i]?.floor||""}}</span>`
        :`<span class="inv-badge">Verfügbar</span>`;

      item.innerHTML=`
        <span class="inv-emoji">${{p.emoji}}</span>
        <span class="inv-name">${{p.name}}</span>
        ${{badgeHtml}}
      `;

      item.addEventListener("click",()=>{{
        activePIdx=i;
        if(positions[i] && positions[i].floor!==currentFloor) {{
          setFloor(positions[i].floor);
        }}
        render(); renderInventory(); renderDetail(i);
      }});

      if(!isPlaced) {{
        item.draggable=true;
        item.addEventListener("dragstart",e=>{{
          dragSrcIdx=i; e.dataTransfer.effectAllowed="move";
          setTimeout(()=>item.classList.add("dragging-source"),0);
        }});
        item.addEventListener("dragend",()=>{{
          item.classList.remove("dragging-source"); dragSrcIdx=null;
        }});
      }}
      grp.appendChild(item);
    }});
    list.appendChild(grp);
  }};

  makeGroup("🟢 Verfügbar",       available,  false, false);
  makeGroup("📍 Hier platziert",  placedHere, true,  false);
  makeGroup("🔵 Anderes OG",      otherFloor, true,  true);
}}

function filterInventory(val) {{ inventoryFilter=val; renderInventory(); }}

// ============================================================
// DROP ONTO MAP
// ============================================================
const mapArea=$("map-area");
mapArea.addEventListener("dragover",e=>{{
  e.preventDefault(); e.dataTransfer.dropEffect="move";
  $("map-canvas").classList.add("drag-over");
}});
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
    const tx=Math.round(positions[idx].x*W-23), ty=Math.round(positions[idx].y*H-23);
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
  pin.addEventListener("pointercancel",e=>{{dragging=false;pin.classList.remove("dragging");}});
}}

// ============================================================
// ★ LIBRARY VIEW — Premium Cards mit Bildern & neuen Feldern
// ============================================================
function renderLibrary() {{
  const grid=$("lib-grid");
  const filter=libraryFilter.toLowerCase();
  grid.innerHTML="";

  const filtered=plants.filter(p=>!filter||p.name.toLowerCase().includes(filter));
  const libSub=$("lib-sub-label");
  if(libSub) {{
    const placed=Object.keys(positions).length;
    libSub.textContent=`${{filtered.length}} Pflanzen · ${{placed}} platziert · ${{MONTHS_DE[NOW_MONTH]}}`;
  }}

  filtered.forEach((p,idx)=>{{
    const i=plants.indexOf(p);
    const pos=positions[i];
    const lf=pos?computeLichtFull(pos.x,pos.y,pos.floor):null;
    const ist=lf?lf.score:null;
    const stat=ist?getLichtStatus(ist,p.licht):null;
    const floorLabel=pos?`📍 ${{pos.floor}}`:"📦 Im Inventar";

    const barColor=stat==='ideal'?'var(--accent)':stat==='ok'?'var(--warn)':'var(--danger)';
    const lightPct=ist?(ist/10*100).toFixed(1):0;

    let statusChip="";
    if(stat) {{
      const cfg={{ideal:{{cls:"ideal",ico:"✅",lbl:"Optimaler Standort"}},ok:{{cls:"ok",ico:"⚠️",lbl:"Akzeptabler Standort"}},bad:{{cls:"bad",ico:"❌",lbl:"Zu dunkel"}}}};
      const c=cfg[stat];
      statusChip=`<span class="lib-status-chip ${{c.cls}}">${{c.ico}} ${{c.lbl}}</span>`;
    }} else {{
      statusChip=`<span class="lib-status-chip none">📦 Nicht platziert</span>`;
    }}

    const imgUrl = getPlantImageUrl(p.name);

    // Besonderheit block
    const besondHTML = p.besonderheit ? `
      <div class="lib-besonderheit">
        <div class="lib-besonderheit-lbl">💡 Besonderheit</div>
        ${{p.besonderheit}}
      </div>
    ` : '';

    // Humidity & Spray
    const humiHTML = (p.luftfeuchtigkeit || p.besprühen) ? `
      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        ${{p.luftfeuchtigkeit ? `<div class="lib-humidity-row">💧 <span class="lib-humidity-badge">${{p.luftfeuchtigkeit}}</span></div>` : ''}}
        ${{p.besprühen ? `<div class="lib-humidity-row">🌫️ Besprühen: <strong style="margin-left:4px;color:var(--text);">${{p.besprühen}}</strong></div>` : ''}}
      </div>
    ` : '';

    const card=document.createElement("div");
    card.className="lib-card";
    card.innerHTML=`
      <div class="lib-card-img">
        <img src="${{imgUrl}}" alt="${{p.name}}"
          onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="lib-card-img-fallback" style="display:none">${{p.emoji}}</div>
        <div class="lib-card-img-overlay">
          <div class="lib-card-name">${{p.name}}</div>
          ${{p.botanisch ? `<div class="lib-card-botanical">${{p.botanisch}}</div>` : ''}}
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
        <div class="lib-light-row">
          <div class="lib-light-icon">☀️</div>
          <div class="lib-light-bar-wrap">
            <div class="lib-light-bar-track">
              <div class="lib-light-bar-fill" style="width:${{lightPct}}%;background:${{ist?'linear-gradient(90deg, var(--accent-glow), '+barColor+')':'rgba(45,71,57,0.1)'}}"></div>
            </div>
            <div class="lib-light-labels">
              <span>Licht verfügbar</span>
              <span>Bedarf: ${{p.licht}}/10</span>
            </div>
          </div>
          <div class="lib-light-score" style="color:${{ist?barColor:'var(--muted)'}}">
            ${{ist?ist+"/10":"—"}}
          </div>
        </div>
        <div class="lib-divider"></div>
        <div class="lib-care-grid">
          <div class="lib-care-cell">
            <div class="lib-care-cell-lbl">💧 Gießen (${{MONTHS_DE[NOW_MONTH]}})</div>
            <div class="lib-care-cell-val">${{p.giessen||"—"}}<span class="lib-care-cell-unit">Tage</span></div>
          </div>
          <div class="lib-care-cell">
            <div class="lib-care-cell-lbl">🌿 Düngen (${{MONTHS_DE[NOW_MONTH]}})</div>
            <div class="lib-care-cell-val">${{p.dungen||"—"}}</div>
          </div>
          <div class="lib-care-cell">
            <div class="lib-care-cell-lbl">☀️ Lichtbedarf</div>
            <div class="lib-care-cell-val">${{p.licht}}<span class="lib-care-cell-unit">/ 10</span></div>
          </div>
          <div class="lib-care-cell">
            <div class="lib-care-cell-lbl">🪴 Umtopfen</div>
            <div class="lib-care-cell-val" style="font-size:13px">${{p.umtopfen||"—"}}</div>
          </div>
        </div>
        ${{humiHTML}}
        ${{besondHTML}}
      </div>
      <div class="lib-card-footer">
        <button class="show-on-map-btn" data-pidx="${{i}}">🗺️ Auf Karte zeigen</button>
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

function filterLibrary(val) {{ libraryFilter=val; renderLibrary(); }}

// ============================================================
// CLICK OUTSIDE → DESELECT
// ============================================================
$("map-area").addEventListener("click",()=>{{activePIdx=null;render();renderInventory();showEmptyDetail();}});

// ============================================================
// ★ PFLEGE-KALENDER — Kalender-Grid
// ============================================================

function changeCalMonth(delta) {{
  calMonth += delta;
  if(calMonth > 11){{ calMonth=0; calYear++; }}
  if(calMonth < 0) {{ calMonth=11; calYear--; }}
  renderCalendar();
}}

function renderCalendar() {{
  const titleEl = $("cal-month-title");
  if(titleEl) titleEl.textContent = MONTHS_DE[calMonth]+" "+calYear;
  const grid = $("cal-grid");
  if(!grid) return;

  // Day headers
  let html = DAYS_DE.map(d=>`<div class="cal-day-header">${{d}}</div>`).join("");

  const firstDay = new Date(calYear, calMonth, 1);
  const lastDay  = new Date(calYear, calMonth+1, 0);
  const startDow = firstDay.getDay(); // 0=So
  const totalDays= lastDay.getDate();

  // Pre-fill previous month days
  const prevLast = new Date(calYear, calMonth, 0).getDate();
  for(let d=startDow-1; d>=0; d--) {{
    html += `<div class="cal-cell other-month"><div class="cal-day-num">${{prevLast-d}}</div></div>`;
  }}

  const todayD = NOW.getDate(), todayM = NOW.getMonth(), todayY = NOW.getFullYear();

  // Collect all events for this month
  const eventsByDay = {{}};

  // Past care history events
  careHistory.forEach(h=>{{
    const d = new Date(h.time);
    if(d.getMonth()===calMonth && d.getFullYear()===calYear) {{
      const day = d.getDate();
      if(!eventsByDay[day]) eventsByDay[day]=[];
      eventsByDay[day].push({{ type:h.type, name:h.name, emoji:h.emoji }});
    }}
  }});

  // Upcoming due events (next 30 days within this month)
  plants.forEach((p,i)=>{{
    const ws = getCareStatus(i,'water');
    const fs = getCareStatus(i,'fertilize');
    [['water',ws],['fertilize',fs]].forEach(([type,status])=>{{
      if(!status) return;
      const nd = status.nextDate;
      if(nd.getMonth()===calMonth && nd.getFullYear()===calYear) {{
        const day = nd.getDate();
        if(!eventsByDay[day]) eventsByDay[day]=[];
        eventsByDay[day].push({{ type:'due-'+type, name:p.name, emoji:p.emoji }});
      }}
    }});
  }});

  for(let d=1; d<=totalDays; d++) {{
    const isToday = d===todayD && calMonth===todayM && calYear===todayY;
    let cellClass = "cal-cell" + (isToday?" today":"");
    const events  = eventsByDay[d] || [];
    const evHTML  = events.slice(0,3).map(e=>{{
      const cls = e.type==='water' ? 'water' : e.type==='fertilize' ? 'fertilize' : e.type==='due-water' ? 'due-water' : 'due-fertilize';
      const icon = e.type.includes('water') ? '💧' : '🌿';
      return `<div class="cal-event ${{cls}}">${{icon}} ${{e.name}}</div>`;
    }}).join("");
    const moreHTML = events.length>3 ? `<div class="cal-event" style="color:var(--muted);background:transparent;">+${{events.length-3}} weitere</div>` : "";
    html += `
      <div class="${{cellClass}}">
        <div class="cal-day-num">${{d}}</div>
        <div class="cal-events">${{evHTML}}${{moreHTML}}</div>
      </div>
    `;
  }}

  // Post-fill next month days
  const cellsUsed = startDow + totalDays;
  const remaining = (7 - (cellsUsed % 7)) % 7;
  for(let d=1; d<=remaining; d++) {{
    html += `<div class="cal-cell other-month"><div class="cal-day-num">${{d}}</div></div>`;
  }}

  grid.innerHTML = html;
}}

// ============================================================
// ★ PFLEGE-STATUS — Liste mit Fortschrittsbalken
// ============================================================
function renderCareStatus() {{
  const overdueItems  = [];
  const soonItems     = [];
  const allItems      = [];
  const now = new Date();
  const in3days = new Date(now.getTime() + 3*24*3600*1000);

  plants.forEach((p, i) => {{
    const ws = getCareStatus(i, 'water');
    const fs = getCareStatus(i, 'fertilize');
    const wOverdue = ws && ws.overdueDays > 0;
    const fOverdue = fs && fs.overdueDays > 0;
    const wSoon = ws && !wOverdue && ws.nextDate <= in3days;
    const fSoon = fs && !fOverdue && fs.nextDate <= in3days;

    const entry = {{idx:i, ws, fs}};
    if(wOverdue || fOverdue) overdueItems.push(entry);
    else if(wSoon || fSoon) soonItems.push(entry);
    else allItems.push(entry);
  }});

  const dueCount  = overdueItems.length;
  const soonCount = soonItems.length;
  $("care-sub-label").textContent =
    `${{plants.length}} Pflanzen · ${{dueCount}} fällig · ${{soonCount}} in den nächsten 3 Tagen`;

  const overdueSection = $("care-overdue-section");
  if(overdueItems.length > 0) {{
    overdueSection.innerHTML = `
      <div class="care-section-title">
        ⚠️ Fällig & Überfällig
        <span class="care-badge">${{overdueItems.length}} Pflanze${{overdueItems.length!==1?'n':''}}</span>
      </div>
      ${{overdueItems.map(e => makeCareCard(e.idx, e.ws, e.fs)).join("")}}
    `;
  }} else {{
    overdueSection.innerHTML = `
      <div class="care-section-title">⚠️ Fällig & Überfällig <span class="care-badge ok">Alles erledigt ✓</span></div>
      <div class="care-empty"><div class="ce-icon">🎉</div><p>Alle Pflanzen sind versorgt!<br>Gute Arbeit.</p></div>
    `;
  }}

  const soonSection = $("care-soon-section");
  if(soonItems.length > 0) {{
    soonSection.innerHTML = `
      <div class="care-section-title">
        📅 In den nächsten 3 Tagen
        <span class="care-badge warn">${{soonItems.length}} Pflanze${{soonItems.length!==1?'n':''}}</span>
      </div>
      ${{soonItems.map(e => makeCareCard(e.idx, e.ws, e.fs)).join("")}}
    `;
  }} else {{
    soonSection.innerHTML = '';
  }}

  const allSection = $("care-all-section");
  if(allItems.length > 0) {{
    allSection.innerHTML = `
      <div class="care-section-title">
        🌿 Alle anderen Pflanzen
        <span class="care-badge ok">${{allItems.length}} versorgt</span>
      </div>
      ${{allItems.map(e => makeCareCard(e.idx, e.ws, e.fs)).join("")}}
    `;
  }} else {{
    allSection.innerHTML = '';
  }}
}}

function renderCareHistory() {{
  const histSection = $("care-history-section");
  if(!histSection) return;
  if(careHistory.length > 0) {{
    const entries = careHistory.slice(0,50).map(h => {{
      const icon = h.type==='water' ? '💧' : '🌿';
      const label = h.type==='water' ? 'gegossen' : 'gedüngt';
      return `
        <div class="history-entry">
          <span class="history-icon">${{icon}}</span>
          <span class="history-text">${{h.emoji}} ${{h.name}} ${{label}}</span>
          <span class="history-time">${{formatAbsDate(h.time)}}</span>
        </div>
      `;
    }}).join("");
    histSection.innerHTML = `
      <div class="care-history">
        <div class="care-history-header">
          📋 Pflege-Historie
          <span style="font-family:'DM Sans';font-size:12px;font-weight:500;color:var(--muted);margin-left:auto;">${{careHistory.length}} Einträge</span>
        </div>
        ${{entries}}
      </div>
    `;
  }} else {{
    histSection.innerHTML = `
      <div class="care-history">
        <div class="care-history-header">📋 Pflege-Historie</div>
        <div style="padding:24px;text-align:center;color:var(--muted);font-size:14px;font-weight:500;">
          Noch keine Aktionen aufgezeichnet.
        </div>
      </div>
    `;
  }}
}}

// ============================================================
// ★ PFLEGE-KALENDER
// ============================================================
function parseIntervalDays(val) {{
  if(!val || val==="—" || val.trim()==="") return null;
  const n = parseFloat(val);
  return isNaN(n) ? null : n;
}}

function getCareStatus(plantIdx, type) {{
  const p = plants[plantIdx];
  const intervalDays = type==='water'
    ? parseIntervalDays(p.giessen)
    : parseIntervalDays(p.dungen);

  if(!intervalDays) return null;

  const cd = careData[plantIdx] || {{}};
  const lastStr = type==='water' ? cd.lastWatered : cd.lastFertilized;
  const lastDate = lastStr ? new Date(lastStr) : null;
  const now = new Date();

  let nextDate;
  let overdueDays = 0;
  let moisturePct = 50;

  if(lastDate) {{
    nextDate = new Date(lastDate.getTime() + intervalDays*24*3600*1000);
    const diffMs = now - nextDate;
    overdueDays = Math.max(0, Math.floor(diffMs / (24*3600*1000)));
    const elapsed = (now - lastDate) / (1000*3600*24);
    moisturePct = Math.max(0, Math.min(100, Math.round((1 - elapsed/intervalDays)*100)));
  }} else {{
    nextDate = new Date(now.getTime() - 24*3600*1000);
    overdueDays = 1;
    moisturePct = 0;
  }}

  return {{ nextDate, overdueDays, intervalDays, moisturePct }};
}}

function formatRelDate(date) {{
  const now = new Date();
  const diffDays = Math.round((date - now) / (24*3600*1000));
  if(diffDays < -1) return `${{Math.abs(diffDays)}} Tage überfällig`;
  if(diffDays === -1) return "Gestern fällig";
  if(diffDays === 0) return "Heute fällig";
  if(diffDays === 1) return "Morgen";
  if(diffDays <= 3) return `In ${{diffDays}} Tagen`;
  return date.toLocaleDateString("de-DE", {{day:"2-digit",month:"2-digit"}});
}}

function formatAbsDate(isoStr) {{
  if(!isoStr) return "—";
  const d = new Date(isoStr);
  return d.toLocaleDateString("de-DE", {{day:"2-digit",month:"2-digit",year:"numeric"}})
    + " " + d.toLocaleTimeString("de-DE",{{hour:"2-digit",minute:"2-digit"}});
}}

function doWater(plantIdx) {{
  if(!careData[plantIdx]) careData[plantIdx]={{}};
  const now = new Date().toISOString();
  careData[plantIdx].lastWatered = now;
  careHistory.unshift({{
    type:'water', plantIdx,
    name: plants[plantIdx].name,
    emoji: plants[plantIdx].emoji,
    time: now
  }});
  saveCareData();
  renderCare();
  renderCalendar();
  showToast(`💧 ${{plants[plantIdx].name}} gegossen`);
}}

function doFertilize(plantIdx) {{
  if(!careData[plantIdx]) careData[plantIdx]={{}};
  const now = new Date().toISOString();
  careData[plantIdx].lastFertilized = now;
  careHistory.unshift({{
    type:'fertilize', plantIdx,
    name: plants[plantIdx].name,
    emoji: plants[plantIdx].emoji,
    time: now
  }});
  saveCareData();
  renderCare();
  renderCalendar();
  showToast(`🌿 ${{plants[plantIdx].name}} gedüngt`);
}}

function waterAllDue() {{
  let count = 0;
  plants.forEach((p,i) => {{
    const ws = getCareStatus(i, 'water');
    if(ws && ws.overdueDays > 0) {{
      if(!careData[i]) careData[i]={{}};
      careData[i].lastWatered = new Date().toISOString();
      careHistory.unshift({{type:'water',plantIdx:i,name:p.name,emoji:p.emoji,time:careData[i].lastWatered}});
      count++;
    }}
  }});
  saveCareData();
  renderCare();
  renderCalendar();
  showToast(`💧 ${{count}} Pflanzen gegossen`);
}}

function refreshCare() {{ renderCare(); renderCalendar(); }}

function renderCare() {{
  if(currentCareSubtab === 'calendar') renderCalendar();
  else if(currentCareSubtab === 'status') renderCareStatus();
  else if(currentCareSubtab === 'history') renderCareHistory();
  // Always update status counts for header
  renderCareStatusCounts();
}}

function renderCareStatusCounts() {{
  const now = new Date();
  const in3days = new Date(now.getTime() + 3*24*3600*1000);
  let dueCount = 0, soonCount = 0;
  plants.forEach((p, i) => {{
    const ws = getCareStatus(i, 'water');
    const fs = getCareStatus(i, 'fertilize');
    const wOverdue = ws && ws.overdueDays > 0;
    const fOverdue = fs && fs.overdueDays > 0;
    const wSoon = ws && !wOverdue && ws.nextDate <= in3days;
    const fSoon = fs && !fOverdue && fs.nextDate <= in3days;
    if(wOverdue||fOverdue) dueCount++;
    else if(wSoon||fSoon) soonCount++;
  }});
  $("care-sub-label").textContent =
    `${{plants.length}} Pflanzen · ${{dueCount}} fällig · ${{soonCount}} in den nächsten 3 Tagen`;
}}

function makeCareCard(plantIdx, waterStatus, fertilizeStatus) {{
  const p = plants[plantIdx];
  const cd = careData[plantIdx] || {{}};

  const wOver = waterStatus && waterStatus.overdueDays > 0;
  const fOver = fertilizeStatus && fertilizeStatus.overdueDays > 0;
  let cardClass = "care-card";
  if(wOver || fOver) cardClass += " overdue";

  // Water chip
  let waterChip = "";
  if(waterStatus) {{
    const cls = waterStatus.overdueDays > 0 ? "overdue" : waterStatus.nextDate <= new Date(Date.now()+3*86400000) ? "soon" : "ok";
    const label = formatRelDate(waterStatus.nextDate);
    waterChip = `<span class="care-chip ${{cls}}">💧 ${{label}}</span>`;
  }}

  // Fertilize chip
  let fertChip = "";
  if(fertilizeStatus) {{
    const cls = fertilizeStatus.overdueDays > 0 ? "overdue" : fertilizeStatus.nextDate <= new Date(Date.now()+3*86400000) ? "soon" : "ok";
    const label = formatRelDate(fertilizeStatus.nextDate);
    fertChip = `<span class="care-chip ${{cls}}">🌿 ${{label}}</span>`;
  }}

  // Progress bars
  let progressBars = "";
  if(waterStatus) {{
    const wPct = waterStatus.moisturePct;
    const fPct = fertilizeStatus ? fertilizeStatus.moisturePct : null;
    progressBars = `
      <div class="care-progress-wrap">
        <div class="care-progress-row">
          <span class="care-progress-icon">💧</span>
          <div class="care-progress-track">
            <div class="care-progress-fill water" style="width:${{wPct}}%"></div>
          </div>
          <span class="care-progress-pct">${{wPct}}%</span>
        </div>
        ${{fPct !== null ? `
        <div class="care-progress-row">
          <span class="care-progress-icon">🌿</span>
          <div class="care-progress-track">
            <div class="care-progress-fill fertilize" style="width:${{fPct}}%"></div>
          </div>
          <span class="care-progress-pct">${{fPct}}%</span>
        </div>` : ''}}
      </div>
    `;
  }}

  // Plant thumbnail
  const imgUrl = getPlantImageUrl(p.name);
  const thumbHTML = `
    <div class="care-card-thumb">
      <img src="${{imgUrl}}" style="width:100%;height:100%;object-fit:cover;"
        onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="care-card-thumb-emoji" style="display:none">${{p.emoji}}</div>
    </div>
  `;

  const waterBtn = waterStatus
    ? `<button class="care-btn water" onclick="doWater(${{plantIdx}})">💧 Gießen</button>`
    : "";
  const fertBtn = fertilizeStatus
    ? `<button class="care-btn fertilize" onclick="doFertilize(${{plantIdx}})">🌿 Düngen</button>`
    : "";

  const lastW = cd.lastWatered ? `Zuletzt: ${{formatAbsDate(cd.lastWatered)}}` : "Noch nie gegossen";
  const lastF = cd.lastFertilized ? `Zuletzt: ${{formatAbsDate(cd.lastFertilized)}}` : "Noch nie gedüngt";

  return `
    <div class="${{cardClass}}">
      ${{thumbHTML}}
      <div class="care-card-info">
        <div class="care-card-name">${{p.name}}</div>
        <div class="care-card-meta">
          ${{waterChip}}${{fertChip}}
        </div>
        ${{progressBars}}
        <div style="font-size:11px;color:var(--muted);margin-top:4px;display:flex;gap:16px;flex-wrap:wrap;">
          <span>💧 ${{lastW}}</span>
          ${{fertilizeStatus?`<span>🌿 ${{lastF}}</span>`:''}}
        </div>
      </div>
      <div class="care-card-actions">
        ${{waterBtn}}
        ${{fertBtn}}
      </div>
    </div>
  `;
}}

// ============================================================
// BOOT
// ============================================================
// Initialize subtab visibility
switchCareSubtab('calendar');
loadPlants();
</script>
</body>
</html>"""

components.html(html_app, height=900, scrolling=False)
