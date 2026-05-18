import pandas as pd
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score


def run_knn_inventory(k=5):

    # load processed data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    train_path = os.path.join(base_dir, "data", "processed", "train.csv")
    test_path = os.path.join(base_dir, "data", "processed", "test.csv")

    if not os.path.exists(train_path) or not os.path.exists(test_path):
        print("Processed data not found. Please run src/data_preparation.py first.")
        return

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    features = [
        "original_price",
        "current_price",
        "Net_Margin",
        "brand_encoded",
        "category_encoded",
        "stock_quantity",
    ]
    target = "stocking_priority"

    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]

    # k-NN
    # for any item in the test set, algo calculates the distance (Euclidian)
    # to all items in the training set.
    # it then finds the 'k' closest neighbors
    # the predicted priority is the majority priority among these neighbors
    knn = KNeighborsClassifier(n_neighbors=k)

    # train model
    knn.fit(X_train, y_train)

    # predict priotities
    y_pred = knn.predict(X_test)

    # evaluation
    accuracy = accuracy_score(y_test, y_pred)
    print(f"--- k-NN Inventory Grouping (k={k}) ---\n")
    print(f"Overall Accuracy: {accuracy:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return knn

if __name__ == "__main__":
    run_knn_inventory()