import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import os
import joblib

def load_data():
    """Loads the processed train and test datasets."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    train_path = os.path.join(base_dir, "data", "processed", "train.csv")
    test_path = os.path.join(base_dir, "data", "processed", "test.csv")
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    return train_df, test_df

def prepare_features(train_df, test_df, target_col='stocking_priority'):
    """Isolates the encoded features and target for training."""
    # Use the same features as KNN for consistency
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

def main(save_model=True):
    train_df, test_df = load_data()
    X_train, X_test, y_train, y_test = prepare_features(train_df, test_df)

    # Train Decision Tree
    # Setting max_depth restricts the tree from growing too complex, maintaining readability
    dt_model = DecisionTreeClassifier(max_depth=4, random_state=42)
    dt_model.fit(X_train, y_train)

    # Evaluate Model
    y_pred = dt_model.predict(X_test)

    print("--- Decision Tree Inventory Logic ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Plot Tree Logic
    plt.figure(figsize=(20, 10))
    class_names = [str(c) for c in dt_model.classes_]
    plot_tree(dt_model, 
              feature_names=X_train.columns.tolist(), 
              class_names=class_names, 
              filled=True, 
              rounded=True,
              fontsize=10)

    # Save the output diagram
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(base_dir, 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    out_path = os.path.join(docs_dir, 'decision_tree_logic.png')
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Saved Decision Tree logic visualization to {out_path}")

    if save_model:
        artifacts_dir = os.path.join(base_dir, "models", "artifacts")
        os.makedirs(artifacts_dir, exist_ok=True)
        model_path = os.path.join(artifacts_dir, "decision_tree_model.joblib")
        joblib.dump(dt_model, model_path)
        print(f"Model saved to: {model_path}")

    return dt_model

if __name__ == '__main__':
    main()