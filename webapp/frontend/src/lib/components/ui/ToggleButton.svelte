<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		// Whether this specific toggle button is currently active
		active: boolean;
		// Click callback handler
		onclick: () => void;
		// Customizable Svelte 5 Snippet for the leading icon
		icon?: Snippet;
		// Svelte 5 children snippet for the label text
		children?: Snippet;
	}

	let { active, onclick, icon, children }: Props = $props();
</script>

<button
	type="button"
	class="relative z-10 w-1/2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300 flex items-center justify-center gap-2 {active ? 'text-white' : 'text-text-muted hover:text-text'}"
	{onclick}
>
	{#if icon}
		{@render icon()}
	{/if}
	{#if children}
		{@render children()}
	{/if}
</button>
