<script lang="ts">
	import ShieldCheckIcon from '$lib/components/icons/ShieldCheckIcon.svelte';
	import FlaskIcon from '$lib/components/icons/FlaskIcon.svelte';

	interface Props {
		type: 'standard' | 'advanced';
		variant?: 'full' | 'compact';
	}

	let { type, variant = 'full' }: Props = $props();
</script>

{#if variant === 'full'}
	<div class="p-6 rounded-2xl bg-surface-1 border border-border shadow-sm relative overflow-hidden flex flex-col md:flex-row gap-6 items-start md:items-center">
		<!-- Subtle background glow -->
		<div class="absolute -right-16 -top-16 w-48 h-48 rounded-full bg-accent/5 blur-3xl pointer-events-none"></div>
		
		<div class="p-3.5 rounded-xl bg-accent/10 text-accent shrink-0">
			{#if type === 'standard'}
				<ShieldCheckIcon class="w-7 h-7" />
			{:else}
				<FlaskIcon class="w-7 h-7" />
			{/if}
		</div>
		
		<div class="flex-1">
			<h2 class="text-lg font-bold mb-1 text-text">
				{type === 'standard' ? 'Standard Ruleset Profile (Ratings-Based)' : 'Advanced Ruleset Profile (Velocity & Profit-Aware)'}
			</h2>
			<p class="text-sm text-text-muted leading-relaxed">
				{#if type === 'standard'}
					Classified strictly using client ratings and returns: <code class="px-1.5 py-0.5 rounded bg-surface-2 text-accent font-semibold text-xs border border-border">Rating &gt; 4.0</code> (No returns) triggers <strong>High Stock</strong>, <code class="px-1.5 py-0.5 rounded bg-surface-2 text-accent font-semibold text-xs border border-border">Rating &lt; 2.0</code> (With returns) triggers <strong>Low Stock</strong>, otherwise <strong>Maintain</strong>.
					This ruleset is easy to predict but prone to stockouts on items that sell fast regardless of rating, and overstocking on items that are highly rated but rarely purchased.
				{:else}
					Classified using inventory turnover velocity and profit margins: combines <code class="px-1.5 py-0.5 rounded bg-surface-2 text-accent font-semibold text-xs border border-border">Net Margin</code>, <code class="px-1.5 py-0.5 rounded bg-surface-2 text-accent font-semibold text-xs border border-border">Units Sold</code> (last 30 days), and customer rating dynamics.
					This ruleset prevents capital tying in slow-moving stock, while boosting replenishment recommendations for highly profitable, high-throughput items.
				{/if}
			</p>
		</div>
	</div>
{:else}
	<p class="text-xs text-text-muted mt-2 px-1 leading-relaxed">
		{#if type === 'standard'}
			<strong>Standard:</strong> Classifies strictly based on customer rating (&gt;4.0) and return history. Easy to predict but reactive.
		{:else}
			<strong>Advanced:</strong> Considers sales velocity (units sold), profit margins, and stock-to-sales ratios. Proactive and profit-aware.
		{/if}
	</p>
{/if}
