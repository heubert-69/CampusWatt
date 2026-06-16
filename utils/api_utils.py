from fastapi import FastAPI
from fastapi.middlewar.cors import CORSMiddleware
import joblib
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from db_utils import init_db


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

#model = joblib.load("models/MODEL_NAME")

@app.get("/predict", methods=["POST"])
def predict(X):
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)[:, 1]


    pred_df = pd.DataFrame({
        "Prediction": y_pred,
        "Probability": y_prob
    })

    return pred_df


@app.get("/causal_predict", methods=["POST"])
def causal_predict(X):
    #causal_model = joblib.load("causal_models/MODEL_NAME") #placeholder. working on the actual model

    preds = causal_model.predict(X)

    causal_df = pd.DataFrame({
        "P_value": causal_model.p_value,
        "Residuals": causal_model.residuals
    })

    return causal_df

@app.get("/login", methods=["GET"])
def login(username, password):
    password_hash = user_retrieval(username, password)

    valid = check_password_hash(username, password_hash)

    if is_valid:
        return {"status": "success", "message": "Authenticated successfully. Generate API Token here."}
    else:
        return {"status": "error", "message": "Invalid credentials."}, 401


#all for now
