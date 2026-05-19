from sklearn.naive_bayes import GaussianNB
from utils import load_processed_data, prepare_features, evaluate_model, save_artifact

def run_naive_bayes(save_model=True):
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, y_train, X_test, y_test = prepare_features(train_df, test_df)

    # Initialize Gaussian Naive Bayes
    nb_model = GaussianNB()

    # Train model
    nb_model.fit(X_train, y_train)

    # Predict
    y_pred = nb_model.predict(X_test)

    # Evaluation
    evaluate_model(y_test, y_pred, "Naive Bayes")

    if save_model:
        save_artifact(nb_model, "naive_bayes_model.joblib")

    return nb_model

if __name__ == "__main__":
    run_naive_bayes()
