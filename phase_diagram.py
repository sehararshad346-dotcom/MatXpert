import pandas as pd
import matplotlib.pyplot as plt


# ==================================================
# LOAD PHASE DIAGRAM DATA
# ==================================================

def load_phase_data(file_path="data/phase_diagrams.csv"):
    """
    Load phase diagram data from CSV.
    """

    try:
        data = pd.read_csv(file_path)
        return data

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Phase diagram data file not found: {file_path}"
        )


# ==================================================
# GET AVAILABLE SYSTEMS
# ==================================================

def get_systems(data):
    """
    Return available material systems.
    """

    return sorted(
        data["System"].unique()
    )


# ==================================================
# GET SELECTED SYSTEM DATA
# ==================================================

def get_system_data(data, system):
    """
    Return data for the selected material system.
    """

    return data[
        data["System"] == system
    ].copy()


# ==================================================
# PHASE REGION DETECTION
# ==================================================

def detect_phase_region(
    data,
    carbon,
    temperature
):
    """
    Detect the closest phase condition
    from the available prototype dataset.
    """

    data = data.copy()

    # Carbon difference
    carbon_difference = abs(
        data["Composition_wt_percent_C"]
        - carbon
    )

    # Temperature difference
    temperature_difference = abs(
        data["Temperature_C"]
        - temperature
    )

    # Normalize temperature difference
    temperature_difference = (
        temperature_difference / 100
    )

    # Combined distance
    data["Distance"] = (
        carbon_difference
        + temperature_difference
    )

    # Find closest reference condition
    nearest = data.loc[
        data["Distance"].idxmin()
    ]

    phase = nearest["Phase"]

    # Count phases
    phase_count = len(
        phase.split("+")
    )

    if phase_count == 1:

        region_type = "Single-Phase Region"

    elif phase_count == 2:

        region_type = "Two-Phase Region"

    else:

        region_type = "Multi-Phase Region"

    return {
        "phase": phase,
        "region_type": region_type,
        "phase_count": phase_count,
        "reference_carbon":
            nearest[
                "Composition_wt_percent_C"
            ],
        "reference_temperature":
            nearest[
                "Temperature_C"
            ]
    }


# ==================================================
# FE-C PHASE DIAGRAM
# ==================================================

def plot_fe_c_phase_diagram(
    data,
    selected_carbon=None,
    selected_temperature=None,
    reference_carbon=None,
    reference_temperature=None
):
    """
    Create an engineering-style Fe-C
    phase diagram visualization.
    """

    fig, ax = plt.subplots(
        figsize=(11, 6.5)
    )

    # --------------------------------------------------
    # REFERENCE DATA
    # --------------------------------------------------

    ax.scatter(
        data[
            "Composition_wt_percent_C"
        ],
        data[
            "Temperature_C"
        ],
        s=40,
        label="Reference Data"
    )

    ax.plot(
        data[
            "Composition_wt_percent_C"
        ],
        data[
            "Temperature_C"
        ],
        linewidth=1.5
    )

    # --------------------------------------------------
    # EUTECTOID POINT
    # --------------------------------------------------

    eutectoid_carbon = 0.76
    eutectoid_temperature = 727

    ax.scatter(
        eutectoid_carbon,
        eutectoid_temperature,
        s=90,
        marker="o",
        label="Eutectoid Point"
    )

    ax.annotate(
        "Eutectoid\n0.76 wt% C\n727 °C",
        xy=(
            eutectoid_carbon,
            eutectoid_temperature
        ),
        xytext=(
            1.1,
            800
        ),
        arrowprops=dict(
            arrowstyle="->"
        ),
        fontsize=9
    )

    # --------------------------------------------------
    # SELECTED CONDITION
    # --------------------------------------------------

    if (
        selected_carbon is not None
        and selected_temperature is not None
    ):

        ax.scatter(
            selected_carbon,
            selected_temperature,
            s=200,
            marker="*",
            label="Selected Condition"
        )

    # --------------------------------------------------
    # NEAREST REFERENCE CONDITION
    # --------------------------------------------------

    if (
        reference_carbon is not None
        and reference_temperature is not None
    ):

        ax.scatter(
            reference_carbon,
            reference_temperature,
            s=80,
            marker="o",
            label="Nearest Reference"
        )

    # --------------------------------------------------
    # PHASE REGION LABELS
    # --------------------------------------------------

    ax.text(
        0.35,
        1510,
        "LIQUID",
        fontsize=11
    )

    ax.text(
        1.2,
        1350,
        "AUSTENITE (γ)",
        fontsize=11
    )

    ax.text(
        0.25,
        900,
        "FERRITE (α)",
        fontsize=10
    )

    ax.text(
        3.8,
        1050,
        "LIQUID +\nAUSTENITE",
        fontsize=9
    )

    ax.text(
        4.8,
        850,
        "LIQUID +\nCEMENTITE",
        fontsize=9
    )

    ax.text(
        5.7,
        760,
        "CEMENTITE\n(Fe₃C)",
        fontsize=9
    )

    # --------------------------------------------------
    # AXIS SETTINGS
    # --------------------------------------------------

    ax.set_xlim(
        0,
        6.67
    )

    ax.set_ylim(
        700,
        1550
    )

    ax.set_xlabel(
        "Carbon Composition (wt% C)",
        fontsize=11
    )

    ax.set_ylabel(
        "Temperature (°C)",
        fontsize=11
    )

    ax.set_title(
        "Fe-C Phase Diagram — Engineering Analysis",
        fontsize=16
    )

    # --------------------------------------------------
    # GRID
    # --------------------------------------------------

    ax.grid(
        True,
        alpha=0.25
    )

    # --------------------------------------------------
    # LEGEND
    # --------------------------------------------------

    ax.legend(
        loc="upper right"
    )

    # --------------------------------------------------
    # FINAL LAYOUT
    # --------------------------------------------------

    fig.tight_layout()

    return fig