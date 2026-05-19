import os
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from utils import load_processed_data, prepare_features, get_project_paths

def find_optimal_k(max_k=20):
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, y_train, X_test, y_test = prepare_features(train_df, test_df)

    error_rates = []

    print(f"Testing k values from 1 to {max_k}...")
    for k in range(1, max_k + 1):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)

        # Error rate is 1 - accuracy
        error = 1 - accuracy_score(y_test, y_pred)
        error_rates.append(error)
        print(f"k={k:2d} | Error Rate: {error:.4f}")

    # Plotting the Elbow Curve
    plt.figure(figsize=(10, 6))
    plt.plot(
        range(1, max_k + 1),
        error_rates,
        color="blue",
        linestyle="dashed",
        marker="o",
        markerfacecolor="red",
        markersize=8,
    )
    plt.title("Error Rate vs. k Value")
    plt.xlabel("k")
    plt.ylabel("Error Rate")
    plt.xticks(range(1, max_k + 1))
    plt.grid(True)

    # Save the plot
    paths = get_project_paths()
    plot_path = os.path.join(paths["base"], "models", "knn_elbow_plot.png")
    plt.savefig(plot_path)
    print(f"\nPlot saved to: {plot_path}")
    print("Look for the 'elbow' where the error rate starts to stabilize or increases.")

if __name__ == "__main__":
    find_optimal_k()
