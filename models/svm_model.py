from sklearn.svm import SVC
from utils import load_processed_data, prepare_features, evaluate_model, save_artifact

def run_svm_inventory(save_model=True):
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, y_train, X_test, y_test = prepare_features(train_df, test_df)

    # Initialize Support Vector Classifier
    # We use a radial basis function (RBF) kernel as a good default
    svm_model = SVC(kernel='rbf', probability=True, random_state=42)

    # Train model
    svm_model.fit(X_train, y_train)

    # Predict
    y_pred = svm_model.predict(X_test)

    # Evaluation
    evaluate_model(y_test, y_pred, "Support Vector Machine")

    if save_model:
        save_artifact(svm_model, "svm_model.joblib")

    return svm_model

if __name__ == "__main__":
    run_svm_inventory()
