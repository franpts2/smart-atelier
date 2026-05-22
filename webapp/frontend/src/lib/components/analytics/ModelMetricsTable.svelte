<script lang="ts">
	import Table from '$lib/components/ui/Table.svelte';
	import type { ModelMetric } from '$lib/types/analytics';

	interface Props {
		models: ModelMetric[];
	}

	let { models }: Props = $props();
</script>

<Table items={models} containerClass="mt-8">
	{#snippet header()}
		<th class="text-left py-4 px-6 font-bold">Model</th>
		<th class="text-right py-4 px-6 font-bold">Accuracy</th>
		<th class="text-right py-4 px-6 font-bold">Precision</th>
		<th class="text-right py-4 px-6 font-bold">Recall</th>
		<th class="text-right py-4 px-6 font-bold">F1 Score</th>
	{/snippet}

	{#snippet row(model)}
		<td class="py-4 px-6 font-semibold text-text">{model.name}</td>
		<td class="text-right py-4 px-6 tabular-nums font-bold">{(model.accuracy * 100).toFixed(1)}%</td>
		<td class="text-right py-4 px-6 tabular-nums text-text-muted">{(model.precision * 100).toFixed(1)}%</td>
		<td class="text-right py-4 px-6 tabular-nums text-text-muted">{(model.recall * 100).toFixed(1)}%</td>
		<td class="text-right py-4 px-6 tabular-nums text-accent font-bold">{(model.f1_score * 100).toFixed(1)}%</td>
	{/snippet}
</Table>
