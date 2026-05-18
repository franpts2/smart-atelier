export interface InventoryItem {
	brand: string;
	category: string;
	originalPrice: number;
	currentPrice: number;
	stockQuantity: number;
}

export interface PredictionResult {
	priority: string;
	net_margin: number;
}

export interface InventoryMeta {
	brands: string[];
	categories: string[];
}
