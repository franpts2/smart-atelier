from pydantic import BaseModel

# Pydantic is a library used for data validation in Python.
# It ensures that the data coming into our API matches the format we expect.
# If someone sends a request with a missing field or the wrong data type (e.g., a string where a number is expected),
# Pydantic will automatically catch the error and send a helpful message back to the user.

class PredictionRequest(BaseModel):
    """
    This class defines the 'schema' (structure) for a prediction request.
    When a user wants to get a recommendation, they must send a JSON object
    that follows this exact structure.
    """
    original_price: float    # Decimal numbers (e.g., 99.99)
    current_price: float     # Decimal numbers
    stock_quantity: int      # Whole numbers (e.g., 10)
    brand: str               # Text (e.g., "Zara")
    category: str            # Text (e.g., "Dress")
