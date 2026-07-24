from typing import Literal
from pydantic import BaseModel, Field


class CustomerChurnRequest(BaseModel):
  """ Customer Churn Prediction Request Schema """

  gender: Literal["Male", "Female"] = Field(...,description="Customer gender")

  SeniorCitizen: Literal["Yes", "No"] = Field(...,description="Whether the customer is a senior citizen")

  Partner: Literal["Yes", "No"] = Field(...,description="Whether the customer has a partner")

  Dependents: Literal["Yes", "No"] = Field(...,description="Whether the customer has dependents")

  tenure: int = Field(...,ge=0,le=100,description="Customer tenure in months")

  Contract: Literal["Month-to-month","One year","Two year"] = Field(...,description="Customer contract type")

  PaperlessBilling: Literal["Yes", "No"] = Field(...,description="Paperless billing enabled")

  PaymentMethod: Literal["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"] = Field(...,description="Payment method")

  MonthlyCharges: float = Field(...,ge=0,description="Monthly bill amount")

  TotalCharges: float = Field(...,ge=0,description="Total amount charged")

  PhoneService: Literal["Yes", "No"] = Field(...,description="Phone service subscription")

  MultipleLines: Literal["Yes","No","No phone service"] = Field(...,description="Multiple phone lines")

  InternetService: Literal["DSL","Fiber optic","No"] = Field(...,description="Internet service type")

  OnlineSecurity: Literal["Yes","No","No internet service"] = Field(...,description="Online security service")

  OnlineBackup: Literal["Yes","No","No internet service"] = Field(...,description="Online backup service")

  DeviceProtection: Literal["Yes","No","No internet service"] = Field(...,description="Device protection service")

  TechSupport: Literal["Yes","No","No internet service"] = Field(...,description="Technical support service")

  StreamingTV: Literal["Yes","No","No internet service"] = Field(...,description="Streaming TV service")

  StreamingMovies: Literal["Yes","No","No internet service"] = Field(...,description="Streaming Movies service")