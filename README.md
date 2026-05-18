# smart-atelier

to run k-nearest neighbours:
```bash
python3 models/knn_model.py
```

1. Start the Backend (FastAPI)

    Open a terminal in the project root and run:

    ```
    python3 webapp/backend/main.py
    ```

    The backend will be running at http://localhost:8000.

2. Start the Frontend (SvelteKit)

    Open a second terminal window in the project root and run:

    ```
    # Navigate to the frontend directory
    cd webapp/frontend

    # Install dependencies (if you haven't already)
    npm install

    # Start the development server
    npm run dev
    ```

    The frontend will typically be running at http://localhost:5173.