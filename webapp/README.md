# Smart Atelier Web App

This directory contains the full-stack web application for Smart Atelier. It is divided into two main parts that work together to provide AI-powered inventory insights.

## 🏗 System Architecture

The app uses a **Client-Server architecture**:

1.  **Backend (`/backend`)**:
    -   **Technology**: Python with FastAPI.
    -   **Role**: The "Brain". It loads the Machine Learning models, processes data, and provides an API (Application Programming Interface).
    -   **Port**: Runs on `http://localhost:8000`.

2.  **Frontend (`/frontend`)**:
    -   **Technology**: SvelteKit with TypeScript.
    -   **Role**: The "Face". It provides the user interface where people can enter product details and see recommendations.
    -   **Port**: Runs on `http://localhost:5173`.

---

## 🚦 How to Run the App

To see the app in action, you need to have **two terminals** open because both the frontend and backend must be running at the same time.

### 1. Start the Backend (The Brain)
Open a terminal and run:
```bash
# Go to the backend folder
cd webapp/backend

# (Optional) Create a virtual environment and install dependencies
# pip install -r requirements.txt

# Run the server
python main.py
```

### 2. Start the Frontend (The Face)
Open a **second** terminal and run:
```bash
# Go to the frontend folder
cd webapp/frontend

# Install the necessary packages (only need to do this once)
npm install

# Run the development server
npm run dev
```

Now, open your browser and go to `http://localhost:5173`.

---

## 🔄 How they talk to each other

1.  The **Frontend** (in your browser) sends a message (a "Request") to `http://localhost:8000/predict`.
2.  The **Backend** receives the data, runs it through the AI model, and sends back a message (a "Response") with the prediction.
3.  The **Frontend** receives that prediction and instantly updates the screen for the user.

---

## 📂 Folders at a Glance

-   `backend/`: Contains the Python code for the API and ML integration.
-   `frontend/`: Contains the Svelte code, styles, and UI components.

For more detailed information, check the **README.md** file inside each folder!
