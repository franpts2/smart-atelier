<script lang="ts">
	import ToggleButton from './ToggleButton.svelte';
	import ClipboardIcon from '$lib/components/icons/ClipboardIcon.svelte';
	import LightningIcon from '$lib/components/icons/LightningIcon.svelte';

	interface Props {
		value: 'standard' | 'advanced';
		onchange?: (val: 'standard' | 'advanced') => void;
		showIcons?: boolean;
		class?: string;
	}

	let { 
		value = $bindable(), 
		onchange, 
		showIcons = true,
		class: className = '' 
	}: Props = $props();

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
			{#if showIcons}
				<ClipboardIcon class="w-4 h-4" strokeWidth={2.5} />
			{/if}
		{/snippet}
		Standard Rules
	</ToggleButton>

	<ToggleButton active={value === 'advanced'} onclick={() => select('advanced')}>
		{#snippet icon()}
			{#if showIcons}
				<LightningIcon class="w-4 h-4" strokeWidth={2.5} />
			{/if}
		{/snippet}
		Advanced Rules
	</ToggleButton>
</div>
