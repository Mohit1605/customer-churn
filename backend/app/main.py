from fastapi import FastAPI
from app.core.model import load_model
from app.core.shap_loader import load_shap
import app.api.health as health_router
import app.api.prediction as predict_router

app = FastAPI(title="Chustomer Churn",version="2.0.0")


@app.on_event("startup")
def startup_event():
  load_model()
  load_shap()

app.include_router(health_router.router)
app.include_router(predict_router.router)
