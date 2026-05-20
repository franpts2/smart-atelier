import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

from utils import load_processed_data, prepare_features, get_project_paths


MODEL_ARTIFACTS = {
    "Decision Tree": "decision_tree_model.joblib",
    "k-NN": "knn_model.joblib",
    "Naive Bayes": "naive_bayes_model.joblib",
    "Random Forest": "random_forest_model.joblib",
    "Random Forest (Optimized)": "random_forest_optimized_model.joblib",
    "SVM": "svm_model.joblib",
    "Neural Network": "neural_network_model.joblib",
    "AdaBoost": "adaboost_model.joblib",
}


def _safe_rate(numerator, denominator):
    return 0.0 if denominator == 0 else numerator / denominator


def evaluate_all_models():
    train_df, test_df = load_processed_data()
    _, _, X_test, y_test = prepare_features(train_df, test_df)

    labels = ["High Stock", "Low Stock", "Maintain"]

    paths = get_project_paths()
    artifacts_dir = paths["artifacts"]
    docs_dir = paths["docs"]
    os.makedirs(docs_dir, exist_ok=True)

    rows = []

    for model_name, artifact_name in MODEL_ARTIFACTS.items():
        artifact_path = os.path.join(artifacts_dir, artifact_name)

        if not os.path.exists(artifact_path):
            print(f"Skipping {model_name}: artifact not found at {artifact_path}")
            continue

        model = joblib.load(artifact_path)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred, labels=labels)

        high_idx = labels.index("High Stock")
        low_idx = labels.index("Low Stock")

        high_to_low = int(cm[high_idx, low_idx])
        low_to_high = int(cm[low_idx, high_idx])

        total_high_true = int(cm[high_idx, :].sum())
        total_low_true = int(cm[low_idx, :].sum())

        rows.append(
            {
                "Model": model_name,
                "Accuracy": round(acc, 4),
                "High->Low": high_to_low,
                "Low->High": low_to_high,
                "High->Low Rate": round(_safe_rate(high_to_low, total_high_true), 4),
                "Low->High Rate": round(_safe_rate(low_to_high, total_low_true), 4),
            }
        )

        plt.figure(figsize=(6.5, 5.5))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
        disp.plot(cmap="Blues", values_format="d", colorbar=False)
        plt.title(f"{model_name} Confusion Matrix")
        plt.tight_layout()

        filename = model_name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        cm_path = os.path.join(docs_dir, f"confusion_matrix_{filename}.png")
        plt.savefig(cm_path, dpi=300, bbox_inches="tight")
        plt.close()

    if not rows:
        print("No model artifacts found to evaluate.")
        return

    comparison_df = pd.DataFrame(rows).sort_values(by="Accuracy", ascending=False)

    csv_path = os.path.join(docs_dir, "model_comparison_metrics.csv")
    comparison_df.to_csv(csv_path, index=False)

    print("\n=== Model Comparison Metrics ===")
    print(comparison_df.to_string(index=False))
    print(f"\nSaved metrics table to: {csv_path}")
    print(f"Saved confusion matrices to: {docs_dir}")


if __name__ == "__main__":
    evaluate_all_models()
