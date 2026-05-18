from pydantic import BaseModel

class PredictionRequest(BaseModel):
    original_price: float
    current_price: float
    stock_quantity: int
    brand: str
    category: str
