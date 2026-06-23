from data_utils import *
import pandas as pd


def json_to_df(json_input):
    import pandas as pd

    df = pd.DataFrame([json_input])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


"""
Then we feature engineer.
"""



def predict_model(df, model):

    pred = model.predict(df)

    prob = (
        model.predict_proba(df)[:, 1]
        if hasattr(model, "predict_proba")
        else None
    )

    return pred, prob



def df_to_json(json_input, pred, prob=None):

    return {
        "timestamp": json_input["timestamp"],
        "building_id": json_input["building_id"],
        "meter": json_input["meter"],
        "site_id": json_input["site_id"],

        "prediction": float(pred[0]),

        "probability":
            float(prob[0]) if prob is not None else None
    }


def run_pipeline(json_input, model):

    # JSON → DF
    df = json_to_df(json_input)

    # Feature engineering
    df = feature_engineer_energy(df)

    # Predict
    pred, prob = predict_model(df, model)

    # DF → JSON
    return df_to_json(json_input, pred, prob)
