import os
import pandas as pd
import yaml
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import mlflow
import mlflow.sklearn

def train():
    # Load parameters
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
        
    processed_dir = params["crop_data"]["processed_dir"]
    random_state = params["base"]["random_state"]
    n_estimators = params["crop_train"]["n_estimators"]
    max_depth = params["crop_train"]["max_depth"]
    model_dir = params["crop_train"]["model_dir"]
    model_path = params["crop_train"]["model_path"]
    
    # Load training data
    train_path = os.path.join(processed_dir, "train_crop.csv")
    print(f"Loading training data from: {train_path}")
    train_df = pd.read_csv(train_path)
    
    X_train = train_df.drop(columns=["label"])
    y_train = train_df["label"]
    
    # Setup MLflow
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
    if mlflow_uri:
        mlflow.set_tracking_uri(mlflow_uri)
        print(f"MLflow Tracking Server configured: {mlflow_uri}")
    else:
        print("MLflow Tracking Server not configured. Logging locally.")
        
    mlflow.set_experiment("AgriSensa_Crop_Training_Pipeline")
    
    with mlflow.start_run(run_name="DVC_Crop_Pipeline_Run") as run:
        print(f"Starting MLflow Run: {run.info.run_id}")
        
        # Log parameters
        mlflow.log_param("estimator", "RandomForestClassifier")
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)
        
        # Encode target
        le = LabelEncoder()
        y_train_encoded = le.fit_transform(y_train)
        
        # Train model
        print("Training model...")
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
        model.fit(X_train, y_train_encoded)
        
        # Save model locally (including LabelEncoder into a pipeline or wrapping it)
        # Since we just have the model, we can save both or use a scikit-learn Pipeline
        from sklearn.pipeline import Pipeline
        # To avoid issues, we will just save the model and label encoder together as a dictionary
        model_artifact = {
            "model": model,
            "label_encoder": le
        }
        
        os.makedirs(model_dir, exist_ok=True)
        joblib.dump(model_artifact, model_path)
        print(f"Model and Label Encoder saved locally to: {model_path}")
        
        # Log model to MLflow (as pyfunc or sklearn)
        signature = mlflow.models.infer_signature(X_train.head(5), model.predict(X_train.head(5)))
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            signature=signature
        )
        print("Model logged to MLflow successfully.")

if __name__ == "__main__":
    train()
