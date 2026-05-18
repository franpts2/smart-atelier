<script lang="ts">
	import { Button, Badge } from '$lib/components';
</script>

<div class="flex flex-col gap-24 items-center">
	<section class="text-center max-w-[900px] flex flex-col items-center gap-6">
		<Badge>AI-Powered Consulting</Badge>
		<h1 class="text-[clamp(2.5rem,8vw,4rem)] leading-[1.1] tracking-[-1px] font-heading text-primary font-bold">Inventory Intelligence for <span class="text-accent-gold block">Modern Brands</span></h1>
		<p class="text-xl text-text-muted max-w-[600px] mb-4">Optimize your stock levels, pricing strategies, and seasonal collections with Smart Atelier's sophisticated AI insights.</p>
		
		<div class="flex gap-4 mt-4">
			<Button href="/inventory" variant="primary">
				Get Started
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
			</Button>
			<Button href="/analytics" variant="outline">View Analytics</Button>
		</div>
	</section>
</div>
