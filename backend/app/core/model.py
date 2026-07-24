import joblib
from typing import Any

from app.core.config import MODEL_PATH
from app.utils.logger import logger

_model: Any = None


def load_model() -> Any:
  """ Load the trained model into memory.
      Returns:
        Loaded model object.
  """

  global _model

  if _model is not None:
    logger.info("Model already loaded.")
    return _model

  logger.info("Loading Customer Churn model...")

  try:
    if not MODEL_PATH.exists():
      raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

    if not MODEL_PATH.is_file():
      raise FileNotFoundError(f"Invalid model path: {MODEL_PATH}")

    _model = joblib.load(MODEL_PATH)

    logger.info("Customer Churn model loaded successfully.")

    return _model

  except FileNotFoundError:
        logger.exception("Model file not found.")
        raise

  except Exception as e:
        logger.exception("Failed to load model.")
        raise RuntimeError(f"Unable to load model: {e}") from e


def get_model() -> Any:
  """ Return the loaded model.
      Raises:
        RuntimeError: If the model has not been loaded.
  """

  if _model is None:
    raise RuntimeError("Model has not been loaded. Call load_model() first.")

  return _model