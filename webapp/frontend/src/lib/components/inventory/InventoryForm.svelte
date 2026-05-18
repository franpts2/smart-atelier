<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
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

<div class="bg-surface-0 p-8 rounded-lg border border-border shadow-sm">
	<h2 class="text-xl mb-6">Item Details</h2>
	
	<div class="space-y-4">
		<div class="flex flex-col gap-1">
			<label for="category" class="text-sm font-semibold text-text-main">Category</label>
			<select 
				id="category" 
				bind:value={category}
				class="p-2 rounded border border-border bg-surface-1 focus:ring-2 focus:ring-accent outline-none"
				disabled={isLoadingMeta}
			>
				<option value="">Select Category</option>
				{#each categories as cat}
					<option value={cat}>{cat}</option>
				{/each}
			</select>
		</div>

		<div class="flex flex-col gap-1">
			<label for="brand" class="text-sm font-semibold text-text-main">Brand</label>
			<select 
				id="brand" 
				bind:value={brand}
				class="p-2 rounded border border-border bg-surface-1 focus:ring-2 focus:ring-accent outline-none"
				disabled={isLoadingMeta}
			>
				<option value="">Select Brand</option>
				{#each brands as b}
					<option value={b}>{b}</option>
				{/each}
			</select>
		</div>

		<div class="grid grid-cols-2 gap-4">
			<div class="flex flex-col gap-1">
				<label for="orig-price" class="text-sm font-semibold text-text-main">Original Price ($)</label>
				<input 
					id="orig-price" 
					type="number" 
					bind:value={originalPrice}
					class="p-2 rounded border border-border bg-surface-1"
				/>
			</div>
			<div class="flex flex-col gap-1">
				<label for="curr-price" class="text-sm font-semibold text-text-main">Current Price ($)</label>
				<input 
					id="curr-price" 
					type="number" 
					bind:value={currentPrice}
					class="p-2 rounded border border-border bg-surface-1"
				/>
			</div>
		</div>

		<div class="flex flex-col gap-1">
			<label for="stock" class="text-sm font-semibold text-text-main">Current Stock Level</label>
			<input 
				id="stock" 
				type="number" 
				bind:value={stockQuantity}
				class="p-2 rounded border border-border bg-surface-1"
			/>
		</div>

		{#if error}
			<p class="text-red-600 text-sm mt-2">{error}</p>
		{/if}

		<div class="pt-4">
			<Button onclick={handleSubmit} variant="primary" class="w-full justify-center py-3">
				{isPredicting ? 'Analyzing...' : 'Get AI Recommendation'}
			</Button>
		</div>
	</div>
</div>

<style>
	select {
		appearance: none;
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 0.5rem center;
		background-size: 1.5em;
		padding-right: 2.5rem;
	}
</style>
