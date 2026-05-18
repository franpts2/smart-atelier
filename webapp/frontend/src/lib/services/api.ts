import type { InventoryItem, PredictionResult, InventoryMeta } from '../types/inventory';

// This is the address of our Python (FastAPI) backend.
// In a real project, this would change when you put the website online.
const API_BASE_URL = 'http://localhost:8000';

/**
 * Fetches the list of brands and categories from the backend.
 * We use this to fill the dropdown menus in our form.
 */
export async function fetchInventoryMeta(): Promise<InventoryMeta> {
	// 'fetch' is a built-in browser tool to get data from a URL.
	const res = await fetch(`${API_BASE_URL}/meta`);
	
	// If the server is down or returns an error, we throw an error here.
	if (!res.ok) throw new Error('Failed to fetch metadata from server');
	
	// Convert the raw response into a JSON object we can use in Svelte.
	return res.json();
}

/**
 * Sends product data to the backend to get an AI-powered prediction.
 */
export async function predictStock(item: InventoryItem): Promise<PredictionResult> {
	const res = await fetch(`${API_BASE_URL}/predict`, {
		method: 'POST', // We use POST because we are SENDING data to the server.
		headers: { 'Content-Type': 'application/json' },
		// We turn our JavaScript object into a JSON string so the server can read it.
		body: JSON.stringify({
			brand: item.brand,
			category: item.category,
			original_price: item.originalPrice,
			current_price: item.currentPrice,
			stock_quantity: item.stockQuantity
		})
	});

	if (!res.ok) {
		const errData = await res.json();
		// If the server returns an error (like 400 or 500), we show the message to the user.
		throw new Error(errData.detail || 'Stock prediction failed');
	}

	return res.json();
}
