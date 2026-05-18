from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from schemas import PredictionRequest
from services import ml_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_service.load_artifacts()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/meta")
async def get_meta():
    if ml_service.brand_map is None or ml_service.category_map is None:
        raise HTTPException(status_code=500, detail="Metadata not loaded")
    return {
        "brands": list(ml_service.brand_map.keys()),
        "categories": list(ml_service.category_map.keys())
    }

@app.post("/predict")
async def predict(request: PredictionRequest):
    if any(v is None for v in [ml_service.model, ml_service.scaler, ml_service.brand_map, ml_service.category_map]):
        raise HTTPException(status_code=500, detail="Model or artifacts not initialized")

    priority, net_margin, brand_enc, cat_enc = ml_service.predict(request)

    if brand_enc is None:
        raise HTTPException(status_code=400, detail=f"Unknown brand: {request.brand}")
    if cat_enc is None:
        raise HTTPException(status_code=400, detail=f"Unknown category: {request.category}")

    return {
        "priority": priority,
        "net_margin": round(net_margin, 2),
        "brand_encoded": int(brand_enc),
        "category_encoded": int(cat_enc),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
