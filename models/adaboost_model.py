from sklearn.ensemble import AdaBoostClassifier
from utils import load_processed_data, prepare_features, evaluate_model, save_artifact

def run_adaboost_inventory(save_model=True):
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, y_train, X_test, y_test = prepare_features(train_df, test_df)

    # Initialize AdaBoost Classifier
    # By default, it uses DecisionTreeClassifier(max_depth=1) as base estimator
    ada_model = AdaBoostClassifier(n_estimators=50, random_state=42)

    # Train model
    ada_model.fit(X_train, y_train)

    # Predict
    y_pred = ada_model.predict(X_test)

    # Evaluation
    evaluate_model(y_test, y_pred, "AdaBoost")

    if save_model:
        save_artifact(ada_model, "adaboost_model.joblib")

    return ada_model

if __name__ == "__main__":
    run_adaboost_inventory()
