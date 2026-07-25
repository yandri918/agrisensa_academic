import os
import json
import pandas as pd
import yaml
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow

def evaluate():
    # Load parameters
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
        
    processed_dir = params["price_data"]["processed_dir"]
    model_path = params["price_train"]["model_path"]
    metrics_path = params["price_evaluate"]["metrics_path"]
    
    # Load test data
    test_path = os.path.join(processed_dir, "test_price.csv")
    print(f"Loading test data from: {test_path}")
    test_df = pd.read_csv(test_path)
    
    X_test = test_df.drop(columns=["harga"])
    y_test = test_df["harga"]
    
    # Load model artifact
    print(f"Loading model from: {model_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
        
    model = joblib.load(model_path)
    
    # Predict
    print("Evaluating model...")
    predictions = model.predict(X_test)
    
    # Metrics
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    r2 = r2_score(y_test, predictions)
    
    metrics = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2)
    }
    
    print(f"Evaluation Metrics: {metrics}")
    
    # Save metrics to JSON file
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to: {metrics_path}")
    
    # Log metrics to MLflow
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
    if mlflow_uri:
        mlflow.set_tracking_uri(mlflow_uri)
    
    mlflow.set_experiment("AgriSensa_Price_Training_Pipeline")
    
    with mlflow.start_run(run_name="DVC_Price_Evaluation_Run") as run:
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(metrics_path)
        print("Metrics and artifacts logged to MLflow.")

if __name__ == "__main__":
    evaluate()
