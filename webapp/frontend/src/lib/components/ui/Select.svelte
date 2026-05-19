<script lang="ts">
	import { onMount } from 'svelte';
	import ChevronDownIcon from "../icons/ChevronDownIcon.svelte";

	interface Option {
		value: string | number;
		label: string;
	}

	interface Props {
		value: string | number;
		options?: (Option | string)[];
		placeholder?: string;
		disabled?: boolean;
		class?: string;
		id?: string;
		direction?: 'up' | 'down';
	}

	let { 
		value = $bindable(), 
		options = [], 
		placeholder = "Select an option", 
		disabled = false,
		class: className = '',
		id,
		direction = 'down'
	}: Props = $props();

	let isOpen = $state(false);
	let container: HTMLDivElement;

	function toggle() {
		if (!disabled) isOpen = !isOpen;
	}

	function selectOption(optValue: string | number) {
		value = optValue;
		isOpen = false;
	}

	// Close when clicking outside
	function handleClickOutside(event: MouseEvent) {
		if (isOpen && container && !container.contains(event.target as Node)) {
			isOpen = false;
		}
	}

	onMount(() => {
		window.addEventListener('click', handleClickOutside);
		return () => window.removeEventListener('click', handleClickOutside);
	});

	const normalizedOptions = $derived(options.map(opt => 
		typeof opt === 'string' ? { value: opt, label: opt } : opt
	));

	const selectedOption = $derived(normalizedOptions.find(opt => opt.value === value));
</script>

<div class="relative w-full {className}" bind:this={container} {id}>
	<button
		type="button"
		class="flex w-full items-center justify-between p-2 rounded border border-border bg-surface-1 focus:ring-2 focus:ring-accent outline-none text-left disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
		onclick={toggle}
		aria-haspopup="listbox"
		aria-expanded={isOpen}
		{disabled}
	>
		<span class="truncate">
			{selectedOption ? selectedOption.label : placeholder}
		</span>
		<ChevronDownIcon class="h-4 w-4 shrink-0 transition-transform duration-200 {isOpen ? 'rotate-180' : ''}" />
	</button>

	{#if isOpen}
		<ul
			class="absolute z-[100] w-full overflow-auto rounded-md border border-border bg-surface-0 shadow-lg focus:outline-none {direction === 'up' ? 'bottom-full mb-1' : 'top-full mt-1'} max-h-60"
			role="listbox"
		>
			{#each normalizedOptions as opt}
				<li>
					<button
						type="button"
						class="w-full text-left relative cursor-pointer select-none py-2 px-3 text-sm hover:bg-surface-2 transition-colors {value === opt.value ? 'bg-surface-2 font-semibold' : ''}"
						role="option"
						aria-selected={value === opt.value}
						onclick={() => selectOption(opt.value)}
					>
						{opt.label}
					</button>
				</li>
			{/each}
			{#if normalizedOptions.length === 0}
				<li class="py-2 px-3 text-sm text-text-muted italic">No options available</li>
			{/if}
		</ul>
	{/if}
</div>

<style>
	/* Custom scrollbar for the dropdown */
	ul::-webkit-scrollbar {
		width: 6px;
	}
	ul::-webkit-scrollbar-track {
		background: transparent;
	}
	ul::-webkit-scrollbar-thumb {
		background: var(--color-border);
		border-radius: 3px;
	}
	ul::-webkit-scrollbar-thumb:hover {
		background: var(--color-text-muted);
	}
</style>
