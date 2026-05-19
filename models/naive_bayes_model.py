import pandas as pd
import os
import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, accuracy_score

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    train_path = os.path.join(base_dir, "data", "processed", "train.csv")
    test_path = os.path.join(base_dir, "data", "processed", "test.csv")
    
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        raise FileNotFoundError("Processed data not found. Please run src/data_preparation.py first.")
        
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df

def prepare_features(train_df, test_df, target_col='stocking_priority'):
    """Isolates the encoded features and target for training."""
    features = [
        "original_price",
        "current_price",
        "Net_Margin",
        "brand_encoded",
        "category_encoded",
        "stock_quantity",
    ]

    X_train = train_df[features]
    y_train = train_df[target_col]
    X_test = test_df[features]
    y_test = test_df[target_col]

    return X_train, X_test, y_train, y_test

def run_naive_bayes(save_model=True):
    try:
        train_df, test_df = load_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, X_test, y_train, y_test = prepare_features(train_df, test_df)

    # Initialize Gaussian Naive Bayes
    nb_model = GaussianNB()

    # Train model
    nb_model.fit(X_train, y_train)

    # Predict
    y_pred = nb_model.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    print("--- Naive Bayes Inventory Classification ---\n")
    print(f"Overall Accuracy: {accuracy:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    if save_model:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        artifacts_dir = os.path.join(base_dir, "models", "artifacts")
        os.makedirs(artifacts_dir, exist_ok=True)
        model_path = os.path.join(artifacts_dir, "naive_bayes_model.joblib")
        joblib.dump(nb_model, model_path)
        print(f"Model saved to: {model_path}")

    return nb_model

if __name__ == "__main__":
    run_naive_bayes()
