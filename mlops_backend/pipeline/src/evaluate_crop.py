import os
import json
import pandas as pd
import yaml
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow

def evaluate():
    # Load parameters
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
        
    processed_dir = params["crop_data"]["processed_dir"]
    model_path = params["crop_train"]["model_path"]
    metrics_path = params["crop_evaluate"]["metrics_path"]
    
    # Load test data
    test_path = os.path.join(processed_dir, "test_crop.csv")
    print(f"Loading test data from: {test_path}")
    test_df = pd.read_csv(test_path)
    
    X_test = test_df.drop(columns=["label"])
    y_test = test_df["label"]
    
    # Load model artifact
    print(f"Loading model from: {model_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
        
    model_artifact = joblib.load(model_path)
    model = model_artifact["model"]
    le = model_artifact["label_encoder"]
    
    # Encode test target
    y_test_encoded = le.transform(y_test)
    
    # Predict
    print("Evaluating model...")
    predictions = model.predict(X_test)
    
    # Metrics
    accuracy = accuracy_score(y_test_encoded, predictions)
    precision = precision_score(y_test_encoded, predictions, average='weighted')
    recall = recall_score(y_test_encoded, predictions, average='weighted')
    f1 = f1_score(y_test_encoded, predictions, average='weighted')
    
    metrics = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
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
    
    mlflow.set_experiment("AgriSensa_Crop_Training_Pipeline")
    
    with mlflow.start_run(run_name="DVC_Crop_Evaluation_Run") as run:
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(metrics_path)
        print("Metrics and artifacts logged to MLflow.")

if __name__ == "__main__":
    evaluate()
