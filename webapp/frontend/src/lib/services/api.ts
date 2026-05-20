import type { InventoryItem, PredictionResult, InventoryMeta } from '../types/inventory';
import type { DistributionItem, ModelMetric, DualRulesetDistribution, DualRulesetComparison } from '../types/analytics';

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

export async function fetchDataDistribution(): Promise<DualRulesetDistribution> {
	const res = await fetch(`${API_BASE_URL}/data-distribution`);
	if (!res.ok) throw new Error('Failed to fetch data distribution');
	const data: any = await res.json();
	
	if (data && data.error) {
		throw new Error(data.error);
	}
	
	const mapToItems = (record: Record<string, number> | undefined): DistributionItem[] => {
		if (!record) return [];
		const order = ['High Stock', 'Maintain', 'Low Stock'];
		const entries = Object.entries(record).map(([label, count]) => ({ label, count }));
		return entries.sort((a, b) => {
			const indexA = order.indexOf(a.label);
			const indexB = order.indexOf(b.label);
			const valA = indexA !== -1 ? indexA : 999;
			const valB = indexB !== -1 ? indexB : 999;
			return valA - valB;
		});
	};

	// Graceful fallback for legacy flat format
	if (data && !data.standard && !data.advanced) {
		const legacyMapped = mapToItems(data);
		return {
			standard: legacyMapped,
			advanced: legacyMapped
		};
	}

	return {
		standard: mapToItems(data.standard),
		advanced: mapToItems(data.advanced)
	};
}

export async function fetchModelComparison(): Promise<DualRulesetComparison> {
	const res = await fetch(`${API_BASE_URL}/model-comparison`);
	if (!res.ok) throw new Error('Failed to fetch model comparison');
	const data: any = await res.json();
	
	if (data && data.error) {
		throw new Error(data.error);
	}
	
	// Graceful fallback for legacy array format
	if (Array.isArray(data)) {
		return {
			standard: data,
			advanced: data
		};
	}
	
	return data;
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
			stock_quantity: item.stockQuantity,
			model_type: item.model_type,
			units_sold: item.unitsSold,
			rule_type: item.rule_type
		})
	});

	if (!res.ok) {
		const errData = await res.json();
		// If the server returns an error (like 400 or 500), we show the message to the user.
		throw new Error(errData.detail || 'Stock prediction failed');
	}

	return res.json();
}
