import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from modules.phase_diagram import (
    load_phase_data,
    get_systems,
    get_system_data,
    detect_phase_region,
    plot_fe_c_phase_diagram
)

from modules.material_analysis import (
    load_material_data,
    get_materials,
    get_material_families,
    get_material_data,
    get_material_properties,
    calculate_strength_to_weight,
    calculate_specific_uts,
    interpret_cost,
    compare_materials,
    plot_property_comparison
)

from modules.calculations import (
    rank_materials,
    get_top_materials,
    get_best_material,
    generate_material_reason
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MatXpert",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM VISUAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL BACKGROUND
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(37, 99, 235, 0.18),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(139, 92, 246, 0.16),
                transparent 25%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(6, 182, 212, 0.10),
                transparent 30%
            ),
            #07111f;

        color: #eaf2ff;
    }


    /* ======================================================
       MAIN CONTENT
       ====================================================== */

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ======================================================
       TYPOGRAPHY
       ====================================================== */

    h1 {
        color: #f8fbff !important;
        font-weight: 850 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #f1f6ff !important;
        font-weight: 800 !important;
    }

    h3 {
        color: #e8f0ff !important;
        font-weight: 750 !important;
    }

    h4 {
        color: #dce8fa !important;
    }

    p {
        color: #aebed5 !important;
    }

    label {
        color: #b9c8dc !important;
    }

    .stCaption {
        color: #71849e !important;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0b1729 0%,
                #08111f 100%
            );

        border-right: 1px solid rgba(90, 130, 190, 0.18);
    }

    section[data-testid="stSidebar"] * {
        color: #d9e5f7;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 2rem !important;
        font-weight: 900 !important;

        background:
            linear-gradient(
                90deg,
                #60a5fa,
                #a78bfa,
                #22d3ee
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(120, 150, 190, 0.15);
    }


    /* ======================================================
       SIDEBAR NAVIGATION
       ====================================================== */

    div[role="radiogroup"] label {
        border-radius: 12px;
        padding: 10px 12px;
        margin: 5px 0;

        background: rgba(255,255,255,0.025);

        transition:
            transform 0.2s ease,
            background 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[role="radiogroup"] label:hover {
        background:
            linear-gradient(
                90deg,
                rgba(37,99,235,0.18),
                rgba(139,92,246,0.12)
            );

        transform: translateX(4px);

        box-shadow:
            0 0 20px rgba(37,99,235,0.12);
    }


    /* ======================================================
       HERO AREA
       ====================================================== */

    .hero-glow {
        padding: 28px 32px;
        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(30,64,175,0.35),
                rgba(88,28,135,0.28),
                rgba(8,145,178,0.22)
            );

        border: 1px solid rgba(120,160,220,0.22);

        box-shadow:
            0 20px 70px rgba(0,0,0,0.30),
            inset 0 1px rgba(255,255,255,0.06);

        animation:
            heroPulse 5s ease-in-out infinite;
    }

    @keyframes heroPulse {

        0%, 100% {
            box-shadow:
                0 20px 70px rgba(0,0,0,0.30),
                0 0 0 rgba(59,130,246,0);
        }

        50% {
            box-shadow:
                0 20px 70px rgba(0,0,0,0.30),
                0 0 35px rgba(59,130,246,0.13);
        }
    }


    /* ======================================================
       GRADIENT TITLE
       ====================================================== */

    .gradient-title {
        background:
            linear-gradient(
                90deg,
                #60a5fa,
                #a78bfa,
                #22d3ee,
                #60a5fa
            );

        background-size: 250% auto;

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        animation:
            gradientMove 5s linear infinite;
    }

    @keyframes gradientMove {

        0% {
            background-position: 0% center;
        }

        100% {
            background-position: 250% center;
        }
    }


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(20,36,61,0.92),
                rgba(10,23,40,0.92)
            );

        border:
            1px solid rgba(100,140,200,0.18);

        border-radius: 16px;

        padding: 20px;

        box-shadow:
            0 10px 35px rgba(0,0,0,0.22);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }

    div[data-testid="stMetric"]:hover {

        transform: translateY(-5px);

        border-color:
            rgba(96,165,250,0.45);

        box-shadow:
            0 15px 45px rgba(37,99,235,0.18);
    }

    div[data-testid="stMetricLabel"] {
        color: #91a5c0 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f5f9ff !important;
        font-weight: 850 !important;
    }


    /* ======================================================
       GLASS CARDS
       ====================================================== */

    .glass-card {

        padding: 22px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(25,43,70,0.75),
                rgba(10,23,40,0.72)
            );

        border:
            1px solid rgba(130,160,210,0.16);

        box-shadow:
            0 15px 45px rgba(0,0,0,0.20),
            inset 0 1px rgba(255,255,255,0.035);

        transition:
            transform 0.25s ease,
            border-color 0.25s ease;
    }

    .glass-card:hover {

        transform: translateY(-4px);

        border-color:
            rgba(96,165,250,0.35);
    }


    /* ======================================================
       COLORFUL MODULE CARDS
       ====================================================== */

    .module-blue {

        border-left:
            4px solid #3b82f6;

        background:
            linear-gradient(
                135deg,
                rgba(37,99,235,0.20),
                rgba(15,23,42,0.72)
            );
    }

    .module-purple {

        border-left:
            4px solid #a855f7;

        background:
            linear-gradient(
                135deg,
                rgba(147,51,234,0.20),
                rgba(15,23,42,0.72)
            );
    }

    .module-cyan {

        border-left:
            4px solid #06b6d4;

        background:
            linear-gradient(
                135deg,
                rgba(6,182,212,0.20),
                rgba(15,23,42,0.72)
            );
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {

        min-height: 48px;

        border: none;

        border-radius: 11px;

        color: white !important;

        font-weight: 750;

        background:
            linear-gradient(
                90deg,
                #2563eb,
                #7c3aed
            );

        box-shadow:
            0 8px 25px rgba(37,99,235,0.25);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            filter 0.2s ease;
    }

    .stButton > button:hover {

        transform: translateY(-3px);

        filter: brightness(1.12);

        box-shadow:
            0 12px 35px rgba(124,58,237,0.30);
    }


    /* ======================================================
       INPUTS
       ====================================================== */

    div[data-baseweb="select"] > div {

        background:
            #111f34 !important;

        border:
            1px solid #2c405e !important;

        border-radius: 10px;
    }

    div[data-baseweb="select"] * {
        color: #e6eefc !important;
    }

    div[data-testid="stNumberInput"] input {

        background:
            #111f34 !important;

        color:
            #e6eefc !important;

        border:
            1px solid #2c405e !important;

        border-radius: 10px;
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    div[data-testid="stAlert"] {

        border-radius: 12px;

        border: 1px solid rgba(100,140,200,0.20);

        background:
            rgba(17,31,52,0.75);
    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    div[data-testid="stExpander"] {

        background:
            rgba(15,28,47,0.75);

        border:
            1px solid rgba(100,140,200,0.16);

        border-radius: 12px;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {

        border-color:
            rgba(120,150,190,0.15);
    }


    /* ======================================================
       STATUS DOT
       ====================================================== */

    .status-dot {

        display: inline-block;

        width: 9px;
        height: 9px;

        background: #22c55e;

        border-radius: 50%;

        margin-right: 8px;

        box-shadow:
            0 0 12px rgba(34,197,94,0.7);

        animation:
            statusPulse 2s infinite;
    }

    @keyframes statusPulse {

        0%,100% {
            opacity: 1;
        }

        50% {
            opacity: 0.45;
        }
    }


    /* ======================================================
       STEP NUMBERS
       ====================================================== */

    .step-number {

        font-size: 2rem;

        font-weight: 900;

        background:
            linear-gradient(
                135deg,
                #60a5fa,
                #a78bfa
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_all_data():

    materials = load_material_data(
        "data/materials.csv"
    )

    phases = load_phase_data(
        "data/phase_diagrams.csv"
    )

    return materials, phases


try:

    materials_data, phase_data = load_all_data()

except Exception as error:

    st.error(
        "MatXpert could not load its engineering database."
    )

    st.exception(error)

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ MatXpert")

    st.caption(
        "Materials Engineering Intelligence"
    )

    st.divider()

    st.caption("WORKSPACE")

    module = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📈 Phase Diagram Analysis",
            "🔬 Material Property Analysis",
            "🎯 Material Selection Engine"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("DATABASE")

    st.write(
        f"📦 **{len(materials_data)}** materials"
    )

    st.write(
        f"🧬 **{len(get_material_families(materials_data))}** families"
    )

    st.write(
        f"📊 **{len(phase_data)}** phase points"
    )

    st.divider()

    st.caption("SYSTEM STATUS")

    st.markdown(
        '<span class="status-dot"></span>Database Ready',
        unsafe_allow_html=True
    )

    st.caption("MatXpert v1.0")


# ============================================================
# DASHBOARD
# ============================================================

if module == "🏠 Dashboard":

    # HERO

    st.markdown(
        '<div class="hero-glow">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### ⚙️ MATXPERT"
    )

    st.markdown(
        '<h1 class="gradient-title">'
        'Materials Engineering Intelligence'
        '</h1>',
        unsafe_allow_html=True
    )

    st.write(
        "An interactive engineering workspace for "
        "phase analysis, material characterization, "
        "comparison, and intelligent material screening."
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # METRICS

    st.subheader("Engineering Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📦 Materials",
            len(materials_data)
        )

    with col2:

        st.metric(
            "🧬 Families",
            len(
                get_material_families(
                    materials_data
                )
            )
        )

    with col3:

        st.metric(
            "📈 Phase Systems",
            len(
                get_systems(
                    phase_data
                )
            )
        )

    with col4:

        st.metric(
            "🔬 Properties",
            "10+"
        )

    st.divider()

    # MODULES

    st.subheader("Analysis Workspace")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="glass-card module-blue">

            <h3>📈 Phase Analysis</h3>

            <p>
            Explore material phase behavior using
            composition and temperature.
            </p>

            <b>Composition → Temperature → Phase</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="glass-card module-purple">

            <h3>🔬 Property Intelligence</h3>

            <p>
            Investigate mechanical, thermal and
            physical material properties.
            </p>

            <b>Properties → Compare → Analyze</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="glass-card module-cyan">

            <h3>🎯 Material Selection</h3>

            <p>
            Screen candidate materials against
            engineering requirements.
            </p>

            <b>Requirements → Score → Select</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # WORKFLOW

    st.subheader("Engineering Workflow")

    col1, col2, col3, col4 = st.columns(4)

    steps = [
        (
            "01",
            "🎯",
            "Define",
            "Set engineering requirements."
        ),
        (
            "02",
            "🧠",
            "Analyze",
            "Process material data."
        ),
        (
            "03",
            "⚖️",
            "Compare",
            "Evaluate candidates."
        ),
        (
            "04",
            "🚀",
            "Select",
            "Identify suitable materials."
        )
    ]

    for column, step in zip(
        [col1, col2, col3, col4],
        steps
    ):

        with column:

            number, icon, title, description = step

            st.markdown(
                f"""
                <div class="glass-card">

                <div class="step-number">
                {number}
                </div>

                <h3>
                {icon} {title}
                </h3>

                <p>
                {description}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    st.info(
        "💡 MatXpert is designed for engineering education "
        "and material screening. Final design decisions "
        "should use verified standards and material data."
    )


# ============================================================
# PHASE DIAGRAM
# ============================================================

elif module == "📈 Phase Diagram Analysis":

    st.title("📈 Phase Diagram Analysis")

    st.write(
        "Investigate phase behavior using composition "
        "and temperature."
    )

    st.divider()

    systems = get_systems(
        phase_data
    )

    selected_system = st.selectbox(
        "Material System",
        systems
    )

    system_data = get_system_data(
        phase_data,
        selected_system
    )

    st.subheader("⚙️ Engineering Condition")

    col1, col2 = st.columns(2)

    with col1:

        carbon = st.number_input(
            "Carbon Composition (wt% C)",
            min_value=0.0,
            max_value=6.67,
            value=0.76,
            step=0.01
        )

    with col2:

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=700.0,
            max_value=1550.0,
            value=727.0,
            step=1.0
        )

    result = detect_phase_region(
        system_data,
        carbon,
        temperature
    )

    st.divider()

    st.subheader("🔎 Analysis Result")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Identified Phase",
            result["phase"]
        )

    with col2:

        st.metric(
            "Region",
            result["region_type"]
        )

    with col3:

        st.metric(
            "Reference Temperature",
            f'{result["reference_temperature"]:.0f} °C'
        )

    st.info(
        f"📍 Selected condition is closest to "
        f"{result['reference_carbon']:.2f} wt% C at "
        f"{result['reference_temperature']:.0f} °C."
    )

    st.subheader("📊 Phase Diagram")

    fig = plot_fe_c_phase_diagram(
        system_data,
        selected_carbon=carbon,
        selected_temperature=temperature,
        reference_carbon=result[
            "reference_carbon"
        ],
        reference_temperature=result[
            "reference_temperature"
        ]
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

    st.warning(
        "⚠️ The current Fe-C dataset is a prototype "
        "screening dataset rather than a complete "
        "thermodynamic equilibrium phase diagram."
    )


# ============================================================
# MATERIAL PROPERTY ANALYSIS
# ============================================================

elif module == "🔬 Material Property Analysis":

    st.title(
        "🔬 Material Property Intelligence"
    )

    st.write(
        "Explore and compare engineering properties "
        "of materials in the MatXpert database."
    )

    st.divider()

    materials = get_materials(
        materials_data
    )

    material_1 = st.selectbox(
        "Primary Material",
        materials
    )

    row = get_material_data(
        materials_data,
        material_1
    )

    properties = get_material_properties(
        row
    )

    st.subheader(
        f"📋 {material_1}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Family",
            properties["family"]
        )

    with col2:

        density = properties["density"]

        st.metric(
            "Density",
            (
                f"{density:.2f}"
                if density is not None
                else "N/A"
            ),
            "g/cm³"
            if density is not None
            else None
        )

    with col3:

        strength = properties[
            "yield_strength"
        ]

        st.metric(
            "Yield Strength",
            (
                f"{strength:.0f}"
                if strength is not None
                else "N/A"
            ),
            "MPa"
            if strength is not None
            else None
        )

    with col4:

        hardness = properties["hardness"]

        st.metric(
            "Hardness",
            (
                f"{hardness:.0f}"
                if hardness is not None
                else "N/A"
            ),
            "HB"
            if hardness is not None
            else None
        )

    st.divider()

    # DERIVED

    st.subheader(
        "⚡ Derived Engineering Metrics"
    )

    specific_strength = calculate_strength_to_weight(
        properties["yield_strength"],
        properties["density"]
    )

    specific_uts = calculate_specific_uts(
        properties["uts"],
        properties["density"]
    )

    cost_category = interpret_cost(
        properties["cost_index"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Specific Strength",
            (
                f"{specific_strength:.1f}"
                if specific_strength is not None
                else "N/A"
            )
        )

        st.caption(
            "Yield strength / density"
        )

    with col2:

        st.metric(
            "Specific UTS",
            (
                f"{specific_uts:.1f}"
                if specific_uts is not None
                else "N/A"
            )
        )

        st.caption(
            "UTS / density"
        )

    with col3:

        st.metric(
            "Cost Category",
            cost_category
        )

    st.divider()

    # PROPERTIES

    st.subheader(
        "📚 Engineering Properties"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.write(
            "**Young's Modulus**"
        )

        value = properties[
            "youngs_modulus"
        ]

        st.write(
            f"{value:.1f} GPa"
            if value is not None
            else "N/A"
        )

        st.write(
            "**Ultimate Tensile Strength**"
        )

        value = properties["uts"]

        st.write(
            f"{value:.0f} MPa"
            if value is not None
            else "N/A"
        )

    with col2:

        st.write(
            "**Thermal Conductivity**"
        )

        value = properties[
            "thermal_conductivity"
        ]

        st.write(
            f"{value:.1f} W/m·K"
            if value is not None
            else "N/A"
        )

        st.write(
            "**Coefficient of Thermal Expansion**"
        )

        value = properties["cte"]

        st.write(
            f"{value:.1f} µm/m·K"
            if value is not None
            else "N/A"
        )

    with col3:

        st.write(
            "**Melting / Reference Temperature**"
        )

        value = properties[
            "melting_temperature"
        ]

        st.write(
            f"{value:.0f} °C"
            if value is not None
            else "N/A"
        )

        st.write(
            "**Cost Index**"
        )

        value = properties["cost_index"]

        st.write(
            f"{value:.0f} / 10"
            if value is not None
            else "N/A"
        )

    st.divider()

    # COMPARISON

    st.subheader(
        "⚖️ Material Comparison"
    )

    material_2 = st.selectbox(
        "Compare With",
        materials,
        index=(
            1 if len(materials) > 1 else 0
        ),
        key="comparison_material"
    )

    comparison = compare_materials(
        materials_data,
        material_1,
        material_2
    )

    if comparison is not None:

        comparison_rows = [

            (
                "Density",
                comparison["Density"],
                "g/cm³"
            ),

            (
                "Young's Modulus",
                comparison["Young's Modulus"],
                "GPa"
            ),

            (
                "Yield Strength",
                comparison["Yield Strength"],
                "MPa"
            ),

            (
                "UTS",
                comparison["UTS"],
                "MPa"
            ),

            (
                "Hardness",
                comparison["Hardness"],
                "HB"
            ),

            (
                "Thermal Conductivity",
                comparison["Thermal Conductivity"],
                "W/m·K"
            ),

            (
                "CTE",
                comparison["CTE"],
                "µm/m·K"
            ),

            (
                "Cost Index",
                comparison["Cost Index"],
                "1–10"
            )
        ]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                "**PROPERTY**"
            )

        with col2:

            st.write(
                f"**{material_1}**"
            )

        with col3:

            st.write(
                f"**{material_2}**"
            )

        st.divider()

        for name, values, unit in comparison_rows:

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(name)

            with col2:

                value = values[0]

                st.write(
                    f"{value:g} {unit}"
                    if value is not None
                    else "N/A"
                )

            with col3:

                value = values[1]

                st.write(
                    f"{value:g} {unit}"
                    if value is not None
                    else "N/A"
                )

        st.divider()

        st.subheader(
            "📊 Visual Comparison"
        )

        property_options = {

            "Yield Strength": (
                "Yield_Strength_MPa",
                "Yield Strength (MPa)"
            ),

            "Density": (
                "Density_g_cm3",
                "Density (g/cm³)"
            ),

            "Hardness": (
                "Hardness_HB",
                "Hardness (HB)"
            ),

            "Thermal Conductivity": (
                "Thermal_Conductivity_W_mK",
                "Thermal Conductivity (W/m·K)"
            )
        }

        selected_property = st.selectbox(
            "Property",
            list(property_options.keys())
        )

        property_column, y_label = (
            property_options[
                selected_property
            ]
        )

        fig = plot_property_comparison(
            materials_data,
            material_1,
            material_2,
            property_column,
            y_label
        )

        if fig is not None:

            st.pyplot(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "Visualization unavailable because "
                "required property data is missing."
            )


# ============================================================
# MATERIAL SELECTION ENGINE
# ============================================================

elif module == "🎯 Material Selection Engine":

    st.title(
        "🎯 Material Selection Engine"
    )

    st.write(
        "Transform engineering requirements into a "
        "quantitative material screening analysis."
    )

    st.divider()

    # REQUIREMENTS

    st.subheader(
        "🎯 Engineering Requirements"
    )

    col1, col2 = st.columns(2)

    with col1:

        min_strength = st.number_input(
            "Minimum Yield Strength (MPa)",
            min_value=0.0,
            value=500.0,
            step=10.0
        )

        max_density = st.number_input(
            "Maximum Density (g/cm³)",
            min_value=0.1,
            value=8.0,
            step=0.1
        )

        min_hardness = st.number_input(
            "Minimum Hardness (HB)",
            min_value=0.0,
            value=150.0,
            step=5.0
        )

    with col2:

        min_thermal_conductivity = st.number_input(
            "Minimum Thermal Conductivity (W/m·K)",
            min_value=0.0,
            value=20.0,
            step=5.0
        )

        max_cost = st.number_input(
            "Maximum Cost Index (1–10)",
            min_value=1.0,
            max_value=10.0,
            value=6.0,
            step=1.0
        )

    st.subheader(
        "⚖️ Requirement Importance"
    )

    importance_options = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        strength_importance = st.selectbox(
            "Strength",
            importance_options,
            index=2
        )

    with col2:

        weight_importance = st.selectbox(
            "Weight",
            importance_options,
            index=2
        )

    with col3:

        hardness_importance = st.selectbox(
            "Hardness",
            importance_options,
            index=1
        )

    with col4:

        thermal_importance = st.selectbox(
            "Thermal",
            importance_options,
            index=1
        )

    with col5:

        cost_importance = st.selectbox(
            "Cost",
            importance_options,
            index=1
        )

    requirements = {

        "min_strength":
            min_strength,

        "max_density":
            max_density,

        "min_hardness":
            min_hardness,

        "min_thermal_conductivity":
            min_thermal_conductivity,

        "max_cost":
            max_cost,

        "strength_importance":
            strength_importance,

        "weight_importance":
            weight_importance,

        "hardness_importance":
            hardness_importance,

        "thermal_importance":
            thermal_importance,

        "cost_importance":
            cost_importance
    }

    st.divider()

    analyze = st.button(
        "🚀 RUN MATERIAL ANALYSIS",
        type="primary",
        use_container_width=True
    )

    if analyze:

        ranked = rank_materials(
            materials_data,
            requirements
        )

        best = get_best_material(
            ranked
        )

        top_materials = get_top_materials(
            ranked,
            3
        )

        if best is not None:

            st.success(
                "✓ Engineering analysis completed."
            )

            st.subheader(
                "🏆 Recommended Candidate"
            )

            st.title(
                best["Material"]
            )

            st.write(
                f"**Material Family:** {best['Family']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Suitability",
                    f"{best['Suitability']:.1f}%"
                )

            with col2:

                st.metric(
                    "Requirement Match",
                    f"{best['Requirement_Match']:.0f}%"
                )

            with col3:

                coverage = best.get(
                    "Data_Coverage",
                    100.0
                )

                st.metric(
                    "Data Coverage",
                    f"{coverage:.0f}%"
                )

            st.divider()

            # ENGINEERING INTERPRETATION

            best_row = get_material_data(
                materials_data,
                best["Material"]
            )

            reason = generate_material_reason(
                best_row,
                requirements
            )

            st.subheader(
                "🧠 Engineering Interpretation"
            )

            st.info(
                reason
            )

            st.divider()

            # REQUIREMENT STATUS

            st.subheader(
                "Requirement Status"
            )

            status_columns = st.columns(5)

            status_data = [

                (
                    "Strength",
                    best["Strength_Pass"]
                ),

                (
                    "Density",
                    best["Density_Pass"]
                ),

                (
                    "Hardness",
                    best["Hardness_Pass"]
                ),

                (
                    "Thermal",
                    best["Thermal_Pass"]
                ),

                (
                    "Cost",
                    best["Cost_Pass"]
                )
            ]

            for column, (name, passed) in zip(
                status_columns,
                status_data
            ):

                with column:

                    if passed:

                        st.success(
                            f"✓ {name}"
                        )

                    else:

                        st.error(
                            f"✗ {name}"
                        )

            st.divider()

            # TOP MATERIALS

            st.subheader(
                "🥇 Top Material Candidates"
            )

            for index, (_, material) in enumerate(
                top_materials.iterrows(),
                start=1
            ):

                col1, col2, col3, col4 = st.columns(
                    [0.5, 3, 1.5, 1.5]
                )

                with col1:

                    st.markdown(
                        f"### #{index}"
                    )

                with col2:

                    st.write(
                        f"**{material['Material']}**"
                    )

                    st.caption(
                        material["Family"]
                    )

                with col3:

                    st.metric(
                        "Score",
                        f"{material['Suitability']:.1f}%"
                    )

                with col4:

                    st.metric(
                        "Match",
                        f"{material['Requirement_Match']:.0f}%"
                    )

            st.divider()

            # SCORE BREAKDOWN

            st.subheader(
                "📊 Score Contribution"
            )

            score_data = {}

            possible_scores = {

                "Strength":
                    "Strength_Score",

                "Density":
                    "Density_Score",

                "Hardness":
                    "Hardness_Score",

                "Thermal":
                    "Thermal_Score",

                "Cost":
                    "Cost_Score"
            }

            for label, key in possible_scores.items():

                if key in best.index:

                    score_data[label] = best[key]

            # ==================================================
            # MATPLOTLIB CHART
            # This replaces st.bar_chart() to avoid PyArrow DLL
            # compatibility problems.
            # ==================================================

            if score_data:

                score_labels = list(
                    score_data.keys()
                )

                score_values = [

                    (
                        float(value) * 100
                        if value is not None
                        else 0
                    )

                    for value
                    in score_data.values()
                ]

                fig, ax = plt.subplots(
                    figsize=(10, 5)
                )

                bars = ax.bar(
                    score_labels,
                    score_values
                )

                ax.set_title(
                    "Material Suitability Score Contribution",
                    fontsize=15,
                    fontweight="bold"
                )

                ax.set_xlabel(
                    "Engineering Property"
                )

                ax.set_ylabel(
                    "Weighted Score (%)"
                )

                max_value = max(
                    score_values
                ) if score_values else 100

                ax.set_ylim(
                    0,
                    max(max_value * 1.20, 100)
                )

                ax.grid(
                    axis="y",
                    alpha=0.25
                )

                # Add percentage values above bars

                for bar, value in zip(
                    bars,
                    score_values
                ):

                    ax.text(
                        bar.get_x()
                        + bar.get_width() / 2,
                        bar.get_height() + 1,
                        f"{value:.1f}%",
                        ha="center",
                        va="bottom",
                        fontweight="bold"
                    )

                plt.xticks(
                    rotation=0
                )

                plt.tight_layout()

                st.pyplot(
                    fig,
                    use_container_width=True
                )

                plt.close(fig)

            else:

                st.info(
                    "Detailed score contribution will become "
                    "available with the enhanced scoring engine."
                )

            st.divider()

            st.warning(
                "⚠️ MatXpert is an engineering screening and "
                "decision-support tool. Final material selection "
                "should consider service conditions, processing, "
                "environment, standards, safety factors and "
                "verified material data."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "⚙️ MatXpert  •  Materials Engineering Intelligence"
)

st.caption(
    "Python • Streamlit • Materials Data Analysis"
)