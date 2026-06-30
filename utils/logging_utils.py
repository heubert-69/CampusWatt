import wandb
import os
import numpy as np

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

WANDB_INIT = False

WANDB_KEY = os.getenv("WANDB_API_KEY")


def wandb_login():

    global WANDB_INIT

    if WANDB_INIT:
        return

    wandb.login(key=WANDB_KEY)

    wandb.init(
        project="CampusWatt",
        name="CampusWatt-Inference-Results"
    )

    WANDB_INIT = True

    print("[WANDB] Initialized")


def log_to_wandb(payload):

    global WANDB_INIT

    if not WANDB_INIT:
        print("[WANDB WARNING] init not called, skipping log")
        return

    try:

        y_true = payload.get("Actual", [])
        y_pred = payload.get("Predicted", [])

        mse = (
            float(mean_squared_error(y_true, y_pred))
            if len(y_true) > 0 else 0.0
        )

        rmse = (
            float(np.sqrt(mse))
            if mse > 0 else 0.0
        )

        mae = (
            float(mean_absolute_error(y_true, y_pred))
            if len(y_true) > 0 else 0.0
        )

        r2 = (
            float(r2_score(y_true, y_pred))
            if len(y_true) > 1 else 0.0
        )

        latency = float(
            payload.get("time", 0.0)
        )

        throughput = (
            1 / max(latency / 1000.0, 1e-6)
            if latency > 0 else 0.0
        )

        wandb.log({
            "prediction_id": payload.get("prediction_id"),
            "MSE": mse,
            "RMSE": rmse,
            "MAE": mae,
            "R2": r2,
            "Inference_Time": latency,
            "Throughput": throughput,
            "Prediction_Mean": (
                float(np.mean(y_pred))
                if len(y_pred) > 0 else 0.0
            ),
            "Prediction_STD": (
                float(np.std(y_pred))
                if len(y_pred) > 0 else 0.0
            )
        })

    except Exception as e:

        try:
            wandb.log({
                "error": str(e)
            })
        except Exception:
            pass

        print(f"[WANDB ERROR] {e}")


