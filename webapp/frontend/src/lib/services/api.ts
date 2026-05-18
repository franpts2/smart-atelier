import type { InventoryItem, PredictionResult, InventoryMeta } from '../types/inventory';

const API_BASE_URL = 'http://localhost:8000';

export async function fetchInventoryMeta(): Promise<InventoryMeta> {
	const res = await fetch(`${API_BASE_URL}/meta`);
	if (!res.ok) throw new Error('Failed to fetch metadata from server');
	return res.json();
}

export async function predictStock(item: InventoryItem): Promise<PredictionResult> {
	const res = await fetch(`${API_BASE_URL}/predict`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
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
		throw new Error(errData.detail || 'Stock prediction failed');
	}

	return res.json();
}
