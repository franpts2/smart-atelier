# Smart Atelier

**Smart Atelier** is an AI-powered stock optimization tool designed for modern fashion boutiques. It utilizes various Machine Learning models (KNN, Random Forest, SVM, etc.) to analyze inventory data and provide strategic recommendations on stock levels and product priority.

---

## Project Goal
This project is a Proof of Concept (POC) that addresses the challenge of inventory management in the fashion industry. It transforms raw sales and inventory data into actionable insights through a modern web interface.

---

## Project Structure

-   **`data/`**: Contains raw and processed datasets.
-   **`models/`**: Scripts for training and optimizing ML models, plus saved artifacts.
-   **`src/`**: Data preparation and preprocessing scripts.
-   **`webapp/`**: The full-stack application.
    -   `backend/`: FastAPI server handling AI logic and data serving.
    -   `frontend/`: SvelteKit interface for analysis and prediction.

---

## Prerequisites

Ensure you have the following installed:
- **Python 3.9+**
- **Node.js (v18+)** and **npm**

---

## Installation & Setup

### 1. Backend Setup
Navigate to the backend directory and install the required Python packages:
```bash
cd webapp/backend
pip install pandas scikit-learn joblib fastapi uvicorn pydantic
```

### 2. Frontend Setup
Navigate to the frontend directory and install the dependencies:
```bash
cd webapp/frontend
npm install
```

---

## Running the Application

To run the full system, you need to start both the backend and frontend servers in separate terminal windows.

### Step 1: Start the Backend
```bash
cd webapp/backend
python3 main.py
```
The backend server will start at `http://localhost:8000`. It will automatically load the pre-trained model artifacts from the `models/artifacts/` directory.

### Step 2: Start the Frontend
```bash
cd webapp/frontend
npm run dev
```
The frontend will be available at `http://localhost:5173`.

---

## How to Use

### 1. Stock Optimization Tool
- Go to the **Inventory** page.
- Fill in the item details (Category, Brand, Prices, Current Stock, and recent Sales).
- Open **Advanced Options** to select a specific AI Model (e.g., Random Forest Optimized) and toggle between **Standard** or **Advanced** stocking rules.
- Click **"Get AI Recommendation"** to see the suggested priority (High Stock, Maintain, or Low Stock) along with business insights.

### 2. Analytics Dashboard
- Go to the **Analytics** page.
- Toggle between **Standard** and **Advanced** rulesets to see how they impact the training data distribution.
- Compare the performance of all integrated models (Accuracy, Precision, Recall, F1-Score) through interactive charts.
- Hover over chart elements to see detailed metrics.

---

## Simulation & Testing Guide

To verify the AI's behavior across different models and rulesets, use the following test scenarios. While different algorithms may have slight variations, these values are optimized to trigger specific recommendations.

### 1. **High Stock** (Top Performer)
*Best for: Capitalizing on high demand and healthy margins.*
- **Category**: `Tops`
- **Brand**: `Uniqlo`
- **Original Price**: `$100.00`
- **Current Price**: `$100.00` (No discount = High demand)
- **Current Stock**: `5` (Low stock)
- **Units Sold**: `30` (High volume)
- **Ruleset**: `Advanced` (Uses Sales Volume)

### 2. **Low Stock** (Risk / Clearance)
*Best for: Identifying dead stock and high-risk assets.*
- **Category**: `Outerwear`
- **Brand**: `Zara`
- **Original Price**: `$250.00`
- **Current Price**: `$60.00` (Heavy markdown = Low margin)
- **Current Stock**: `150` (Overstocked)
- **Units Sold**: `2` (Stagnant sales)
- **Ruleset**: `Advanced`

### 3. **Maintain** (Stable Asset)
*Best for: Consistent performance without immediate action.*
- **Category**: `Bottoms`
- **Brand**: `Mango`
- **Original Price**: `$60.00`
- **Current Price**: `$55.00` (Balanced margin)
- **Current Stock**: `40`
- **Units Sold**: `12`
- **Ruleset**: `Standard` or `Advanced`

<br>

> **Note on Algorithms**: 
> - **Random Forest Optimized** and **Neural Network** are generally the most sensitive to these inputs.
> - **Naive Bayes** and **SVM** may default to "Maintain" more often due to the underlying distribution of the artificial training data.

---

## (Optional) Training Models
If you wish to retrain all models (standard and advanced versions):
```bash
python3 models/train_models.py
```
This will update the `.joblib` files in `models/artifacts/` which are used by the backend.
