from typing import Literal
from pydantic import BaseModel, Field


class CustomerChurnResponse(BaseModel):
  """ Customer Churn Prediction Response Schema """
  prediction: Literal["Churn", "No Churn"] = Field(...,description="Predicted customer churn status.")

  prediction_probability: float = Field(...,ge=0.0,le=1.0,description="Probability of the predicted class.")

  confidence: Literal["Low", "Medium", "High"] = Field(...,description="Confidence level based on prediction probability.")

  message: str = Field(...,description="Response message.")