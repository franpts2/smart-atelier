import os
import sys
import joblib
import pandas as pd

# This is the path to the root of our project.
# We use it to find the 'models' folder no matter where we run this script from.
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MLService:
    """
    This service handles everything related to our Machine Learning model.
    It loads the pre-trained model and uses it to make predictions.
    """

    def __init__(self):
        # We initialize these as None and load them later in load_artifacts()
        self.model = None  # The trained KNN model
        self.scaler = None  # Used to scale numerical data (normalization)
        self.brand_map = None  # Dictionary to convert brand names to numbers
        self.category_map = None  # Dictionary to convert category names to numbers


    def load_artifacts(self):
        """
        Loads the .joblib files from the models/artifacts directory.
        Joblib is a library used to save and load Python objects (like our ML model).
        """
        artifacts_dir = os.path.join(root_dir, "models", "artifacts")
        try:
            print("Loading model artifacts...")
            # Load the main model and its supporting tools
            self.model = joblib.load(os.path.join(artifacts_dir, "knn_model.joblib"))
            self.scaler = joblib.load(os.path.join(artifacts_dir, "scaler.joblib"))
            self.brand_map = joblib.load(
                os.path.join(artifacts_dir, "brand_map.joblib")
            )
            self.category_map = joblib.load(
                os.path.join(artifacts_dir, "category_map.joblib")
            )
            print("All artifacts loaded successfully!")
        except Exception as e:
            # If the files are missing, we try to train the model on the fly
            print(f"Error loading artifacts: {e}")
            self.train_fallback(artifacts_dir)


    def train_fallback(self, artifacts_dir):
        """
        If we can't find the saved model, this function runs the training script
        to create a new one. This is a safety measure.
        """
        print("Attempting to train model...")
        sys.path.append(root_dir)
        from models.knn_model import run_knn_inventory

        self.model = run_knn_inventory(k=15)
        try:
            # Even if we retrain the model, we still need these mappings
            self.brand_map = joblib.load(
                os.path.join(artifacts_dir, "brand_map.joblib")
            )
            self.category_map = joblib.load(
                os.path.join(artifacts_dir, "category_map.joblib")
            )
            self.scaler = joblib.load(os.path.join(artifacts_dir, "scaler.joblib"))
        except:
            pass


    def predict(self, request):
        """
        Takes a PredictionRequest, processes the data, and returns a prediction.
        """
        # 1. Calculate Net_Margin (Profit)
        # We assume cost is 40% of the original price
        theoretical_cost = request.original_price * 0.40
        net_margin = request.current_price - theoretical_cost

        # 2. Convert text (Brand/Category) to numbers
        # Machine learning models only understand numbers, not text.
        brand_encoded = self.brand_map.get(request.brand)
        category_encoded = self.category_map.get(request.category)

        # If the brand or category is not in our known list, we can't predict
        if brand_encoded is None or category_encoded is None:
            return None, net_margin, brand_encoded, category_encoded

        # 3. Scale numerical features
        # Models work better when numbers are in a similar range (e.g., 0 to 1).
        # We use the 'scaler' we saved during training to do this.
        numerical_features = pd.DataFrame(
            [[request.original_price, request.current_price, net_margin]],
            columns=["original_price", "current_price", "Net_Margin"],
        )
        scaled_numerical = self.scaler.transform(numerical_features)

        # 4. Prepare the final feature list for the model
        # The order of columns must be EXACTLY the same as during training.
        features = pd.DataFrame(
            [
                [
                    scaled_numerical[0][0],  # scaled original_price
                    scaled_numerical[0][1],  # scaled current_price
                    scaled_numerical[0][2],  # scaled Net_Margin
                    brand_encoded,
                    category_encoded,
                    request.stock_quantity,
                ]
            ],
            columns=[
                "original_price",
                "current_price",
                "Net_Margin",
                "brand_encoded",
                "category_encoded",
                "stock_quantity",
            ],
        )

        # 5. Run the prediction
        prediction = self.model.predict(features)

        # prediction[0] is the result (e.g., "High Priority", "Low Priority")
        return str(prediction[0]), net_margin, brand_encoded, category_encoded


# We create a single instance of this service (a Singleton)
# so the whole app can use the same loaded model.
ml_service = MLService()
