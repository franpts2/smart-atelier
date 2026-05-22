<script lang="ts">
	import ToggleButton from './ToggleButton.svelte';
	import ClipboardIcon from '$lib/components/icons/ClipboardIcon.svelte';
	import LightningIcon from '$lib/components/icons/LightningIcon.svelte';

	interface Props {
		// Value representing the selected ruleset (uses two-way Svelte 5 binding)
		value: 'standard' | 'advanced';
		// Optional callback to listen to selection changes
		onchange?: (val: 'standard' | 'advanced') => void;
		// Optional class name for the wrapper
		class?: string;
	}

	let { value = $bindable(), onchange, class: className = '' }: Props = $props();

	function select(newValue: 'standard' | 'advanced') {
		value = newValue;
		if (onchange) onchange(newValue);
	}
</script>

<div class="relative flex p-1 bg-surface-2 border border-border rounded-lg shadow-inner {className.includes('w-') ? '' : 'w-80 md:w-90'} {className}">
	<!-- Hardware-accelerated sliding backplate highlight pill -->
	<div 
		class="absolute top-1 bottom-1 left-1 rounded-lg bg-accent shadow-md transition-all duration-300 ease-out pointer-events-none"
		style="width: calc(50% - 4px); transform: translateX({value === 'advanced' ? '100%' : '0%'});"
	></div>

	<ToggleButton active={value === 'standard'} onclick={() => select('standard')}>
		{#snippet icon()}
			<ClipboardIcon class="w-4 h-4" strokeWidth={2.5} />
		{/snippet}
		Standard Rules
	</ToggleButton>

	<ToggleButton active={value === 'advanced'} onclick={() => select('advanced')}>
		{#snippet icon()}
			<LightningIcon class="w-4 h-4" strokeWidth={2.5} />
		{/snippet}
		Advanced Rules
	</ToggleButton>
</div>
