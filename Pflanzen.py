import streamlit as st
import streamlit.components.v1 as components
import json, math
from dataclasses import dataclass, field
from typing import Optional, Dict

# ============================================================
# KONFIGURATION
# ============================================================
st.set_page_config(layout="wide", page_title="Pflanzen-Planer Pro", page_icon="🌿")

st.markdown("""
<style>
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  .stApp { background: #F9F7F2; }
</style>
""", unsafe_allow_html=True)

SHEET_ID  = "1cbOPNq-CrYrin-U0OkUJ5AE2AWF6Ba7RqIHlVOtUCK0"
CSV_URL   = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

GITHUB_BASE = "https://raw.githubusercontent.com/simondereck1-hue/Pflanzen-bersicht/main"

# ============================================================
# DATACLASS: Plant
# ============================================================
# (Python-seitig für spätere Erweiterungen; JS-Parsing erfolgt im Browser)
@dataclass
class Plant:
    """Repräsentiert eine Pflanze aus dem Google Sheet."""
    id: int
    name: str
    botanisch: str = ""
    licht: float = 5.0
    giessen: str = "—"           # Gießintervall aktueller Monat (Tage)
    dungen: str = "—"            # Düngungsintervall aktueller Monat
    umtopfen: str = "—"
    luftfeuchtigkeit: str = ""
    besprühen: str = ""
    besonderheit: str = ""
    emoji: str = "🌿"
    giessAll: Dict[str, str] = field(default_factory=dict)
    duengAll: Dict[str, str] = field(default_factory=dict)
    # Vital-Score-Felder (werden clientseitig berechnet und gespeichert)
    vital_score: Optional[float] = None    # 0-100 Glücks-Index
    licht_score: Optional[float] = None    # Lichtanteil am Score
    giess_score: Optional[float] = None    # Gießanteil am Score
    dueng_score: Optional[float] = None    # Düngungsanteil am Score
    staunässe_risk: bool = False           # True wenn Gießintervall stark unterschritten

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
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<style>
/* ══════════════════════════════════════════════════════
   DESIGN TOKENS — Biophilic High-End Palette
   ══════════════════════════════════════════════════════ */
:root {{
  /* Farben */
  --bg:           #F9F7F2;          /* Warmes Creme */
  --bg-2:         #F3F0E8;
  --surface:      rgba(255,255,255,0.82);
  --surface-solid:#FFFFFF;
  --surface-2:    rgba(141,170,145,0.10);
  --surface-3:    rgba(141,170,145,0.18);
  --border:       rgba(74,90,78,0.09);
  --border-2:     rgba(74,90,78,0.17);

  /* Sage-Grün Akzent */
  --accent:       #8DAA91;
  --accent-dark:  #5C7A62;
  --accent-deep:  #3D5C42;
  --accent-dim:   rgba(141,170,145,0.18);
  --accent-glow:  rgba(141,170,145,0.38);

  /* Status */
  --warn:         #C9956A;
  --warn-dim:     rgba(201,149,106,0.14);
  --danger:       #C97070;
  --danger-dim:   rgba(201,112,112,0.13);
  --staunaesse:   #7BAEC4;
  --staunaesse-dim:rgba(123,174,196,0.14);
  --dli-color:    #6B9EC4;
  --dli-dim:      rgba(107,158,196,0.14);

  /* Typografie */
  --text:         #2C3B2E;          /* Tiefes Waldgrün */
  --text-2:       #3F5442;
  --muted:        #6E8A72;
  --muted2:       #9BB39F;

  /* Geometrie */
  --r:  14px; --rs: 10px; --rx: 22px;
  --sidebar-w: 340px;
  --header-h:  70px; --tab-h: 60px;

  /* Transitions */
  --ease:  cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-s:cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --t:     0.3s;
}}

*,*::before,*::after {{ box-sizing:border-box; margin:0; padding:0 }}
html,body {{ width:100%; height:100%; overflow:hidden }}
body {{
  font-family:'DM Sans',sans-serif;
  background: var(--bg);
  background-image:
    radial-gradient(ellipse 80% 60% at 0% 0%, rgba(141,170,145,0.12) 0%, transparent 55%),
    radial-gradient(ellipse 60% 80% at 100% 100%, rgba(201,149,106,0.07) 0%, transparent 55%);
  color:var(--text);
  display:flex; flex-direction:column;
}}
button {{ font-family:inherit; cursor:pointer; border:none; background:none; color:inherit }}
input,select {{ font-family:inherit }}

/* ── HEADER ── */
#header {{
  height:var(--header-h);
  background: rgba(255,255,255,0.75);
  backdrop-filter: blur(24px) saturate(1.4);
  -webkit-backdrop-filter: blur(24px) saturate(1.4);
  border-bottom: 1px solid rgba(255,255,255,0.5);
  box-shadow: 0 2px 24px rgba(44,59,46,0.05);
  display:flex; align-items:center; padding:0 28px; gap:14px;
  flex-shrink:0; z-index:200;
}}
.logo {{
  font-family:'Playfair Display',serif;
  font-weight:700; font-size:19px;
  color:var(--accent-deep); letter-spacing:-.3px;
}}
.logo-sep {{ color:var(--border-2); font-size:22px; font-weight:200 }}
.header-meta {{ display:flex; align-items:center; gap:14px; margin-left:auto }}
.sun-info {{
  display:flex; align-items:center; gap:9px;
  font-size:13px; font-weight:500; color:var(--text-2);
  background:rgba(255,255,255,0.7);
  border:1px solid var(--border);
  border-radius:99px; padding:7px 18px;
  backdrop-filter:blur(8px);
  box-shadow:0 2px 12px rgba(44,59,46,0.04);
  transition: box-shadow var(--t) var(--ease-s);
}}
.sun-info:hover {{ box-shadow:0 4px 20px rgba(141,170,145,0.15) }}
.sun-dot {{
  width:8px; height:8px; border-radius:50%;
  background:var(--warn); box-shadow:0 0 10px var(--warn);
  flex-shrink:0; animation:sunPulse 3s ease-in-out infinite;
}}
@keyframes sunPulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.5}} }}
.status-wrap {{
  display:flex; align-items:center; gap:8px;
  font-size:13px; color:var(--muted); font-weight:500;
}}
.sdot {{
  width:8px; height:8px; border-radius:50%;
  background:var(--muted2); transition:all .4s;
}}
.sdot.ok {{
  background:var(--accent);
  box-shadow:0 0 10px var(--accent-glow);
}}

/* ── TABS ── */
#tabs {{
  height:var(--tab-h);
  display:flex; align-items:center;
  padding:0 28px; gap:10px;
  flex-shrink:0; z-index:150;
  margin-top:10px;
}}
.tab {{
  padding:11px 26px; font-size:13.5px; font-weight:500;
  color:var(--muted); border-radius:99px; cursor:pointer;
  background:rgba(255,255,255,0.55);
  backdrop-filter:blur(8px) saturate(1.2);
  border:1px solid rgba(255,255,255,0.6);
  transition:all var(--t) var(--ease);
  box-shadow:0 2px 8px rgba(44,59,46,0.02);
  letter-spacing:.01em;
}}
.tab:hover {{
  color:var(--text);
  background:rgba(255,255,255,0.88);
  transform:translateY(-2px);
  box-shadow:0 6px 20px rgba(44,59,46,0.06);
}}
.tab.active {{
  color:var(--accent-deep);
  background:var(--surface-solid);
  border-color:var(--accent-glow);
  box-shadow:0 4px 18px var(--accent-dim);
  font-weight:600;
}}
.tab-icon {{ margin-right:7px; font-size:15px }}

/* ── MAIN ── */
#main {{
  display:flex; flex:1; overflow:hidden;
  position:relative; padding:0 16px 16px 16px; gap:14px;
}}

/* ── SIDEBARS (Glassmorphism) ── */
#left-sidebar, #right-sidebar {{
  width:var(--sidebar-w);
  background:rgba(255,255,255,0.78);
  backdrop-filter:blur(28px) saturate(1.3);
  -webkit-backdrop-filter:blur(28px) saturate(1.3);
  border:1px solid rgba(255,255,255,0.7);
  border-radius:var(--rx);
  box-shadow:0 8px 40px rgba(44,59,46,0.06), inset 0 1px 0 rgba(255,255,255,0.8);
  display:flex; flex-direction:column; overflow:hidden; flex-shrink:0;
}}
#left-sidebar.hidden, #right-sidebar.hidden {{ display:none }}

.sidebar-header {{
  padding:22px 22px 16px;
  font-family:'Playfair Display',serif;
  font-weight:600; font-size:14px;
  color:var(--accent-deep); letter-spacing:.02em;
  border-bottom:1px solid var(--border);
  flex-shrink:0; display:flex; align-items:center; gap:10px;
}}
.sidebar-header span {{ flex:1 }}

.inv-search {{
  margin:14px 16px; padding:11px 18px;
  background:rgba(255,255,255,0.8);
  border:1px solid var(--border);
  border-radius:var(--r); color:var(--text);
  font-size:13.5px; width:calc(100% - 32px);
  box-shadow:inset 0 2px 6px rgba(44,59,46,0.03);
  transition:all var(--t) var(--ease-s);
}}
.inv-search::placeholder {{ color:var(--muted2) }}
.inv-search:focus {{
  outline:none;
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-dim);
}}

.inv-group {{ padding:10px 0 4px }}
.inv-group-label {{
  padding:4px 22px 8px;
  font-size:10.5px; font-weight:600;
  color:var(--muted); text-transform:uppercase; letter-spacing:.09em;
}}
.inv-item {{
  display:flex; align-items:center; gap:12px;
  padding:10px 22px; cursor:pointer;
  transition:all var(--t) var(--ease-s);
  user-select:none; border-left:3px solid transparent;
}}
.inv-item:hover {{ background:rgba(141,170,145,0.08) }}
.inv-item.selected {{
  background:rgba(255,255,255,0.7);
  border-left:3px solid var(--accent);
  box-shadow:0 2px 12px rgba(141,170,145,0.08);
}}
.inv-item.placed-elsewhere {{ opacity:.55 }}
.inv-item.dragging-source {{ opacity:.35; transform:scale(0.95) }}
.inv-emoji {{
  font-size:20px; width:30px; text-align:center;
  background:var(--surface-2); border-radius:9px; padding:5px;
}}
.inv-name {{ font-size:13.5px; font-weight:500; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap }}
.inv-badge {{
  font-size:10.5px; padding:4px 10px; border-radius:99px; font-weight:600;
  background:var(--bg-2); color:var(--muted); white-space:nowrap;
  border:1px solid var(--border);
}}
.inv-badge.placed-badge {{
  background:rgba(255,255,255,0.9);
  border:1px solid var(--accent-glow); color:var(--accent-dark);
}}

.inv-floor-switcher {{
  margin:auto 16px 16px;
  padding:6px; background:rgba(255,255,255,0.7);
  border:1px solid var(--border); border-radius:var(--rx);
  display:flex; gap:4px; flex-shrink:0;
  box-shadow:0 4px 16px rgba(44,59,46,0.03);
}}
.floor-btn {{
  flex:1; padding:10px 8px; font-size:13px; font-weight:600;
  border-radius:var(--r); transition:all var(--t) var(--ease); color:var(--muted);
}}
.floor-btn:hover {{ background:var(--surface-2); color:var(--text) }}
.floor-btn.active {{
  background:var(--accent); color:#fff;
  box-shadow:0 4px 14px var(--accent-glow);
}}

/* ── MAP AREA ── */
#map-area {{
  flex:1; position:relative; overflow:hidden;
  background:radial-gradient(ellipse at 50% 50%, rgba(141,170,145,0.06) 0%, transparent 70%);
  border-radius:var(--rx);
  box-shadow:inset 0 0 40px rgba(44,59,46,0.02);
}}
#map-canvas {{
  position:absolute; top:50%; left:50%;
  transform:translate(-50%,-50%);
  border-radius:12px;
}}
#floor-img {{
  position:absolute; inset:0; width:100%; height:100%;
  object-fit:contain; pointer-events:none; user-select:none; opacity:0.95;
}}
#light-canvas {{
  position:absolute; inset:0; width:100%; height:100%;
  pointer-events:none; opacity:.6; mix-blend-mode:multiply;
}}
#map-canvas.drag-over {{
  outline:2px dashed var(--accent); outline-offset:8px; border-radius:16px;
  background:rgba(141,170,145,0.04);
}}

/* DLI Toggle */
.dli-toggle-wrap {{
  position:absolute; top:16px; right:16px; z-index:100;
  display:flex; gap:9px; align-items:center;
  background:rgba(255,255,255,0.88); backdrop-filter:blur(12px);
  border:1px solid var(--border); border-radius:99px; padding:7px 16px;
  box-shadow:0 4px 18px rgba(44,59,46,0.07);
}}
.dli-toggle-label {{ font-size:12px; font-weight:600; color:var(--muted) }}
.dli-toggle {{
  width:36px; height:20px; border-radius:10px; background:var(--muted2);
  position:relative; cursor:pointer; transition:background var(--t) var(--ease-s); border:none;
}}
.dli-toggle.on {{ background:var(--dli-color) }}
.dli-toggle::after {{
  content:''; position:absolute; top:3px; left:3px;
  width:14px; height:14px; border-radius:50%;
  background:#fff; transition:transform var(--t) var(--ease);
  box-shadow:0 1px 4px rgba(0,0,0,.15);
}}
.dli-toggle.on::after {{ transform:translateX(16px) }}

/* ── PLANT PINS ── */
.plant-pin {{
  position:absolute; display:flex; flex-direction:column; align-items:center;
  cursor:grab; user-select:none; touch-action:none; z-index:10;
  transition:transform .12s;
}}
.plant-pin:hover {{ z-index:50 }}
.plant-pin.dragging {{ cursor:grabbing; z-index:100 }}
.plant-pin.active .pin-bubble {{
  background:rgba(255,255,255,0.95);
  border-color:var(--accent);
  box-shadow:0 0 0 4px var(--accent-dim), 0 8px 28px rgba(44,59,46,0.12);
  transform:scale(1.18);
}}
.plant-pin.highlight-pulse .pin-bubble {{ animation:highlightPulse 1.6s ease-in-out 3 }}
@keyframes highlightPulse {{
  0%,100% {{ box-shadow:0 0 0 0 var(--accent-glow) }}
  50%      {{ box-shadow:0 0 0 18px rgba(141,170,145,0) }}
}}
.pin-bubble {{
  width:48px; height:48px; border-radius:50%;
  background:rgba(255,255,255,0.88);
  backdrop-filter:blur(6px) saturate(1.2);
  border:1.5px solid rgba(141,170,145,0.4);
  display:flex; align-items:center; justify-content:center;
  font-size:22px;
  transition:transform var(--t) var(--ease), box-shadow var(--t) var(--ease-s);
  box-shadow:0 4px 18px rgba(44,59,46,0.09);
}}
.plant-pin:hover .pin-bubble {{
  transform:scale(1.22);
  box-shadow:0 10px 28px rgba(141,170,145,0.28);
  border-color:var(--accent);
}}
.plant-pin.dragging .pin-bubble {{
  transform:scale(1.12) translateY(-6px);
  box-shadow:0 14px 36px rgba(141,170,145,0.32);
}}
.pin-indicator {{
  width:10px; height:10px; border-radius:50%;
  margin-top:5px; background:var(--muted);
  transition:background .3s; border:2px solid rgba(255,255,255,0.9);
}}
.pin-indicator.ideal {{ background:var(--accent);  box-shadow:0 0 8px var(--accent) }}
.pin-indicator.ok    {{ background:var(--warn);    box-shadow:0 0 8px var(--warn)   }}
.pin-indicator.bad   {{ background:var(--danger);  box-shadow:0 0 8px var(--danger) }}
.pin-label {{
  font-size:11px; font-weight:600; color:var(--text);
  margin-top:4px; white-space:nowrap; max-width:82px;
  overflow:hidden; text-overflow:ellipsis; text-align:center;
  background:rgba(255,255,255,0.82); padding:3px 9px; border-radius:8px;
  backdrop-filter:blur(6px);
  box-shadow:0 2px 8px rgba(44,59,46,0.06);
}}
.pin-light-badge {{
  font-size:10px; font-weight:600; padding:2px 8px;
  border-radius:99px; margin-top:3px;
  background:rgba(255,255,255,0.85); color:var(--muted);
  font-variant-numeric:tabular-nums;
  box-shadow:0 2px 6px rgba(44,59,46,0.04);
}}

/* ── RIGHT SIDEBAR (Detail) ── */
#rsb-empty {{
  flex:1; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  gap:16px; color:var(--muted); padding:32px; text-align:center;
}}
#rsb-empty .empty-icon {{ font-size:56px; opacity:.4; filter:grayscale(0.3) }}
#rsb-detail {{ flex:1; display:none; flex-direction:column; overflow-y:auto; padding:24px; gap:18px }}
#rsb-detail.visible {{ display:flex }}
#rsb-detail::-webkit-scrollbar {{ width:5px }}
#rsb-detail::-webkit-scrollbar-thumb {{ background:var(--border-2); border-radius:3px }}

/* Detail Plant Image */
.detail-img-wrap {{
  width:100%; height:155px; border-radius:var(--rx); overflow:hidden;
  position:relative; background:var(--surface-2); border:1px solid var(--border);
  box-shadow:0 4px 18px rgba(44,59,46,0.05);
}}
.detail-img-wrap img {{ width:100%; height:100%; object-fit:cover }}
.detail-img-fallback {{
  width:100%; height:100%; display:flex; align-items:center;
  justify-content:center; font-size:60px; opacity:.35;
}}

.plant-hdr {{ display:flex; align-items:flex-start; gap:14px }}
.big-emoji {{
  font-size:40px; flex-shrink:0; line-height:1;
  background:var(--surface-2); padding:12px; border-radius:var(--r);
  box-shadow:0 4px 14px rgba(44,59,46,0.05);
}}
.plant-hdr-text h2 {{
  font-family:'Playfair Display',serif;
  font-size:21px; font-weight:700; line-height:1.25; color:var(--text);
}}
.plant-hdr-text .botanical {{ font-size:12px; color:var(--muted); font-style:italic; margin-top:3px }}
.coords-row {{ font-size:12px; color:var(--muted); margin-top:6px; font-variant-numeric:tabular-nums; font-weight:500 }}
.floor-tag {{
  display:inline-block; padding:4px 11px; border-radius:99px;
  font-size:11px; font-weight:600;
  background:rgba(255,255,255,0.8); color:var(--text); margin-top:8px;
  border:1px solid var(--border); box-shadow:0 2px 8px rgba(44,59,46,0.03);
}}

/* ══ VITAL-SCORE RING (NEU) ══ */
.vital-card {{
  background:rgba(255,255,255,0.75);
  backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,0.65);
  border-radius:var(--rx);
  padding:20px;
  display:flex; align-items:center; gap:20px;
  box-shadow:0 8px 32px rgba(44,59,46,0.06), inset 0 1px 0 rgba(255,255,255,0.8);
}}
.vital-ring-wrap {{
  flex-shrink:0; position:relative;
  width:82px; height:82px;
}}
.vital-ring-wrap svg {{ transform:rotate(-90deg) }}
.vital-ring-track {{ fill:none; stroke:rgba(44,59,46,0.07); stroke-width:8 }}
.vital-ring-fill  {{ fill:none; stroke-width:8; stroke-linecap:round; transition:stroke-dashoffset 1.2s var(--ease) }}
.vital-score-label {{
  position:absolute; inset:0;
  display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:1px;
}}
.vital-score-num {{
  font-family:'Playfair Display',serif;
  font-size:21px; font-weight:700; line-height:1;
  color:var(--text);
}}
.vital-score-pct {{ font-size:10px; font-weight:600; color:var(--muted) }}
.vital-info {{ flex:1 }}
.vital-title {{
  font-family:'Playfair Display',serif;
  font-size:15px; font-weight:600; color:var(--text); margin-bottom:6px;
}}
.vital-sub-row {{ display:flex; flex-direction:column; gap:6px }}
.vital-sub {{
  display:flex; align-items:center; gap:8px;
  font-size:12px; font-weight:500; color:var(--muted);
}}
.vital-sub-bar-wrap {{ flex:1 }}
.vital-sub-bar-track {{
  height:5px; border-radius:3px;
  background:rgba(44,59,46,0.07); overflow:hidden;
}}
.vital-sub-bar-fill {{
  height:100%; border-radius:3px;
  transition:width 1s var(--ease);
}}
.vital-sub-val {{
  font-size:11px; font-weight:700;
  min-width:30px; text-align:right; color:var(--text);
}}

/* Staunässe-Warnung (NEU) */
.staunaesse-warn {{
  background:rgba(123,174,196,0.12);
  border:1px solid rgba(123,174,196,0.35);
  border-radius:var(--rs); padding:12px 14px;
  display:flex; align-items:flex-start; gap:10px;
  backdrop-filter:blur(8px);
}}
.staunaesse-icon {{ font-size:20px; flex-shrink:0 }}
.staunaesse-text {{ font-size:12.5px; font-weight:500; color:var(--text-2); line-height:1.5 }}
.staunaesse-title {{ font-weight:700; color:var(--staunaesse); font-size:13px; margin-bottom:2px }}

/* DLI Panel */
.dli-panel {{
  background:linear-gradient(135deg, rgba(107,158,196,0.07) 0%, rgba(141,170,145,0.06) 100%);
  border:1px solid rgba(107,158,196,0.22); border-radius:var(--rx); padding:16px;
  display:flex; flex-direction:column; gap:12px;
  box-shadow:0 4px 18px rgba(107,158,196,0.05);
}}
.dli-panel-title {{
  font-size:11px; font-weight:700; color:var(--dli-color);
  text-transform:uppercase; letter-spacing:.08em;
  display:flex; align-items:center; gap:6px;
}}
.dli-score-row {{ display:flex; align-items:baseline; gap:8px }}
.dli-score-val {{
  font-family:'Playfair Display',serif;
  font-size:30px; font-weight:700; color:var(--text);
}}
.dli-score-unit {{ font-size:13px; color:var(--muted); font-weight:500 }}
.dli-bar-wrap {{ display:flex; flex-direction:column; gap:6px }}
.dli-bar-track {{
  height:7px; border-radius:4px;
  background:rgba(44,59,46,0.07); position:relative; overflow:hidden;
}}
.dli-bar-fill {{
  height:100%; border-radius:4px;
  transition:width .8s var(--ease);
  background:linear-gradient(90deg, var(--dli-dim), var(--dli-color));
}}
.dli-bar-labels {{
  display:flex; justify-content:space-between;
  font-size:11px; font-weight:600; color:var(--muted);
}}
.dli-live-row {{
  display:flex; align-items:center; gap:8px; padding:8px 12px;
  background:rgba(255,255,255,0.65); border-radius:var(--rs); border:1px solid var(--border);
}}
.dli-live-dot {{
  width:6px; height:6px; border-radius:50%;
  background:var(--warn); box-shadow:0 0 6px var(--warn);
  animation:pulse2 2s infinite; flex-shrink:0;
}}
@keyframes pulse2 {{ 0%,100%{{opacity:1}} 50%{{opacity:.4}} }}
.dli-live-text {{ font-size:12px; font-weight:600; color:var(--text); flex:1 }}
.dli-live-val  {{ font-size:12px; font-weight:700; color:var(--muted); font-variant-numeric:tabular-nums }}

.score-badge {{
  border-radius:var(--rx); padding:14px 16px;
  display:flex; align-items:center; gap:14px;
  background:rgba(255,255,255,0.75); backdrop-filter:blur(8px);
  box-shadow:0 4px 18px rgba(44,59,46,0.04);
}}
.score-badge .sc-icon {{ font-size:26px }}
.score-badge .sc-text h3 {{ font-family:'Playfair Display',serif; font-size:15px; font-weight:600 }}
.score-badge .sc-text p  {{ font-size:12.5px; color:var(--muted); margin-top:4px; line-height:1.45 }}
.score-badge.ideal {{ border:1px solid var(--accent-glow) }}
.score-badge.ideal .sc-text h3 {{ color:var(--accent-dark) }}
.score-badge.ok    {{ border:1px solid rgba(201,149,106,0.35) }}
.score-badge.ok .sc-text h3    {{ color:var(--warn) }}
.score-badge.bad   {{ border:1px solid rgba(201,112,112,0.35) }}
.score-badge.bad .sc-text h3   {{ color:var(--danger) }}

.astro-panel {{
  background:rgba(255,255,255,0.72); backdrop-filter:blur(10px);
  border:1px solid var(--border); border-radius:var(--rx); padding:16px;
  display:flex; flex-direction:column; gap:10px;
  box-shadow:0 4px 18px rgba(44,59,46,0.04);
}}
.astro-title {{
  font-size:12px; font-weight:600; color:var(--muted);
  text-transform:uppercase; letter-spacing:.08em; margin-bottom:4px;
}}
.astro-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:10px }}
.astro-cell {{ background:rgba(249,247,242,0.8); border-radius:var(--rs); padding:12px }}
.astro-cell-lbl {{ font-size:10px; font-weight:600; color:var(--muted2); text-transform:uppercase; letter-spacing:.05em; margin-bottom:4px }}
.astro-cell-val {{
  font-family:'Playfair Display',serif;
  font-size:20px; font-weight:700; color:var(--text);
}}
.astro-cell-unit {{ font-size:12px; font-weight:500; color:var(--muted); margin-left:4px }}
.window-chips {{ display:flex; gap:6px; flex-wrap:wrap }}
.win-chip {{
  font-size:11px; font-weight:600; padding:4px 10px; border-radius:99px;
  background:var(--bg-2); border:1px solid var(--border); color:var(--muted);
}}
.win-chip.hit {{ background:var(--warn-dim); border-color:rgba(201,149,106,0.35); color:#a06b3a }}

.light-bar-wrap {{
  display:flex; flex-direction:column; gap:10px;
  background:rgba(255,255,255,0.72); padding:16px; border-radius:var(--rx);
  border:1px solid var(--border); box-shadow:0 4px 18px rgba(44,59,46,0.04);
}}
.lbw-label {{ display:flex; justify-content:space-between; font-size:13px; font-weight:600; color:var(--text) }}
.lbw-track {{ height:11px; border-radius:6px; background:rgba(44,59,46,0.06); position:relative; overflow:hidden }}
.lbw-fill {{
  height:100%; border-radius:6px;
  background:linear-gradient(90deg, var(--accent-glow), var(--accent));
  transition:width .8s var(--ease);
}}
.lbw-needle {{
  position:absolute; top:-2px; bottom:-2px; width:3px;
  background:#fff; border-radius:2px; box-shadow:0 0 4px rgba(0,0,0,.15);
}}

.data-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:10px }}
.dc {{
  background:rgba(255,255,255,0.72); backdrop-filter:blur(8px);
  border:1px solid var(--border); border-radius:var(--r); padding:14px;
  box-shadow:0 4px 14px rgba(44,59,46,0.03);
}}
.dc-lbl {{ font-size:11px; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; margin-bottom:5px }}
.dc-val {{ font-family:'Playfair Display',serif; font-size:21px; font-weight:700; color:var(--text) }}
.dc-unit {{ font-size:12px; font-weight:500; color:var(--muted); margin-left:4px }}
.detail-extra-row {{
  background:rgba(255,255,255,0.72); backdrop-filter:blur(8px);
  border:1px solid var(--border); border-radius:var(--r); padding:14px 16px;
  display:flex; flex-direction:column; gap:4px;
  box-shadow:0 4px 14px rgba(44,59,46,0.03);
}}
.detail-extra-lbl {{ font-size:10px; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:.06em }}
.detail-extra-val {{ font-size:13px; font-weight:500; color:var(--text); line-height:1.5 }}

.action-row {{ display:flex; gap:10px; margin-top:6px }}
.act-btn {{
  flex:1; padding:12px; border-radius:var(--r); font-size:13px; font-weight:600;
  transition:all var(--t) var(--ease);
  border:1px solid var(--border); background:rgba(255,255,255,0.75); color:var(--text);
  box-shadow:0 2px 8px rgba(44,59,46,0.03);
}}
.act-btn:hover {{
  background:rgba(255,255,255,0.95);
  transform:translateY(-1px);
  box-shadow:0 5px 16px rgba(44,59,46,0.07);
}}
.act-btn.primary {{
  background:var(--accent); border-color:var(--accent); color:#fff;
}}
.act-btn.primary:hover {{
  background:var(--accent-dark);
  box-shadow:0 5px 18px var(--accent-glow);
}}
.act-btn.danger-btn {{
  background:rgba(255,255,255,0.75);
  border-color:rgba(201,112,112,0.35); color:var(--danger);
}}
.act-btn.danger-btn:hover {{ background:var(--danger-dim) }}

/* ── LIBRARY VIEW ── */
#library-view {{
  display:none; flex:1; overflow-y:auto; padding:24px 30px;
  flex-direction:column; gap:22px;
}}
#library-view.active {{ display:flex }}
#library-view::-webkit-scrollbar {{ width:7px }}
#library-view::-webkit-scrollbar-thumb {{ background:var(--border-2); border-radius:4px }}

.lib-header {{
  display:flex; align-items:center; gap:16px; flex-shrink:0; flex-wrap:wrap;
  background:rgba(255,255,255,0.75); backdrop-filter:blur(20px) saturate(1.3);
  padding:22px 26px; border-radius:var(--rx); border:1px solid rgba(255,255,255,0.7);
  box-shadow:0 8px 36px rgba(44,59,46,0.05), inset 0 1px 0 rgba(255,255,255,0.85);
}}
.lib-header h2 {{
  font-family:'Playfair Display',serif;
  font-size:25px; font-weight:700; color:var(--text);
}}
.lib-header-sub {{ font-size:13.5px; font-weight:500; color:var(--muted); margin-top:4px }}
.lib-search {{
  padding:11px 20px; background:rgba(255,255,255,0.8);
  border:1px solid var(--border); border-radius:99px;
  color:var(--text); font-size:14px; width:230px;
  box-shadow:inset 0 2px 6px rgba(44,59,46,0.03); transition:all var(--t) var(--ease-s);
}}
.lib-search::placeholder {{ color:var(--muted2) }}
.lib-search:focus {{ outline:none; border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-dim) }}

.lib-sort-wrap {{ display:flex; align-items:center; gap:10px; margin-left:auto }}
.lib-sort-label {{ font-size:12px; font-weight:600; color:var(--muted); white-space:nowrap }}
.lib-sort-select {{
  padding:8px 14px; background:rgba(255,255,255,0.8);
  border:1px solid var(--border); border-radius:99px;
  color:var(--text); font-size:13px; font-weight:600; cursor:pointer;
  box-shadow:0 2px 8px rgba(44,59,46,0.03); transition:all var(--t) var(--ease-s);
  appearance:none; -webkit-appearance:none; padding-right:28px;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236E8A72' stroke-width='2.5'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat:no-repeat; background-position:right 10px center;
}}
.lib-sort-select:focus {{ outline:none; border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-dim) }}
.lib-sort-dir-btn {{
  width:36px; height:36px; border-radius:99px; border:1px solid var(--border);
  background:rgba(255,255,255,0.8); color:var(--text); font-size:15px;
  display:flex; align-items:center; justify-content:center;
  transition:all var(--t) var(--ease); cursor:pointer; flex-shrink:0;
  box-shadow:0 2px 8px rgba(44,59,46,0.03);
}}
.lib-sort-dir-btn:hover {{ background:var(--surface-2); border-color:var(--accent-glow); transform:scale(1.1) }}

.lib-grid {{
  display:grid;
  grid-template-columns:repeat(auto-fill, minmax(370px, 1fr));
  gap:22px; padding-bottom:28px;
}}

/* ══ LIBRARY CARD mit Vital-Score Ring ══ */
.lib-card {{
  background:rgba(255,255,255,0.8);
  backdrop-filter:blur(16px) saturate(1.2);
  border:1px solid rgba(255,255,255,0.75);
  border-radius:var(--rx); display:flex; flex-direction:column;
  overflow:hidden; position:relative;
  transition:all var(--t) var(--ease);
  box-shadow:0 8px 28px rgba(44,59,46,0.05), inset 0 1px 0 rgba(255,255,255,0.9);
}}
.lib-card:hover {{
  border-color:var(--accent-glow);
  box-shadow:0 22px 64px rgba(44,59,46,0.11), inset 0 1px 0 rgba(255,255,255,0.9);
  transform:translateY(-7px);
}}
.lib-card-img {{
  width:100%; height:175px; overflow:hidden; position:relative;
  background:linear-gradient(135deg, var(--surface-2), var(--surface-3));
  flex-shrink:0;
}}
.lib-card-img img {{
  width:100%; height:100%; object-fit:cover;
  transition:transform .65s var(--ease-s);
}}
.lib-card:hover .lib-card-img img {{ transform:scale(1.07) }}
.lib-card-img-fallback {{
  width:100%; height:100%; display:flex;
  align-items:center; justify-content:center;
  font-size:70px; opacity:.3;
}}
.lib-card-img-overlay {{
  position:absolute; bottom:0; left:0; right:0;
  background:linear-gradient(to top, rgba(44,59,46,0.65) 0%, transparent 100%);
  padding:16px;
}}
.lib-card-img-overlay .lib-card-name {{
  font-family:'Playfair Display',serif; font-size:17px; font-weight:700;
  color:#fff; text-shadow:0 2px 8px rgba(0,0,0,.3);
}}
.lib-card-img-overlay .lib-card-botanical {{
  font-size:11.5px; color:rgba(255,255,255,0.72); font-style:italic; margin-top:2px;
}}

/* Vital-Score Badge auf der Karte */
.lib-vital-badge {{
  position:absolute; top:12px; right:12px;
  width:52px; height:52px;
  background:rgba(255,255,255,0.92); backdrop-filter:blur(8px);
  border-radius:50%; border:1px solid rgba(255,255,255,0.8);
  box-shadow:0 4px 16px rgba(44,59,46,0.12);
  display:flex; align-items:center; justify-content:center;
  flex-direction:column; gap:1px;
}}
.lib-vital-badge svg {{ transform:rotate(-90deg) }}
.lib-vital-badge-num {{
  position:absolute; font-family:'Playfair Display',serif;
  font-size:13px; font-weight:700; color:var(--text); line-height:1;
}}
.lib-vital-badge-pct {{
  position:absolute; font-size:8px; font-weight:600;
  color:var(--muted); margin-top:16px;
}}

.lib-card-body {{ padding:18px; display:flex; flex-direction:column; gap:14px }}

.lib-card-top-row {{ display:flex; align-items:center; gap:10px }}
.lib-card-loc {{ display:flex; align-items:center; gap:6px; font-size:13px; font-weight:500; color:var(--muted) }}
.lib-card-loc-dot {{ width:6px; height:6px; border-radius:50%; background:var(--muted2); flex-shrink:0 }}
.lib-card-loc-dot.placed {{ background:var(--accent); box-shadow:0 0 6px var(--accent) }}

.lib-light-row {{
  display:flex; align-items:center; gap:12px;
  background:var(--bg-2); padding:11px 14px; border-radius:var(--rs);
  border:1px solid var(--border);
}}
.lib-light-icon {{ font-size:17px; flex-shrink:0 }}
.lib-light-bar-wrap {{ flex:1 }}
.lib-light-bar-track {{ height:7px; border-radius:4px; background:rgba(44,59,46,0.07); position:relative; overflow:hidden }}
.lib-light-bar-fill {{ height:100%; border-radius:4px; transition:width .8s var(--ease) }}
.lib-light-labels {{ display:flex; justify-content:space-between; font-size:11px; font-weight:600; color:var(--muted); margin-top:5px }}
.lib-light-score {{ font-family:'Playfair Display',serif; font-size:16px; font-weight:700; min-width:44px; text-align:right; flex-shrink:0 }}

/* ── VITAL-SCORE AUFSCHLÜSSELUNG IN BIBLIOTHEKSKARTE ── */
.lib-vital-breakdown {{
  background:linear-gradient(135deg, rgba(141,170,145,0.06), rgba(249,247,242,0.9));
  border:1px solid var(--border); border-radius:var(--rs); padding:12px 14px;
  display:flex; flex-direction:column; gap:8px;
}}
.lib-vital-breakdown-title {{
  font-size:10px; font-weight:700; color:var(--accent-dark);
  text-transform:uppercase; letter-spacing:.08em;
  display:flex; align-items:center; justify-content:space-between;
}}
.lib-vital-total-badge {{
  font-family:'Playfair Display',serif; font-size:14px; font-weight:700;
}}
.lib-vital-row {{
  display:flex; align-items:center; gap:8px;
}}
.lib-vital-row-icon {{ font-size:13px; width:18px; text-align:center; flex-shrink:0; }}
.lib-vital-row-label {{ font-size:11px; font-weight:500; color:var(--muted); width:62px; flex-shrink:0; }}
.lib-vital-row-track {{
  flex:1; height:5px; border-radius:3px;
  background:rgba(44,59,46,0.07); overflow:hidden;
}}
.lib-vital-row-fill {{
  height:100%; border-radius:3px;
  transition:width .9s var(--ease);
}}
.lib-vital-row-fill.licht     {{ background:linear-gradient(90deg,rgba(201,149,106,.4),var(--warn)); }}
.lib-vital-row-fill.giessen   {{ background:linear-gradient(90deg,rgba(107,158,196,.4),var(--dli-color)); }}
.lib-vital-row-fill.duengen   {{ background:linear-gradient(90deg,var(--accent-dim),var(--accent)); }}
.lib-vital-row-val {{
  font-size:11px; font-weight:700; color:var(--text);
  min-width:34px; text-align:right; flex-shrink:0;
}}
.lib-vital-weight {{
  font-size:9.5px; font-weight:500; color:var(--muted2);
  min-width:30px; text-align:right; flex-shrink:0;
}}

.lib-divider {{ height:1px; background:var(--border) }}
.lib-care-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:9px }}
.lib-care-cell {{
  background:var(--bg-2); border-radius:var(--rs); padding:10px 13px;
  display:flex; flex-direction:column; gap:4px; border:1px solid var(--border);
}}
.lib-care-cell-lbl {{ font-size:10px; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:.08em }}
.lib-care-cell-val {{ font-size:14.5px; font-weight:700; color:var(--text) }}
.lib-care-cell-unit {{ font-size:11px; color:var(--muted); margin-left:3px; font-weight:500 }}

.lib-besonderheit {{
  background:linear-gradient(135deg, rgba(141,170,145,0.06), rgba(107,158,196,0.05));
  border:1px solid var(--border); border-radius:var(--rs); padding:12px 14px;
  font-size:12.5px; color:var(--text); line-height:1.55; font-style:italic;
  border-left:3px solid var(--accent-glow);
}}
.lib-besonderheit-lbl {{ font-size:10px; font-weight:700; color:var(--accent-dark); text-transform:uppercase; letter-spacing:.08em; margin-bottom:3px; font-style:normal }}

.lib-humidity-row {{ display:flex; align-items:center; gap:9px; font-size:13px; color:var(--muted); font-weight:500 }}
.lib-humidity-badge {{
  padding:4px 10px; border-radius:99px; font-size:11px; font-weight:700;
  background:var(--dli-dim); color:var(--dli-color); border:1px solid rgba(107,158,196,0.2);
}}

.lib-status-chip {{
  display:inline-flex; align-items:center; gap:6px;
  padding:5px 12px; border-radius:99px; font-size:12px; font-weight:600;
}}
.lib-status-chip.ideal {{
  background:rgba(255,255,255,0.8); color:var(--accent-dark);
  border:1px solid var(--accent-glow); box-shadow:0 2px 8px var(--accent-dim);
}}
.lib-status-chip.ok {{
  background:rgba(255,255,255,0.8); color:#a06b3a;
  border:1px solid rgba(201,149,106,0.35); box-shadow:0 2px 8px var(--warn-dim);
}}
.lib-status-chip.bad {{
  background:rgba(255,255,255,0.8); color:var(--danger);
  border:1px solid rgba(201,112,112,0.35); box-shadow:0 2px 8px var(--danger-dim);
}}
.lib-status-chip.none {{
  background:rgba(255,255,255,0.8); color:var(--muted); border:1px solid var(--border);
}}

.lib-card-footer {{ display:flex; align-items:center; gap:10px; padding:0 18px 18px; margin-top:auto }}
.show-on-map-btn {{
  flex:1; padding:11px; border-radius:var(--r); font-size:13px; font-weight:600;
  background:rgba(255,255,255,0.75); border:1px solid var(--border); color:var(--text);
  transition:all var(--t) var(--ease); box-shadow:0 2px 8px rgba(44,59,46,0.03);
}}
.show-on-map-btn:hover {{
  background:rgba(255,255,255,0.95); border-color:var(--accent-glow);
  color:var(--accent-dark); transform:translateY(-1px);
  box-shadow:0 5px 16px rgba(44,59,46,0.07);
}}

/* ── PFLEGE-KALENDER VIEW ── */
#care-view {{
  display:none; flex:1; overflow-y:auto; padding:24px 30px;
  flex-direction:column; gap:18px;
}}
#care-view.active {{ display:flex }}
#care-view::-webkit-scrollbar {{ width:7px }}
#care-view::-webkit-scrollbar-thumb {{ background:var(--border-2); border-radius:4px }}

.care-header {{
  display:flex; align-items:center; gap:16px; flex-shrink:0; flex-wrap:wrap;
  background:rgba(255,255,255,0.75); backdrop-filter:blur(20px) saturate(1.3);
  padding:22px 26px; border-radius:var(--rx); border:1px solid rgba(255,255,255,0.7);
  box-shadow:0 8px 36px rgba(44,59,46,0.05), inset 0 1px 0 rgba(255,255,255,0.85);
}}
.care-header h2 {{
  font-family:'Playfair Display',serif; font-size:25px; font-weight:700; color:var(--text);
}}
.care-header-sub {{ font-size:13.5px; font-weight:500; color:var(--muted); margin-top:4px }}
.care-header-actions {{ margin-left:auto; display:flex; gap:10px; align-items:center; flex-wrap:wrap }}
.care-mass-btn {{
  padding:10px 20px; font-size:13px; font-weight:600; border-radius:99px;
  border:1px solid var(--border); background:rgba(255,255,255,0.75); color:var(--text);
  transition:all var(--t) var(--ease); box-shadow:0 2px 8px rgba(44,59,46,0.03); cursor:pointer;
}}
.care-mass-btn:hover {{
  background:rgba(255,255,255,0.95); border-color:var(--accent-glow);
  color:var(--accent-dark); transform:translateY(-1px);
}}
.care-mass-btn.primary {{
  background:var(--accent); border-color:var(--accent); color:#fff;
}}
.care-mass-btn.primary:hover {{
  background:var(--accent-dark); box-shadow:0 5px 18px var(--accent-glow); transform:translateY(-1px);
}}

/* Care Sub-tabs */
.care-subtabs {{
  display:flex; gap:7px; background:rgba(255,255,255,0.7); backdrop-filter:blur(12px);
  border:1px solid var(--border); border-radius:var(--rx);
  padding:6px; box-shadow:0 4px 18px rgba(44,59,46,0.04); flex-shrink:0;
}}
.care-subtab {{
  flex:1; padding:10px 20px; font-size:13px; font-weight:600; color:var(--muted);
  border-radius:var(--r); transition:all var(--t) var(--ease);
}}
.care-subtab:hover {{ color:var(--text); background:var(--surface-2) }}
.care-subtab.active {{
  background:var(--accent); color:#fff; box-shadow:0 4px 14px var(--accent-glow);
}}

/* Calendar Grid */
#care-calendar-pane {{ display:flex; flex-direction:column; gap:18px }}
#care-status-pane   {{ display:none; flex-direction:column; gap:14px }}

.calendar-wrap {{
  background:rgba(255,255,255,0.75); backdrop-filter:blur(16px);
  border:1px solid rgba(255,255,255,0.7); border-radius:var(--rx); overflow:hidden;
  box-shadow:0 8px 36px rgba(44,59,46,0.05);
}}
.calendar-nav {{
  display:flex; align-items:center; justify-content:space-between;
  padding:18px 24px; border-bottom:1px solid var(--border);
}}
.calendar-nav-title {{
  font-family:'Playfair Display',serif; font-size:17px; font-weight:700; color:var(--text);
}}
.calendar-nav-btn {{
  width:36px; height:36px; border-radius:50%; border:1px solid var(--border);
  background:rgba(255,255,255,0.8); color:var(--text); font-size:15px;
  display:flex; align-items:center; justify-content:center;
  transition:all var(--t) var(--ease); cursor:pointer;
}}
.calendar-nav-btn:hover {{ background:var(--surface-2); border-color:var(--accent-glow); transform:scale(1.1) }}
.cal-grid {{ display:grid; grid-template-columns:repeat(7,1fr) }}
.cal-day-header {{
  padding:11px 8px; text-align:center; font-size:11px; font-weight:700; color:var(--muted);
  text-transform:uppercase; letter-spacing:.06em; background:var(--bg-2);
  border-bottom:1px solid var(--border);
}}
.cal-cell {{
  min-height:88px; padding:10px 8px;
  border-right:1px solid var(--border); border-bottom:1px solid var(--border);
  position:relative; transition:background .2s;
}}
.cal-cell:nth-child(7n) {{ border-right:none }}
.cal-cell:nth-last-child(-n+7) {{ border-bottom:none }}
.cal-cell.other-month .cal-day-num {{ color:var(--muted2); opacity:.45 }}
.cal-cell.today {{ background:linear-gradient(135deg,rgba(141,170,145,0.07),rgba(141,170,145,0.03)) }}
.cal-cell.today .cal-day-num {{
  background:var(--accent); color:#fff; width:27px; height:27px; border-radius:50%;
  display:flex; align-items:center; justify-content:center; font-weight:700;
  box-shadow:0 2px 10px var(--accent-glow);
}}
.cal-day-num {{
  font-size:13px; font-weight:600; color:var(--text); margin-bottom:5px;
  width:27px; height:27px; display:flex; align-items:center; justify-content:center;
}}
.cal-events {{ display:flex; flex-direction:column; gap:3px }}
.cal-event {{
  font-size:10px; font-weight:600; padding:2px 6px; border-radius:4px;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}}
.cal-event.water          {{ background:rgba(107,158,196,0.13); color:#2b6e9e }}
.cal-event.fertilize      {{ background:var(--accent-dim); color:var(--accent-dark) }}
.cal-event.due-water      {{ background:rgba(107,158,196,0.28); color:#2b6e9e; border:1px solid rgba(107,158,196,0.35) }}
.cal-event.due-fertilize  {{ background:rgba(141,170,145,0.22); color:var(--accent-dark); border:1px solid var(--accent-glow) }}

/* ── KALENDER KLICKBARE ZELLEN ── */
.cal-cell {{
  cursor: pointer;
}}
.cal-cell:not(.other-month):hover {{
  background: rgba(141,170,145,0.09);
}}
.cal-cell.selected-day {{
  background: rgba(141,170,145,0.15);
  outline: 2px solid var(--accent-glow);
  outline-offset: -2px;
}}

/* ── TAG-DETAIL MODAL ── */
#day-modal-overlay {{
  display:none; position:fixed; inset:0; z-index:800;
  background:rgba(44,59,46,0.28); backdrop-filter:blur(6px);
  align-items:center; justify-content:center;
}}
#day-modal-overlay.open {{ display:flex; }}
#day-modal {{
  background:var(--surface-solid);
  border:1px solid rgba(255,255,255,0.8);
  border-radius:var(--rx);
  box-shadow:0 32px 80px rgba(44,59,46,0.18), inset 0 1px 0 rgba(255,255,255,0.9);
  width:min(520px, 95vw); max-height:80vh;
  display:flex; flex-direction:column; overflow:hidden;
  animation: modalIn .28s var(--ease) both;
}}
@keyframes modalIn {{
  from {{ transform:scale(0.92) translateY(12px); opacity:0; }}
  to   {{ transform:scale(1)    translateY(0);    opacity:1; }}
}}
.day-modal-header {{
  padding:22px 26px 18px;
  border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:12px;
}}
.day-modal-title {{
  font-family:'Playfair Display',serif;
  font-size:19px; font-weight:700; color:var(--text); flex:1;
}}
.day-modal-close {{
  width:32px; height:32px; border-radius:50%;
  border:1px solid var(--border); background:rgba(255,255,255,0.8);
  color:var(--muted); font-size:14px; display:flex;
  align-items:center; justify-content:center;
  transition:all var(--t) var(--ease); cursor:pointer; flex-shrink:0;
}}
.day-modal-close:hover {{ background:var(--danger-dim); color:var(--danger); border-color:rgba(201,112,112,0.35); }}
.day-modal-body {{ padding:20px 26px; overflow-y:auto; flex:1; display:flex; flex-direction:column; gap:10px; }}
.day-modal-empty {{
  text-align:center; padding:32px 0; color:var(--muted);
  font-size:14px; font-weight:500;
}}
.day-modal-empty .dm-icon {{ font-size:36px; margin-bottom:10px; opacity:.4; }}
.day-event-row {{
  display:flex; align-items:center; gap:12px;
  padding:11px 14px; border-radius:var(--r);
  border:1px solid var(--border);
  background:rgba(255,255,255,0.7);
  transition:background .18s;
}}
.day-event-row:hover {{ background:rgba(255,255,255,0.95); }}
.day-event-icon {{
  width:34px; height:34px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:16px; flex-shrink:0;
}}
.day-event-icon.water {{ background:rgba(107,158,196,0.14); }}
.day-event-icon.fertilize {{ background:var(--accent-dim); }}
.day-event-icon.due-water {{ background:rgba(107,158,196,0.22); }}
.day-event-icon.due-fertilize {{ background:rgba(141,170,145,0.22); }}
.day-event-info {{ flex:1; min-width:0; }}
.day-event-name {{ font-size:14px; font-weight:600; color:var(--text); }}
.day-event-sub {{ font-size:11.5px; color:var(--muted); margin-top:2px; }}
.day-event-chip {{
  font-size:11px; font-weight:700; padding:3px 10px;
  border-radius:99px; border:1px solid transparent; flex-shrink:0;
}}
.day-event-chip.done {{ background:rgba(107,158,196,0.12); color:#2b6e9e; border-color:rgba(107,158,196,0.3); }}
.day-event-chip.due  {{ background:var(--accent-dim); color:var(--accent-dark); border-color:var(--accent-glow); }}
.day-event-chip.overdue {{ background:var(--danger-dim); color:var(--danger); border-color:rgba(201,112,112,0.28); }}

/* Bulk-Action-Bar */
#bulk-action-bar {{
  display:none; align-items:center; gap:12px; padding:14px 20px;
  background:rgba(255,255,255,0.82); backdrop-filter:blur(12px);
  border:1px solid var(--accent-glow); border-radius:var(--rx);
  box-shadow:0 4px 18px var(--accent-dim); flex-shrink:0; flex-wrap:wrap;
}}
#bulk-action-bar.visible {{ display:flex }}
.bulk-count-badge {{
  font-family:'Playfair Display',serif; font-size:14px; font-weight:700; color:var(--text);
  background:var(--surface-2); padding:6px 14px; border-radius:99px; border:1px solid var(--border);
}}
.bulk-btn {{
  padding:10px 20px; font-size:13px; font-weight:600; border-radius:99px; cursor:pointer;
  border:1px solid var(--border); background:rgba(255,255,255,0.75); color:var(--text);
  transition:all var(--t) var(--ease); box-shadow:0 2px 8px rgba(44,59,46,0.03);
}}
.bulk-btn:hover {{ transform:translateY(-1px) }}
.bulk-btn.water {{
  border-color:rgba(107,158,196,0.45); color:#2b6e9e;
  background:rgba(107,158,196,0.08);
}}
.bulk-btn.water:hover {{ background:rgba(107,158,196,0.16); box-shadow:0 4px 14px rgba(107,158,196,0.16) }}
.bulk-btn.fertilize {{
  border-color:var(--accent-glow); color:var(--accent-dark); background:var(--surface-2);
}}
.bulk-btn.fertilize:hover {{ background:var(--surface-3); box-shadow:0 4px 14px var(--accent-dim) }}
.bulk-btn.clear {{ color:var(--muted) }}
.bulk-btn.clear:hover {{ color:var(--danger); border-color:rgba(201,112,112,0.35); background:var(--danger-dim) }}

/* Care Status */
.care-section-title {{
  font-family:'Playfair Display',serif;
  font-size:16px; font-weight:700; color:var(--text);
  display:flex; align-items:center; gap:10px; margin-bottom:4px;
}}
.care-section-title .care-badge {{
  font-family:'DM Sans',sans-serif; font-size:12px; font-weight:600;
  padding:3px 10px; border-radius:99px;
  background:var(--danger-dim); color:var(--danger); border:1px solid rgba(201,112,112,0.28);
}}
.care-section-title .care-badge.warn {{ background:var(--warn-dim); color:#a06b3a; border-color:rgba(201,149,106,0.28) }}
.care-section-title .care-badge.ok  {{ background:var(--surface-2); color:var(--accent-dark); border-color:var(--accent-glow) }}

/* Pflege-Karten */
.care-card {{
  background:rgba(255,255,255,0.78); backdrop-filter:blur(14px);
  border:1px solid rgba(255,255,255,0.7); border-radius:var(--rx); padding:18px;
  display:flex; align-items:center; gap:14px;
  transition:all var(--t) var(--ease-s);
  box-shadow:0 6px 24px rgba(44,59,46,0.05);
  position:relative; overflow:hidden;
}}
.care-card::before {{
  content:''; position:absolute; left:0; top:0; bottom:0; width:4px;
  background:var(--accent); border-radius:0; transition:background var(--t) var(--ease-s);
}}
.care-card.overdue::before {{ background:var(--danger) }}
.care-card.soon::before   {{ background:var(--warn) }}
.care-card.done::before   {{ background:var(--muted2) }}
.care-card:hover {{
  box-shadow:0 10px 36px rgba(44,59,46,0.08);
  transform:translateY(-1px);
}}
.care-card.selected-card {{
  border-color:var(--accent-glow);
  box-shadow:0 0 0 3px var(--accent-dim), 0 10px 36px rgba(44,59,46,0.08);
}}

/* Checkbox */
.care-card-checkbox-wrap {{ flex-shrink:0; display:flex; align-items:center; justify-content:center; width:24px; height:24px }}
.care-checkbox {{
  width:18px; height:18px; border-radius:6px; border:2px solid var(--border-2);
  background:rgba(255,255,255,0.85); cursor:pointer; appearance:none; -webkit-appearance:none;
  transition:all .2s; flex-shrink:0; position:relative;
}}
.care-checkbox:checked {{ background:var(--accent); border-color:var(--accent) }}
.care-checkbox:checked::after {{
  content:'✓'; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  font-size:11px; font-weight:700; color:#fff; line-height:1;
}}
.care-checkbox:hover {{ border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-dim) }}

/* Thumbnails in care cards */
.care-card-thumb {{
  width:52px; height:52px; border-radius:var(--r); overflow:hidden; flex-shrink:0;
  background:var(--surface-2); border:1px solid var(--border);
  display:flex; align-items:center; justify-content:center;
}}
.care-card-thumb img {{ width:100%; height:100%; object-fit:cover }}
.care-card-thumb-emoji {{ font-size:25px }}
.care-card-info {{ flex:1; min-width:0 }}
.care-card-name {{
  font-family:'Playfair Display',serif; font-size:15px; font-weight:700;
  color:var(--text); margin-bottom:4px;
}}
.care-card-meta {{ display:flex; gap:9px; flex-wrap:wrap; align-items:center; margin-bottom:9px }}
.care-chip {{
  font-size:11px; font-weight:600; padding:3px 10px; border-radius:99px;
  background:var(--surface-2); color:var(--muted); border:1px solid var(--border);
}}
.care-chip.overdue {{ background:var(--danger-dim); color:var(--danger); border-color:rgba(201,112,112,0.28) }}
.care-chip.soon    {{ background:var(--warn-dim); color:#a06b3a; border-color:rgba(201,149,106,0.28) }}
.care-chip.ok      {{ background:var(--surface-2); color:var(--accent-dark); border-color:var(--accent-glow) }}

.care-progress-wrap {{ display:flex; flex-direction:column; gap:5px; margin-bottom:7px }}
.care-progress-row  {{ display:flex; align-items:center; gap:8px }}
.care-progress-icon {{ font-size:12px; flex-shrink:0; width:16px }}
.care-progress-track {{ flex:1; height:5px; border-radius:3px; background:rgba(44,59,46,0.08); overflow:hidden }}
.care-progress-fill {{ height:100%; border-radius:3px; transition:width 1s var(--ease) }}
.care-progress-fill.water {{ background:linear-gradient(90deg, rgba(107,158,196,0.45), #6B9EC4) }}
.care-progress-fill.fertilize {{ background:linear-gradient(90deg, var(--accent-dim), var(--accent)) }}
.care-progress-pct {{ font-size:10px; font-weight:700; color:var(--muted); min-width:30px; text-align:right }}

.care-card-actions {{ display:flex; flex-direction:column; gap:7px; flex-shrink:0 }}
.care-btn {{
  padding:9px 14px; font-size:12px; font-weight:600; border-radius:var(--r);
  border:1px solid var(--border); background:rgba(255,255,255,0.75); color:var(--text);
  transition:all var(--t) var(--ease); cursor:pointer; white-space:nowrap;
  box-shadow:0 2px 8px rgba(44,59,46,0.03);
}}
.care-btn:hover {{ background:rgba(255,255,255,0.95); transform:translateY(-1px) }}
.care-btn:active {{ transform:scale(0.96) }}
.care-btn.water {{
  border-color:rgba(107,158,196,0.45); color:#2b6e9e;
  background:rgba(107,158,196,0.08);
}}
.care-btn.water:hover {{ background:rgba(107,158,196,0.16); box-shadow:0 4px 12px rgba(107,158,196,0.14) }}
.care-btn.fertilize {{
  border-color:var(--accent-glow); color:var(--accent-dark); background:var(--surface-2);
}}
.care-btn.fertilize:hover {{ background:var(--surface-3); box-shadow:0 4px 12px var(--accent-dim) }}
.care-btn.done-btn {{ opacity:.45; pointer-events:none }}
.care-btn.location {{
  border-color:rgba(107,158,196,0.35); color:var(--dli-color);
  background:rgba(107,158,196,0.07);
}}
.care-btn.location:hover {{ background:rgba(107,158,196,0.14); box-shadow:0 4px 12px rgba(107,158,196,0.13) }}

/* Historie */
.care-history {{
  background:rgba(255,255,255,0.75); backdrop-filter:blur(14px);
  border:1px solid rgba(255,255,255,0.7); border-radius:var(--rx); overflow:hidden;
  box-shadow:0 6px 24px rgba(44,59,46,0.05);
}}
.care-history-header {{
  padding:15px 20px; border-bottom:1px solid var(--border);
  font-family:'Playfair Display',serif; font-size:14px; font-weight:700;
  color:var(--text); display:flex; align-items:center; gap:10px;
}}
.history-entry {{
  display:flex; align-items:center; gap:12px; padding:12px 20px;
  border-bottom:1px solid var(--border); font-size:13px; transition:background .2s;
}}
.history-entry:last-child {{ border-bottom:none }}
.history-entry:hover {{ background:rgba(141,170,145,0.05) }}
.history-icon {{ font-size:15px; flex-shrink:0 }}
.history-text {{ flex:1; color:var(--text); font-weight:500 }}
.history-time {{ font-size:12px; color:var(--muted); font-variant-numeric:tabular-nums }}

.care-empty {{
  text-align:center; padding:44px 24px; color:var(--muted);
  background:rgba(255,255,255,0.7); border:1px dashed var(--border-2);
  border-radius:var(--rx); backdrop-filter:blur(8px);
}}
.care-empty .ce-icon {{ font-size:46px; margin-bottom:12px; opacity:.45 }}
.care-empty p {{ font-size:14px; font-weight:500; line-height:1.6 }}

/* ── TOAST & TOOLTIP ── */
#tooltip {{
  position:fixed; z-index:500; pointer-events:none;
  background:rgba(255,255,255,0.92); backdrop-filter:blur(10px);
  border:1px solid var(--border-2); border-radius:var(--rs);
  padding:10px 14px; font-size:12px; font-weight:600; color:var(--text);
  box-shadow:0 8px 28px rgba(44,59,46,0.09); opacity:0; transition:opacity .15s; max-width:240px;
}}
#tooltip.visible {{ opacity:1 }}

#save-toast {{
  position:fixed; bottom:24px; right:24px; z-index:999;
  background:rgba(255,255,255,0.92); backdrop-filter:blur(16px);
  border:1px solid var(--accent-glow); border-radius:var(--r);
  padding:14px 20px; font-size:14px; font-weight:600; color:var(--text);
  box-shadow:0 8px 36px rgba(141,170,145,0.18);
  transform:translateY(30px); opacity:0;
  transition:all .4s var(--ease);
  display:flex; align-items:center; gap:10px;
}}
#save-toast.show {{ transform:translateY(0); opacity:1 }}

/* ── LOADING ── */
#loading {{
  position:fixed; inset:0; z-index:9999; background:var(--bg);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:20px;
  transition:opacity .6s, visibility .6s;
}}
#loading.hidden {{ opacity:0; visibility:hidden }}
#loading .ld-icon {{ font-size:56px; animation:breathe 3s ease-in-out infinite }}
#loading p {{ font-size:16px; font-weight:400; color:var(--muted); letter-spacing:.01em }}
@keyframes breathe {{
  0%,100% {{ transform:scale(1); opacity:.55 }}
  50%      {{ transform:scale(1.12); opacity:1 }}
}}
</style>
</head>
<body>

<div id="loading"><div class="ld-icon">🌿</div><p>Natürliches Umfeld wird geladen…</p></div>
<div id="tooltip"></div>
<div id="save-toast">💾 <span id="toast-msg">Gespeichert</span></div>

<!-- HEADER -->
<div id="header">
  <span class="logo">🌿 Pflanzen-Planer</span>
  <span class="logo-sep">|</span>
  <span style="font-size:14px;font-weight:500;color:var(--muted)" id="month-label"></span>
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
           onerror="this.src='https://placehold.co/1100x600/F9F7F2/8DAA91?text=Grundriss+nicht+gefunden'">
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
      <div class="lib-sort-wrap">
        <span class="lib-sort-label">Sortieren:</span>
        <select class="lib-sort-select" id="lib-sort-key" onchange="renderLibrary()">
          <option value="name">Name</option>
          <option value="licht">Lichtbedarf</option>
          <option value="giessen">Gießbedarf</option>
          <option value="vital">Vital-Score</option>
        </select>
        <button class="lib-sort-dir-btn" id="lib-sort-dir-btn" title="Sortierrichtung umkehren"
                onclick="toggleSortDir()" style="font-size:14px;">↑</button>
      </div>
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
        <span id="care-sync-status" style="font-size:12px;font-weight:600;color:var(--muted);padding:0 4px;">☁️ …</span>
        <button class="care-mass-btn" onclick="exportCareCSV()">📥 Export CSV</button>
        <button class="care-mass-btn" onclick="waterAllDue()">💧 Alle fälligen gießen</button>
        <button class="care-mass-btn primary" onclick="refreshCareFromSheets()">🔄 Aktualisieren</button>
      </div>
    </div>

    <div class="care-subtabs">
      <button class="care-subtab active" id="subtab-calendar" onclick="switchCareSubtab('calendar')">📅 Kalender</button>
      <button class="care-subtab" id="subtab-status" onclick="switchCareSubtab('status')">📋 Pflege-Status</button>
      <button class="care-subtab" id="subtab-history" onclick="switchCareSubtab('history')">🕐 Historie</button>
    </div>

    <div id="care-calendar-pane">
      <div id="care-upcoming-section" style="display:none"></div>
      <div class="calendar-wrap">
        <div class="calendar-nav">
          <button class="calendar-nav-btn" onclick="changeCalMonth(-1)">‹</button>
          <span class="calendar-nav-title" id="cal-month-title"></span>
          <button class="calendar-nav-btn" onclick="changeCalMonth(1)">›</button>
        </div>
        <div class="cal-grid" id="cal-grid"></div>
      </div>
    </div>

    <div id="care-status-pane">
      <div id="bulk-action-bar">
        <span class="bulk-count-badge" id="bulk-count-label">0 ausgewählt</span>
        <button class="bulk-btn water" onclick="bulkWater()">💧 Alle ausgewählten gießen</button>
        <button class="bulk-btn fertilize" onclick="bulkFertilize()">🌿 Alle ausgewählten düngen</button>
        <button class="bulk-btn clear" onclick="clearSelection()" style="margin-left:auto;">✕ Auswahl aufheben</button>
      </div>
      <div id="care-overdue-section"></div>
      <div id="care-soon-section"></div>
      <div id="care-all-section"></div>
    </div>

    <div id="care-history-pane" style="display:none">
      <div id="care-history-section"></div>
    </div>
  </div>

  <!-- RIGHT SIDEBAR -->
  <div id="right-sidebar">
    <div id="rsb-empty">
      <div class="empty-icon">🪴</div>
      <p style="font-size:14px;line-height:1.7;color:var(--muted);font-weight:400;">Klicke auf eine Pflanze<br>für Details &amp; Pflegehinweise.</p>
    </div>
    <div id="rsb-detail"></div>
  </div>

</div><!-- /main -->

<!-- TAG-DETAIL MODAL -->
<div id="day-modal-overlay" onclick="closeDayModal(event)">
  <div id="day-modal">
    <div class="day-modal-header">
      <div class="day-modal-title" id="day-modal-title">Tag</div>
      <button class="day-modal-close" onclick="closeDayModal()">✕</button>
    </div>
    <div class="day-modal-body" id="day-modal-body"></div>
  </div>
</div>

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
let dliMode         = false;
let dliCache        = {{}};
let calMonth        = NOW_MONTH;
let calYear         = NOW.getFullYear();
let libSortKey      = "name";
let libSortAsc      = true;
let selectedPlantIdxs = new Set();

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
// ★ VITAL-SCORE BERECHNUNG (0–100 Glücks-Index)
// ============================================================

/**
 * Berechnet den Glücks-Index (0–100) einer Pflanze.
 * Komponenten:
 *   - Licht-Score:     Verhältnis verfügbares/benötigtes Licht (40%)
 *   - Gieß-Score:      Nähe zum optimalen Gießzeitpunkt (35%)
 *   - Dünge-Score:     Nähe zum optimalen Düngezeitpunkt (25%)
 *
 * Gibt außerdem staunaesseRisk zurück (true wenn
 * das Gießintervall zu weniger als 20% verbraucht ist).
 */
function computeVitalScore(plantIdx) {{
  const p = plants[plantIdx];
  const pos = positions[plantIdx];

  // 1) Licht-Score (40%)
  let lichtScore = 0;
  if (pos) {{
    const ist = computeLicht(pos.x, pos.y, pos.floor);
    const soll = p.licht || 5;
    lichtScore = Math.min(1, ist / soll);
  }} else {{
    lichtScore = 0.5; // Unbekannt → neutral
  }}

  // 2) Gieß-Score (35%)
  const ws = getCareStatus(plantIdx, 'water');
  let giessScore = 0;
  let staunaesseRisk = false;
  if (ws) {{
    const elapsed = ws.lastDate
      ? (Date.now() - ws.lastDate.getTime()) / (1000 * 3600 * 24)
      : ws.intervalDays; // noch nie → als überfällig werten
    const ratio = elapsed / ws.intervalDays; // 0=gerade gegossen, 1=genau fällig, >1=überfällig
    if (ratio <= 0.2) {{
      // Gerade gegossen: zu feucht → Staunässegefahr
      staunaesseRisk = true;
      giessScore = 0.7; // nicht perfekt, aber besser als gar nicht
    }} else if (ratio <= 1.0) {{
      // Optimaler Bereich: Score zwischen 0.7 → 1.0 → 0.7 (Parabel)
      const normalized = (ratio - 0.2) / 0.8; // 0 → 1
      giessScore = 0.7 + 0.3 * Math.sin(normalized * Math.PI);
    }} else {{
      // Überfällig: Score fällt ab
      const overRatio = Math.min(1, (ratio - 1) / 1); // 0 → 1 über 1 weiteren Zyklus
      giessScore = Math.max(0, 0.7 * (1 - overRatio));
    }}
  }} else {{
    giessScore = 0.6; // Kein Intervall → neutral-positiv
  }}

  // 3) Dünge-Score (25%)
  const fs = getCareStatus(plantIdx, 'fertilize');
  let duengScore = 0;
  if (fs) {{
    const elapsedF = fs.lastDate
      ? (Date.now() - fs.lastDate.getTime()) / (1000 * 3600 * 24)
      : fs.intervalDays;
    const ratioF = elapsedF / fs.intervalDays;
    if (ratioF <= 1.0) {{
      const normalizedF = ratioF;
      duengScore = 0.65 + 0.35 * Math.sin(normalizedF * Math.PI);
    }} else {{
      const overRatioF = Math.min(1, (ratioF - 1) / 1.5);
      duengScore = Math.max(0, 0.65 * (1 - overRatioF));
    }}
  }} else {{
    duengScore = 0.6;
  }}

  const total = (lichtScore * 0.40 + giessScore * 0.35 + duengScore * 0.25) * 100;
  return {{
    score:         Math.round(Math.max(0, Math.min(100, total))),
    lichtPct:      Math.round(lichtScore * 100),
    giessPct:      Math.round(giessScore * 100),
    duengPct:      Math.round(duengScore * 100),
    staunaesseRisk
  }};
}}

/**
 * Erzeugt einen SVG-Ring-Chart für den Vital-Score.
 * r = Radius, cx/cy = Mittelpunkt, strokeColor = Farbe des Bogens
 */
function makeSvgRing(score, size=82, strokeColor=null) {{
  const r = (size / 2) - 5;
  const cx = size / 2, cy = size / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (score / 100) * circ;
  let color = strokeColor;
  if (!color) {{
    if (score >= 72) color = "var(--accent)";
    else if (score >= 45) color = "var(--warn)";
    else color = "var(--danger)";
  }}
  return `
    <svg width="${{size}}" height="${{size}}" viewBox="0 0 ${{size}} ${{size}}">
      <circle class="vital-ring-track" cx="${{cx}}" cy="${{cy}}" r="${{r}}"/>
      <circle class="vital-ring-fill"
        cx="${{cx}}" cy="${{cy}}" r="${{r}}"
        stroke="${{color}}"
        stroke-dasharray="${{circ.toFixed(1)}}"
        stroke-dashoffset="${{offset.toFixed(1)}}"/>
    </svg>
  `;
}}

/** Kleiner Inline-Ring für Bibliothekskarten */
function makeSmallRingSvg(score, size=48) {{
  const r = (size / 2) - 4;
  const cx = size / 2, cy = size / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (score / 100) * circ;
  let color = score >= 72 ? "var(--accent)" : score >= 45 ? "var(--warn)" : "var(--danger)";
  return `
    <svg width="${{size}}" height="${{size}}" viewBox="0 0 ${{size}} ${{size}}" style="transform:rotate(-90deg)">
      <circle fill="none" stroke="rgba(44,59,46,0.08)" stroke-width="5" cx="${{cx}}" cy="${{cy}}" r="${{r}}"/>
      <circle fill="none" stroke="${{color}}" stroke-width="5" stroke-linecap="round"
        cx="${{cx}}" cy="${{cy}}" r="${{r}}"
        stroke-dasharray="${{circ.toFixed(1)}}"
        stroke-dashoffset="${{offset.toFixed(1)}}"
        style="transition:stroke-dashoffset 1.2s cubic-bezier(0.34,1.56,0.64,1)"/>
    </svg>
    <div class="lib-vital-badge-num">${{score}}</div>
    <div class="lib-vital-badge-pct">%</div>
  `;
}}

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
// ★ DLI SIMULATION
// ============================================================
function computeDLI(px, py, floor) {{
  const today = new Date();
  const year = today.getFullYear(), month = today.getMonth(), day = today.getDate();
  let sumScore = 0, weightSum = 0;
  for(let h = 0; h < 24; h++) {{
    const dt = new Date(Date.UTC(year, month, day, h - 1, 0, 0));
    const sun = calcSunPosition(dt);
    if(sun.elevation <= 0) continue;
    const savedState = {{...sunState}};
    sunState = sun;
    const score = computeLichtFull(px, py, floor).score;
    sunState = savedState;
    const weight = Math.sin(sun.elevation * Math.PI / 180);
    sumScore  += score * weight;
    weightSum += weight;
  }}
  if(weightSum === 0) return 1;
  return Math.min(10, Math.max(1, Math.round(sumScore / weightSum * 10) / 10));
}}

let dliComputeScheduled = false;
function scheduleDLICompute(floor) {{
  if(dliComputeScheduled) return;
  dliComputeScheduled = true;
  requestAnimationFrame(()=>{{
    dliComputeScheduled = false;
    if(!dliMode) return;
    const step = 0.05;
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
    let winContrib = 0, samplesVisible = 0, totalSamples = 0, bestIncFactor = 0;
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
      const winMeter = isVertical ? (winPxLen / fh) * realH : (winPxLen / fw) * realW;
      const winSizeFactor = Math.min(3, winMeter) / 1.0;
      totalIlluminance += avgContrib * winSizeFactor;
    }}
    windowHits.push({{
      side: w.side, winAz: winAz.toFixed(0),
      incFactor: bestIncFactor.toFixed(2),
      visRatio: (samplesVisible/totalSamples).toFixed(2),
      occluded: samplesVisible === 0,
    }});
  }}
  totalIlluminance *= (1 + wallReflectance);
  const scaleFactor = 22;
  const score = Math.min(10, Math.max(1, Math.round(totalIlluminance * scaleFactor * 10) / 10));
  return {{ score, components: {{ totalIlluminance, skyDiff, sunDirect }}, windowHits }};
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
        const alpha = (lv/10)*0.26;
        const r = Math.round(92 + (lv/10)*50);
        const g = Math.round(155 + (lv/10)*30);
        const b = Math.round(214 - (lv/10)*50);
        ctx.fillStyle=`rgba(${{r}},${{g}},${{b}},${{alpha.toFixed(3)}})`;
      }} else {{
        lv = computeLicht(rx, ry, currentFloor);
        const alpha=(lv/10)*0.22;
        const r = Math.round(lv/10*251), g=222, b=Math.round((1-lv/10)*128+74);
        ctx.fillStyle=`rgba(${{r}},${{g}},${{b}},${{alpha.toFixed(3)}})`;
      }}
      ctx.fillRect(ix,iy,step,step);
    }}
  }}
}}

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
      {{name:"Monstera Deliciosa",botanisch:"Monstera deliciosa",licht:7,giessen:"3",dungen:"4",umtopfen:"Alle 2 Jahre",info:"Robuste Zimmerpflanze",emoji:"🌿",luftfeuchtigkeit:"60-80%",besprühen:"Ja",besonderheit:"Bekannt für ihre spektakulären Blattlöcher.",giessAll:{{}},duengAll:{{}}}},
      {{name:"Sukkulente",botanisch:"Echeveria spp.",licht:9,giessen:"14",dungen:"8",umtopfen:"Alle 3 Jahre",info:"Viel Sonne",emoji:"🌵",luftfeuchtigkeit:"30-50%",besprühen:"Nein",besonderheit:"Speichert Wasser in Blättern – extrem pflegeleicht.",giessAll:{{}},duengAll:{{}}}},
    ];
    setStatus(false,"Offline-Modus");
  }}
  plants.forEach((p,i)=>{{ if(!p.emoji) p.emoji=PLANT_EMOJIS[i%PLANT_EMOJIS.length]; }});
  $("inv-count").textContent = plants.length;
  await loadPositionsFromSheets();  // lädt lokal + Cloud (geräteübergreifend)
  renderInventory();
  loadCareData();
  renderLibrary();
  setFloor(currentFloor);
  $("loading").classList.add("hidden");
  updateSunInfo();
  renderCalendar();
  setInterval(()=>{{ updateSunInfo(); drawLightMap(); render(); }}, 60000);
}}

// ============================================================
// CSV PARSE — robust dataclass-style conversion
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

  function norm(s) {{
    return s.toLowerCase()
      .replace(/ä/g,"ae").replace(/ö/g,"oe").replace(/ü/g,"ue")
      .replace(/ß/g,"ss").replace(/Ä/g,"ae").replace(/Ö/g,"oe").replace(/Ü/g,"ue")
      .replace(/gißen/g,"giessen").replace(/düngen/g,"duengen")
      .replace(/[_ ]/g,"");
  }}
  function colFor(prefix, month) {{
    const target = norm(prefix + month);
    let idx = headers.findIndex(h => norm(h) === target);
    if(idx >= 0) return idx;
    const nMonth = norm(month);
    const nPre   = norm(prefix);
    idx = headers.findIndex(h => {{ const nh=norm(h); return nh.includes(nMonth) && nh.includes(nPre.slice(0,4)); }});
    return idx;
  }}

  const monthName = MONTHS_DE[NOW_MONTH];
  const colGiess  = colFor("Gießen_", monthName);
  const colDueng  = colFor("Düngen_", monthName);
  const giessAll={{}}, duengAll={{}};
  MONTHS_DE.forEach(m=>{{
    giessAll[m] = colFor("Gießen_", m);
    duengAll[m] = colFor("Düngen_", m);
  }});

  /**
   * Konvertiert eine CSV-Zeile robust in ein Plant-ähnliches Objekt.
   * Alle Felder werden typsicher extrahiert und validiert.
   */
  return lines.slice(1).filter(l=>l.trim()).map((line, i) => {{
    const cols = splitCSVLine(line);
    const safeCol = (idx) => idx>=0 ? (cols[idx]||"").trim().replace(/"/g,"") : "";
    const safeFloat = (idx, fallback=5) => {{
      const n = parseFloat(safeCol(idx));
      return isNaN(n) ? fallback : n;
    }};

    // Robust: alle monatlichen Intervalle als Dictionary
    const giessAllObj = {{}}, duengAllObj = {{}};
    MONTHS_DE.forEach(m => {{
      giessAllObj[m] = giessAll[m] >= 0 ? (safeCol(giessAll[m]) || "—") : "—";
      duengAllObj[m] = duengAll[m] >= 0 ? (safeCol(duengAll[m]) || "—") : "—";
    }});

    return {{
      id:            i,
      name:          safeCol(colName) || "Pflanze "+(i+1),
      botanisch:     safeCol(colBotanisch),
      licht:         safeFloat(colLicht, 5),
      giessen:       colGiess >= 0 ? (safeCol(colGiess) || "—") : "—",
      dungen:        colDueng >= 0 ? (safeCol(colDueng) || "—") : "—",
      umtopfen:      safeCol(colUmtopf) || "—",
      luftfeuchtigkeit: safeCol(colLuft) || "",
      "besprühen":   safeCol(colBespr) || "",
      besonderheit:  safeCol(colBesond) || "",
      emoji:         PLANT_EMOJIS[i % PLANT_EMOJIS.length],
      giessAll:      giessAllObj,
      duengAll:      duengAllObj,
      // Vital-Score-Felder: werden clientseitig bei Bedarf befüllt
      vital_score:   null,
      licht_score:   null,
      giess_score:   null,
      dueng_score:   null,
      staunaesse_risk: false,
    }};
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

const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx9Vf0xJ4gJPFt6j3SaQQjW2PKT29upU-UxmyoioOEs_upOXVA0MgKGmu17yZQm0uuM/exec";

let careSheetSyncing = false;
let careSyncPending  = false;

function saveCareDataLocal() {{
  try {{
    localStorage.setItem("pflanzen_care_v2", JSON.stringify(careData));
    localStorage.setItem("pflanzen_history_v2", JSON.stringify(careHistory.slice(0,200)));
  }} catch(e) {{ console.warn("care localStorage write failed:", e); }}
}}

async function saveCareDataToSheets() {{
  saveCareDataLocal();
  if(!APPS_SCRIPT_URL) return;
  if(careSheetSyncing) {{ careSyncPending = true; return; }}
  careSheetSyncing = true;
  updateCareSyncStatus("sync");
  try {{
    const payload = {{ action: "saveCare", careData: careData, careHistory: careHistory.slice(0, 200) }};
    await fetch(APPS_SCRIPT_URL, {{
      method: "POST", mode: "no-cors",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify(payload),
    }});
    updateCareSyncStatus("ok");
  }} catch(e) {{
    console.warn("Sheets saveCare failed:", e);
    updateCareSyncStatus("offline");
  }} finally {{
    careSheetSyncing = false;
    if(careSyncPending) {{ careSyncPending = false; saveCareDataToSheets(); }}
  }}
}}

function saveCareData() {{
  saveCareDataLocal();
  if(saveCareTimeout) clearTimeout(saveCareTimeout);
  saveCareTimeout = setTimeout(saveCareDataToSheets, 600);
}}
let saveCareTimeout = null;

async function loadCareData() {{
  try {{
    const rc = localStorage.getItem("pflanzen_care_v2");
    if(rc) careData = JSON.parse(rc);
    const rh = localStorage.getItem("pflanzen_history_v2");
    if(rh) careHistory = JSON.parse(rh);
  }} catch(e) {{ careData={{}}; careHistory=[]; }}

  if(!APPS_SCRIPT_URL) return;
  updateCareSyncStatus("sync");
  try {{
    const res = await fetch(APPS_SCRIPT_URL + "?action=loadCare", {{ method: "GET", mode: "cors" }});
    if(res.ok) {{
      const data = await res.json();
      if(data && data.careData) Object.assign(careData, data.careData);
      if(data && data.careHistory && Array.isArray(data.careHistory) && data.careHistory.length > 0) {{
        const merged = [...careHistory, ...data.careHistory];
        const seen = new Set();
        careHistory = merged
          .filter(h => {{ const k=h.time+h.type+h.plantIdx; if(seen.has(k)) return false; seen.add(k); return true; }})
          .sort((a,b) => new Date(b.time) - new Date(a.time))
          .slice(0, 200);
      }}
      saveCareDataLocal();
      updateCareSyncStatus("ok");
      renderCare();
      renderCalendar();
    }} else {{ updateCareSyncStatus("offline"); }}
  }} catch(e) {{
    console.warn("Sheets loadCare failed:", e);
    updateCareSyncStatus("offline");
  }}
}}

function updateCareSyncStatus(state) {{
  const el = $("care-sync-status");
  if(!el) return;
  if(state === "sync")    {{ el.textContent = "☁️ Synchronisiert…"; el.style.color = "var(--muted)"; }}
  else if(state === "ok") {{ el.textContent = "☁️ Synced"; el.style.color = "var(--accent-dark)"; }}
  else                    {{ el.textContent = "💾 Lokal"; el.style.color = "var(--warn)"; }}
}}

async function savePositionsToSheets() {{
  savePositionsLocal();
  if(!APPS_SCRIPT_URL) return;
  const payload = {{
    action: "savePositions",
    positions: Object.entries(positions).map(([idx,pos])=>{{
      return {{ idx:parseInt(idx), floor:pos.floor, x:pos.x, y:pos.y }};
    }})
  }};
  try {{
    await fetch(APPS_SCRIPT_URL, {{
      method:"POST", mode:"no-cors",
      headers:{{"Content-Type":"application/json"}},
      body: JSON.stringify(payload),
    }});
    showToast("☁️ Standorte synchronisiert");
  }} catch(e) {{
    showToast("💾 Lokal gespeichert (offline)");
  }}
}}

async function loadPositionsFromSheets() {{
  loadPositionsLocal();
  if(!APPS_SCRIPT_URL) return;
  try {{
    const res = await fetch(APPS_SCRIPT_URL + "?action=loadPositions", {{ method:"GET", mode:"cors" }});
    if(!res.ok) return;
    const data = await res.json();
    if(data && data.positions && Array.isArray(data.positions)) {{
      const cloud = {{}};
      data.positions.forEach(p => {{ cloud[p.idx] = {{ floor:p.floor, x:p.x, y:p.y }}; }});
      Object.assign(positions, cloud);
      savePositionsLocal();
      render();
      renderInventory();
    }}
  }} catch(e) {{
    console.warn("loadPositionsFromSheets failed:", e);
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
  if(isCare) {{ renderCare(); renderUpcoming(); renderCalendar(); }}
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
  if(tab==="calendar") {{ renderUpcoming(); renderCalendar(); }}
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
    const tx=Math.round(pos.x*W-24), ty=Math.round(pos.y*H-24);
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
// ★ RENDER DETAIL (mit Vital-Score Ring + Staunässe-Warnung)
// ============================================================
function renderDetail(idx) {{
  const p   = plants[idx];
  const pos = positions[idx];
  const floor = pos ? pos.floor : currentFloor;
  const lf = pos ? computeLichtFull(pos.x, pos.y, floor) : null;
  const liveScore = lf ? lf.score : null;
  const dliScore = pos ? getDLIScore(pos.x, pos.y, floor) : null;
  const primaryScore = dliMode && dliScore ? dliScore : liveScore;
  const stat = primaryScore ? getLichtStatus(primaryScore, p.licht) : null;
  const sc   = stat ? STATUS_CFG[stat] : null;

  // Vital-Score berechnen
  const vital = computeVitalScore(idx);

  $("rsb-empty").style.display="none";
  const det = $("rsb-detail");
  det.classList.add("visible");

  // Vital-Score Ring-Chart (groß, im Detail)
  const vColor = vital.score >= 72 ? "var(--accent)" : vital.score >= 45 ? "var(--warn)" : "var(--danger)";
  const vLabel = vital.score >= 72 ? "Glücklich 🌟" : vital.score >= 45 ? "Okay ⛅" : "Gestresst 🌑";
  const vitalHTML = `
    <div class="vital-card">
      <div class="vital-ring-wrap">
        ${{makeSvgRing(vital.score)}}
        <div class="vital-score-label">
          <span class="vital-score-num">${{vital.score}}</span>
          <span class="vital-score-pct">%</span>
        </div>
      </div>
      <div class="vital-info">
        <div class="vital-title">Glücks-Index · ${{vLabel}}</div>
        <div class="vital-sub-row">
          <div class="vital-sub">
            <span style="font-size:14px;flex-shrink:0">☀️</span>
            <div class="vital-sub-bar-wrap">
              <div class="vital-sub-bar-track">
                <div class="vital-sub-bar-fill" style="width:${{vital.lichtPct}}%;background:linear-gradient(90deg,var(--accent-dim),var(--accent))"></div>
              </div>
            </div>
            <span class="vital-sub-val">${{vital.lichtPct}}%</span>
          </div>
          <div class="vital-sub">
            <span style="font-size:14px;flex-shrink:0">💧</span>
            <div class="vital-sub-bar-wrap">
              <div class="vital-sub-bar-track">
                <div class="vital-sub-bar-fill" style="width:${{vital.giessPct}}%;background:linear-gradient(90deg,rgba(107,158,196,0.4),var(--dli-color))"></div>
              </div>
            </div>
            <span class="vital-sub-val">${{vital.giessPct}}%</span>
          </div>
          <div class="vital-sub">
            <span style="font-size:14px;flex-shrink:0">🌿</span>
            <div class="vital-sub-bar-wrap">
              <div class="vital-sub-bar-track">
                <div class="vital-sub-bar-fill" style="width:${{vital.duengPct}}%;background:linear-gradient(90deg,rgba(201,149,106,0.4),var(--warn))"></div>
              </div>
            </div>
            <span class="vital-sub-val">${{vital.duengPct}}%</span>
          </div>
        </div>
      </div>
    </div>
  `;

  // Staunässe-Warnung
  const stauHTML = vital.staunaesseRisk ? `
    <div class="staunaesse-warn">
      <div class="staunaesse-icon">🚱</div>
      <div class="staunaesse-text">
        <div class="staunaesse-title">Staunässegefahr</div>
        Das Substrat wurde erst kürzlich gegossen. Warte noch etwas, bevor du erneut gießt –
        Staunässe kann Wurzelfäule verursachen.
      </div>
    </div>
  ` : "";

  const imgUrl = getPlantImageUrl(p.name);
  const imgHTML = `
    <div class="detail-img-wrap">
      <img src="${{imgUrl}}" style="width:100%;height:100%;object-fit:cover;"
        onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="detail-img-fallback" style="display:none">${{p.emoji}}</div>
    </div>
  `;

  const coordsHTML = pos
    ? `<div class="coords-row">Rel. ${{(pos.x*100).toFixed(1)}}% · ${{(pos.y*100).toFixed(1)}}%</div>
       <span class="floor-tag">📍 ${{pos.floor}}</span>`
    : `<span class="floor-tag">📦 Im Inventar</span>`;

  // DLI Panel
  let dliHTML = "";
  if(pos) {{
    const hasCache = dliScore !== null;
    const dliVal   = hasCache ? dliScore : "—";
    const dliPct   = hasCache ? ((dliScore/10)*100).toFixed(0) : 0;
    const liveVal  = liveScore !== null ? liveScore : "—";
    const nightMode = sunState.elevation <= -6;
    const liveLabel = nightMode ? "🌙 Nacht (kein Tageslicht)" : `☀️ Live-Score ${{liveVal}}/10`;
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

  // Astro Panel
  let astroHTML="";
  if(lf) {{
    const winChips=lf.windowHits.map(w=>{{
      const visRatio = parseFloat(w.visRatio||0);
      const bright = !w.occluded && parseFloat(w.incFactor)>0.2;
      const partialLabel = visRatio>0&&visRatio<1 ? ` (${{Math.round(visRatio*100)}}%)` : "";
      return `<span class="win-chip ${{bright?"hit":""}}">${{w.side}}${{w.occluded?" (verdeckt)": bright?" ☀️":""}}${{partialLabel}}</span>`;
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
  const lightHTML = scoreToShow ? `
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
      <div class="lbw-label"><span style="color:var(--muted);font-weight:400;">Bedarf: ${{p.licht}}/10</span><span style="color:var(--muted);font-weight:400;">Verfügbar: ${{scoreToShow}}/10</span></div>
    </div>
    ${{dliHTML}}${{astroHTML}}
  ` : `
    ${{dliHTML || '<div style="font-size:13.5px;font-weight:500;color:var(--muted);background:rgba(255,255,255,0.72);border-radius:var(--rx);padding:20px;text-align:center;border:1px solid var(--border);">Pflanze auf Karte platzieren, um Lichtwert zu berechnen.</div>'}}
  `;

  const removeHTML = pos ? `<button class="act-btn danger-btn" onclick="removePlant(${{idx}})">🗑️ Entfernen</button>` : "";

  const extraHTML = `
    <div style="display:flex;flex-direction:column;gap:10px;">
      ${{p.luftfeuchtigkeit ? `<div class="detail-extra-row"><div class="detail-extra-lbl">💧 Opt. Luftfeuchtigkeit</div><div class="detail-extra-val">${{p.luftfeuchtigkeit}}</div></div>` : ''}}
      ${{p["besprühen"] ? `<div class="detail-extra-row"><div class="detail-extra-lbl">🌫️ Besprühen</div><div class="detail-extra-val">${{p["besprühen"]}}</div></div>` : ''}}
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
    ${{vitalHTML}}
    ${{stauHTML}}
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
  const list  = $("inv-list");
  const filter= inventoryFilter.toLowerCase();
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
        if(positions[i] && positions[i].floor!==currentFloor) setFloor(positions[i].floor);
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
function setupPinDrag(pin, idx) {{
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
    const tx=Math.round(positions[idx].x*W-24), ty=Math.round(positions[idx].y*H-24);
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
// ★ SORT HELPERS (Bibliothek)
// ============================================================
function toggleSortDir() {{
  libSortAsc = !libSortAsc;
  $("lib-sort-dir-btn").textContent = libSortAsc ? "↑" : "↓";
  $("lib-sort-dir-btn").title = libSortAsc ? "Aufsteigend" : "Absteigend";
  renderLibrary();
}}

function getSortValue(plant, key) {{
  if(key === "licht") return plant.licht || 0;
  if(key === "vital") {{
    const i = plants.indexOf(plant);
    const v = computeVitalScore(i);
    return v.score;
  }}
  if(key === "giessen") {{
    const monthName = MONTHS_DE[NOW_MONTH];
    const raw = plant.giessAll ? plant.giessAll[monthName] : plant.giessen;
    const n = parseFloat(raw);
    return isNaN(n) ? 9999 : n;
  }}
  return plant.name.toLowerCase();
}}

// ============================================================
// ★ LIBRARY VIEW — mit Vital-Score Ring
// ============================================================
function renderLibrary() {{
  const grid=$("lib-grid");
  const filter=libraryFilter.toLowerCase();
  grid.innerHTML="";

  libSortKey = $("lib-sort-key") ? $("lib-sort-key").value : libSortKey;
  let filtered = plants.filter(p=>!filter||p.name.toLowerCase().includes(filter));

  filtered = [...filtered].sort((a,b) => {{
    const va = getSortValue(a, libSortKey);
    const vb = getSortValue(b, libSortKey);
    if(va < vb) return libSortAsc ? -1 : 1;
    if(va > vb) return libSortAsc ?  1 : -1;
    return 0;
  }});

  const libSub=$("lib-sub-label");
  if(libSub) {{
    const placed=Object.keys(positions).length;
    const sortLabel = libSortKey==="licht" ? "Lichtbedarf" : libSortKey==="giessen" ? "Gießbedarf" : libSortKey==="vital" ? "Vital-Score" : "Name";
    libSub.textContent=`${{filtered.length}} Pflanzen · ${{placed}} platziert · ${{sortLabel}} ${{libSortAsc?"↑":"↓"}}`;
  }}

  filtered.forEach((p) => {{
    const i=plants.indexOf(p);
    const pos=positions[i];
    const lf=pos?computeLichtFull(pos.x,pos.y,pos.floor):null;
    const ist=lf?lf.score:null;
    const stat=ist?getLichtStatus(ist,p.licht):null;
    const floorLabel=pos?`📍 ${{pos.floor}}`:"📦 Im Inventar";
    const barColor=stat==='ideal'?'var(--accent)':stat==='ok'?'var(--warn)':'var(--danger)';
    const lightPct=ist?(ist/10*100).toFixed(1):0;

    // Vital-Score für Karte
    const vital = computeVitalScore(i);
    const vColor = vital.score >= 72 ? "var(--accent)" : vital.score >= 45 ? "var(--warn)" : "var(--danger)";

    let statusChip="";
    if(stat) {{
      const cfg={{ideal:{{cls:"ideal",ico:"✅",lbl:"Optimaler Standort"}},ok:{{cls:"ok",ico:"⚠️",lbl:"Akzeptabler Standort"}},bad:{{cls:"bad",ico:"❌",lbl:"Zu dunkel"}}}};
      const c=cfg[stat];
      statusChip=`<span class="lib-status-chip ${{c.cls}}">${{c.ico}} ${{c.lbl}}</span>`;
    }} else {{
      statusChip=`<span class="lib-status-chip none">📦 Nicht platziert</span>`;
    }}

    const imgUrl = getPlantImageUrl(p.name);
    const besondHTML = p.besonderheit ? `
      <div class="lib-besonderheit">
        <div class="lib-besonderheit-lbl">💡 Besonderheit</div>
        ${{p.besonderheit}}
      </div>
    ` : '';
    const humiHTML = (p.luftfeuchtigkeit || p["besprühen"]) ? `
      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        ${{p.luftfeuchtigkeit ? `<div class="lib-humidity-row">💧 <span class="lib-humidity-badge">${{p.luftfeuchtigkeit}}</span></div>` : ''}}
        ${{p["besprühen"] ? `<div class="lib-humidity-row">🌫️ Besprühen: <strong style="margin-left:4px;color:var(--text);">${{p["besprühen"]}}</strong></div>` : ''}}
      </div>
    ` : '';

    const stauBadge = vital.staunaesseRisk ? `
      <span style="display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;
        padding:4px 10px;border-radius:99px;background:rgba(123,174,196,0.14);
        color:var(--staunaesse);border:1px solid rgba(123,174,196,0.3);">
        🚱 Staunässegefahr
      </span>
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
        <!-- Vital-Score Miniatur-Ring (oben rechts auf dem Bild) -->
        <div class="lib-vital-badge" style="position:absolute;top:12px;right:12px;">
          ${{makeSmallRingSvg(vital.score)}}
        </div>
      </div>
      <div class="lib-card-body">
        <div class="lib-card-top-row">
          ${{statusChip}}
          ${{stauBadge}}
          <div class="lib-card-loc" style="margin-left:auto">
            <div class="lib-card-loc-dot ${{pos?"placed":""}}"></div>
            ${{floorLabel}}
          </div>
        </div>
        <div class="lib-light-row">
          <div class="lib-light-icon">☀️</div>
          <div class="lib-light-bar-wrap">
            <div class="lib-light-bar-track">
              <div class="lib-light-bar-fill" style="width:${{lightPct}}%;background:${{ist?'linear-gradient(90deg, var(--accent-glow), '+barColor+')':'rgba(44,59,46,0.08)'}}"></div>
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
        <!-- ✦ Vital-Score Aufschlüsselung -->
        <div class="lib-vital-breakdown">
          <div class="lib-vital-breakdown-title">
            <span>💚 Vital-Score Aufschlüsselung</span>
            <span class="lib-vital-total-badge" style="color:${{vColor}}">${{vital.score}}%</span>
          </div>
          <div class="lib-vital-row">
            <span class="lib-vital-row-icon">☀️</span>
            <span class="lib-vital-row-label">Licht</span>
            <div class="lib-vital-row-track"><div class="lib-vital-row-fill licht" style="width:${{vital.lichtPct}}%"></div></div>
            <span class="lib-vital-row-val">${{vital.lichtPct}}%</span>
            <span class="lib-vital-weight">×40%</span>
          </div>
          <div class="lib-vital-row">
            <span class="lib-vital-row-icon">💧</span>
            <span class="lib-vital-row-label">Gießen</span>
            <div class="lib-vital-row-track"><div class="lib-vital-row-fill giessen" style="width:${{vital.giessPct}}%"></div></div>
            <span class="lib-vital-row-val">${{vital.giessPct}}%</span>
            <span class="lib-vital-weight">×35%</span>
          </div>
          <div class="lib-vital-row">
            <span class="lib-vital-row-icon">🌿</span>
            <span class="lib-vital-row-label">Düngen</span>
            <div class="lib-vital-row-track"><div class="lib-vital-row-fill duengen" style="width:${{vital.duengPct}}%"></div></div>
            <span class="lib-vital-row-val">${{vital.duengPct}}%</span>
            <span class="lib-vital-weight">×25%</span>
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

  let html = DAYS_DE.map(d=>`<div class="cal-day-header">${{d}}</div>`).join("");
  const firstDay = new Date(calYear, calMonth, 1);
  const lastDay  = new Date(calYear, calMonth+1, 0);
  const startDow = firstDay.getDay();
  const totalDays= lastDay.getDate();
  const prevLast = new Date(calYear, calMonth, 0).getDate();

  for(let d=startDow-1; d>=0; d--) {{
    html += `<div class="cal-cell other-month"><div class="cal-day-num">${{prevLast-d}}</div></div>`;
  }}

  const todayD = NOW.getDate(), todayM = NOW.getMonth(), todayY = NOW.getFullYear();
  const eventsByDay = {{}};

  careHistory.forEach(h=>{{
    const d = new Date(h.time);
    if(d.getMonth()===calMonth && d.getFullYear()===calYear) {{
      const day = d.getDate();
      if(!eventsByDay[day]) eventsByDay[day]=[];
      eventsByDay[day].push({{ type:h.type, name:h.name, emoji:h.emoji }});
    }}
  }});

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
    html += `<div class="${{cellClass}}" onclick="openDayModal(${{d}},${{calMonth}},${{calYear}})"><div class="cal-day-num">${{d}}</div><div class="cal-events">${{evHTML}}${{moreHTML}}</div></div>`;
  }}

  const cellsUsed = startDow + totalDays;
  const remaining = (7 - (cellsUsed % 7)) % 7;
  for(let d=1; d<=remaining; d++) {{
    html += `<div class="cal-cell other-month"><div class="cal-day-num">${{d}}</div></div>`;
  }}
  grid.innerHTML = html;
}}

// ============================================================
// ★ PFLEGE-STATUS — Liste
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
  soonSection.innerHTML = soonItems.length > 0 ? `
    <div class="care-section-title">
      📅 In den nächsten 3 Tagen
      <span class="care-badge warn">${{soonItems.length}} Pflanze${{soonItems.length!==1?'n':''}}</span>
    </div>
    ${{soonItems.map(e => makeCareCard(e.idx, e.ws, e.fs)).join("")}}
  ` : '';

  const allSection = $("care-all-section");
  allSection.innerHTML = allItems.length > 0 ? `
    <div class="care-section-title">
      🌿 Alle anderen Pflanzen
      <span class="care-badge ok">${{allItems.length}} versorgt</span>
    </div>
    ${{allItems.map(e => makeCareCard(e.idx, e.ws, e.fs)).join("")}}
  ` : '';

  bindCheckboxEvents();
  restoreSelection();
  updateBulkBar();
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
        <div style="padding:24px;text-align:center;color:var(--muted);font-size:14px;font-weight:400;">
          Noch keine Aktionen aufgezeichnet.
        </div>
      </div>
    `;
  }}
}}

// ============================================================
// ★ MULTI-SELEKTION
// ============================================================
function bindCheckboxEvents() {{
  document.querySelectorAll(".care-checkbox").forEach(cb => {{
    cb.addEventListener("change", () => {{
      const idx = parseInt(cb.dataset.pidx);
      if(cb.checked) selectedPlantIdxs.add(idx);
      else selectedPlantIdxs.delete(idx);
      const card = cb.closest(".care-card");
      if(card) card.classList.toggle("selected-card", cb.checked);
      updateBulkBar();
    }});
  }});
}}

function restoreSelection() {{
  document.querySelectorAll(".care-checkbox").forEach(cb => {{
    const idx = parseInt(cb.dataset.pidx);
    const isSelected = selectedPlantIdxs.has(idx);
    cb.checked = isSelected;
    const card = cb.closest(".care-card");
    if(card) card.classList.toggle("selected-card", isSelected);
  }});
}}

function updateBulkBar() {{
  const bar = $("bulk-action-bar");
  const countEl = $("bulk-count-label");
  const n = selectedPlantIdxs.size;
  if(n > 0) {{ bar.classList.add("visible"); countEl.textContent = `${{n}} ausgewählt`; }}
  else {{ bar.classList.remove("visible"); }}
}}

function clearSelection() {{
  selectedPlantIdxs.clear();
  document.querySelectorAll(".care-checkbox").forEach(cb => {{
    cb.checked = false;
    const card = cb.closest(".care-card");
    if(card) card.classList.remove("selected-card");
  }});
  updateBulkBar();
}}

function bulkWater() {{
  if(selectedPlantIdxs.size === 0) return;
  const now = new Date().toISOString();
  selectedPlantIdxs.forEach(idx => {{
    if(!careData[idx]) careData[idx]={{}};
    careData[idx].lastWatered = now;
    careHistory.unshift({{ type:'water', plantIdx:idx, name:plants[idx].name, emoji:plants[idx].emoji, time:now }});
  }});
  const count = selectedPlantIdxs.size;
  selectedPlantIdxs.clear();
  saveCareData(); renderCare(); renderCalendar();
  showToast(`💧 ${{count}} Pflanzen gegossen`);
}}

function bulkFertilize() {{
  if(selectedPlantIdxs.size === 0) return;
  const now = new Date().toISOString();
  selectedPlantIdxs.forEach(idx => {{
    if(!careData[idx]) careData[idx]={{}};
    careData[idx].lastFertilized = now;
    careData[idx].lastWatered    = now;
    careHistory.unshift({{ type:'fertilize', plantIdx:idx, name:plants[idx].name, emoji:plants[idx].emoji, time:now }});
    careHistory.unshift({{ type:'water',      plantIdx:idx, name:plants[idx].name, emoji:plants[idx].emoji, time:now }});
  }});
  const count = selectedPlantIdxs.size;
  selectedPlantIdxs.clear();
  saveCareData(); renderCare(); renderCalendar();
  showToast(`🌿 ${{count}} Pflanzen gedüngt & gegossen`);
}}

// ============================================================
// ★ PFLEGE-KERN-LOGIK
// ============================================================
function parseIntervalDays(val) {{
  if(!val || val==="—" || val.trim()==="") return null;
  const n = parseFloat(val);
  if(isNaN(n) || n <= 0) return null;
  return n;
}}

function getCareStatus(plantIdx, type) {{
  const p = plants[plantIdx];
  const monthName = MONTHS_DE[NOW.getMonth()];
  const rawVal = type==='water'
    ? (p.giessAll ? p.giessAll[monthName] : p.giessen)
    : (p.duengAll ? p.duengAll[monthName] : p.dungen);
  const intervalDays = parseIntervalDays(rawVal);
  if(!intervalDays) return null;

  const cd = careData[plantIdx] || {{}};
  const lastStr = type==='water' ? cd.lastWatered : cd.lastFertilized;
  const lastDate = lastStr ? new Date(lastStr) : null;
  const now = new Date();
  let nextDate, overdueDays = 0, moisturePct = 50;

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
  return {{ nextDate, overdueDays, intervalDays, moisturePct, lastDate }};
}}

function formatRelDate(date) {{
  const now = new Date();
  const diffDays = Math.round((date - now) / (24*3600*1000));
  if(diffDays < -1) return `${{Math.abs(diffDays)}} Tage überfällig`;
  if(diffDays === -1) return "Gestern fällig";
  if(diffDays === 0)  return "Heute fällig";
  if(diffDays === 1)  return "Morgen";
  if(diffDays <= 3)   return `In ${{diffDays}} Tagen`;
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
  careHistory.unshift({{ type:'water', plantIdx, name:plants[plantIdx].name, emoji:plants[plantIdx].emoji, time:now }});
  saveCareData(); renderCare(); renderCalendar();
  showToast(`💧 ${{plants[plantIdx].name}} gegossen`);
}}

function doFertilize(plantIdx) {{
  if(!careData[plantIdx]) careData[plantIdx]={{}};
  const now = new Date().toISOString();
  careData[plantIdx].lastFertilized = now;
  careData[plantIdx].lastWatered    = now;
  careHistory.unshift({{ type:'fertilize', plantIdx, name:plants[plantIdx].name, emoji:plants[plantIdx].emoji, time:now }});
  careHistory.unshift({{ type:'water',      plantIdx, name:plants[plantIdx].name, emoji:plants[plantIdx].emoji, time:now }});
  saveCareData(); renderCare(); renderCalendar();
  showToast(`🌿 ${{plants[plantIdx].name}} gedüngt & gegossen`);
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
  saveCareData(); renderCare(); renderCalendar();
  showToast(`💧 ${{count}} Pflanzen gegossen`);
}}

async function refreshCareFromSheets() {{
  showToast("🔄 Lade Daten…", 1500);
  await loadCareData();
  renderCare(); renderCalendar();
}}

function exportCareCSV() {{
  const rows = [["Zeitstempel","Typ","Pflanze"]];
  careHistory.forEach(h => {{
    const label = h.type==='water' ? 'Gießen' : 'Düngen';
    rows.push([h.time, label, h.name]);
  }});
  const csv = rows.map(r => r.map(v=>`"${{v}}"`).join(",")).join("\\n");
  const blob = new Blob([csv], {{type:"text/csv;charset=utf-8;"}});
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement("a");
  a.href=url; a.download="pflege_historie.csv"; a.click();
  URL.revokeObjectURL(url);
}}

function renderCare() {{
  if(currentCareSubtab === 'calendar') {{ renderUpcoming(); renderCalendar(); }}
  else if(currentCareSubtab === 'status') renderCareStatus();
  else if(currentCareSubtab === 'history') renderCareHistory();
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

// ============================================================
// ★ UPCOMING-PANEL
// ============================================================
function renderUpcoming() {{
  const el = $("care-upcoming-section");
  if(!el) return;
  const now    = new Date();
  const in14   = new Date(now.getTime() + 14*24*3600*1000);
  const items  = [];
  plants.forEach((p, i) => {{
    [['water','💧'],['fertilize','🌿']].forEach(([type, icon]) => {{
      const s = getCareStatus(i, type);
      if(!s) return;
      if(s.nextDate <= in14 || s.overdueDays > 0) {{
        const diffDays = Math.round((s.nextDate - now) / (24*3600*1000));
        items.push({{ plantIdx:i, type, icon, plant:p, status:s, diffDays }});
      }}
    }});
  }});

  if(items.length === 0) {{
    el.innerHTML = `
      <div style="background:rgba(255,255,255,0.75);backdrop-filter:blur(14px);
        border:1px solid rgba(255,255,255,0.7);border-radius:var(--rx);
        padding:20px 24px;display:flex;align-items:center;gap:14px;
        box-shadow:0 6px 24px rgba(44,59,46,0.05);">
        <span style="font-size:28px;">🎉</span>
        <div>
          <div style="font-family:'Playfair Display',serif;font-size:15px;font-weight:700;color:var(--text);">Alles versorgt!</div>
          <div style="font-size:13px;color:var(--muted);margin-top:2px;">In den nächsten 14 Tagen keine Aktionen fällig.</div>
        </div>
      </div>`;
    return;
  }}

  items.sort((a,b) => a.diffDays - b.diffDays);
  const overdueItems = items.filter(it => it.diffDays < 0);

  let html = `
    <div style="background:rgba(255,255,255,0.75);backdrop-filter:blur(14px);
      border:1px solid rgba(255,255,255,0.7);border-radius:var(--rx);overflow:hidden;
      box-shadow:0 6px 24px rgba(44,59,46,0.05);">
      <div style="padding:16px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;">
        <span style="font-family:'Playfair Display',serif;font-size:15px;font-weight:700;color:var(--text);">📅 Nächste 14 Tage</span>
        ${{overdueItems.length > 0 ? `<span style="font-size:12px;font-weight:600;padding:3px 10px;border-radius:99px;
          background:var(--danger-dim);color:var(--danger);border:1px solid rgba(201,112,112,0.28);">
          ${{overdueItems.length}} überfällig</span>` : ''}}
        <span style="font-size:12px;font-weight:600;padding:3px 10px;border-radius:99px;
          background:var(--surface-2);color:var(--muted);margin-left:auto;">${{items.length}} Aktionen</span>
      </div>
      <div style="display:flex;flex-direction:column;">
  `;

  items.forEach((it, idx) => {{
    const isOverdue = it.diffDays < 0;
    const bgColor   = isOverdue ? 'rgba(201,112,112,0.04)' : it.diffDays===0 ? 'rgba(201,149,106,0.04)' : 'transparent';
    const chipCls   = isOverdue ? 'overdue' : it.diffDays<=0 ? 'soon' : it.diffDays<=3 ? 'soon' : 'ok';
    const chipLabel = formatRelDate(it.status.nextDate);
    const lastLabel = it.status.lastDate ? `Zuletzt: ${{formatAbsDate(it.status.lastDate.toISOString())}}` : "Noch nie";
    const actionLabel = it.type==='water' ? 'Gießen' : 'Düngen';
    const btnCls      = it.type==='water' ? 'water' : 'fertilize';
    const fnName      = it.type==='water' ? 'doWater' : 'doFertilize';
    const border      = idx < items.length-1 ? 'border-bottom:1px solid var(--border);' : '';

    html += `
      <div style="display:flex;align-items:center;gap:14px;padding:12px 20px;background:${{bgColor}};${{border}}transition:background .2s;">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--surface-2);
          display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">${{it.icon}}</div>
        <div style="flex:1;min-width:0;">
          <div style="font-weight:600;font-size:14px;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
            ${{it.plant.emoji}} ${{it.plant.name}}
          </div>
          <div style="font-size:11px;color:var(--muted);margin-top:2px;">
            ${{actionLabel}} · ${{lastLabel}} · alle ${{it.status.intervalDays}} Tage
          </div>
        </div>
        <span class="care-chip ${{chipCls}}" style="flex-shrink:0;">${{chipLabel}}</span>
        <button class="care-btn ${{btnCls}}" style="flex-shrink:0;padding:7px 14px;font-size:12px;"
          onclick="${{fnName}}(${{it.plantIdx}})">${{it.icon}} ${{actionLabel}}</button>
      </div>
    `;
  }});

  html += `</div></div>`;
  el.innerHTML = html;
}}

// ============================================================
// ★ TAG-DETAIL MODAL
// ============================================================
function openDayModal(day, month, year) {{
  const overlay = $("day-modal-overlay");
  const title   = $("day-modal-title");
  const body    = $("day-modal-body");
  if(!overlay || !title || !body) return;

  const date = new Date(year, month, day);
  const dayName = date.toLocaleDateString("de-DE", {{weekday:"long"}});
  const dateStr = date.toLocaleDateString("de-DE", {{day:"2-digit", month:"long", year:"numeric"}});
  title.textContent = `${{dayName}}, ${{dateStr}}`;

  // Ereignisse sammeln: durchgeführte Aktionen (careHistory) + geplante (nextDate)
  const events = [];

  // 1) Durchgeführte Aktionen aus careHistory
  careHistory.forEach(h => {{
    const d = new Date(h.time);
    if(d.getDate()===day && d.getMonth()===month && d.getFullYear()===year) {{
      events.push({{
        type: h.type,
        name: h.name,
        emoji: h.emoji,
        kind: 'done',
        time: d.toLocaleTimeString("de-DE", {{hour:"2-digit",minute:"2-digit"}})
      }});
    }}
  }});

  // 2) Geplante Aktionen (nextDate fällt auf diesen Tag)
  plants.forEach((p, i) => {{
    [['water','💧'],['fertilize','🌿']].forEach(([type, icon]) => {{
      const s = getCareStatus(i, type);
      if(!s) return;
      const nd = s.nextDate;
      if(nd.getDate()===day && nd.getMonth()===month && nd.getFullYear()===year) {{
        // Nur anzeigen wenn nicht schon als "done" erfasst (gleiche Pflanze+Typ heute)
        const alreadyDone = events.some(e => e.name===p.name && e.type===type && e.kind==='done');
        if(!alreadyDone) {{
          const now = new Date();
          const isPast = nd < now;
          events.push({{
            type: 'due-'+type,
            name: p.name,
            emoji: p.emoji,
            kind: isPast ? 'overdue' : 'due',
            intervalDays: s.intervalDays
          }});
        }}
      }}
    }});
  }});

  if(events.length === 0) {{
    body.innerHTML = `
      <div class="day-modal-empty">
        <div class="dm-icon">📅</div>
        <p>Keine Aktionen an diesem Tag.</p>
      </div>`;
  }} else {{
    const typeLabel = t => {{
      if(t==='water'||t==='due-water')      return 'Gießen';
      if(t==='fertilize'||t==='due-fertilize') return 'Düngen';
      return t;
    }};
    const iconClass = t => {{
      if(t==='water')          return 'water';
      if(t==='fertilize')      return 'fertilize';
      if(t==='due-water')      return 'due-water';
      return 'due-fertilize';
    }};
    const iconEmoji = t => t.includes('water') ? '💧' : '🌿';

    body.innerHTML = events.map(e => `
      <div class="day-event-row">
        <div class="day-event-icon ${{iconClass(e.type)}}">${{iconEmoji(e.type)}}</div>
        <div class="day-event-info">
          <div class="day-event-name">${{e.emoji}} ${{e.name}}</div>
          <div class="day-event-sub">${{typeLabel(e.type)}}${{e.time ? ' · ' + e.time : ''}}${{e.intervalDays ? ' · alle ' + e.intervalDays + ' Tage' : ''}}</div>
        </div>
        <span class="day-event-chip ${{e.kind}}">
          ${{e.kind==='done' ? '✓ Erledigt' : e.kind==='overdue' ? '⚠️ Überfällig' : '📅 Geplant'}}
        </span>
      </div>
    `).join("");
  }}

  overlay.classList.add("open");
}}

function closeDayModal(event) {{
  if(event && event.target !== $("day-modal-overlay")) return;
  $("day-modal-overlay").classList.remove("open");
}}

// Escape-Taste schließt Modal
document.addEventListener("keydown", e => {{
  if(e.key === "Escape") $("day-modal-overlay").classList.remove("open");
}});

// ============================================================
// ★ STANDORT-QUICKLINK
// ============================================================
function showOnMap(plantIdx) {{
  const pos = positions[plantIdx];
  if(pos) setFloor(pos.floor);
  switchTab("planer");
  setTimeout(()=>{{
    activePIdx = plantIdx;
    render();
    renderDetail(plantIdx);
    const pin = $("map-canvas").querySelector(`[data-idx="${{plantIdx}}"]`);
    if(pin) {{
      pin.classList.add("highlight-pulse");
      setTimeout(()=>pin.classList.remove("highlight-pulse"), 4500);
    }}
  }}, 120);
}}

// ============================================================
// ★ CARE CARD (mit Checkbox + Vital-Score Mini-Indikator)
// ============================================================
function makeCareCard(plantIdx, waterStatus, fertilizeStatus) {{
  const p  = plants[plantIdx];
  const cd = careData[plantIdx] || {{}};
  const vital = computeVitalScore(plantIdx);
  const wOver = waterStatus && waterStatus.overdueDays > 0;
  const fOver = fertilizeStatus && fertilizeStatus.overdueDays > 0;
  let cardClass = "care-card";
  if(wOver || fOver) cardClass += " overdue";

  let waterChip = "";
  if(waterStatus) {{
    const cls = waterStatus.overdueDays > 0 ? "overdue" : waterStatus.nextDate <= new Date(Date.now()+3*86400000) ? "soon" : "ok";
    waterChip = `<span class="care-chip ${{cls}}">💧 ${{formatRelDate(waterStatus.nextDate)}}</span>`;
  }}
  let fertChip = "";
  if(fertilizeStatus) {{
    const cls = fertilizeStatus.overdueDays > 0 ? "overdue" : fertilizeStatus.nextDate <= new Date(Date.now()+3*86400000) ? "soon" : "ok";
    fertChip = `<span class="care-chip ${{cls}}">🌿 ${{formatRelDate(fertilizeStatus.nextDate)}}</span>`;
  }}

  let progressBars = "";
  if(waterStatus) {{
    const wPct = waterStatus.moisturePct;
    const fPct = fertilizeStatus ? fertilizeStatus.moisturePct : null;
    progressBars = `
      <div class="care-progress-wrap">
        <div class="care-progress-row">
          <span class="care-progress-icon">💧</span>
          <div class="care-progress-track"><div class="care-progress-fill water" style="width:${{wPct}}%"></div></div>
          <span class="care-progress-pct">${{wPct}}%</span>
        </div>
        ${{fPct !== null ? `
        <div class="care-progress-row">
          <span class="care-progress-icon">🌿</span>
          <div class="care-progress-track"><div class="care-progress-fill fertilize" style="width:${{fPct}}%"></div></div>
          <span class="care-progress-pct">${{fPct}}%</span>
        </div>` : ''}}
      </div>
    `;
  }}

  const imgUrl = getPlantImageUrl(p.name);
  const thumbHTML = `
    <div class="care-card-thumb">
      <img src="${{imgUrl}}" style="width:100%;height:100%;object-fit:cover;"
        onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="care-card-thumb-emoji" style="display:none">${{p.emoji}}</div>
    </div>
  `;

  const lastW = cd.lastWatered    ? `Zuletzt: ${{formatAbsDate(cd.lastWatered)}}`    : "Noch nie gegossen";
  const lastF = cd.lastFertilized ? `Zuletzt: ${{formatAbsDate(cd.lastFertilized)}}` : "Noch nie gedüngt";

  const hasPos = !!positions[plantIdx];
  const locationBtn = hasPos
    ? `<button class="care-btn location" onclick="showOnMap(${{plantIdx}})">📍 Standort</button>`
    : '';

  // Staunässe-Chip
  const stauChip = vital.staunaesseRisk
    ? `<span class="care-chip" style="background:rgba(123,174,196,0.14);color:var(--staunaesse);border-color:rgba(123,174,196,0.3);">🚱 Staunässe</span>`
    : '';

  // Vital-Score Mini-Indikator
  const vColor = vital.score >= 72 ? "var(--accent)" : vital.score >= 45 ? "var(--warn)" : "var(--danger)";
  const vitalMini = `
    <span style="display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;
      padding:3px 10px;border-radius:99px;background:rgba(255,255,255,0.7);
      border:1px solid var(--border);color:${{vColor}};">
      💚 ${{vital.score}}%
    </span>
  `;

  return `
    <div class="${{cardClass}}" data-plant-idx="${{plantIdx}}">
      <div class="care-card-checkbox-wrap">
        <input type="checkbox" class="care-checkbox" data-pidx="${{plantIdx}}">
      </div>
      ${{thumbHTML}}
      <div class="care-card-info">
        <div class="care-card-name">${{p.name}}</div>
        <div class="care-card-meta">
          ${{waterChip}}${{fertChip}}${{stauChip}}${{vitalMini}}
          ${{!waterChip && !fertChip ? '<span class="care-chip">Kein Intervall hinterlegt</span>' : ''}}
        </div>
        ${{progressBars}}
        <div style="font-size:11px;color:var(--muted);margin-top:4px;display:flex;gap:16px;flex-wrap:wrap;">
          <span>💧 ${{lastW}}</span>
          <span>🌿 ${{lastF}}</span>
        </div>
      </div>
      <div class="care-card-actions">
        <button class="care-btn water" onclick="doWater(${{plantIdx}})">💧 Gießen</button>
        <button class="care-btn fertilize" onclick="doFertilize(${{plantIdx}})">🌿 Düngen</button>
        ${{locationBtn}}
      </div>
    </div>
  `;
}}

// ============================================================
// BOOT
// ============================================================
switchCareSubtab('calendar');
loadPlants();
</script>
</body>
</html>"""

components.html(html_app, height=900, scrolling=False)
