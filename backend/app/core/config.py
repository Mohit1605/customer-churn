from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODELS_DIR = BASE_DIR / "models"


MODEL_FILENAME = "customer_churn_pipeline.pkl"
MODEL_PATH = MODELS_DIR / MODEL_FILENAME

SHAP_BACKGROUND_PATH = MODELS_DIR / "shap_background.pkl"