<script lang="ts">
	import { onMount } from 'svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import RulesetToggle from '$lib/components/ui/RulesetToggle.svelte';
	import PriorityDistributionChart from '$lib/components/analytics/PriorityDistributionChart.svelte';
	import ModelComparisonChart from '$lib/components/analytics/ModelComparisonChart.svelte';
	import ModelMetricsTable from '$lib/components/analytics/ModelMetricsTable.svelte';
	import ProgressBar from '$lib/components/ui/ProgressBar.svelte';
	import PageHeader from '$lib/components/ui/PageHeader.svelte';
	import LoadingState from '$lib/components/ui/LoadingState.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import RulesetProfile from '$lib/components/inventory/RulesetProfile.svelte';
	import { fetchDataDistribution, fetchModelComparison } from '$lib/services/api';
	import { THEME_COLORS } from '$lib/constants';
	import type { DualRulesetDistribution, DualRulesetComparison, DistributionItem, ModelMetric } from '$lib/types/analytics';

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
	<PageHeader 
		title="Analytics Dashboard" 
		description="Compare Standard and Advanced stocking rule performance and training set statistics"
	>
		<RulesetToggle bind:value={selectedRuleset} />
	</PageHeader>

	{#if loading}
		<LoadingState message="Loading analytics datasets and evaluating models..." />
	{:else if error}
		<Alert variant="error">{error}</Alert>
	{:else}
		<!-- Pedagogical Profile Card -->
		<div class="mb-10">
			<RulesetProfile type={selectedRuleset} />
		</div>

		<!-- Data distribution section -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
			<Card title="Priority Distribution">
				<p class="text-sm text-text-muted mb-4">
					How items are distributed across priority classes in the training set
				</p>
				<PriorityDistributionChart data={activeDistribution} />
			</Card>

			<Card title="Total Samples" class="h-full flex flex-col">
				<p class="text-sm text-text-muted">Breakdown of priority counts under the active ruleset</p>
				<div class="flex-1 flex flex-col justify-center space-y-6">
					{#each activeDistribution as item}
						<ProgressBar 
							label={item.label} 
							value={item.count} 
							maxValue={Math.max(...activeDistribution.map(d => d.count))}
							color={THEME_COLORS[activeDistribution.indexOf(item)]}
						/>
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

			<ModelMetricsTable models={activeModels} />
		</Card>
	{/if}
</div>
