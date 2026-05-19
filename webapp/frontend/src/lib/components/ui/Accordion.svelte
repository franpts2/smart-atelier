<script lang="ts">
	interface Props {
		title: string;
		children?: import('svelte').Snippet;
		isOpen?: boolean;
	}

	let { title, children, isOpen: initialOpen = false }: Props = $props();
	let isOpen = $state(initialOpen);

	function toggle() {
		isOpen = !isOpen;
	}
</script>

<div class="border-b border-slate-200 dark:border-slate-800">
	<button
		type="button"
		class="flex w-full items-center justify-between py-4 text-sm font-medium transition-all hover:underline [&[aria-expanded=true]>svg]:rotate-180"
		onclick={toggle}
		aria-expanded={isOpen}
	>
		{title}
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="24"
			height="24"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
			class="h-4 w-4 shrink-0 transition-transform duration-200"
		>
			<polyline points="6 9 12 15 18 9"></polyline>
		</svg>
	</button>
	{#if isOpen}
		<div class="overflow-hidden text-sm transition-all pb-4">
			{@render children?.()}
		</div>
	{/if}
</div>
