<script lang="ts">
	import type { HTMLSelectAttributes } from 'svelte/elements';
	import type { Snippet } from 'svelte';

	interface Props extends HTMLSelectAttributes {
		value: string | number;
		children: Snippet;
		placeholder?: string;
	}

	let { value = $bindable(), children, placeholder, class: className = '', ...rest }: Props = $props();
</script>

<select 
	bind:value={value}
	class="p-2 rounded border border-border bg-surface-1 focus:ring-2 focus:ring-accent outline-none {className}"
	{...rest}
>
	{#if placeholder}
		<option value="">{placeholder}</option>
	{/if}
	{@render children()}
</select>

<style>
	select {
		appearance: none;
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 0.5rem center;
		background-size: 1.5em;
		padding-right: 2.5rem;
	}
</style>
