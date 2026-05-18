<script lang="ts">
	import type { HTMLInputAttributes } from 'svelte/elements';

	interface Props extends HTMLInputAttributes {
		value: string | number;
	}

	let { value = $bindable(), class: className = '', ...rest }: Props = $props();
</script>

<input 
	bind:value={value}
	class="p-2 rounded border border-border bg-surface-1 focus:ring-2 focus:ring-accent outline-none {className}"
	{...rest}
/>
