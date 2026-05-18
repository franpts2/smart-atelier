<script lang="ts">
	import { onMount } from 'svelte';
	import Button from '$lib/components/Button.svelte';
	import Badge from '$lib/components/Badge.svelte';

	// Form state
	let brand = $state('');
	let category = $state('');
	let originalPrice = $state(0);
	let currentPrice = $state(0);
	let stockQuantity = $state(0);

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

	async function handlePredict() {
		if (!brand || !category) {
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
					brand,
					category,
					original_price: originalPrice,
					current_price: currentPrice,
					stock_quantity: stockQuantity
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

	function getPriorityLabel(priority: string) {
		switch (priority) {
			case 'High Stock': return { text: '🌟 Top Performer', class: 'bg-green-100 text-green-800 border-green-200' };
			case 'Low Stock': return { text: '⚠️ Risk / Clearance', class: 'bg-orange-100 text-orange-800 border-orange-200' };
			default: return { text: '✅ Stable Asset', class: 'bg-blue-100 text-blue-800 border-blue-200' };
		}
	}
</script>

<div class="max-w-4xl mx-auto py-12 px-4">
	<div class="mb-12 text-center">
		<Badge>Inventory Intelligence</Badge>
		<h1 class="text-4xl mt-4 mb-4">Stock Optimization Tool</h1>
		<p class="text-text-muted">Analyze your collection items to determine optimal stock levels and profitability.</p>
	</div>

	<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
		<!-- Form Section -->
		<div class="bg-surface-0 p-8 rounded-lg border border-border shadow-sm">
			<h2 class="text-xl mb-6">Item Details</h2>
			
			<div class="space-y-4">
				<div class="flex flex-col gap-1">
					<label for="category" class="text-sm font-semibold text-text-main">Category</label>
					<select 
						id="category" 
						bind:value={category}
						class="p-2 rounded border border-border bg-surface-1 focus:ring-2 focus:ring-accent-gold outline-none"
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
						class="p-2 rounded border border-border bg-surface-1 focus:ring-2 focus:ring-accent-gold outline-none"
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
					<Button onclick={handlePredict} variant="primary" class="w-full justify-center py-3">
						{isPredicting ? 'Analyzing...' : 'Get AI Recommendation'}
					</Button>
				</div>
			</div>
		</div>

		<!-- Results Section -->
		<div class="flex flex-col">
			{#if prediction}
				{@const label = getPriorityLabel(prediction.priority)}
				<div class="bg-surface-0 p-8 rounded-lg border border-border shadow-sm flex-1 animate-in fade-in slide-in-from-bottom-4 duration-500">
					<h2 class="text-xl mb-6">AI Recommendation</h2>
					
					<div class="flex flex-col items-center text-center space-y-6">
						<div class="py-3 px-6 rounded-full border {label.class} text-lg font-bold">
							{label.text}
						</div>

						<div class="grid grid-cols-2 gap-8 w-full">
							<div class="p-4 bg-surface-1 rounded border border-border">
								<p class="text-xs text-text-muted uppercase tracking-wider font-bold mb-1">Net Margin</p>
								<p class="text-2xl font-heading text-primary">${prediction.net_margin}</p>
							</div>
							<div class="p-4 bg-surface-1 rounded border border-border">
								<p class="text-xs text-text-muted uppercase tracking-wider font-bold mb-1">Status</p>
								<p class="text-xl font-semibold">{prediction.priority}</p>
							</div>
						</div>

						<div class="text-left w-full space-y-4 pt-4 border-t border-border">
							<h3 class="text-sm uppercase text-text-muted tracking-widest">Business Insights</h3>
							{#if prediction.priority === 'High Stock'}
								<p class="text-sm">This item shows strong market potential. We recommend <strong>increasing inventory</strong> levels to capitalize on high demand and low return rates.</p>
							{:else if prediction.priority === 'Low Stock'}
								<p class="text-sm">High risk detected. Consider <strong>phasing out</strong> this item or applying markdowns. Return frequency or low margins make this a poor asset.</p>
							{:else}
								<p class="text-sm">Performance is consistent. <strong>Maintain current stock levels</strong> and monitor weekly for any shifts in sell-through rate.</p>
							{/if}
						</div>
					</div>
				</div>
			{:else}
				<div class="bg-surface-2 p-8 rounded-lg border-2 border-dashed border-border flex-1 flex flex-col items-center justify-center text-center text-text-muted">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
					</svg>
					<p>Fill out the item details and click analyze to see AI-powered stock recommendations.</p>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	/* Custom styles for select to match the theme */
	select {
		appearance: none;
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 0.5rem center;
		background-size: 1.5em;
		padding-right: 2.5rem;
	}
</style>
