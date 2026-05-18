from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# These are our own files
from schemas import PredictionRequest
from services import ml_service

# The 'lifespan' function handles tasks that need to happen when the server starts or stops.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # When the server starts, we load our ML model into memory.
    # This makes predictions much faster because we don't have to load the file every time.
    ml_service.load_artifacts()
    yield
    # Any code here would run when the server shuts down.

# This is our main FastAPI application instance.
app = FastAPI(lifespan=lifespan)

# CORS (Cross-Origin Resource Sharing) is a security feature.
# By default, browsers block websites from making requests to a different domain.
# Since our frontend (Svelte) and backend (FastAPI) might run on different ports,
# we need to explicitly allow the frontend to talk to the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # In production, you should list only your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],       # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],       # Allow all headers
)

# This is a 'GET' route. It's used to fetch data.
# We use it to get the list of available brands and categories for the frontend dropdowns.
@app.get("/meta")
async def get_meta():
    if ml_service.brand_map is None or ml_service.category_map is None:
        raise HTTPException(status_code=500, detail="Metadata not loaded")
    return {
        "brands": list(ml_service.brand_map.keys()),
        "categories": list(ml_service.category_map.keys())
    }

# This is a 'POST' route. It's used when we want to send data to the server.
# Here, we send the product details to get a priority prediction.
@app.post("/predict")
async def predict(request: PredictionRequest):
    # First, we check if everything is loaded correctly
    if any(v is None for v in [ml_service.model, ml_service.scaler, ml_service.brand_map, ml_service.category_map]):
        raise HTTPException(status_code=500, detail="Model or artifacts not initialized")

    # We call our ML service to get the prediction
    priority, net_margin, brand_enc, cat_enc = ml_service.predict(request)

    # If the user sent a brand or category we don't know, we return an error (400 Bad Request)
    if brand_enc is None:
        raise HTTPException(status_code=400, detail=f"Unknown brand: {request.brand}")
    if cat_enc is None:
        raise HTTPException(status_code=400, detail=f"Unknown category: {request.category}")

    # Return the results as JSON
    return {
        "priority": priority,
        "net_margin": round(net_margin, 2),
        "brand_encoded": int(brand_enc),
        "category_encoded": int(cat_enc),
    }

# This block runs the server if you execute this file directly with 'python main.py'
if __name__ == "__main__":
    import uvicorn
    # Uvicorn is the actual web server that handles the network connections.
    uvicorn.run(app, host="0.0.0.0", port=8000)
