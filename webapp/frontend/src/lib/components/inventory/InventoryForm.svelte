<script lang="ts">
	import Button from "$lib/components/ui/Button.svelte";
	import Card from "$lib/components/ui/Card.svelte";
	import FormField from "$lib/components/ui/FormField.svelte";
	import Input from "$lib/components/ui/Input.svelte";
	import Select from "$lib/components/ui/Select.svelte";
	import Accordion from "$lib/components/ui/Accordion.svelte";
	import type { InventoryItem } from "$lib/types/inventory";

	// In Svelte 5, we use 'Props' to define what data this component expects from its parent.
	interface Props {
		brands: string[];
		categories: string[];
		models: string[];
		isLoadingMeta: boolean;
		isPredicting: boolean;
		error?: string;
		onPredict: (data: InventoryItem) => void;
	}

	// '$props()' is a Svelte 5 'Rune'. It gathers the inputs sent to this component.
	let {
		brands,
		categories,
		models,
		isLoadingMeta,
		isPredicting,
		error,
		onPredict,
	}: Props = $props();

	// '$state()' makes these variables "reactive". 
	// If you change them, Svelte automatically updates the text in the input fields.
	let brand = $state("");
	let category = $state("");
	let originalPrice = $state(0);
	let currentPrice = $state(0);
	let stockQuantity = $state(0);
	let selectedModel = $state("knn");
	let unitsSold = $state(15);
	let ruleType = $state("original");

	// Format model names for display
	function formatModelName(name: string) {
		return name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
	}

	/**
	 * When the user clicks the button, we bundle all the form data 
	 * and send it back to the parent component (the Inventory Page).
	 */
	function handleSubmit() {
		onPredict({
			brand,
			category,
			originalPrice,
			currentPrice,
			stockQuantity,
			model_type: selectedModel,
			unitsSold,
			rule_type: ruleType
		});
	}
</script>

<Card title="Item Details">
	<div class="space-y-4">
		<!-- Dropdown for Category -->
		<FormField label="Category" id="category">
			<!-- 'bind:value' connects the dropdown choice directly to our 'category' variable above. -->
			<Select
				id="category"
				bind:value={category}
				disabled={isLoadingMeta}
				placeholder="Select Category"
				options={categories}
			/>
		</FormField>

		<!-- Dropdown for Brand -->
		<FormField label="Brand" id="brand">
			<Select
				id="brand"
				bind:value={brand}
				disabled={isLoadingMeta}
				placeholder="Select Brand"
				options={brands}
			/>
		</FormField>

		<!-- Numerical Inputs -->
		<div class="grid grid-cols-2 gap-4">
			<FormField label="Original Price ($)" id="orig-price">
				<Input
					id="orig-price"
					type="number"
					bind:value={originalPrice}
				/>
			</FormField>
			<FormField label="Current Price ($)" id="curr-price">
				<Input
					id="curr-price"
					type="number"
					bind:value={currentPrice}
				/>
			</FormField>
		</div>

		<!-- Stock and Sales Inputs -->
		<div class="grid grid-cols-2 gap-4">
			<FormField label="Current Stock Level" id="stock">
				<Input id="stock" type="number" bind:value={stockQuantity} />
			</FormField>
			<FormField label="Units Sold (Last 30 Days)" id="units-sold">
				<Input id="units-sold" type="number" bind:value={unitsSold} />
			</FormField>
		</div>

		<!-- Advanced Section -->
		<Accordion title="Advanced Options">
			<FormField label="AI Model" id="model-select" class="px-2">
				<Select 
					id="model-select" 
					bind:value={selectedModel} 
					disabled={isLoadingMeta}
					options={models.length > 0 
						? models.map(m => ({ value: m, label: formatModelName(m) }))
						: [{ value: 'knn', label: 'K-Nearest Neighbors (Default)' }]
					}
				/>
			</FormField>

			<FormField label="Stocking Ruleset / Decision Logic" id="ruleset-select" class="px-2 mt-4">
				<div class="grid grid-cols-2 gap-2 mt-1">
					<button
						type="button"
						class="py-2.5 px-3 rounded-lg border text-sm font-semibold transition-all duration-300 flex items-center justify-center gap-2 {ruleType === 'original' ? 'bg-primary text-white border-primary shadow-lg shadow-primary/20' : 'bg-surface-2 text-text-muted border-border hover:bg-surface-3'}"
						onclick={() => ruleType = 'original'}
					>
						Standard Rules
					</button>
					<button
						type="button"
						class="py-2.5 px-3 rounded-lg border text-sm font-semibold transition-all duration-300 flex items-center justify-center gap-2 {ruleType === 'advanced' ? 'bg-accent text-white border-accent shadow-lg shadow-accent/20' : 'bg-surface-2 text-text-muted border-border hover:bg-surface-3'}"
						onclick={() => ruleType = 'advanced'}
					>
						Advanced Rules
					</button>
				</div>
				<p class="text-xs text-text-muted mt-2 px-1 leading-relaxed">
					{ruleType === 'original' 
						? 'Standard: Classifies strictly based on customer rating (>4.0) and return history.' 
						: 'Advanced: Considers sales velocity (units sold), profit margins, and stock-to-sales ratios.'}
				</p>
			</FormField>
		</Accordion>

		<!-- Show an error message if something goes wrong -->
		{#if error}
			<p class="text-red-600 text-sm mt-2">{error}</p>
		{/if}

		<div class="pt-4">
			<Button
				onclick={handleSubmit}
				variant="primary"
				class="w-full justify-center py-3"
			>
				{isPredicting ? "Analyzing..." : "Get AI Recommendation"}
			</Button>
		</div>
	</div>
</Card>
