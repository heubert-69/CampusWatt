from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from werkzeug.security import check_password_hash
import joblib
import pandas as pd
from pathlib import Path
import jwt
from datetime import datetime, timedelta
import datetime
from data_utils import *
from db_utils import *
from input_utils import *
import time
import asyncio


app = FastAPI()

origins = ["*"]  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#For Protection
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

auth_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):

    try:
        decoded = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return decoded

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )



#General Utils
model = joblib.load("models/rfr_model.pkl")
#causal_model = joblib.load("models/causal_models/model.pkl") //later

print(model.feature_names_in_)

@app.post("/predict")
async def predict(request: PredictionRequest, user=Depends(verify_token)):
    start_time = time.perf_counter()
    # JSON → DF
    df = pd.DataFrame([request.model_dump()])
    #df["timestamp"] = pd.to_datetime(df["timestamp"]) // not required due to the datetime being the index of the data

    #df = feature_engineer_energy(df) //will be restored, i promise.

    # Prediction
    y_pred = model.predict(df)

    y_prob = (
        model.predict_proba(df)[:, 1]
        if hasattr(model, "predict_proba")
        else None
    )
    end_time = time.perf_counter()

    inference_time_ms = (
        end_time - start_time
    ) * 1000

    prediction_value = float(y_pred[0])

    response = {
        "prediction": prediction_value,
        "probability": None
    }

    await save_prediction_result(
        model_name="rfr.pkl",
        input_data=request.model_dump(mode="json"),
        prediction_output=response,
        explanation="Random Forest Energy Forecast",
        confidence_score=None,
        inference_time_ms=int(inference_time_ms)
    )

    return response


@app.post("/causal_predict")
def causal_predict(request: PredictionRequest, user=Depends(verify_token)):

    df = pd.DataFrame([request.model_dump()])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # causal model may depend on same engineered features
    df = feature_engineer_energy(df)

    if "causal_model" not in globals() or causal_model is None:
        raise HTTPException(
            status_code=500,
            detail="Causal model not loaded"
        )

    preds = causal_model.predict(df)

    return {
        "causal_prediction": float(preds[0]),
        "p_value": getattr(causal_model, "p_value", None),
        "residuals": getattr(causal_model, "residuals", None)
    }

@app.post("/login")
async def login(request: LoginRequest):

    user_record = await user_retrieval(
        request.username
    )

    if not user_record:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    password_hash = user_record["password_hash"]

    valid = check_password_hash(
        password_hash,
        request.password
    )

    if not valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_token({
        "username": request.username
    })

    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer"
    }

#all for now
