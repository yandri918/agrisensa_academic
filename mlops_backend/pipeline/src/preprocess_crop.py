import os
import pandas as pd
from sklearn.model_selection import train_test_split
import yaml

def preprocess():
    # Load parameters
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
        
    raw_path = params["crop_data"]["raw_path"]
    processed_dir = params["crop_data"]["processed_dir"]
    test_size = params["crop_data"]["test_size"]
    random_state = params["base"]["random_state"]
    
    print(f"Loading raw data from: {raw_path}")
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_path}")
        
    df = pd.read_csv(raw_path)
    print(f"Loaded dataset of shape: {df.shape}")
    
    df = df.dropna()
    
    # Train-test split
    train_df, test_df = train_test_split(
        df, 
        test_size=test_size, 
        random_state=random_state,
        stratify=df['label']
    )
    
    # Save processed data
    os.makedirs(processed_dir, exist_ok=True)
    train_path = os.path.join(processed_dir, "train_crop.csv")
    test_path = os.path.join(processed_dir, "test_crop.csv")
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"Train data saved to: {train_path} (shape: {train_df.shape})")
    print(f"Test data saved to: {test_path} (shape: {test_df.shape})")

if __name__ == "__main__":
    preprocess()
