import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from utils import load_processed_data, prepare_features, evaluate_model, save_artifact

def optimize_random_forest(save_model=True):
    """
    Optimizes Random Forest hyperparameters using GridSearchCV.
    Tests different combinations of n_estimators, max_depth, and min_samples_split.
    """
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, y_train, X_test, y_test = prepare_features(train_df, test_df)

    print("Starting Random Forest Hyperparameter Optimization...")
    print("This may take several minutes depending on hardware...\n")

    # Define hyperparameter grid
    param_grid = {
        'n_estimators': [50, 100, 150, 200],          # Number of trees
        'max_depth': [10, 15, 20, 25],                # Tree depth
        'min_samples_split': [2, 5, 10],              # Min samples to split
        'min_samples_leaf': [1, 2, 4],                # Min samples at leaf
    }

    # Create base Random Forest classifier
    rf_base = RandomForestClassifier(random_state=42, n_jobs=-1, warm_start=False)

    # Perform Grid Search with 5-fold cross-validation
    grid_search = GridSearchCV(
        estimator=rf_base,
        param_grid=param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        verbose=2
    )

    print("Grid Search Configuration:")
    print(f"Total combinations to test: {len(param_grid['n_estimators']) * len(param_grid['max_depth']) * len(param_grid['min_samples_split']) * len(param_grid['min_samples_leaf'])}")
    print(f"Cross-validation folds: 5\n")

    # Fit the grid search
    grid_search.fit(X_train, y_train)

    # Print results
    print("\n" + "="*70)
    print("GRID SEARCH RESULTS")
    print("="*70)
    print(f"\nBest Parameters: {grid_search.best_params_}")
    print(f"Best Cross-Validation Accuracy: {grid_search.best_score_:.4f}\n")

    # Evaluate best model on test set
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)

    print(f"Test Set Accuracy with Best Model: {test_accuracy:.4f}\n")
    evaluate_model(y_test, y_pred, "Optimized Random Forest Ensemble")

    # Feature importance for best model
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nFeature Importance (Optimized Model):")
    print(feature_importance.to_string(index=False))

    # Save top hyperparameter combinations
    results_df = pd.DataFrame(grid_search.cv_results_)
    top_results = results_df[['param_n_estimators', 'param_max_depth', 
                               'param_min_samples_split', 'param_min_samples_leaf',
                               'mean_test_score']].nlargest(10, 'mean_test_score')
    
    print("\n" + "="*70)
    print("TOP 10 HYPERPARAMETER COMBINATIONS")
    print("="*70)
    print(top_results.to_string(index=False))

    # Save models
    if save_model:
        save_artifact(best_model, "random_forest_optimized_model.joblib")
        save_artifact(grid_search, "random_forest_gridsearch.joblib")

    return best_model, grid_search


if __name__ == "__main__":
    optimize_random_forest()
