<script lang="ts">
	import { onMount } from 'svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import PriorityDistributionChart from '$lib/components/analytics/PriorityDistributionChart.svelte';
	import ModelComparisonChart from '$lib/components/analytics/ModelComparisonChart.svelte';
	import { fetchDataDistribution, fetchModelComparison } from '$lib/services/api';
	import type { DistributionItem, ModelMetric } from '$lib/types/analytics';

	let distribution = $state<DistributionItem[]>([]);
	let models = $state<ModelMetric[]>([]);
	let loading = $state(true);
	let error = $state('');

	onMount(async () => {
		try {
			const [dist, mod] = await Promise.all([
				fetchDataDistribution(),
				fetchModelComparison()
			]);
			distribution = dist;
			models = mod;
		} catch (e: any) {
			error = e.message || 'Failed to load analytics';
		} finally {
			loading = false;
		}
	});
</script>

<div class="max-w-6xl mx-auto py-12 px-4">
	<h1 class="text-3xl mb-2">Analytics</h1>
	<p class="text-text-muted mb-10">Model performance and training data overview</p>

	{#if loading}
		<p class="text-text-muted">Loading analytics...</p>
	{:else if error}
		<p class="text-red-500">{error}</p>
	{:else}
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
			<Card title="Priority Distribution">
				<p class="text-sm text-text-muted mb-4">
					How items are distributed across priority classes in the training set
				</p>
				<PriorityDistributionChart data={distribution} />
			</Card>

			<Card title="Total Samples">
				<p class="text-sm text-text-muted mb-4">Breakdown by priority class</p>
				<div class="space-y-4">
					{#each distribution as item}
						<div class="flex items-center justify-between">
							<span class="font-medium">{item.label}</span>
							<span class="text-text-muted tabular-nums">{item.count} samples</span>
						</div>
						<div class="w-full h-2 bg-surface-2 rounded-full overflow-hidden">
							<div
								class="h-full rounded-full transition-all"
								style="width: {(item.count / Math.max(...distribution.map(d => d.count))) * 100}%;
									background: {['#6C4060', '#7B9DBF', '#0F172A'][distribution.indexOf(item)]}"
							></div>
						</div>
					{/each}
				</div>
			</Card>
		</div>

		<Card title="Model Comparison">
			<p class="text-sm text-text-muted mb-3">
				Performance metrics across all trained models
			</p>
			<ModelComparisonChart data={models} />

			<div class="overflow-x-auto mt-8">
				<table class="w-full text-sm">
					<thead>
						<tr class="border-b border-border">
							<th class="text-left py-3 pr-4 font-semibold">Model</th>
							<th class="text-right py-3 px-2 font-semibold">Accuracy</th>
							<th class="text-right py-3 px-2 font-semibold">Precision</th>
							<th class="text-right py-3 px-2 font-semibold">Recall</th>
							<th class="text-right py-3 px-2 font-semibold">F1 Score</th>
						</tr>
					</thead>
					<tbody>
						{#each models as model}
							<tr class="border-b border-border">
								<td class="py-3 pr-4 font-medium">{model.name}</td>
								<td class="text-right py-3 px-2 tabular-nums">{(model.accuracy * 100).toFixed(1)}%</td>
								<td class="text-right py-3 px-2 tabular-nums">{(model.precision * 100).toFixed(1)}%</td>
								<td class="text-right py-3 px-2 tabular-nums">{(model.recall * 100).toFixed(1)}%</td>
								<td class="text-right py-3 px-2 tabular-nums">{(model.f1_score * 100).toFixed(1)}%</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</Card>
	{/if}
</div>
