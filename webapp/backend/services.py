import os
import sys
import joblib
import pandas as pd

# Add root dir for potential training fallback imports
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MLService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.brand_map = None
        self.category_map = None

    def load_artifacts(self):
        artifacts_dir = os.path.join(root_dir, "models", "artifacts")
        try:
            print("Loading model artifacts...")
            self.model = joblib.load(os.path.join(artifacts_dir, "knn_model.joblib"))
            self.scaler = joblib.load(os.path.join(artifacts_dir, "scaler.joblib"))
            self.brand_map = joblib.load(os.path.join(artifacts_dir, "brand_map.joblib"))
            self.category_map = joblib.load(os.path.join(artifacts_dir, "category_map.joblib"))
            print("All artifacts loaded successfully!")
        except Exception as e:
            print(f"Error loading artifacts: {e}")
            self.train_fallback(artifacts_dir)

    def train_fallback(self, artifacts_dir):
        print("Attempting to train model...")
        sys.path.append(root_dir)
        from models.knn_model import run_knn_inventory
        self.model = run_knn_inventory(k=15)
        try:
            self.brand_map = joblib.load(os.path.join(artifacts_dir, "brand_map.joblib"))
            self.category_map = joblib.load(os.path.join(artifacts_dir, "category_map.joblib"))
            self.scaler = joblib.load(os.path.join(artifacts_dir, "scaler.joblib"))
        except:
            pass

    def predict(self, request):
        # Calculate Net_Margin
        theoretical_cost = request.original_price * 0.40
        net_margin = request.current_price - theoretical_cost

        # Encode
        brand_encoded = self.brand_map.get(request.brand)
        category_encoded = self.category_map.get(request.category)

        if brand_encoded is None or category_encoded is None:
            return None, net_margin, brand_encoded, category_encoded

        # Scale and Prepare Features
        numerical_features = pd.DataFrame(
            [[request.original_price, request.current_price, net_margin]],
            columns=["original_price", "current_price", "Net_Margin"],
        )
        scaled_numerical = self.scaler.transform(numerical_features)

        features = pd.DataFrame(
            [[
                scaled_numerical[0][0],
                scaled_numerical[0][1],
                scaled_numerical[0][2],
                brand_encoded,
                category_encoded,
                request.stock_quantity,
            ]],
            columns=["original_price", "current_price", "Net_Margin", "brand_encoded", "category_encoded", "stock_quantity"],
        )

        prediction = self.model.predict(features)
        return str(prediction[0]), net_margin, brand_encoded, category_encoded

ml_service = MLService()
