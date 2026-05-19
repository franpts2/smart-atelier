<script lang="ts">
	import ChevronDownIcon from "../icons/ChevronDownIcon.svelte";

	interface Props {
		title: string;
		children?: import('svelte').Snippet;
		isOpen?: boolean;
	}

	let { title, children, isOpen = $bindable(false) }: Props = $props();

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
		<ChevronDownIcon class="h-4 w-4 shrink-0 transition-transform duration-200" />
	</button>
	{#if isOpen}
		<div class="overflow-hidden text-sm transition-all pb-4">
			{@render children?.()}
		</div>
	{/if}
</div>
