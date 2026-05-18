<script lang="ts">
	import { onMount } from "svelte";
	import InventoryHeader from "$lib/components/inventory/InventoryHeader.svelte";
	import InventoryForm from "$lib/components/inventory/InventoryForm.svelte";
	import RecommendationDisplay from "$lib/components/inventory/RecommendationDisplay.svelte";
	import { fetchInventoryMeta, predictStock } from "$lib/services/api";
	import type { InventoryItem, PredictionResult } from "$lib/types/inventory";

	// Metadata from backend
	let brands = $state<string[]>([]);
	let categories = $state<string[]>([]);
	let isLoadingMeta = $state(true);

	// Prediction result
	let prediction = $state<PredictionResult | null>(null);
	let isPredicting = $state(false);
	let error = $state("");

	onMount(async () => {
		try {
			const data = await fetchInventoryMeta();
			brands = data.brands;
			categories = data.categories;
		} catch (e: any) {
			console.error(e);
			error = e.message || "Could not connect to the backend.";
		} finally {
			isLoadingMeta = false;
		}
	});

	async function handlePredict(formData: InventoryItem) {
		if (!formData.brand || !formData.category) {
			error = "Please select both brand and category.";
			return;
		}

		error = "";
		isPredicting = true;
		prediction = null;

		try {
			prediction = await predictStock(formData);
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
