<script lang="ts">
	// We import components from the $lib folder. 
	// The '$lib' alias is a shortcut to 'src/lib'.
	import Button from "$lib/components/ui/Button.svelte";
	import Hero from "$lib/components/Hero.svelte";
	import ArrowIcon from "$lib/components/icons/ArrowIcon.svelte";
</script>

<div class="flex flex-col gap-24 items-center">
	<!-- 
		The Hero component is the main banner at the top of the page.
		We pass it simple text as 'badge' and 'subtitle'.
	-->
	<Hero
		badge="AI-Powered Consulting"
		subtitle="Optimize your stock levels, pricing strategies, and seasonal collections with Smart Atelier's sophisticated AI insights."
	>
		<!-- 
			{#snippet title()} is a Svelte 5 feature. 
			It allows us to pass HTML content into a specific part of the Hero component.
		-->
		{#snippet title()}
			Inventory Intelligence for <span class="text-accent block"
				>Modern Brands</span
			>
		{/snippet}

		<!-- These buttons allow the user to navigate to other parts of the site -->
		<Button href="/inventory" variant="primary">
			Get Started
			<ArrowIcon />
		</Button>
		<Button href="/analytics" variant="outline">View Analytics</Button>
	</Hero>
</div>
