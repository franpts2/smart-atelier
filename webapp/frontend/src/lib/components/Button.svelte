<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		variant?: 'primary' | 'outline';
		href?: string;
		children: Snippet;
		class?: string;
		[key: string]: any;
	}

	let { variant = 'primary', href, children, class: className = '', ...rest }: Props = $props();

	const baseStyles = "inline-flex items-center justify-center px-7 py-3 rounded-lg font-semibold text-[0.95rem] transition-all duration-200 gap-2 border-none cursor-pointer no-underline";
	
	const variants = {
		primary: "bg-primary text-white shadow-[0_4px_14px_0_rgba(15,23,42,0.3)] hover:bg-primary-light hover:-translate-y-px hover:shadow-[0_6px_20px_rgba(15,23,42,0.4)]",
		outline: "bg-transparent border border-border text-text-main hover:bg-surface-2 hover:border-primary border-solid"
	};
</script>

{#if href}
	<a {href} class="{baseStyles} {variants[variant]} {className}" {...rest}>
		{@render children()}
	</a>
{:else}
	<button class="{baseStyles} {variants[variant]} {className}" {...rest}>
		{@render children()}
	</button>
{/if}
