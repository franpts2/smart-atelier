<script lang="ts">
	import Card from "$lib/components/ui/Card.svelte";
	import Stat from "$lib/components/ui/Stat.svelte";
	import BarChartIcon from "$lib/components/icons/BarChartIcon.svelte";
	import { PRIORITY_LABELS } from "$lib/constants";
	import type { PredictionResult } from "$lib/types/inventory";

	interface Props {
		prediction: PredictionResult | null;
	}

	let { prediction }: Props = $props();

	function getPriorityLabel(priority: string) {
		switch (priority) {
			case "High Stock":
				return {
					text: `🌟 ${PRIORITY_LABELS["High Stock"]}`,
					class: "bg-accent text-surface-0 border-accent",
				};
			case "Low Stock":
				return {
					text: `⚠️ ${PRIORITY_LABELS["Low Stock"]}`,
					class: "bg-surface-2 text-text-muted border-border",
				};
			default:
				return {
					text: `✅ ${PRIORITY_LABELS["Maintain"]}`,
					class: "border-accent text-accent bg-surface-0",
				};
		}
	}
</script>

<div class="flex flex-col h-full">
	{#if prediction}
		{@const label = getPriorityLabel(prediction.priority)}
		<Card
			title="AI Recommendation"
			class="flex-1 animate-in fade-in slide-in-from-bottom-4 duration-500"
		>
			<div class="flex flex-col items-center text-center space-y-6">
				<div
					class="py-3 px-6 rounded-full border {label.class} text-lg font-bold"
				>
					{label.text}
				</div>

				<div class="grid grid-cols-2 gap-8 w-full">
					<Stat
						label="Net Margin"
						value="${prediction.net_margin}"
						valueClass="text-2xl text-primary"
					/>
					<Stat
						label="Status"
						value={prediction.priority}
						valueClass="font-semibold"
					/>
				</div>

				<div
					class="text-left w-full space-y-4 pt-4 border-t border-border"
				>
					<h3
						class="text-sm uppercase text-text-muted tracking-widest"
					>
						Business Insights
					</h3>
					{#if prediction.priority === "High Stock"}
						<p class="text-sm">
							This item shows strong market potential. We
							recommend <strong>increasing inventory</strong> levels
							to capitalize on high demand and low return rates.
						</p>
					{:else if prediction.priority === "Low Stock"}
						<p class="text-sm">
							High risk detected. Consider <strong
								>phasing out</strong
							> this item or applying markdowns. Return frequency or
							low margins make this a poor asset.
						</p>
					{:else}
						<p class="text-sm">
							Performance is consistent. <strong
								>Maintain current stock levels</strong
							> and monitor weekly for any shifts in sell-through rate.
						</p>
					{/if}
				</div>
			</div>
		</Card>
	{:else}
		<div
			class="bg-surface-2 p-8 rounded-lg border-2 border-dashed border-border flex-1 flex flex-col items-center justify-center text-center text-text-muted min-h-[400px]"
		>
			<BarChartIcon class="h-12 w-12 mb-4 opacity-20" />
			<p>
				Fill out the item details and click analyze to see AI-powered
				stock recommendations.
			</p>
		</div>
	{/if}
</div>
