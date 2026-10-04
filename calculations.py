import pandas as pd


# ==================================================
# SAFE NUMERIC CONVERSION
# ==================================================

def safe_numeric(value):
    """
    Safely convert a value to float.
    Returns None if the value is missing.
    """

    if pd.isna(value):
        return None

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


# ==================================================
# IMPORTANCE WEIGHTS
# ==================================================

IMPORTANCE_WEIGHTS = {

    "Low": 0.10,

    "Medium": 0.25,

    "High": 0.40,

    "Critical": 0.60
}


def get_importance_weight(importance):
    """
    Return numerical weight for an importance level.
    """

    return IMPORTANCE_WEIGHTS.get(
        importance,
        0.25
    )


# ==================================================
# PERFORMANCE SCORE
# ==================================================

def calculate_performance_score(
    value,
    requirement,
    importance,
    higher_is_better=True
):
    """
    Calculate normalized engineering performance.

    A material that exactly meets the requirement
    receives a full requirement score.

    Performance beyond the requirement is also
    recognized, but the score is capped at 100%.
    """

    value = safe_numeric(value)
    requirement = safe_numeric(requirement)

    if value is None or requirement is None:
        return None

    weight = get_importance_weight(
        importance
    )

    # ----------------------------------------------
    # Higher value is better
    # ----------------------------------------------

    if higher_is_better:

        if requirement <= 0:

            normalized = 1.0

        else:

            normalized = value / requirement

    # ----------------------------------------------
    # Lower value is better
    # ----------------------------------------------

    else:

        if value <= 0:

            normalized = 1.0

        elif requirement <= 0:

            normalized = 0.0

        else:

            normalized = requirement / value

    normalized = max(
        0.0,
        min(1.0, normalized)
    )

    return normalized * weight


# ==================================================
# CHECK REQUIREMENTS
# ==================================================

def check_material_requirements(
    material_row,
    requirements
):
    """
    Check whether a material satisfies
    the selected engineering requirements.
    """

    results = {}

    # ----------------------------------------------
    # Yield Strength
    # ----------------------------------------------

    strength = safe_numeric(
        material_row[
            "Yield_Strength_MPa"
        ]
    )

    results["strength"] = (
        strength is not None
        and strength >= requirements[
            "min_strength"
        ]
    )

    # ----------------------------------------------
    # Density
    # ----------------------------------------------

    density = safe_numeric(
        material_row[
            "Density_g_cm3"
        ]
    )

    results["density"] = (
        density is not None
        and density <= requirements[
            "max_density"
        ]
    )

    # ----------------------------------------------
    # Hardness
    # ----------------------------------------------

    hardness = safe_numeric(
        material_row[
            "Hardness_HB"
        ]
    )

    results["hardness"] = (
        hardness is not None
        and hardness >= requirements[
            "min_hardness"
        ]
    )

    # ----------------------------------------------
    # Thermal Conductivity
    # ----------------------------------------------

    thermal = safe_numeric(
        material_row[
            "Thermal_Conductivity_W_mK"
        ]
    )

    results["thermal"] = (
        thermal is not None
        and thermal >= requirements[
            "min_thermal_conductivity"
        ]
    )

    # ----------------------------------------------
    # Cost
    # ----------------------------------------------

    cost = safe_numeric(
        material_row[
            "Cost_Index_1_10"
        ]
    )

    results["cost"] = (
        cost is not None
        and cost <= requirements[
            "max_cost"
        ]
    )

    return results


# ==================================================
# COUNT PASSED REQUIREMENTS
# ==================================================

def count_passed_requirements(
    requirement_results
):
    """
    Count the number of satisfied requirements.
    """

    return sum(
        1
        for result in requirement_results.values()
        if result is True
    )


# ==================================================
# REQUIREMENT MATCH %
# ==================================================

def calculate_requirement_match(
    requirement_results
):
    """
    Calculate percentage of requirements satisfied.
    """

    if not requirement_results:

        return 0.0

    passed = count_passed_requirements(
        requirement_results
    )

    total = len(
        requirement_results
    )

    return (
        passed / total
    ) * 100


# ==================================================
# MATERIAL SUITABILITY SCORE
# ==================================================

def calculate_material_score(
    material_row,
    requirements
):
    """
    Calculate overall material suitability.

    Properties considered:

    - Yield Strength
    - Density
    - Hardness
    - Thermal Conductivity
    - Cost

    Missing properties are excluded from the
    weighted score instead of automatically
    receiving zero performance.
    """

    # ----------------------------------------------
    # Extract properties
    # ----------------------------------------------

    yield_strength = safe_numeric(
        material_row[
            "Yield_Strength_MPa"
        ]
    )

    density = safe_numeric(
        material_row[
            "Density_g_cm3"
        ]
    )

    hardness = safe_numeric(
        material_row[
            "Hardness_HB"
        ]
    )

    thermal_conductivity = safe_numeric(
        material_row[
            "Thermal_Conductivity_W_mK"
        ]
    )

    cost = safe_numeric(
        material_row[
            "Cost_Index_1_10"
        ]
    )

    # ----------------------------------------------
    # Requirements
    # ----------------------------------------------

    min_strength = requirements[
        "min_strength"
    ]

    max_density = requirements[
        "max_density"
    ]

    min_hardness = requirements[
        "min_hardness"
    ]

    min_thermal_conductivity = requirements[
        "min_thermal_conductivity"
    ]

    max_cost = requirements[
        "max_cost"
    ]

    # ----------------------------------------------
    # Importance
    # ----------------------------------------------

    strength_importance = requirements[
        "strength_importance"
    ]

    weight_importance = requirements[
        "weight_importance"
    ]

    hardness_importance = requirements[
        "hardness_importance"
    ]

    thermal_importance = requirements[
        "thermal_importance"
    ]

    cost_importance = requirements[
        "cost_importance"
    ]

    # ----------------------------------------------
    # Individual weighted scores
    # ----------------------------------------------

    strength_score = calculate_performance_score(
        yield_strength,
        min_strength,
        strength_importance,
        higher_is_better=True
    )

    density_score = calculate_performance_score(
        density,
        max_density,
        weight_importance,
        higher_is_better=False
    )

    hardness_score = calculate_performance_score(
        hardness,
        min_hardness,
        hardness_importance,
        higher_is_better=True
    )

    thermal_score = calculate_performance_score(
        thermal_conductivity,
        min_thermal_conductivity,
        thermal_importance,
        higher_is_better=True
    )

    cost_score = calculate_performance_score(
        cost,
        max_cost,
        cost_importance,
        higher_is_better=False
    )

    # ----------------------------------------------
    # Store scores and weights
    # ----------------------------------------------

    score_data = [

        (
            strength_score,
            get_importance_weight(
                strength_importance
            )
        ),

        (
            density_score,
            get_importance_weight(
                weight_importance
            )
        ),

        (
            hardness_score,
            get_importance_weight(
                hardness_importance
            )
        ),

        (
            thermal_score,
            get_importance_weight(
                thermal_importance
            )
        ),

        (
            cost_score,
            get_importance_weight(
                cost_importance
            )
        )
    ]

    # ----------------------------------------------
    # Only use properties with available data
    # ----------------------------------------------

    valid_scores = [
        score
        for score, weight in score_data
        if score is not None
    ]

    valid_weights = [
        weight
        for score, weight in score_data
        if score is not None
    ]

    if not valid_scores:

        return 0.0

    total_score = sum(
        valid_scores
    )

    total_weight = sum(
        valid_weights
    )

    if total_weight == 0:

        return 0.0

    # ----------------------------------------------
    # Normalize to 0–100
    # ----------------------------------------------

    suitability = (
        total_score
        / total_weight
    ) * 100

    return max(
        0.0,
        min(100.0, suitability)
    )


# ==================================================
# DATA COVERAGE
# ==================================================

def calculate_data_coverage(
    material_row
):
    """
    Calculate how much required engineering
    property data is available.

    Returns percentage from 0 to 100.
    """

    properties = [

        "Yield_Strength_MPa",

        "Density_g_cm3",

        "Hardness_HB",

        "Thermal_Conductivity_W_mK",

        "Cost_Index_1_10"
    ]

    available = 0

    for property_name in properties:

        value = safe_numeric(
            material_row[property_name]
        )

        if value is not None:

            available += 1

    return (
        available
        / len(properties)
    ) * 100


# ==================================================
# RANK MATERIALS
# ==================================================

def rank_materials(
    data,
    requirements
):
    """
    Calculate suitability for every material
    and return materials ranked by score.
    """

    results = []

    for _, row in data.iterrows():

        material_name = row[
            "Material"
        ]

        # ------------------------------------------
        # Suitability
        # ------------------------------------------

        suitability = calculate_material_score(
            row,
            requirements
        )

        # ------------------------------------------
        # Requirement checks
        # ------------------------------------------

        requirement_results = (
            check_material_requirements(
                row,
                requirements
            )
        )

        requirement_match = (
            calculate_requirement_match(
                requirement_results
            )
        )

        # ------------------------------------------
        # Data coverage
        # ------------------------------------------

        data_coverage = (
            calculate_data_coverage(
                row
            )
        )

        # ------------------------------------------
        # Individual property scores
        # ------------------------------------------

        strength_score = (
            calculate_performance_score(
                row[
                    "Yield_Strength_MPa"
                ],
                requirements[
                    "min_strength"
                ],
                requirements[
                    "strength_importance"
                ],
                True
            )
        )

        density_score = (
            calculate_performance_score(
                row[
                    "Density_g_cm3"
                ],
                requirements[
                    "max_density"
                ],
                requirements[
                    "weight_importance"
                ],
                False
            )
        )

        hardness_score = (
            calculate_performance_score(
                row[
                    "Hardness_HB"
                ],
                requirements[
                    "min_hardness"
                ],
                requirements[
                    "hardness_importance"
                ],
                True
            )
        )

        thermal_score = (
            calculate_performance_score(
                row[
                    "Thermal_Conductivity_W_mK"
                ],
                requirements[
                    "min_thermal_conductivity"
                ],
                requirements[
                    "thermal_importance"
                ],
                True
            )
        )

        cost_score = (
            calculate_performance_score(
                row[
                    "Cost_Index_1_10"
                ],
                requirements[
                    "max_cost"
                ],
                requirements[
                    "cost_importance"
                ],
                False
            )
        )

        results.append({

            "Material":
                material_name,

            "Family":
                row["Family"],

            "Suitability":
                suitability,

            "Requirement_Match":
                requirement_match,

            "Data_Coverage":
                data_coverage,

            "Strength_Score":
                strength_score,

            "Density_Score":
                density_score,

            "Hardness_Score":
                hardness_score,

            "Thermal_Score":
                thermal_score,

            "Cost_Score":
                cost_score,

            "Strength_Pass":
                requirement_results[
                    "strength"
                ],

            "Density_Pass":
                requirement_results[
                    "density"
                ],

            "Hardness_Pass":
                requirement_results[
                    "hardness"
                ],

            "Thermal_Pass":
                requirement_results[
                    "thermal"
                ],

            "Cost_Pass":
                requirement_results[
                    "cost"
                ]
        })

    results_df = pd.DataFrame(
        results
    )

    # ----------------------------------------------
    # Ranking
    # ----------------------------------------------

    results_df = results_df.sort_values(
        by=[
            "Suitability",
            "Requirement_Match",
            "Data_Coverage"
        ],
        ascending=False
    )

    results_df = results_df.reset_index(
        drop=True
    )

    return results_df


# ==================================================
# GET TOP MATERIALS
# ==================================================

def get_top_materials(
    ranked_data,
    number_of_materials=3
):
    """
    Return the top N materials.
    """

    return ranked_data.head(
        number_of_materials
    ).copy()


# ==================================================
# GET BEST MATERIAL
# ==================================================

def get_best_material(
    ranked_data
):
    """
    Return the highest-ranked material.
    """

    if ranked_data.empty:

        return None

    return ranked_data.iloc[0]


# ==================================================
# GENERATE ENGINEERING REASON
# ==================================================

def generate_material_reason(
    material_row,
    requirements
):
    """
    Generate an engineering explanation
    for the selected material.
    """

    results = check_material_requirements(
        material_row,
        requirements
    )

    passed = count_passed_requirements(
        results
    )

    total = len(
        results
    )

    reasons = []

    if results["strength"]:

        reasons.append(
            "meets the required yield strength"
        )

    if results["density"]:

        reasons.append(
            "meets the density limit"
        )

    if results["hardness"]:

        reasons.append(
            "meets the hardness requirement"
        )

    if results["thermal"]:

        reasons.append(
            "meets the thermal conductivity requirement"
        )

    if results["cost"]:

        reasons.append(
            "meets the cost constraint"
        )

    if reasons:

        reason_text = ", ".join(
            reasons
        )

        return (
            f"This material satisfies "
            f"{passed} of {total} primary requirements "
            f"and {reason_text}."
        )

    return (
        "This material does not satisfy "
        "the selected primary requirements."
    )