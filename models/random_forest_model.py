import os
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from utils import load_processed_data, prepare_features, evaluate_model, save_artifact, get_project_paths

def main(save_model=True):
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, y_train, X_test, y_test = prepare_features(train_df, test_df)

    # Train Random Forest Ensemble
    # n_estimators: number of trees in the forest (higher = more accurate but slower)
    # max_depth: maximum depth of trees (prevents overfitting)
    # min_samples_split: minimum samples required to split a node
    # min_samples_leaf: minimum samples required at leaf nodes
    # random_state: ensures reproducibility
    # n_jobs: use all available processors for training
    rf_model = RandomForestClassifier(
        n_estimators=100,           # 100 trees in the ensemble
        max_depth=15,               # Allow deeper trees than single decision tree
        min_samples_split=5,        # Minimum samples to split internal node
        min_samples_leaf=2,         # Minimum samples in leaf nodes
        random_state=42,            # Reproducibility
        n_jobs=-1,                  # Use all available processors
        warm_start=False,           # Build whole forest at once
    )
    
    print("Training Random Forest Ensemble with 100 trees...")
    rf_model.fit(X_train, y_train)
    print("Training complete!\n")

    # Evaluate Model
    y_pred = rf_model.predict(X_test)
    accuracy = evaluate_model(y_test, y_pred, "Random Forest Ensemble")

    # Feature Importance Analysis
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nFeature Importance:")
    print(feature_importance.to_string(index=False))

    # Plot Feature Importance
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance['feature'], feature_importance['importance'], color='steelblue')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.title('Random Forest Feature Importance for Inventory Forecasting')
    plt.tight_layout()

    # Save the feature importance visualization
    paths = get_project_paths()
    os.makedirs(paths["docs"], exist_ok=True)
    out_path = os.path.join(paths["docs"], 'random_forest_feature_importance.png')
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"\nSaved feature importance visualization to {out_path}")

    # Plot Tree Count vs Accuracy Insight
    # Shows cumulative performance as more trees are added
    plt.figure(figsize=(10, 6))
    tree_predictions = []
    tree_accuracies = []
    
    # Get predictions from progressively more trees
    for n_trees in range(1, rf_model.n_estimators + 1, 5):
        estimator = RandomForestClassifier(
            n_estimators=n_trees,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        estimator.fit(X_train, y_train)
        from sklearn.metrics import accuracy_score
        y_pred_temp = estimator.predict(X_test)
        acc = accuracy_score(y_test, y_pred_temp)
        tree_accuracies.append(acc)
        tree_predictions.append(n_trees)
    
    plt.plot(tree_predictions, tree_accuracies, marker='o', linewidth=2, markersize=6, color='darkgreen')
    plt.xlabel('Number of Trees in Ensemble')
    plt.ylabel('Accuracy Score')
    plt.title('Random Forest Accuracy vs Number of Trees')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    ensemble_path = os.path.join(paths["docs"], 'random_forest_ensemble_growth.png')
    plt.savefig(ensemble_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved ensemble growth visualization to {ensemble_path}")

    if save_model:
        save_artifact(rf_model, "random_forest_model.joblib")

    return rf_model


if __name__ == '__main__':
    main()
