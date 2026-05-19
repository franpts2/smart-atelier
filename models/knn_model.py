from sklearn.neighbors import KNeighborsClassifier
from utils import load_processed_data, prepare_features, evaluate_model, save_artifact

def run_knn_inventory(k=15, save_model=True):
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, y_train, X_test, y_test = prepare_features(train_df, test_df)

    # k-NN
    knn = KNeighborsClassifier(n_neighbors=k)

    # train model
    knn.fit(X_train, y_train)

    # predict
    y_pred = knn.predict(X_test)

    # evaluation
    evaluate_model(y_test, y_pred, f"k-NN (k={k})")

    if save_model:
        save_artifact(knn, "knn_model.joblib")

    return knn

if __name__ == "__main__":
    run_knn_inventory()
