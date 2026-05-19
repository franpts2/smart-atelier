import os
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from utils import load_processed_data, prepare_features, evaluate_model, save_artifact, get_project_paths

def main(save_model=True):
    try:
        train_df, test_df = load_processed_data()
    except FileNotFoundError as e:
        print(e)
        return

    X_train, y_train, X_test, y_test = prepare_features(train_df, test_df)

    # Train Decision Tree
    dt_model = DecisionTreeClassifier(max_depth=4, random_state=42)
    dt_model.fit(X_train, y_train)

    # Evaluate Model
    y_pred = dt_model.predict(X_test)
    evaluate_model(y_test, y_pred, "Decision Tree")

    # Plot Tree Logic
    plt.figure(figsize=(20, 10))
    class_names = [str(c) for c in dt_model.classes_]
    plot_tree(dt_model, 
              feature_names=X_train.columns.tolist(), 
              class_names=class_names, 
              filled=True, 
              rounded=True,
              fontsize=10)

    # Save the output diagram
    paths = get_project_paths()
    os.makedirs(paths["docs"], exist_ok=True)
    out_path = os.path.join(paths["docs"], 'decision_tree_logic.png')
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Saved Decision Tree logic visualization to {out_path}")

    if save_model:
        save_artifact(dt_model, "decision_tree_model.joblib")

    return dt_model

if __name__ == '__main__':
    main()
