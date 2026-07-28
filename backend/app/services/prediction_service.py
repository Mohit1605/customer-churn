from typing import Literal
import pandas as pd
from app.core.model import get_model
from app.schemas.request import CustomerChurnRequest
from app.schemas.response import CustomerChurnResponse
from app.utils.logger import logger
from app.services.shap_services import generate_explanation
from app.core.shap_loader import get_classifier, get_preprocessor

SENIOR_CITIZEN_MAP = {
    "No": 0,
    "Yes": 1,
}
PREDICTION_MAP: dict[int, Literal["No Churn", "Churn"]] = {
    0: "No Churn",
    1: "Churn",
}


def create_features(df: pd.DataFrame) -> pd.DataFrame:
  """ Create additional features required by the ML pipeline. """

  internet_services = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
  ]

  df = df.copy()

  df["ServiceCount"] = (df[internet_services].eq("Yes").sum(axis=1))

  df["IsNewCustomer"] = (
        df["tenure"] <= 12
    ).astype(int)

  return df


def _calculate_confidence(probability: float) -> str:
  """ Convert probability into a confidence level. """

  if probability >= 0.80:
    return "High"

  if probability >= 0.60:
    return "Medium"

  return "Low"


def predict_customer_churn(request: CustomerChurnRequest,) -> CustomerChurnResponse:
  """ Predict customer churn.
      Parameters
      ----------
      request : CustomerChurnRequest
      
      Returns
      -------
      CustomerChurnResponse
  """

  logger.info("Received prediction request.")

  try:

    model = get_model()

    data = request.model_dump()

    data["SeniorCitizen"] = SENIOR_CITIZEN_MAP[data["SeniorCitizen"]]

    df = pd.DataFrame([data])

    df = create_features(df)
    # logger.info("Data",df)
    logger.info("Running prediction...")

    preprocessor = get_preprocessor()

    classifier = get_classifier()

    encoded_customer  = preprocessor.transform(df)

    prediction = int(classifier.predict(encoded_customer )[0])

    probability = float(classifier.predict_proba(encoded_customer )[0][1])

    top_features = generate_explanation(transformed_customer=encoded_customer,original_customer=df,)

    prediction_label = PREDICTION_MAP.get(prediction, "Unknown")

    confidence = _calculate_confidence(probability)

    logger.info("Prediction completed successfully.")

    return CustomerChurnResponse(
        prediction=prediction_label,
        prediction_probability=round(probability, 4),
        confidence=confidence,
        top_features=top_features,
        message="Prediction generated successfully."
    )

  except KeyError as e:
    logger.exception("Failed during feature mapping.")

    raise ValueError(f"Invalid input value: {e}") from e

  except ValueError:
    logger.exception("Validation error during prediction.")
    raise

  except Exception as e:
    logger.exception("Unexpected error during prediction.")

    raise RuntimeError("Prediction failed.") from e