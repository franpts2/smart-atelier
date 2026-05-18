<script lang="ts">
	import { page } from '$app/state';
	import type { Snippet } from 'svelte';

	interface Props {
		href: string;
		children: Snippet;
	}

	let { href, children }: Props = $props();

	let isActive = $derived(page.url.pathname === href);
</script>

<li>
	<a
		{href}
		class="no-underline text-[0.95rem] font-medium transition-colors duration-200 hover:text-primary relative group {isActive
			? 'text-text-main'
			: 'text-text-muted'}"
	>
		{@render children()}
		<span
			class="absolute -bottom-1 left-0 h-0.5 bg-accent transition-all duration-200 group-hover:w-full {isActive
				? 'w-full'
				: 'w-0'}"
		></span>
	</a>
</li>
