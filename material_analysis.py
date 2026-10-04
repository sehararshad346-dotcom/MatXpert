import pandas as pd
import matplotlib.pyplot as plt


# ==================================================
# LOAD MATERIAL DATA
# ==================================================

def load_material_data(
    file_path="data/materials.csv"
):
    """
    Load material property data from CSV.
    """

    try:
        data = pd.read_csv(file_path)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Material data file not found: {file_path}"
        )

    data.columns = (
        data.columns
        .str.strip()
    )

    return data


# ==================================================
# GET AVAILABLE MATERIALS
# ==================================================

def get_materials(data):
    """
    Return available material names.
    """

    return sorted(
        data["Material"]
        .dropna()
        .unique()
    )


# ==================================================
# GET MATERIAL FAMILIES
# ==================================================

def get_material_families(data):
    """
    Return available material families.
    """

    return sorted(
        data["Family"]
        .dropna()
        .unique()
    )


# ==================================================
# GET SELECTED MATERIAL
# ==================================================

def get_material_data(
    data,
    material
):
    """
    Return selected material.
    """

    selected = data[
        data["Material"] == material
    ].copy()

    if selected.empty:
        return None

    return selected.iloc[0]


# ==================================================
# SAFE NUMERIC VALUE
# ==================================================

def safe_numeric(
    value
):
    """
    Safely convert a value to float.
    Returns None when the value is missing.
    """

    if pd.isna(value):
        return None

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


# ==================================================
# GET MATERIAL PROPERTIES
# ==================================================

def get_material_properties(
    material_row
):
    """
    Extract engineering properties
    from the selected material.
    """

    return {

        "family":
            material_row["Family"],

        "subfamily":
            material_row["Subfamily"],

        "density":
            safe_numeric(
                material_row[
                    "Density_g_cm3"
                ]
            ),

        "youngs_modulus":
            safe_numeric(
                material_row[
                    "Youngs_Modulus_GPa"
                ]
            ),

        "yield_strength":
            safe_numeric(
                material_row[
                    "Yield_Strength_MPa"
                ]
            ),

        "uts":
            safe_numeric(
                material_row[
                    "UTS_MPa"
                ]
            ),

        "hardness":
            safe_numeric(
                material_row[
                    "Hardness_HB"
                ]
            ),

        "thermal_conductivity":
            safe_numeric(
                material_row[
                    "Thermal_Conductivity_W_mK"
                ]
            ),

        "cte":
            safe_numeric(
                material_row[
                    "CTE_um_m_mK"
                ]
            ),

        "melting_temperature":
            safe_numeric(
                material_row[
                    "Melting_or_Reference_Temp_C"
                ]
            ),

        "cost_index":
            safe_numeric(
                material_row[
                    "Cost_Index_1_10"
                ]
            ),

        "data_basis":
            material_row[
                "Data_Basis"
            ],

        "reference":
            material_row[
                "Primary_Reference"
            ],

        "use_limit":
            material_row[
                "Use_Limit"
            ]
    }


# ==================================================
# SPECIFIC STRENGTH
# ==================================================

def calculate_strength_to_weight(
    yield_strength,
    density
):
    """
    Calculate specific yield strength.
    """

    if (
        yield_strength is None
        or density is None
        or density <= 0
    ):
        return None

    return (
        yield_strength
        / density
    )


# ==================================================
# SPECIFIC UTS
# ==================================================

def calculate_specific_uts(
    uts,
    density
):
    """
    Calculate specific ultimate tensile strength.
    """

    if (
        uts is None
        or density is None
        or density <= 0
    ):
        return None

    return (
        uts
        / density
    )


# ==================================================
# COST INTERPRETATION
# ==================================================

def interpret_cost(
    cost_index
):
    """
    Convert cost index into a category.
    """

    if cost_index is None:
        return "Not Available"

    if cost_index <= 3:
        return "Low"

    elif cost_index <= 6:
        return "Moderate"

    elif cost_index <= 8:
        return "High"

    else:
        return "Very High"


# ==================================================
# MATERIAL COMPARISON
# ==================================================

def compare_materials(
    data,
    material_1,
    material_2
):
    """
    Compare two materials.
    """

    row_1 = get_material_data(
        data,
        material_1
    )

    row_2 = get_material_data(
        data,
        material_2
    )

    if (
        row_1 is None
        or row_2 is None
    ):
        return None

    properties_1 = get_material_properties(
        row_1
    )

    properties_2 = get_material_properties(
        row_2
    )

    return {

        "Material 1":
            material_1,

        "Material 2":
            material_2,

        "Density":
            [
                properties_1["density"],
                properties_2["density"]
            ],

        "Young's Modulus":
            [
                properties_1[
                    "youngs_modulus"
                ],
                properties_2[
                    "youngs_modulus"
                ]
            ],

        "Yield Strength":
            [
                properties_1[
                    "yield_strength"
                ],
                properties_2[
                    "yield_strength"
                ]
            ],

        "UTS":
            [
                properties_1["uts"],
                properties_2["uts"]
            ],

        "Hardness":
            [
                properties_1["hardness"],
                properties_2["hardness"]
            ],

        "Thermal Conductivity":
            [
                properties_1[
                    "thermal_conductivity"
                ],
                properties_2[
                    "thermal_conductivity"
                ]
            ],

        "CTE":
            [
                properties_1["cte"],
                properties_2["cte"]
            ],

        "Cost Index":
            [
                properties_1["cost_index"],
                properties_2["cost_index"]
            ]
    }


# ==================================================
# PROPERTY COMPARISON GRAPH
# ==================================================

def plot_property_comparison(
    data,
    material_1,
    material_2,
    property_column,
    y_label
):
    """
    Create a comparison graph
    for a selected property.
    """

    row_1 = get_material_data(
        data,
        material_1
    )

    row_2 = get_material_data(
        data,
        material_2
    )

    if (
        row_1 is None
        or row_2 is None
    ):
        return None

    value_1 = safe_numeric(
        row_1[property_column]
    )

    value_2 = safe_numeric(
        row_2[property_column]
    )

    if (
        value_1 is None
        or value_2 is None
    ):
        return None

    materials = [
        material_1,
        material_2
    ]

    values = [
        value_1,
        value_2
    ]

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    ax.bar(
        materials,
        values
    )

    ax.set_ylabel(
        y_label
    )

    ax.set_title(
        f"{y_label} Comparison",
        fontsize=15
    )

    ax.grid(
        axis="y",
        alpha=0.25
    )

    fig.tight_layout()

    return fig


# ==================================================
# SPECIFIC STRENGTH GRAPH
# ==================================================

def plot_strength_to_weight(
    data,
    material_1,
    material_2
):
    """
    Plot specific strength comparison.
    """

    row_1 = get_material_data(
        data,
        material_1
    )

    row_2 = get_material_data(
        data,
        material_2
    )

    if (
        row_1 is None
        or row_2 is None
    ):
        return None

    strength_1 = calculate_strength_to_weight(
        safe_numeric(
            row_1["Yield_Strength_MPa"]
        ),
        safe_numeric(
            row_1["Density_g_cm3"]
        )
    )

    strength_2 = calculate_strength_to_weight(
        safe_numeric(
            row_2["Yield_Strength_MPa"]
        ),
        safe_numeric(
            row_2["Density_g_cm3"]
        )
    )

    if (
        strength_1 is None
        or strength_2 is None
    ):
        return None

    materials = [
        material_1,
        material_2
    ]

    values = [
        strength_1,
        strength_2
    ]

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    ax.bar(
        materials,
        values
    )

    ax.set_ylabel(
        "Specific Strength"
    )

    ax.set_title(
        "Strength-to-Weight Comparison",
        fontsize=15
    )

    ax.grid(
        axis="y",
        alpha=0.25
    )

    fig.tight_layout()

    return fig