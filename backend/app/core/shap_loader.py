from typing import Any
import joblib
import shap
from app.core.config import SHAP_BACKGROUND_PATH
from app.core.model import get_model
from app.utils.logger import logger

_explainer: Any = None
_preprocessor: Any = None
_model: Any = None
_feature_names: list[str] | None = None


def load_shap() -> None:
  """ Initialize SHAP resources. This function should be called once during application startup."""

  global _explainer
  global _preprocessor
  global _model
  global _feature_names

  if _explainer is not None:
    logger.info("SHAP explainer already initialized.")
    return

  logger.info("Initializing SHAP explainer...")

  try:

    pipeline = get_model()

    _preprocessor = pipeline.named_steps["preprocessor"]
    _model = pipeline.named_steps["model"]

    background = joblib.load(SHAP_BACKGROUND_PATH)

    transformed_background = _preprocessor.transform(background)

    _feature_names = list(_preprocessor.get_feature_names_out())

    masker = shap.maskers.Independent(
        transformed_background,
        max_samples=len(transformed_background)
    )
    _explainer = shap.Explainer(_model,masker,feature_names=_feature_names,)

    logger.info("SHAP explainer initialized successfully.")

  except FileNotFoundError:
    logger.exception("SHAP background dataset not found.")
    raise

  except KeyError as e:
    logger.exception("Pipeline missing required step.")
    raise RuntimeError(f"Pipeline missing required step: {e}") from e

  except Exception as e:
    logger.exception("Failed to initialize SHAP explainer.")
    raise RuntimeError(f"Unable to initialize SHAP: {e}") from e


def get_explainer():
  """ Return initialized SHAP explainer. """

  if _explainer is None:
    raise RuntimeError("SHAP explainer has not been initialized.")

  return _explainer


def get_preprocessor():
  """Return fitted preprocessor."""

  if _preprocessor is None:
    raise RuntimeError("Preprocessor has not been initialized.")

  return _preprocessor


def get_classifier():
  """ Return trained classifier. """

  if _model is None:
    raise RuntimeError("Classifier has not been initialized.")

  return _model


def get_feature_names():
  """ Return transformed feature names. """

  if _feature_names is None:
    raise RuntimeError("Feature names are not available.")

  return _feature_names