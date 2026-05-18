<script lang="ts">
	import { onMount } from 'svelte';
	import InventoryHeader from '$lib/components/inventory/InventoryHeader.svelte';
	import InventoryForm from '$lib/components/inventory/InventoryForm.svelte';
	import RecommendationDisplay from '$lib/components/inventory/RecommendationDisplay.svelte';

	// Metadata from backend
	let brands = $state<string[]>([]);
	let categories = $state<string[]>([]);
	let isLoadingMeta = $state(true);

	// Prediction result
	let prediction = $state<{
		priority: string;
		net_margin: number;
	} | null>(null);
	let isPredicting = $state(false);
	let error = $state('');

	const API_URL = 'http://localhost:8000';

	onMount(async () => {
		try {
			const res = await fetch(`${API_URL}/meta`);
			if (!res.ok) throw new Error('Failed to fetch metadata');
			const data = await res.json();
			brands = data.brands;
			categories = data.categories;
		} catch (e) {
			console.error(e);
			error = 'Could not connect to the backend. Please ensure the server is running.';
		} finally {
			isLoadingMeta = false;
		}
	});

	async function handlePredict(formData: {
		brand: string;
		category: string;
		originalPrice: number;
		currentPrice: number;
		stockQuantity: number;
	}) {
		if (!formData.brand || !formData.category) {
			error = 'Please select both brand and category.';
			return;
		}
		
		error = '';
		isPredicting = true;
		prediction = null;

		try {
			const res = await fetch(`${API_URL}/predict`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					brand: formData.brand,
					category: formData.category,
					original_price: formData.originalPrice,
					current_price: formData.currentPrice,
					stock_quantity: formData.stockQuantity
				})
			});

			if (!res.ok) {
				const errData = await res.json();
				throw new Error(errData.detail || 'Prediction failed');
			}

			prediction = await res.json();
		} catch (e: any) {
			error = e.message;
		} finally {
			isPredicting = false;
		}
	}
</script>

<div class="max-w-4xl mx-auto py-12 px-4">
	<InventoryHeader />

	<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
		<InventoryForm 
			{brands} 
			{categories} 
			{isLoadingMeta} 
			{isPredicting} 
			{error} 
			onPredict={handlePredict} 
		/>

		<RecommendationDisplay {prediction} />
	</div>
</div>
