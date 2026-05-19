# Smart Atelier

**Smart Atelier** is an AI-powered consulting tool designed for modern fashion boutiques. It uses Machine Learning (K-Nearest Neighbors, Decision Trees, Naive Bayes, and Support Vector Machines) to analyze inventory data and provide strategic recommendations on stock levels, pricing, and product priority.

---

## The Big Picture

This project is a complete "Data to App" pipeline. Here is how it flows:

1.  **Data Processing**: We take raw boutique data and clean/prepare it for AI.
2.  **Model Training**: We train models to recognize patterns in fashion sales.
3.  **Deployment**: We serve that model through a web application so users can get real-time insights.

---

## Project Structure

-   **`data/`**: The library of our project. Contains `raw/` data and the `processed/` files used for training.
-   **`models/`**: The brain factory. Contains the scripts to train the AI (e.g., `knn_model.py`, `decision_tree_model.py`, `naive_bayes_model.py`, `svm_model.py`) and the saved `artifacts/` (the actual "brains" our web app uses).
-   **`src/`**: The workshop. Contains utility scripts for data preparation and scaling metrics.
-   **`webapp/`**: The storefront.
    -   `backend/`: A FastAPI server that handles the AI logic.
    -   `frontend/`: A SvelteKit website for the user interface.

---

## Prerequisites

Before you begin, ensure you have the following installed:

### 1. Core Tools
-   **Python 3.9+**: The language used for our AI and Backend.
-   **Node.js (v18+) & npm**: The environment and package manager for our Frontend.

### 2. Python Packages
You can install all necessary Python packages using pip:
```bash
pip install pandas scikit-learn joblib fastapi uvicorn pydantic
```
-   `pandas` & `scikit-learn`: For data processing and the ML models.
-   `joblib`: For saving and loading the AI model files.
-   `fastapi` & `uvicorn`: For running the web server.
-   `pydantic`: For data validation.

---

## Quick Start

### 1. (Optional) Train the Models
If you want to re-run the AI training:
```bash
python3 models/knn_model.py
python3 models/decision_tree_model.py
python3 models/naive_bayes_model.py
python3 models/svm_model.py
```

### 2. Run the Full Application
You need **two terminals** running at the same time:

**Terminal A (Backend):**
```bash
cd webapp/backend
python3 main.py
```

**Terminal B (Frontend):**
```bash
cd webapp/frontend
npm install
npm run dev
```
Visit `http://localhost:5173` to see the app!
