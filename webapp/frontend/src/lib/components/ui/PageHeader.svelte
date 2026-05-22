<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title: string;
		description?: string;
		children?: Snippet;
		class?: string;
		center?: boolean;
	}

	let { 
		title, 
		description, 
		children, 
		class: className = '',
		center = false
	}: Props = $props();
</script>

<div class="mb-8 p-6 rounded-2xl bg-surface-1 border border-border shadow-sm {center ? 'text-center' : 'flex flex-col md:flex-row md:items-center md:justify-between'} gap-6 {className}">
	<div class={center ? 'max-w-2xl mx-auto' : ''}>
		<h1 class="text-3xl font-bold mb-1">{title}</h1>
		{#if description}
			<p class="text-text-muted text-sm">{description}</p>
		{/if}
	</div>
	
	{#if children}
		<div class={center ? 'flex justify-center' : ''}>
			{@render children()}
		</div>
	{/if}
</div>
