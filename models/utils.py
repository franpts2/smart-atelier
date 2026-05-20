import pandas as pd
import os
import joblib
from sklearn.metrics import classification_report, accuracy_score

def get_project_paths():
    """Returns essential project directory paths."""
    # We use the location of this file to find the root of the project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data", "processed")
    artifacts_dir = os.path.join(base_dir, "models", "artifacts")
    docs_dir = os.path.join(base_dir, "docs")
    
    return {
        "base": base_dir,
        "train": os.path.join(data_dir, "train.csv"),
        "test": os.path.join(data_dir, "test.csv"),
        "artifacts": artifacts_dir,
        "docs": docs_dir
    }

def load_processed_data():
    """Loads the processed train and test datasets."""
    paths = get_project_paths()
    
    if not os.path.exists(paths["train"]) or not os.path.exists(paths["test"]):
        raise FileNotFoundError("Processed data not found. Please run src/data_preparation.py first.")
        
    train_df = pd.read_csv(paths["train"])
    test_df = pd.read_csv(paths["test"])
    return train_df, test_df

def prepare_features(train_df, test_df, target_col='stocking_priority'):
    """Isolates the encoded features and target for training."""
    # Centralized list of features used across all models
    features = [
        "original_price",
        "current_price",
        "Net_Margin",
        "brand_encoded",
        "category_encoded",
        "stock_quantity",
    ]
    if target_col == "stocking_priority_advanced":
        features.append("units_sold")

    X_train = train_df[features]
    y_train = train_df[target_col]
    X_test = test_df[features]
    y_test = test_df[target_col]

    return X_train, y_train, X_test, y_test

def evaluate_model(y_test, y_pred, model_name):
    """Prints standard classification metrics."""
    accuracy = accuracy_score(y_test, y_pred)
    print(f"--- {model_name} Inventory Classification ---\n")
    print(f"Overall Accuracy: {accuracy:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    return accuracy

def save_artifact(obj, filename):
    """Saves a joblib artifact to the models/artifacts directory."""
    paths = get_project_paths()
    os.makedirs(paths["artifacts"], exist_ok=True)
    save_path = os.path.join(paths["artifacts"], filename)
    joblib.dump(obj, save_path)
    print(f"Artifact saved to: {save_path}")
    return save_path
