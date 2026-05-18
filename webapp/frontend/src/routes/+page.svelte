<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import Hero from '$lib/components/Hero.svelte';
	import ArrowIcon from '$lib/icons/ArrowIcon.svelte';
</script>

<div class="flex flex-col gap-24 items-center">
	<Hero 
		badge="AI-Powered Consulting"
		subtitle="Optimize your stock levels, pricing strategies, and seasonal collections with Smart Atelier's sophisticated AI insights."
	>
		{#snippet title()}
			Inventory Intelligence for <span class="text-accent block">Modern Brands</span>
		{/snippet}

		<Button href="/inventory" variant="primary">
			Get Started
			<ArrowIcon />
		</Button>
		<Button href="/analytics" variant="outline">View Analytics</Button>
	</Hero>
</div>
