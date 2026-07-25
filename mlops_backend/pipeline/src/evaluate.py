import os
import json
import pandas as pd
import yaml
import joblib
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import mlflow

def evaluate():
    # Load parameters
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
        
    processed_dir = params["data"]["processed_dir"]
    model_path = params["train"]["model_path"]
    metrics_path = params["evaluate"]["metrics_path"]
    
    # Load test data
    test_path = os.path.join(processed_dir, "test.csv")
    print(f"Loading test data from: {test_path}")
    test_df = pd.read_csv(test_path)
    
    X_test = test_df.drop(columns=["Value"])
    y_test = test_df["Value"]
    
    # Load model
    print(f"Loading model from: {model_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    model = joblib.load(model_path)
    
    # Predict
    print("Evaluating model...")
    predictions = model.predict(X_test)
    
    # Metrics
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)
    
    metrics = {
        "mse": float(mse),
        "rmse": float(rmse),
        "r2_score": float(r2)
    }
    
    print(f"Evaluation Metrics: {metrics}")
    
    # Save metrics to JSON file (for DVC metric tracking)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to: {metrics_path}")
    
    # Log metrics to MLflow if run is active
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
    if mlflow_uri:
        mlflow.set_tracking_uri(mlflow_uri)
    
    mlflow.set_experiment("AgriSensa_Yield_Training_Pipeline")
    
    # If this is run via DVC, there might not be an active MLflow run in this process,
    # so we start/resume run or log it. DVC executes scripts as separate processes.
    # To attach metrics to the same experiment run, we can log them or start a new run.
    with mlflow.start_run(run_name="DVC_Evaluation_Run") as run:
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(metrics_path)
        print("Metrics and artifacts logged to MLflow.")

if __name__ == "__main__":
    evaluate()
