import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ============================================================
# MATXPERT — MATERIALS ENGINEERING INTELLIGENCE
# Clean single-file version
# ============================================================

st.set_page_config(
    page_title="MatXpert | Materials Engineering Intelligence",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# PROFESSIONAL THEME
# ------------------------------------------------------------

st.markdown(
    """
    <style>
/* ==========================================================
   MATXPERT — PREMIUM ENGINEERING INTERFACE
   Visual layer only: application logic remains unchanged.
   ========================================================== */

:root {
  --mx-ink: #14253d;
  --mx-muted: #60748c;
  --mx-blue: #3978c8;
  --mx-violet: #7a62d8;
  --mx-teal: #2aa79a;
  --mx-border: rgba(67, 104, 146, .16);
  --mx-shadow: 0 14px 40px rgba(35, 67, 104, .10);
}

.stApp {
  background:
    radial-gradient(900px 500px at 5% 0%, rgba(95, 169, 255, .24), transparent 62%),
    radial-gradient(800px 520px at 100% 8%, rgba(164, 125, 255, .20), transparent 60%),
    radial-gradient(760px 500px at 78% 100%, rgba(61, 205, 179, .16), transparent 60%),
    linear-gradient(135deg, #f8fbff 0%, #edf6ff 38%, #f5f1ff 70%, #effcf9 100%);
  background-attachment: fixed;
  color: var(--mx-ink);
}

/* floating atmospheric light */
.stApp::before,
.stApp::after {
  content: "";
  position: fixed;
  pointer-events: none;
  z-index: 0;
  border-radius: 999px;
  filter: blur(2px);
}
.stApp::before {
  width: 340px;
  height: 340px;
  top: 8%;
  left: 27%;
  background: radial-gradient(circle, rgba(93,160,255,.12), transparent 68%);
  animation: mx-float 13s ease-in-out infinite;
}
.stApp::after {
  width: 300px;
  height: 300px;
  right: 7%;
  bottom: 10%;
  background: radial-gradient(circle, rgba(126,91,220,.10), transparent 68%);
  animation: mx-float 16s ease-in-out infinite reverse;
}
@keyframes mx-float {
  0%,100% { transform: translate3d(0,0,0) scale(1); }
  50% { transform: translate3d(18px,-14px,0) scale(1.06); }
}

.main .block-container {
  position: relative;
  z-index: 1;
  max-width: 1450px;
  padding-top: 2rem;
  padding-bottom: 3rem;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
  background:
    radial-gradient(circle at 20% 0%, rgba(76,151,225,.24), transparent 30%),
    linear-gradient(180deg, #10253e 0%, #163957 48%, #10263f 100%);
  box-shadow: 12px 0 38px rgba(18,45,72,.16);
  border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] * { color: #edf6ff !important; }
[data-testid="stSidebar"] .stRadio label {
  padding: 10px 12px;
  margin: 3px 0;
  border-radius: 12px;
  transition: all .22s ease;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: linear-gradient(90deg, rgba(101,176,255,.17), rgba(255,255,255,.05));
  transform: translateX(4px);
}

/* ---------- TYPOGRAPHY ---------- */
h1, h2, h3, h4 {
  color: #142c49 !important;
  letter-spacing: -.025em;
}
p, label, [data-testid="stMarkdownContainer"] { color: #30465e; }

/* headings get a restrained premium gradient */
h1 {
  background: linear-gradient(90deg, #153c62, #3978c8 52%, #735cc5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ---------- METRICS ---------- */
[data-testid="stMetric"] {
  position: relative;
  overflow: hidden;
  background: linear-gradient(145deg, rgba(255,255,255,.92), rgba(240,247,255,.76));
  border: 1px solid var(--mx-border);
  border-radius: 20px;
  padding: 16px 17px;
  box-shadow: var(--mx-shadow);
  backdrop-filter: blur(14px);
  transition: transform .26s cubic-bezier(.2,.8,.2,1), box-shadow .26s ease, border-color .26s ease;
}
[data-testid="stMetric"]::before {
  content: "";
  position: absolute;
  left: 0; top: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, #4d91df, #7c65d8, #35b7a5);
  opacity: .78;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-6px) scale(1.012);
  box-shadow: 0 22px 48px rgba(35,67,104,.15);
  border-color: rgba(70,126,190,.30);
}
[data-testid="stMetricLabel"] { color: #61758b !important; font-weight: 600; }
[data-testid="stMetricValue"] { color: #173d60 !important; font-weight: 800; }

/* ---------- GENERAL STREAMLIT BLOCKS ---------- */
[data-testid="stVerticalBlock"] > div:has(> [data-testid="stExpander"]),
[data-testid="stVerticalBlock"] > div:has(> [data-testid="stMetricContainer"]) {
  transition: transform .2s ease;
}

/* Expanders */
[data-testid="stExpander"] {
  border: 1px solid rgba(72,111,151,.15) !important;
  border-radius: 18px !important;
  background: linear-gradient(145deg, rgba(255,255,255,.78), rgba(247,250,255,.56)) !important;
  box-shadow: 0 10px 30px rgba(39,73,110,.065) !important;
  overflow: hidden;
  backdrop-filter: blur(12px);
  transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
}
[data-testid="stExpander"]:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 38px rgba(39,73,110,.11) !important;
  border-color: rgba(74,132,197,.28) !important;
}

/* Buttons */
.stButton > button {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(66,112,157,.20) !important;
  border-radius: 13px !important;
  min-height: 44px;
  padding: 0 18px;
  font-weight: 750;
  color: #183d60 !important;
  background: linear-gradient(135deg, rgba(255,255,255,.98), rgba(229,242,255,.90)) !important;
  box-shadow: 0 8px 22px rgba(37,77,116,.09);
  transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease, background .22s ease;
}
.stButton > button::after {
  content: "";
  position: absolute;
  top: 0; left: -110%;
  width: 55%; height: 100%;
  background: linear-gradient(100deg, transparent, rgba(255,255,255,.55), transparent);
  transform: skewX(-18deg);
  transition: left .55s ease;
}
.stButton > button:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 30px rgba(37,77,116,.15);
  border-color: rgba(62,125,191,.42) !important;
  background: linear-gradient(135deg, #ffffff, #e8f4ff) !important;
}
.stButton > button:hover::after { left: 125%; }
.stButton > button:active { transform: translateY(-1px); }

/* Inputs */
.stSelectbox > div > div,
.stNumberInput > div > div,
.stTextInput > div > div,
.stMultiSelect > div > div {
  border-radius: 13px !important;
  border: 1px solid rgba(75,113,151,.18) !important;
  background: rgba(255,255,255,.78) !important;
  box-shadow: 0 5px 16px rgba(35,70,105,.04);
  transition: all .2s ease;
}
.stSelectbox > div > div:hover,
.stNumberInput > div > div:hover,
.stTextInput > div > div:hover,
.stMultiSelect > div > div:hover {
  border-color: rgba(69,130,194,.42) !important;
  box-shadow: 0 8px 22px rgba(35,70,105,.08);
  transform: translateY(-1px);
}

/* Slider */
[data-testid="stSlider"] {
  padding: 10px 12px 5px;
  border-radius: 15px;
  transition: background .2s ease, transform .2s ease;
}
[data-testid="stSlider"]:hover {
  background: rgba(255,255,255,.38);
  transform: translateY(-1px);
}

/* Tabs */
[data-testid="stTabs"] [role="tab"] {
  border-radius: 11px 11px 0 0;
  padding: 8px 14px;
  font-weight: 650;
  color: #536a81;
  transition: all .2s ease;
}
[data-testid="stTabs"] [role="tab"]:hover {
  background: rgba(255,255,255,.55);
  color: #275f91;
  transform: translateY(-2px);
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: #205d91;
  font-weight: 800;
}

/* Radio */
[data-testid="stRadio"] label {
  transition: transform .18s ease, color .18s ease;
}
[data-testid="stRadio"] label:hover {
  transform: translateX(3px);
  color: #2c6fa5 !important;
}

/* Info / success / warning panels */
[data-testid="stAlert"] {
  border-radius: 15px !important;
  border: 1px solid rgba(76,115,155,.13) !important;
  box-shadow: 0 8px 22px rgba(35,70,105,.055);
  backdrop-filter: blur(8px);
}

/* Make matplotlib chart surfaces blend with the premium theme */
.stPyplot, [data-testid="stImage"] {
  border-radius: 18px;
  overflow: hidden;
}

/* subtle horizontal separator */
hr {
  border: 0 !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, rgba(75,113,151,.22), transparent) !important;
  margin: 1.4rem 0 !important;
}

.mx-small { color:#647990; font-size:.90rem; }
.mx-footer { color:#708399; text-align:center; font-size:.78rem; padding:28px 0 5px; }

@media (prefers-reduced-motion: reduce) {
  .stApp::before, .stApp::after { animation: none; }
  [data-testid="stMetric"], .stButton > button, [data-testid="stExpander"] { transition: none; }
}
</style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# MATERIAL DATABASE — ONE CONSISTENT SCHEMA
# ------------------------------------------------------------

MATERIAL_ROWS = [
    ("AISI 1020", "Carbon Steel", 350, 420, 7.87, 120, 51.9, 205, 2, 4),
    ("AISI 1045", "Carbon Steel", 485, 515, 7.87, 170, 49.8, 206, 2, 4),
    ("AISI 4140", "Alloy Steel", 655, 1020, 7.85, 197, 42.6, 205, 3, 5),
    ("Tool Steel D2", "Tool Steel", 1800, 2000, 7.70, 600, 20.0, 210, 7, 4),
    ("Stainless Steel 304", "Stainless Steel", 205, 515, 8.00, 201, 16.2, 193, 6, 10),
    ("Stainless Steel 316", "Stainless Steel", 290, 580, 8.00, 217, 16.3, 193, 7, 10),
    ("Cast Iron", "Ferrous Alloy", 250, 300, 7.20, 180, 50.0, 110, 2, 4),
    ("Pure Iron", "Ferrous Metal", 50, 200, 7.87, 80, 80.0, 211, 2, 3),
    ("Al 6061-T6", "Aluminum Alloy", 276, 310, 2.70, 95, 167, 68.9, 4, 8),
    ("Al 7075-T6", "Aluminum Alloy", 503, 572, 2.81, 150, 130, 71.7, 5, 6),
    ("Al 2024-T3", "Aluminum Alloy", 345, 483, 2.78, 120, 121, 73.1, 5, 6),
    ("Copper C11000", "Copper Alloy", 69, 220, 8.89, 95, 391, 117, 7, 8),
    ("Brass C36000", "Copper Alloy", 155, 345, 8.49, 95, 115, 97, 6, 7),
    ("Bronze C93200", "Copper Alloy", 150, 275, 8.80, 90, 50, 103, 7, 8),
    ("Titanium Ti-6Al-4V", "Titanium Alloy", 880, 950, 4.43, 349, 6.7, 114, 10, 10),
    ("Magnesium AZ31B", "Magnesium Alloy", 200, 290, 1.77, 56, 96, 45, 5, 3),
    ("Nickel 200", "Nickel Alloy", 148, 462, 8.89, 110, 70.2, 204, 8, 10),
    ("Inconel 718", "Nickel Superalloy", 1035, 1240, 8.19, 331, 11.4, 200, 10, 10),
    ("Zinc", "Non-Ferrous Metal", 110, 120, 7.14, 30, 116, 108, 4, 7),
    ("Cobalt", "Cobalt Alloy", 275, 760, 8.90, 250, 100, 209, 9, 8),
    ("Silver", "Precious Metal", 55, 170, 10.49, 25, 429, 83, 10, 9),
    ("Gold", "Precious Metal", 100, 205, 19.30, 25, 318, 79, 10, 10),
    ("Lead", "Non-Ferrous Metal", 18, 20, 11.34, 5, 35, 16, 3, 6),
    ("Tin", "Non-Ferrous Metal", 9, 18, 7.31, 5, 67, 50, 5, 7),
    ("Tungsten", "Refractory Metal", 750, 1510, 19.25, 350, 174, 411, 9, 7),
    ("Molybdenum", "Refractory Metal", 550, 620, 10.28, 230, 138, 329, 9, 8),
    ("Niobium", "Refractory Metal", 275, 585, 8.57, 120, 53, 105, 9, 8),
    ("Zirconium", "Refractory Metal", 330, 550, 6.52, 200, 22.7, 88, 8, 10),
    ("PEEK", "Polymer", 100, 100, 1.32, 100, 0.25, 3.6, 9, 9),
    ("PTFE", "Polymer", 23, 35, 2.20, 50, 0.25, 0.5, 6, 10),
    ("Alumina Ceramic", "Ceramic", 300, 300, 3.95, 1500, 30, 370, 6, 10),
    ("Silicon Carbide", "Ceramic", 350, 550, 3.21, 2200, 120, 410, 8, 10),
]

COLUMNS = [
    "Material", "Family", "Yield Strength (MPa)", "Tensile Strength (MPa)",
    "Density (g/cm³)", "Hardness (HB)", "Thermal Conductivity (W/m·K)",
    "Young's Modulus (GPa)", "Cost Index (1–10)", "Corrosion Resistance (1–10)"
]

MATERIALS = pd.DataFrame(MATERIAL_ROWS, columns=COLUMNS)

# ------------------------------------------------------------
# CONSTANTS + SESSION STATE
# ------------------------------------------------------------

IMPORTANCE_WEIGHTS = {"Low": 0.10, "Medium": 0.25, "High": 0.40, "Critical": 0.60}

for key, default in {
    "history": [],
    "last_selection": None,
    "quiz_score": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def record(module, result):
    st.session_state.history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "module": module,
        "result": result,
    })


def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, float(value)))


def normalize_min(value, requirement):
    if requirement <= 0:
        return 1.0
    return clamp(value / requirement)


def normalize_max(value, requirement):
    if value <= 0:
        return 1.0
    return clamp(requirement / value)

# ------------------------------------------------------------
# HEADER / COMMON UI
# ------------------------------------------------------------

def header(title, subtitle):
    st.title(title)
    st.caption(subtitle)


def plot_material_bars(df, column, title, ylabel=None, horizontal=False):
    fig, ax = plt.subplots(figsize=(10, 5))
    work = df.copy()
    if horizontal:
        work = work.sort_values(column)
        ax.barh(work["Material"], work[column])
        ax.set_xlabel(ylabel or column)
        ax.set_ylabel("Material")
    else:
        ax.bar(work["Material"], work[column])
        ax.set_ylabel(ylabel or column)
        ax.set_xlabel("Material")
        plt.setp(ax.get_xticklabels(), rotation=38, ha="right")
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.20)
    fig.tight_layout()
    return fig

# ============================================================
# MATERIAL SELECTION ENGINE
# ============================================================

def selection_score(value, requirement, direction):
    if direction == "min":
        return normalize_min(value, requirement)
    return normalize_max(value, requirement)


def rank_materials(min_yield, max_density, min_hardness, max_cost, priorities):
    criteria = [
        ("Yield Strength", "Yield Strength (MPa)", min_yield, "min", priorities["Strength"]),
        ("Density", "Density (g/cm³)", max_density, "max", priorities["Weight"]),
        ("Hardness", "Hardness (HB)", min_hardness, "min", priorities["Hardness"]),
        ("Cost", "Cost Index (1–10)", max_cost, "max", priorities["Cost"]),
    ]

    results = []
    for _, row in MATERIALS.iterrows():
        scores = []
        passed = []
        weighted_total = 0.0
        total_weight = 0.0

        for _, col, req, direction, importance in criteria:
            score = selection_score(float(row[col]), float(req), direction)
            scores.append(score)
            passed.append(score >= 0.999999)
            weighted_total += score * importance
            total_weight += importance

        suitability = 100 * weighted_total / total_weight if total_weight else 0
        match = 100 * sum(passed) / len(passed)

        results.append({
            "Material": row["Material"],
            "Family": row["Family"],
            "Suitability": suitability,
            "Requirement Match": match,
            "Pass": all(passed),
            "Scores": scores,
        })

    results.sort(key=lambda x: (x["Suitability"], x["Requirement Match"]), reverse=True)
    return results, criteria

# ============================================================
# PHASE DIAGRAM FUNCTIONS
# ============================================================

def fe_c_phase(carbon, temperature):
    if temperature >= 1493 and carbon < 0.53:
        return "Liquid + δ-ferrite region"
    if temperature >= 1147 and carbon >= 0.0:
        return "Liquid-containing region"
    if temperature >= 912 and carbon < 0.76:
        return "α-ferrite + γ-austenite region"
    if temperature >= 727 and carbon < 2.11:
        return "γ-austenite / austenite field"
    if temperature < 727 and carbon < 0.76:
        return "α-ferrite + pearlite"
    if temperature < 727 and carbon <= 2.11:
        return "Pearlite + cementite"
    if carbon > 4.30 and temperature < 1147:
        return "Cementite-rich region"
    return "Two-phase / transformation region"


def cu_ni_phase(nickel, temperature):
    # Educational approximation for the isomorphous Cu–Ni system.
    liquidus = 1085 + 633 * nickel / 100
    solidus = 1085 + 560 * nickel / 100
    if temperature >= liquidus:
        return "Liquid"
    if temperature <= solidus:
        return "Solid solution (α)"
    return "Liquid + α solid solution"


def plot_fe_c(carbon, temperature):
    c = np.linspace(0, 6.67, 300)
    liquidus = np.where(c < 4.3, 1538 - 91 * c, 1147 + 5 * (c - 4.3))
    austenite_boundary = 912 - 243 * np.clip(c, 0, 0.76) / 0.76

    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.plot(c, liquidus, label="Approx. liquidus")
    ax.plot(np.linspace(0, 2.11, 180), 727 + 185 * (1 - np.linspace(0, 2.11, 180) / 2.11), label="Approx. solid-state boundary")
    ax.axhline(727, linestyle="--", alpha=0.55, label="Eutectoid temperature")
    ax.axvline(0.76, linestyle=":", alpha=0.55)
    ax.scatter([0.76], [727], s=80, zorder=5, label="Eutectoid point")
    ax.scatter([4.30], [1147], s=80, zorder=5, label="Eutectic point")
    ax.scatter([carbon], [temperature], s=130, marker="*", zorder=6, label="Selected state")
    ax.set_xlim(0, 6.67)
    ax.set_ylim(600, 1600)
    ax.set_xlabel("Carbon composition (wt% C)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Fe–C Educational Phase Diagram")
    ax.grid(alpha=0.18)
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    return fig


def plot_cu_ni(nickel, temperature):
    x = np.linspace(0, 100, 300)
    liquidus = 1085 + 633 * x / 100
    solidus = 1085 + 560 * x / 100

    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.plot(x, liquidus, label="Approx. liquidus")
    ax.plot(x, solidus, label="Approx. solidus")
    ax.scatter([nickel], [temperature], s=130, marker="*", zorder=5, label="Selected state")
    ax.set_xlim(0, 100)
    ax.set_ylim(1000, 1800)
    ax.set_xlabel("Nickel composition (wt% Ni)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Cu–Ni Educational Isomorphous Diagram")
    ax.grid(alpha=0.18)
    ax.legend()
    fig.tight_layout()
    return fig

# ============================================================
# ENGINEERING CALCULATORS
# ============================================================

def calc_specific_strength(uts, density):
    return None if density <= 0 else uts / density


def calc_specific_yield(yield_strength, density):
    return None if density <= 0 else yield_strength / density


def calc_mass(density, volume_cm3):
    return None if density < 0 or volume_cm3 < 0 else density * volume_cm3


def calc_expansion(length_mm, cte_um_mk, delta_t):
    return length_mm * (cte_um_mk * 1e-6) * delta_t


def calc_thermal_stress(modulus_gpa, cte_um_mk, delta_t):
    return modulus_gpa * 1000 * (cte_um_mk * 1e-6) * delta_t


def calc_fos(yield_strength, applied_stress):
    return None if applied_stress <= 0 else yield_strength / applied_stress


def calc_corrosion_rate(K, weight_loss, density, area, time):
    if min(density, area, time) <= 0:
        return None
    return K * weight_loss / (density * area * time)

# ============================================================
# LEARNING CONTENT
# ============================================================

LESSONS = {
    "Material Selection": {
        "concept": "Material selection combines design requirements, constraints, properties, processing and cost to identify suitable candidates.",
        "equation": "Weighted suitability = Σ(property score × importance) / Σ(importance)",
        "takeaway": "A high score is a screening result; final engineering selection still requires detailed design verification.",
    },
    "Stress & Strain": {
        "concept": "Stress describes internal force per unit area, while strain describes deformation relative to the original dimension.",
        "equation": "σ = F/A     and     ε = ΔL/L₀",
        "takeaway": "The stress–strain relationship provides the foundation for understanding strength and elastic behaviour.",
    },
    "Young's Modulus": {
        "concept": "Young's modulus measures elastic stiffness: how strongly a material resists elastic deformation.",
        "equation": "E = σ/ε",
        "takeaway": "A higher E generally means less elastic strain under the same stress, but it does not automatically mean higher strength.",
    },
    "Phase Diagrams": {
        "concept": "Phase diagrams show equilibrium phase fields as a function of composition and temperature.",
        "equation": "Lever Rule: Wα = (Cβ − C₀)/(Cβ − Cα)",
        "takeaway": "Phase diagrams connect composition and temperature to microstructure and therefore to material behaviour.",
    },
    "Heat Treatment": {
        "concept": "Controlled heating and cooling can change microstructure and therefore hardness, strength, ductility and toughness.",
        "equation": "Processing → Microstructure → Properties → Performance",
        "takeaway": "Cooling rate matters because diffusion and transformation kinetics determine the resulting structure.",
    },
    "Thermal Behaviour": {
        "concept": "Temperature changes can cause dimensional changes. If expansion or contraction is restrained, thermal stress can develop.",
        "equation": "ΔL = L₀ α ΔT",
        "takeaway": "Thermal expansion must be considered in assemblies, pipes, engines and other temperature-sensitive structures.",
    },
}

QUIZ = [
    ("Which property indicates the beginning of significant permanent plastic deformation?", ["Density", "Yield strength", "Thermal conductivity", "Melting point"], "Yield strength"),
    ("Which indicator is useful for lightweight structural screening?", ["Specific strength", "Color", "Electrical resistance", "Melting point only"], "Specific strength"),
    ("What variables are normally plotted on a binary equilibrium phase diagram?", ["Force and area", "Composition and temperature", "Time and strain", "Mass and volume"], "Composition and temperature"),
    ("What normally happens to a free metal when its temperature increases?", ["It expands", "It always melts", "It loses all strength", "It becomes ceramic"], "It expands"),
    ("Why is steel commonly tempered after quenching?", ["To increase brittleness", "To reduce excessive brittleness while retaining useful hardness", "To remove all carbon", "To lower density"], "To reduce excessive brittleness while retaining useful hardness"),
]

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("MatXpert")
st.sidebar.caption("Materials Engineering Intelligence")
st.sidebar.success("Engineering Engine Online")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Material Selection",
        "Phase Diagram Analysis",
        "Engineering Calculators",
        "Learning Mode",
        "Analysis History",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption(f"{len(MATERIALS)} engineering materials")
st.sidebar.caption("Python • Streamlit • Pandas • NumPy • Matplotlib")

# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":
    header("MatXpert", "Materials Engineering Intelligence Platform")

    st.write("A practical engineering environment for material selection, phase analysis, calculations and learning.")

    a, b, c, d = st.columns(4)
    a.metric("Materials", len(MATERIALS))
    b.metric("Families", MATERIALS["Family"].nunique())
    c.metric("Phase Systems", 2)
    d.metric("Engineering Tools", 7)

    st.markdown("## Engineering Workflow")
    w1, w2, w3, w4 = st.columns(4)
    w1.info("**01 — Define**\n\nSet the engineering requirements.")
    w2.info("**02 — Analyse**\n\nStudy properties and phase behaviour.")
    w3.info("**03 — Compare**\n\nRank candidates and calculate performance.")
    w4.info("**04 — Decide**\n\nInterpret results for engineering use.")

    st.markdown("## Material Landscape")
    family_counts = MATERIALS["Family"].value_counts().sort_values(ascending=True)
    family_df = pd.DataFrame({"Family": family_counts.index, "Count": family_counts.values})
    st.pyplot(plot_material_bars(family_df.rename(columns={"Family":"Material", "Count":"Count"}), "Count", "Materials by Family", "Number of materials", horizontal=True), use_container_width=True)

    st.markdown("## Engineering Highlights")
    strongest = MATERIALS.loc[MATERIALS["Yield Strength (MPa)"].idxmax()]
    lightest = MATERIALS.loc[MATERIALS["Density (g/cm³)"].idxmin()]
    stiffest = MATERIALS.loc[MATERIALS["Young's Modulus (GPa)"].idxmax()]
    x1, x2, x3 = st.columns(3)
    x1.metric("Highest Yield Strength", strongest["Material"], f"{strongest['Yield Strength (MPa)']:.0f} MPa")
    x2.metric("Lowest Density", lightest["Material"], f"{lightest['Density (g/cm³)']:.2f} g/cm³")
    x3.metric("Highest Modulus", stiffest["Material"], f"{stiffest["Young's Modulus (GPa)"]:.1f} GPa")

    st.markdown("## Explore MatXpert")
    st.info("Use **Material Selection** for multi-criteria decisions, **Phase Diagram Analysis** for composition/temperature studies, and **Engineering Calculators** for practical calculations.")

# ============================================================
# MATERIAL SELECTION
# ============================================================

elif page == "Material Selection":
    header("Material Selection Engine", "Interactive multi-criteria screening for engineering material decisions")

    left, right = st.columns([1, 1])

    with left:
        st.markdown("### Design Requirements")
        min_yield = st.number_input("Minimum yield strength (MPa)", 0.0, 2000.0, 300.0, 10.0)
        max_density = st.number_input("Maximum density (g/cm³)", 0.1, 25.0, 8.0, 0.1)
        min_hardness = st.number_input("Minimum hardness (HB)", 0.0, 2500.0, 100.0, 10.0)
        max_cost = st.number_input("Maximum cost index", 1.0, 10.0, 6.0, 1.0)

    with right:
        st.markdown("### Engineering Priorities")
        p_strength = st.select_slider("Strength importance", options=list(IMPORTANCE_WEIGHTS), value="High")
        p_weight = st.select_slider("Low-density importance", options=list(IMPORTANCE_WEIGHTS), value="High")
        p_hardness = st.select_slider("Hardness importance", options=list(IMPORTANCE_WEIGHTS), value="Medium")
        p_cost = st.select_slider("Cost importance", options=list(IMPORTANCE_WEIGHTS), value="Medium")

    priorities = {
        "Strength": IMPORTANCE_WEIGHTS[p_strength],
        "Weight": IMPORTANCE_WEIGHTS[p_weight],
        "Hardness": IMPORTANCE_WEIGHTS[p_hardness],
        "Cost": IMPORTANCE_WEIGHTS[p_cost],
    }

    st.markdown("### Priority Profile")
    priority_df = pd.DataFrame({"Criterion": list(priorities), "Weight": list(priorities.values())})
    fig, ax = plt.subplots(figsize=(9, 3.7))
    ax.bar(priority_df["Criterion"], priority_df["Weight"])
    ax.set_ylim(0, 0.65)
    ax.set_ylabel("Importance weight")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    run = st.button("Run Material Selection", type="primary", use_container_width=True)
    if run:
        results, criteria = rank_materials(min_yield, max_density, min_hardness, max_cost, priorities)
        st.session_state.last_selection = {
            "results": results,
            "requirements": (min_yield, max_density, min_hardness, max_cost),
        }
        best = results[0]
        record("Material Selection", f"Best candidate: {best['Material']} with suitability {best['Suitability']:.1f}%.")

    if st.session_state.last_selection:
        results = st.session_state.last_selection["results"]
        best = results[0]

        st.markdown("## Recommended Candidate")
        r1, r2, r3 = st.columns(3)
        r1.metric("Best Material", best["Material"])
        r2.metric("Suitability", f"{best['Suitability']:.1f}%")
        r3.metric("Requirement Match", f"{best['Requirement Match']:.0f}%")

        if best["Pass"]:
            st.success(f"{best['Material']} satisfies all four selected screening constraints.")
        else:
            st.warning(f"{best['Material']} is the highest-ranked candidate, but not every constraint is fully satisfied.")

        st.markdown("### Ranked Candidates")
        top = pd.DataFrame([
            {"Rank": i + 1, "Material": x["Material"], "Family": x["Family"], "Suitability (%)": round(x["Suitability"], 1), "Requirement Match (%)": round(x["Requirement Match"], 0), "All Constraints": "Yes" if x["Pass"] else "No"}
            for i, x in enumerate(results[:8])
        ])
        headers = list(top.columns)
        header_line = "| " + " | ".join(headers) + " |"
        divider_line = "| " + " | ".join(["---"] * len(headers)) + " |"
        body_lines = ["| " + " | ".join(str(row[h]) for h in headers) + " |" for _, row in top.iterrows()]
        st.markdown("\n".join([header_line, divider_line] + body_lines))

        chart_df = top.sort_values("Suitability (%)", ascending=True)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(chart_df["Material"], chart_df["Suitability (%)"])
        ax.set_xlim(0, 100)
        ax.set_xlabel("Suitability (%)")
        ax.set_title("Top Candidate Suitability")
        ax.grid(axis="x", alpha=0.2)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)

        st.markdown("### Engineering Interpretation")
        st.write(
            f"**{best['Material']}** ranks first because its combined strength, density, hardness and cost performance provides the strongest match to the current priority profile. "
            "The ranking is a screening tool; service temperature, fatigue, fracture, corrosion, manufacturing route and safety factors should be checked before a final design decision."
        )

# ============================================================
# PHASE DIAGRAM ANALYSIS
# ============================================================

elif page == "Phase Diagram Analysis":
    header("Phase Diagram Analysis", "Interactive composition–temperature exploration for binary alloy systems")

    system = st.radio("Alloy system", ["Fe–C (Iron–Carbon)", "Cu–Ni (Copper–Nickel)"], horizontal=True)

    if system.startswith("Fe"):
        c1, c2 = st.columns(2)
        with c1:
            carbon = st.slider("Carbon composition (wt% C)", 0.0, 6.67, 0.76, 0.01)
        with c2:
            temperature = st.slider("Temperature (°C)", 600, 1600, 727, 1)

        phase = fe_c_phase(carbon, temperature)
        m1, m2, m3 = st.columns(3)
        m1.metric("Composition", f"{carbon:.2f} wt% C")
        m2.metric("Temperature", f"{temperature:.0f} °C")
        m3.metric("Estimated Region", phase)

        st.pyplot(plot_fe_c(carbon, temperature), use_container_width=True)
        st.info("Educational model: the displayed boundaries are simplified approximations for learning and screening, not CALPHAD-quality thermodynamic data.")
        record("Phase Diagram", f"Fe–C: {carbon:.2f} wt% C at {temperature:.0f} °C → {phase}.")

    else:
        c1, c2 = st.columns(2)
        with c1:
            nickel = st.slider("Nickel composition (wt% Ni)", 0.0, 100.0, 50.0, 0.5)
        with c2:
            temperature = st.slider("Temperature (°C)", 1000, 1800, 1350, 1)

        phase = cu_ni_phase(nickel, temperature)
        m1, m2, m3 = st.columns(3)
        m1.metric("Composition", f"{nickel:.1f} wt% Ni")
        m2.metric("Temperature", f"{temperature:.0f} °C")
        m3.metric("Estimated Region", phase)

        st.pyplot(plot_cu_ni(nickel, temperature), use_container_width=True)
        st.info("Educational model: Cu–Ni is represented as a simplified isomorphous system with approximate liquidus and solidus boundaries.")
        record("Phase Diagram", f"Cu–Ni: {nickel:.1f} wt% Ni at {temperature:.0f} °C → {phase}.")

# ============================================================
# ENGINEERING CALCULATORS
# ============================================================

elif page == "Engineering Calculators":
    header("Engineering Calculators", "Practical mechanical, thermal and materials-engineering calculations")

    tool = st.selectbox(
        "Select calculator",
        [
            "Specific Strength",
            "Specific Yield Strength",
            "Mass from Volume",
            "Thermal Expansion",
            "Thermal Stress",
            "Factor of Safety",
            "Corrosion Rate",
            "Material Property Comparison",
        ],
    )

    if tool == "Specific Strength":
        st.subheader("Specific Strength")
        uts = st.number_input("Ultimate tensile strength (MPa)", 0.0, 5000.0, 572.0, 10.0)
        density = st.number_input("Density (g/cm³)", 0.01, 25.0, 2.81, 0.01)
        if st.button("Calculate", type="primary"):
            result = calc_specific_strength(uts, density)
            st.metric("Specific strength", f"{result:.2f} MPa/(g/cm³)")
            record("Engineering Calculator", f"Specific strength = {result:.2f} MPa/(g/cm³).")

    elif tool == "Specific Yield Strength":
        st.subheader("Specific Yield Strength")
        ys = st.number_input("Yield strength (MPa)", 0.0, 3000.0, 503.0, 10.0)
        density = st.number_input("Density (g/cm³)", 0.01, 25.0, 2.81, 0.01)
        if st.button("Calculate", type="primary"):
            result = calc_specific_yield(ys, density)
            st.metric("Specific yield strength", f"{result:.2f} MPa/(g/cm³)")
            record("Engineering Calculator", f"Specific yield strength = {result:.2f} MPa/(g/cm³).")

    elif tool == "Mass from Volume":
        st.subheader("Mass from Volume")
        density = st.number_input("Density (g/cm³)", 0.01, 25.0, 7.87, 0.01)
        volume = st.number_input("Volume (cm³)", 0.0, 1_000_000.0, 100.0, 10.0)
        if st.button("Calculate", type="primary"):
            result = calc_mass(density, volume)
            st.metric("Mass", f"{result:.2f} g")
            record("Engineering Calculator", f"Mass = {result:.2f} g for {volume:.2f} cm³.")

    elif tool == "Thermal Expansion":
        st.subheader("Thermal Expansion")
        length = st.number_input("Initial length (mm)", 0.01, 1_000_000.0, 1000.0, 10.0)
        cte = st.number_input("CTE (µm/m·K)", 0.0, 100.0, 12.0, 0.1)
        delta_t = st.number_input("Temperature change (°C)", -2000.0, 2000.0, 100.0, 10.0)
        if st.button("Calculate", type="primary"):
            result = calc_expansion(length, cte, delta_t)
            st.metric("Change in length", f"{result:.4f} mm")
            record("Engineering Calculator", f"Thermal expansion = {result:.4f} mm.")

    elif tool == "Thermal Stress":
        st.subheader("Fully Restrained Thermal Stress — Simplified")
        modulus = st.number_input("Young's modulus (GPa)", 0.01, 500.0, 200.0, 1.0)
        cte = st.number_input("CTE (µm/m·K)", 0.0, 100.0, 12.0, 0.1)
        delta_t = st.number_input("Temperature change (°C)", -2000.0, 2000.0, 100.0, 10.0)
        if st.button("Calculate", type="primary"):
            result = calc_thermal_stress(modulus, cte, delta_t)
            st.metric("Thermal stress", f"{result:.2f} MPa")
            st.warning("This is a simplified fully restrained elastic model; real components may require temperature-dependent properties, creep, plasticity and boundary-condition analysis.")
            record("Engineering Calculator", f"Simplified thermal stress = {result:.2f} MPa.")

    elif tool == "Factor of Safety":
        st.subheader("Factor of Safety")
        ys = st.number_input("Yield/failure reference stress (MPa)", 0.1, 5000.0, 350.0, 10.0)
        applied = st.number_input("Applied stress (MPa)", 0.1, 5000.0, 100.0, 10.0)
        if st.button("Calculate", type="primary"):
            result = calc_fos(ys, applied)
            st.metric("Factor of Safety", f"{result:.2f}")
            record("Engineering Calculator", f"Factor of safety = {result:.2f}.")

    elif tool == "Corrosion Rate":
        st.subheader("Weight-Loss Corrosion Rate")
        K = st.number_input("Unit constant K", 0.000001, 1_000_000.0, 87_600.0, 100.0)
        weight_loss = st.number_input("Weight loss", 0.0, 1_000_000.0, 1.0, 0.1)
        density = st.number_input("Density", 0.001, 30.0, 7.87, 0.01)
        area = st.number_input("Exposed area", 0.0001, 1_000_000.0, 10.0, 1.0)
        time = st.number_input("Exposure time", 0.0001, 1_000_000.0, 100.0, 1.0)
        if st.button("Calculate", type="primary"):
            result = calc_corrosion_rate(K, weight_loss, density, area, time)
            if result is None:
                st.error("Density, area and time must be positive.")
            else:
                st.metric("Corrosion rate", f"{result:.6f} mm/year")
                record("Engineering Calculator", f"Corrosion rate = {result:.6f} mm/year.")

    else:
        st.subheader("Material Property Comparison")
        chosen = st.multiselect("Select materials", MATERIALS["Material"].tolist(), default=MATERIALS["Material"].tolist()[:5])
        prop_map = {
            "Yield Strength": "Yield Strength (MPa)",
            "Tensile Strength": "Tensile Strength (MPa)",
            "Density": "Density (g/cm³)",
            "Hardness": "Hardness (HB)",
            "Thermal Conductivity": "Thermal Conductivity (W/m·K)",
            "Young's Modulus": "Young's Modulus (GPa)",
        }
        prop = st.selectbox("Property", list(prop_map))
        if chosen:
            subset = MATERIALS[MATERIALS["Material"].isin(chosen)].copy()
            st.pyplot(plot_material_bars(subset, prop_map[prop], f"{prop} Comparison", prop_map[prop]), use_container_width=True)
        else:
            st.info("Select at least one material.")

# ============================================================
# LEARNING MODE
# ============================================================

elif page == "Learning Mode":
    header("Learning Mode", "Interactive materials-engineering concepts, equations and knowledge checks")

    topic = st.selectbox("Learning topic", list(LESSONS))
    lesson = LESSONS[topic]

    st.markdown(f"### {topic}")
    st.write(lesson["concept"])
    st.markdown("#### Engineering Equation / Principle")
    st.code(lesson["equation"])
    st.info(lesson["takeaway"])

    if topic == "Phase Diagrams":
        st.markdown("#### Phase Diagram Exploration")
        st.write("Use the dedicated Phase Diagram Analysis page for the full interactive Fe–C and Cu–Ni diagrams.")
        st.markdown("**Key idea:** composition + temperature → phase field → microstructure → properties")

    if topic == "Heat Treatment":
        rate = st.slider("Relative cooling rate", 1, 10, 5)
        if rate <= 3:
            st.success("Slow cooling: more time for diffusion and near-equilibrium transformations.")
        elif rate <= 7:
            st.info("Intermediate cooling: transformation behaviour depends strongly on alloy composition and kinetics.")
        else:
            st.warning("Rapid cooling: diffusion may be suppressed and harder non-equilibrium structures may form in suitable alloys.")

    if topic in ["Material Selection", "Stress & Strain", "Young's Modulus", "Thermal Behaviour"]:
        st.markdown("#### Quick Engineering Check")
        if topic == "Material Selection":
            st.write("If two materials have equal strength, the lower-density material will normally have the better strength-to-weight ratio.")
        elif topic == "Stress & Strain":
            force = st.number_input("Force (N)", 0.0, 1_000_000.0, 10000.0, 1000.0)
            area = st.number_input("Area (mm²)", 0.1, 1_000_000.0, 100.0, 10.0)
            st.metric("Stress", f"{force / area:.2f} MPa")
        elif topic == "Young's Modulus":
            st.write("Remember: stiffness and strength are different concepts. A stiff material is not necessarily the strongest material.")
        else:
            st.write("If expansion is restrained, thermal stress can become important even without an externally applied mechanical load.")

    st.markdown("---")
    st.markdown("## Engineering Knowledge Check")

    answers = []
    for i, (question, options, correct) in enumerate(QUIZ):
        answers.append(st.radio(f"{i + 1}. {question}", options, key=f"quiz_{i}"))

    if st.button("Check Quiz", type="primary"):
        score = sum(answer == item[2] for answer, item in zip(answers, QUIZ))
        st.session_state.quiz_score = score

    if st.session_state.quiz_score is not None:
        score = st.session_state.quiz_score
        st.metric("Quiz Score", f"{score}/{len(QUIZ)}", f"{100 * score / len(QUIZ):.0f}%")
        if score >= 4:
            st.success("Excellent — strong fundamentals.")
        elif score >= 3:
            st.info("Good progress — review the missed concepts and try again.")
        else:
            st.warning("Keep practicing — the learning sections above are designed to build these fundamentals.")

# ============================================================
# ANALYSIS HISTORY
# ============================================================

else:
    header("Analysis History", "Review engineering calculations and selection decisions from this session")

    total = len(st.session_state.history)
    st.metric("Recorded Activities", total)

    if total == 0:
        st.info("No activities recorded yet. Run a calculation, selection or phase analysis first.")
    else:
        filter_type = st.selectbox("Filter", ["All"] + sorted(set(x["module"] for x in st.session_state.history)) )
        records = st.session_state.history if filter_type == "All" else [x for x in st.session_state.history if x["module"] == filter_type]
        for i, item in enumerate(reversed(records), 1):
            with st.expander(f"{i}. {item['module']} • {item['time']}"):
                st.write(item["result"])

        if st.button("Clear Session History"):
            st.session_state.history = []
            st.session_state.last_selection = None
            st.success("Session history cleared.")
            st.rerun()

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown("---")
st.caption("MatXpert • Materials Engineering Intelligence • Python + Streamlit + Pandas + NumPy + Matplotlib")
