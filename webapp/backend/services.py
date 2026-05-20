import os
import sys
import joblib
import pandas as pd
import glob

# This is the path to the root of our project.
# We use it to find the 'models' folder no matter where we run this script from.
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MLService:
    """
    This service handles everything related to our Machine Learning models.
    It loads pre-trained models and uses the selected one to make predictions.
    """

    def __init__(self):
        # We initialize these as None and load them later in load_artifacts()
        self.models = {}  # Dictionary to store multiple models {model_id: model_object}
        self.scaler = None  # Used to scale numerical data (normalization)
        self.scaler_advanced = None # Scaler including units_sold
        self.units_sold_map = {} # Mapping of (category, brand) -> units_sold
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
            
            # Load common artifacts
            self.scaler = joblib.load(os.path.join(artifacts_dir, "scaler.joblib"))
            self.scaler_advanced = joblib.load(os.path.join(artifacts_dir, "scaler_advanced.joblib"))
            self.units_sold_map = joblib.load(os.path.join(artifacts_dir, "units_sold_map.joblib"))
            self.brand_map = joblib.load(
                os.path.join(artifacts_dir, "brand_map.joblib")
            )
            self.category_map = joblib.load(
                os.path.join(artifacts_dir, "category_map.joblib")
            )

            # Discover and load all model artifacts
            model_files = glob.glob(os.path.join(artifacts_dir, "*_model.joblib"))
            for model_path in model_files:
                model_name = os.path.basename(model_path).replace("_model.joblib", "")
                self.models[model_name] = joblib.load(model_path)
                print(f"Loaded model: {model_name}")

            if not self.models:
                 print("No models found in artifacts directory.")
                 self.train_fallback(artifacts_dir)
            else:
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

        knn_model = run_knn_inventory(k=15)
        if knn_model:
            self.models["knn"] = knn_model

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
        Takes a PredictionRequest, processes the data, and returns a prediction using the specified model.
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

        # 3. Determine if using advanced rule/model
        is_advanced = (request.rule_type == "advanced")
        
        # Determine units sold:
        # If the user supplied it, use it.
        # Otherwise, look it up in the units_sold_map.
        # If not found in map, default to 10.
        units_sold_raw = request.units_sold
        if units_sold_raw is None or units_sold_raw <= 0:
            units_sold_raw = self.units_sold_map.get((request.category, request.brand), 10)

        # 4. Scale numerical features
        if is_advanced:
            # Features: [original_price, current_price, Net_Margin, units_sold]
            numerical_features = pd.DataFrame(
                [[request.original_price, request.current_price, net_margin, units_sold_raw]],
                columns=["original_price", "current_price", "Net_Margin", "units_sold"],
            )
            scaled_numerical = self.scaler_advanced.transform(numerical_features)
            
            # Prepare the final feature list for advanced model
            features = pd.DataFrame(
                [
                    [
                        scaled_numerical[0][0],  # scaled original_price
                        scaled_numerical[0][1],  # scaled current_price
                        scaled_numerical[0][2],  # scaled Net_Margin
                        brand_encoded,
                        category_encoded,
                        request.stock_quantity,
                        scaled_numerical[0][3],  # scaled units_sold
                    ]
                ],
                columns=[
                    "original_price",
                    "current_price",
                    "Net_Margin",
                    "brand_encoded",
                    "category_encoded",
                    "stock_quantity",
                    "units_sold",
                ],
            )
        else:
            # Standard features: [original_price, current_price, Net_Margin]
            numerical_features = pd.DataFrame(
                [[request.original_price, request.current_price, net_margin]],
                columns=["original_price", "current_price", "Net_Margin"],
            )
            scaled_numerical = self.scaler.transform(numerical_features)
            
            # Prepare the final feature list for standard model
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

        # 5. Run the prediction using the requested model
        model_id = request.model_type
        if is_advanced:
            model_id = f"{model_id}_advanced"
            
        if model_id not in self.models:
            # Fallback to the first available model if requested is missing
            model_id = next(iter(self.models)) if self.models else None
        
        if model_id and model_id in self.models:
            prediction = self.models[model_id].predict(features)
            return str(prediction[0]), net_margin, brand_encoded, category_encoded
        else:
            return "Unknown", net_margin, brand_encoded, category_encoded


# We create a single instance of this service (a Singleton)
# so the whole app can use the same loaded model.
ml_service = MLService()
