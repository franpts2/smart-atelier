<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		children: Snippet;
		class?: string;
	}

	let { children, class: className = '' }: Props = $props();
</script>

<span class="bg-surface-2 text-text-muted px-4 py-2 rounded-full text-[0.8rem] font-semibold uppercase tracking-[1px] border border-border {className}">
	{@render children()}
</span>
