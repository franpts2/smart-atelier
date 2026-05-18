<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import FormField from '$lib/components/ui/FormField.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import type { InventoryItem } from '$lib/types/inventory';

	interface Props {
		brands: string[];
		categories: string[];
		isLoadingMeta: boolean;
		isPredicting: boolean;
		error?: string;
		onPredict: (data: InventoryItem) => void;
	}

	let { 
		brands, 
		categories, 
		isLoadingMeta, 
		isPredicting, 
		error,
		onPredict 
	}: Props = $props();

	let brand = $state('');
	let category = $state('');
	let originalPrice = $state(0);
	let currentPrice = $state(0);
	let stockQuantity = $state(0);

	function handleSubmit() {
		onPredict({
			brand,
			category,
			originalPrice,
			currentPrice,
			stockQuantity
		});
	}
</script>

<Card title="Item Details">
	<div class="space-y-4">
		<FormField label="Category" id="category">
			<Select 
				id="category" 
				bind:value={category}
				disabled={isLoadingMeta}
				placeholder="Select Category"
			>
				{#each categories as cat}
					<option value={cat}>{cat}</option>
				{/each}
			</Select>
		</FormField>

		<FormField label="Brand" id="brand">
			<Select 
				id="brand" 
				bind:value={brand}
				disabled={isLoadingMeta}
				placeholder="Select Brand"
			>
				{#each brands as b}
					<option value={b}>{b}</option>
				{/each}
			</Select>
		</FormField>

		<div class="grid grid-cols-2 gap-4">
			<FormField label="Original Price ($)" id="orig-price">
				<Input id="orig-price" type="number" bind:value={originalPrice} />
			</FormField>
			<FormField label="Current Price ($)" id="curr-price">
				<Input id="curr-price" type="number" bind:value={currentPrice} />
			</FormField>
		</div>

		<FormField label="Current Stock Level" id="stock">
			<Input id="stock" type="number" bind:value={stockQuantity} />
		</FormField>

		{#if error}
			<p class="text-red-600 text-sm mt-2">{error}</p>
		{/if}

		<div class="pt-4">
			<Button onclick={handleSubmit} variant="primary" class="w-full justify-center py-3">
				{isPredicting ? 'Analyzing...' : 'Get AI Recommendation'}
			</Button>
		</div>
	</div>
</Card>
