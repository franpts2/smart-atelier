# Smart Atelier Web App - Frontend

Welcome to the frontend of Smart Atelier! We use **SvelteKit**, a modern framework that makes building websites fast and fun.

## What are we using?

1.  **Svelte**: The core "language" we use. It looks like HTML but with superpowers (like automatically updating the screen when data changes).
2.  **SvelteKit**: The "engine" that handles things like moving between pages (routing) and making the site feel like a single-page app.
3.  **TypeScript**: A version of JavaScript that helps us catch bugs early by making sure we use the right types of data (e.g., preventing you from accidentally adding a number to a piece of text).
4.  **Vite**: The tool that builds our project and makes the development experience super fast.

---

## Project Structure (Where is everything?)

SvelteKit has a specific way of organizing files. Here’s the breakdown:

-   **`src/routes/`**: This is where our **pages** live.
    -   `+page.svelte`: This file represents a page (e.g., `/` is `src/routes/+page.svelte`).
    -   Folders like `inventory/` or `analytics/` create new URLs automatically (e.g., `/inventory`).
    -   `+layout.svelte`: This file contains things that stay the same on every page, like the Header and Footer.

-   **`src/lib/`**: This is where we keep **reusable bits** (short for "library").
    -   `components/`: Smaller pieces of the UI like Buttons, Cards, or the Inventory Form. We build them once and use them everywhere.
    -   `services/api.ts`: This is the bridge to our backend. It’s where we write the code to "talk" to the FastAPI server.
    -   `types/`: Definitions for our data (like what an "Inventory Item" looks like).

-   _!!! all other files aren't important for you probably!_

---

## What is a `.svelte` file?

In Svelte, we keep everything related to a component in **one file**. It usually has three parts:

```svelte
<script>
  // 1. Logic (JavaScript/TypeScript) goes here.
  let name = "Junior Developer";
</script>

<!-- 2. The Look (HTML) goes here. -->
<h1>Hello {name}!</h1>

<style>
  /* 3. Styles (CSS) go here. They only affect THIS file! */
  h1 { color: purple; }
</style>
```

---

# How to run it?

1.  **Install dependencies**:
    Make sure you have [Node.js](https://nodejs.org/) installed, then run:
    ```bash
    npm install
    ```

2.  **Start the development server**:
    ```bash
    npm run dev
    ```
    Open `http://localhost:5173` in your browser. The page will update automatically whenever you save a file!

---

## Connecting to the Backend

The frontend talks to the backend using the `src/lib/services/api.ts` file. 
- When you fill out the form in the `inventory` page, it sends that data to our Python server (`http://localhost:8000/predict`).
- The server sends back the prediction, and Svelte automatically updates the UI to show the result.

---
<!-- TODO: remove this section -->
## Tips

-   **The Console is your friend**: Right-click the website, choose "Inspect", and go to the "Console" tab. Any errors or `console.log` messages will show up there.
-   **Reusable Components**: If you find yourself writing the same HTML twice, turn it into a component in `src/lib/ui/`!
-   **Reactive Variables**: In Svelte, if you want a variable to trigger a UI update, just declare it with `let`. If you update it, the UI updates instantly!
