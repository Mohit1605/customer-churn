from fastapi import APIRouter, HTTPException, status
from app.schemas.request import CustomerChurnRequest
from app.schemas.response import CustomerChurnResponse
from app.services.prediction_service import predict_customer_churn
from app.utils.logger import logger


router = APIRouter(prefix="/predict",tags=["Customer Churn Prediction"],)


@router.post("",response_model=CustomerChurnResponse)
def predict(request: CustomerChurnRequest,) -> CustomerChurnResponse:

  logger.info("Prediction API called.")

  try:

    response = predict_customer_churn(request)

    logger.info("Prediction API completed successfully.")

    return response

  except ValueError as e:

    logger.exception("Validation error during prediction.")

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e),)

  except RuntimeError as e:

    logger.exception("Prediction service failed.")

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e),)

  except Exception:

    logger.exception("Unexpected API error.")

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal Server Error",)