<script lang="ts">
	import type { PredictionResult } from '$lib/types/inventory';

	interface Props {
		prediction: PredictionResult | null;
	}

	let { prediction }: Props = $props();

	function getPriorityLabel(priority: string) {
		switch (priority) {
			case 'High Stock': return { text: '🌟 Top Performer', class: 'bg-accent text-surface-0 border-accent' };
			case 'Low Stock': return { text: '⚠️ Risk / Clearance', class: 'bg-surface-2 text-text-muted border-border' };
			default: return { text: '✅ Stable Asset', class: 'border-accent text-accent bg-surface-0' };
		}
	}
</script>

<div class="flex flex-col h-full">
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
		<div class="bg-surface-2 p-8 rounded-lg border-2 border-dashed border-border flex-1 flex flex-col items-center justify-center text-center text-text-muted min-h-[400px]">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
			</svg>
			<p>Fill out the item details and click analyze to see AI-powered stock recommendations.</p>
		</div>
	{/if}
</div>
