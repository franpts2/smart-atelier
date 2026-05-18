<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title?: string;
		children: Snippet;
		class?: string;
	}

	let { title, children, class: className = '' }: Props = $props();
</script>

<div class="bg-surface-0 p-8 rounded-lg border border-border shadow-sm {className}">
	{#if title}
		<h2 class="text-xl mb-6">{title}</h2>
	{/if}
	{@render children()}
</div>
