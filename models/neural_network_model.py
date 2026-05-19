from sklearn.neural_network import MLPClassifier
from utils import load_processed_data, prepare_features, evaluate_model, save_artifact

def run_neural_network_inventory(save_model=True):
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, y_train, X_test, y_test = prepare_features(train_df, test_df)

    # Initialize Multi-Layer Perceptron (Neural Network)
    # hidden_layer_sizes=(64, 32) creates two hidden layers
    # 'relu' is the standard activation function for deep learning
    # 'adam' is a robust optimizer for smaller datasets
    nn_model = MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation='relu',
        solver='adam',
        max_iter=500,
        random_state=42
    )

    # Train model
    print("Training Neural Network (this may take a few seconds)...")
    nn_model.fit(X_train, y_train)

    # Predict
    y_pred = nn_model.predict(X_test)

    # Evaluation
    evaluate_model(y_test, y_pred, "Neural Network (MLP)")

    if save_model:
        save_artifact(nn_model, "neural_network_model.joblib")

    return nn_model

if __name__ == "__main__":
    run_neural_network_inventory()
