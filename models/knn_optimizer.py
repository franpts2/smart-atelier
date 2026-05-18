import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def find_optimal_k(max_k=20):
    # load data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    train_path = os.path.join(base_dir, 'data', 'processed', 'train.csv')
    test_path = os.path.join(base_dir, 'data', 'processed', 'test.csv')
    
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        print("Processed data not found. Please run src/data_preparation.py first.")
        return

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    features = ['original_price', 'current_price', 'Net_Margin', 'brand_encoded', 'category_encoded', 'stock_quantity']
    target = 'stocking_priority'

    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]

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
    plt.plot(range(1, max_k + 1), error_rates, color='blue', linestyle='dashed', marker='o',
             markerfacecolor='red', markersize=8)
    plt.title('Error Rate vs. k Value')
    plt.xlabel('k')
    plt.ylabel('Error Rate')
    plt.xticks(range(1, max_k + 1))
    plt.grid(True)
    
    # Save the plot
    plot_path = os.path.join(base_dir, 'models', 'knn_elbow_plot.png')
    plt.savefig(plot_path)
    print(f"\nPlot saved to: {plot_path}")
    print("Look for the 'elbow' where the error rate starts to stabilize or increases.")

if __name__ == "__main__":
    find_optimal_k()