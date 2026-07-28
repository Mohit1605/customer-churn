"""
SHAP Explainability Service

Responsibilities
----------------
- Generate SHAP explanations
- Rank features by importance
- Return frontend-friendly explanations
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from app.core.shap_loader import (
    get_explainer,
    get_feature_names,
)
from app.utils.logger import logger


TOP_FEATURES = 5


def _clean_feature_name(feature_name: str) -> str:
    """
    Convert transformed feature names into human-readable names.
    """

    feature_name = feature_name.removeprefix("num__")
    feature_name = feature_name.removeprefix("cat__")

    if "_" in feature_name:
        return feature_name.split("_", 1)[0]

    return feature_name


def _get_original_feature_value(
    encoded_feature: str,
    customer: pd.DataFrame,
) -> Any:
    """
    Return the original customer value corresponding
    to an encoded feature.
    """

    encoded_feature = encoded_feature.removeprefix("num__")
    encoded_feature = encoded_feature.removeprefix("cat__")

    if encoded_feature in customer.columns:
        return customer.iloc[0][encoded_feature]

    if "_" in encoded_feature:
        original_column = encoded_feature.split("_", 1)[0]

        if original_column in customer.columns:
            return customer.iloc[0][original_column]

    return None


def generate_explanation(
    transformed_customer: Any,
    original_customer: pd.DataFrame,
) -> list[dict[str, Any]]:
    """
    Generate SHAP explanations for a single customer prediction.

    Parameters
    ----------
    transformed_customer
        Encoded customer features.

    original_customer
        Customer dataframe after feature engineering
        but before preprocessing.

    Returns
    -------
    list[dict[str, Any]]
        Top contributing features.
    """

    logger.info("Generating SHAP explanation.")

    explainer = get_explainer()
    feature_names = get_feature_names()

    explanation = explainer(transformed_customer)

    shap_values = explanation.values[0]

    explanations: list[dict[str, Any]] = []

    for feature_name, shap_value in zip(
        feature_names,
        shap_values,
    ):

        shap_value = float(shap_value)

        explanations.append(
            {
                "feature": _clean_feature_name(feature_name),
                "feature_value": _get_original_feature_value(
                    feature_name,
                    original_customer,
                ),
                "shap_value": round(shap_value, 6),
                "abs_importance": round(abs(shap_value), 6),
                "direction": (
                    "Increase Churn"
                    if shap_value >= 0
                    else "Decrease Churn"
                ),
            }
        )

    explanations.sort(
        key=lambda item: item["abs_importance"],
        reverse=True,
    )

    logger.info("SHAP explanation generated successfully.")

    return explanations[:TOP_FEATURES]