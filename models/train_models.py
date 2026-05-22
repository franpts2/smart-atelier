import sys
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier

# Add parent directory to path so we can import from models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import load_processed_data, prepare_features, evaluate_model, save_artifact

models_config = [
    {
        "name": "knn",
        "label": "K-Nearest Neighbors (k=15)",
        "clf": lambda: KNeighborsClassifier(n_neighbors=15)
    },
    {
        "name": "decision_tree",
        "label": "Decision Tree",
        "clf": lambda: DecisionTreeClassifier(max_depth=4, random_state=42)
    },
    {
        "name": "naive_bayes",
        "label": "Naive Bayes",
        "clf": lambda: GaussianNB()
    },
    {
        "name": "svm",
        "label": "Support Vector Machine",
        "clf": lambda: SVC(kernel='rbf', probability=True, random_state=42)
    },
    {
        "name": "adaboost",
        "label": "AdaBoost",
        "clf": lambda: AdaBoostClassifier(n_estimators=50, random_state=42)
    },
    {
        "name": "neural_network",
        "label": "Neural Network (MLP)",
        "clf": lambda: MLPClassifier(
            hidden_layer_sizes=(64, 32),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=42
        )
    }
]

def train_all(save_models=True):
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    for config in models_config:
        name = config["name"]
        label = config["label"]

        # === 1. Train Standard Model ===
        print(f"\n=========================================")
        print(f"Training STANDARD model: {label}")
        print(f"=========================================")
        X_train_std, y_train_std, X_test_std, y_test_std = prepare_features(
            train_df, test_df, target_col="stocking_priority"
        )
        clf_std = config["clf"]()
        clf_std.fit(X_train_std, y_train_std)
        
        y_pred_std = clf_std.predict(X_test_std)
        evaluate_model(y_test_std, y_pred_std, f"Standard {label}")
        
        if save_models:
            save_artifact(clf_std, f"{name}_model.joblib")

        # === 2. Train Advanced Model ===
        print(f"\n=========================================")
        print(f"Training ADVANCED model: {label}")
        print(f"=========================================")
        X_train_adv, y_train_adv, X_test_adv, y_test_adv = prepare_features(
            train_df, test_df, target_col="stocking_priority_advanced"
        )
        clf_adv = config["clf"]()
        clf_adv.fit(X_train_adv, y_train_adv)
        
        y_pred_adv = clf_adv.predict(X_test_adv)
        evaluate_model(y_test_adv, y_pred_adv, f"Advanced {label}")
        
        if save_models:
            save_artifact(clf_adv, f"{name}_advanced_model.joblib")

if __name__ == "__main__":
    train_all()
