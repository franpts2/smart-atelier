# Smart Atelier Web App - Backend
Welcome! This is the backend for the Smart Atelier project

## What are we using?

We use several modern Python libraries to make this work:

1.  **FastAPI**: A modern, fast web framework for building APIs with Python. It handles the "web" part—receiving requests from the internet and sending back responses.
2.  **Uvicorn**: The actual web server that runs our FastAPI application.
3.  **Pydantic**: Used for data validation. It ensures that the data sent to our API is correct (e.g., that a price is actually a number and not text).
4.  **Scikit-learn & Joblib**: These handle the Machine Learning part. Scikit-learn is the library used to train the model, and Joblib is used to save and load that model.
5.  **Pandas**: A powerful tool for data manipulation. We use it to prepare the data before sending it to the ML model.

---

## Project Structure

-   `main.py`: The **entry point**. This is where we define our routes (URLs like `/predict`) and start the server.
-   `schemas.py`: Where we define the **shape of the data**. It's like a contract between the frontend and the backend.
-   `services.py`: The **brain** of the operation. This is where we load the ML model and use it to make predictions.

---

## How to run it?

1.  **Install dependencies**:
    Make sure you have Python installed, then run:
    ```bash
    pip install fastapi uvicorn pydantic pandas joblib scikit-learn
    ```

2.  **Start the server**:
    From this directory (`webapp/backend`), run:
    ```bash
    python main.py
    ```
    or from the root of the project:
    ```bash
    python webapp/backend/main.py
    ```
    The server will start at `http://localhost:8000`.

---

## How does it work? (The Flow)

1.  **Startup**: When you run `main.py`, the `lifespan` function runs. It tells the `MLService` in `services.py` to load the pre-trained model files (the `.joblib` files).
2.  **Request**: When a user on the website clicks "Predict", the frontend sends a **POST request** to `http://localhost:8000/predict` with the product information in JSON format.
3.  **Validation**: FastAPI uses the `PredictionRequest` class in `schemas.py` to check if the data sent by the user is valid.
4.  **Processing**: The data is sent to `ml_service.predict()`. This function:
    -   Calculates the "Net Margin" (profit).
    -   Converts text (like "Zara") into numbers (like `5`) because ML models only understand numbers.
    -   Scales the numbers so they are in a consistent range.
5.  **Prediction**: The processed data is fed into the KNN model, which returns a prediction (e.g., "High Priority").
6.  **Response**: The backend sends this prediction back to the frontend as a JSON response.
