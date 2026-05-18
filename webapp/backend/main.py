from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import pandas as pd
import numpy as np
import sys
import os
import joblib

# Add the root directory to path so we can import from models
# Current file: .../webapp/backend/main.py
# Root dir: .../
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

# Global instances
model = None
scaler = None
brand_map = None
category_map = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, scaler, brand_map, category_map
    artifacts_dir = os.path.join(root_dir, "models", "artifacts")

    try:
        print("Loading model artifacts...")
        model = joblib.load(os.path.join(artifacts_dir, "knn_model.joblib"))
        scaler = joblib.load(os.path.join(artifacts_dir, "scaler.joblib"))
        brand_map = joblib.load(os.path.join(artifacts_dir, "brand_map.joblib"))
        category_map = joblib.load(os.path.join(artifacts_dir, "category_map.joblib"))
        print("All artifacts loaded successfully!")
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        print("Attempting to train model...")
        from models.knn_model import run_knn_inventory

        model = run_knn_inventory(k=15)
        # Re-load maps if training succeeded
        try:
            brand_map = joblib.load(os.path.join(artifacts_dir, "brand_map.joblib"))
            category_map = joblib.load(
                os.path.join(artifacts_dir, "category_map.joblib")
            )
            scaler = joblib.load(os.path.join(artifacts_dir, "scaler.joblib"))
        except:
            pass
    yield


app = FastAPI(lifespan=lifespan)

# Enable CORS for the Svelte frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    original_price: float
    current_price: float
    stock_quantity: int
    brand: str
    category: str


@app.get("/meta")
async def get_meta():
    if brand_map is None or category_map is None:
        raise HTTPException(status_code=500, detail="Metadata not loaded")
    return {"brands": list(brand_map.keys()), "categories": list(category_map.keys())}


@app.post("/predict")
async def predict(request: PredictionRequest):
    if model is None or scaler is None or brand_map is None or category_map is None:
        raise HTTPException(
            status_code=500, detail="Model or artifacts not initialized"
        )

    # 1. Encode brand and category
    brand_encoded = brand_map.get(request.brand)
    category_encoded = category_map.get(request.category)

    if brand_encoded is None:
        raise HTTPException(status_code=400, detail=f"Unknown brand: {request.brand}")
    if category_encoded is None:
        raise HTTPException(
            status_code=400, detail=f"Unknown category: {request.category}"
        )

    # 2. Calculate Net_Margin (consistent with data_preparation.py)
    # Theoretical cost is 40% of original price
    theoretical_cost = request.original_price * 0.40
    net_margin = request.current_price - theoretical_cost

    # 3. Scale numerical features
    # Features in order: ["original_price", "current_price", "Net_Margin"]
    numerical_features = pd.DataFrame(
        [[request.original_price, request.current_price, net_margin]],
        columns=["original_price", "current_price", "Net_Margin"],
    )

    scaled_numerical = scaler.transform(numerical_features)

    # 4. Prepare full feature vector
    # Features: ["original_price", "current_price", "Net_Margin", "brand_encoded", "category_encoded", "stock_quantity"]
    features = pd.DataFrame(
        [
            [
                scaled_numerical[0][0],  # original_price scaled
                scaled_numerical[0][1],  # current_price scaled
                scaled_numerical[0][2],  # Net_Margin scaled
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

    # 5. Predict
    prediction = model.predict(features)

    return {
        "priority": str(prediction[0]),
        "net_margin": round(net_margin, 2),
        "brand_encoded": int(brand_encoded),
        "category_encoded": int(category_encoded),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
