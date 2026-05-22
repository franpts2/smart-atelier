<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		label: string;
		id: string;
		children: Snippet;
		class?: string;
	}

	let { label, id, children, class: className = '' }: Props = $props();
</script>

<div class="flex flex-col gap-1 {className}">
	<label for={id} class="text-xs font-semibold text-text-main">{label}</label>
	{@render children()}
</div>
