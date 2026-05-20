<script lang="ts">
	import { onMount } from 'svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import RulesetToggle from '$lib/components/ui/RulesetToggle.svelte';
	import PriorityDistributionChart from '$lib/components/analytics/PriorityDistributionChart.svelte';
	import ModelComparisonChart from '$lib/components/analytics/ModelComparisonChart.svelte';
	import { fetchDataDistribution, fetchModelComparison } from '$lib/services/api';
	import type { DualRulesetDistribution, DualRulesetComparison, DistributionItem, ModelMetric } from '$lib/types/analytics';
	import AlertIcon from '$lib/components/icons/AlertIcon.svelte';
	import ShieldCheckIcon from '$lib/components/icons/ShieldCheckIcon.svelte';
	import FlaskIcon from '$lib/components/icons/FlaskIcon.svelte';

	let dualDistribution = $state<DualRulesetDistribution | null>(null);
	let dualModels = $state<DualRulesetComparison | null>(null);
	let selectedRuleset = $state<'standard' | 'advanced'>('standard');
	let loading = $state(true);
	let error = $state('');

	// Compute active data based on selection using Svelte 5 reactive derived values
	let activeDistribution = $derived<DistributionItem[]>(
		dualDistribution ? dualDistribution[selectedRuleset] : []
	);
	let activeModels = $derived<ModelMetric[]>(
		dualModels ? dualModels[selectedRuleset] : []
	);

	onMount(async () => {
		try {
			const [dist, mod] = await Promise.all([
				fetchDataDistribution(),
				fetchModelComparison()
			]);
			dualDistribution = dist;
			dualModels = mod;
		} catch (e: any) {
			error = e.message || 'Failed to load analytics';
		} finally {
			loading = false;
		}
	});
</script>

<div class="max-w-6xl mx-auto py-12 px-4">
	<!-- Hero header with ruleset segmented control -->
	<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-8 bg-surface-1 p-6 rounded-2xl border border-border shadow-sm">
		<div>
			<h1 class="text-3xl mb-1 font-bold">Analytics Dashboard</h1>
			<p class="text-text-muted text-sm">Compare Standard and Advanced stocking rule performance and training set statistics</p>
		</div>
		
		<RulesetToggle bind:value={selectedRuleset} />
	</div>

	{#if loading}
		<div class="flex flex-col items-center justify-center py-20">
			<div class="w-10 h-10 border-4 border-accent border-t-transparent rounded-full animate-spin mb-4"></div>
			<p class="text-text-muted text-sm font-medium">Loading analytics datasets and evaluating models...</p>
		</div>
	{:else if error}
		<div class="p-6 rounded-2xl bg-red-50 border border-red-200 text-red-600 flex items-center gap-3">
			<AlertIcon class="w-6 h-6 shrink-0" />
			<p class="font-semibold">{error}</p>
		</div>
	{:else}
		<!-- Pedagogical Profile Card -->
		<div class="mb-10 p-6 rounded-2xl bg-surface-1 border border-border shadow-sm relative overflow-hidden flex flex-col md:flex-row gap-6 items-start md:items-center">
			<!-- Subtle background glow -->
			<div class="absolute -right-16 -top-16 w-48 h-48 rounded-full bg-accent/5 blur-3xl pointer-events-none"></div>
			
			<div class="p-3.5 rounded-xl bg-accent/10 text-accent shrink-0">
				{#if selectedRuleset === 'standard'}
					<ShieldCheckIcon class="w-7 h-7" />
				{:else}
					<FlaskIcon class="w-7 h-7" />
				{/if}
			</div>
			
			<div class="flex-1">
				<h2 class="text-lg font-bold mb-1 text-text">
					{#if selectedRuleset === 'standard'}
						Standard Ruleset Profile (Ratings-Based)
					{:else}
						Advanced Ruleset Profile (Velocity & Profit-Aware)
					{/if}
				</h2>
				<p class="text-sm text-text-muted leading-relaxed">
					{#if selectedRuleset === 'standard'}
						Classified strictly using client ratings and returns: <code class="px-1.5 py-0.5 rounded bg-surface-2 text-accent font-semibold text-xs border border-border">Rating &gt; 4.0</code> (No returns) triggers <strong>High Stock</strong>, <code class="px-1.5 py-0.5 rounded bg-surface-2 text-accent font-semibold text-xs border border-border">Rating &lt; 2.0</code> (With returns) triggers <strong>Low Stock</strong>, otherwise <strong>Maintain</strong>.
						This ruleset is easy to predict but prone to stockouts on items that sell fast regardless of rating, and overstocking on items that are highly rated but rarely purchased.
					{:else}
						Classified using inventory turnover velocity and profit margins: combines <code class="px-1.5 py-0.5 rounded bg-surface-2 text-accent font-semibold text-xs border border-border">Net Margin</code>, <code class="px-1.5 py-0.5 rounded bg-surface-2 text-accent font-semibold text-xs border border-border">Units Sold</code> (last 30 days), and customer rating dynamics.
						This ruleset prevents capital tying in slow-moving stock, while boosting replenishment recommendations for highly profitable, high-throughput items.
					{/if}
				</p>
			</div>
		</div>

		<!-- Data distribution section -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
			<Card title="Priority Distribution">
				<p class="text-sm text-text-muted mb-4">
					How items are distributed across priority classes in the training set
				</p>
				<PriorityDistributionChart data={activeDistribution} />
			</Card>

			<Card title="Total Samples">
				<p class="text-sm text-text-muted mb-4">Breakdown of priority counts under the active ruleset</p>
				<div class="space-y-4">
					{#each activeDistribution as item}
						<div class="flex items-center justify-between">
							<span class="font-medium text-text">{item.label}</span>
							<span class="text-text-muted text-sm tabular-nums">{item.count} samples</span>
						</div>
						<div class="w-full h-2.5 bg-surface-2 rounded-full overflow-hidden">
							<div
								class="h-full rounded-full transition-all duration-500"
								style="width: {(item.count / Math.max(...activeDistribution.map(d => d.count))) * 100}%;
									background: {['#6C4060', '#7B9DBF', '#0F172A'][activeDistribution.indexOf(item)]}"
							></div>
						</div>
					{/each}
				</div>
			</Card>
		</div>

		<!-- Model comparison section -->
		<Card title="Model Comparison">
			<p class="text-sm text-text-muted mb-3">
				Performance metrics across all trained models under the active ruleset
			</p>
			<ModelComparisonChart data={activeModels} />

			<div class="overflow-x-auto mt-8">
				<table class="w-full text-sm">
					<thead>
						<tr class="border-b border-border text-text-muted">
							<th class="text-left py-3 pr-4 font-semibold">Model</th>
							<th class="text-right py-3 px-2 font-semibold">Accuracy</th>
							<th class="text-right py-3 px-2 font-semibold">Precision</th>
							<th class="text-right py-3 px-2 font-semibold">Recall</th>
							<th class="text-right py-3 px-2 font-semibold">F1 Score</th>
						</tr>
					</thead>
					<tbody>
						{#each activeModels as model}
							<tr class="border-b border-border hover:bg-surface-2 transition-colors">
								<td class="py-3 pr-4 font-semibold text-text">{model.name}</td>
								<td class="text-right py-3 px-2 tabular-nums font-bold">{(model.accuracy * 100).toFixed(1)}%</td>
								<td class="text-right py-3 px-2 tabular-nums text-text-muted">{(model.precision * 100).toFixed(1)}%</td>
								<td class="text-right py-3 px-2 tabular-nums text-text-muted">{(model.recall * 100).toFixed(1)}%</td>
								<td class="text-right py-3 px-2 tabular-nums text-accent font-semibold">{(model.f1_score * 100).toFixed(1)}%</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</Card>
	{/if}
</div>
