<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		href: string;
		children: Snippet;
	}

	let { href, children }: Props = $props();
</script>

<li>
	<a {href} class="no-underline text-text-muted text-[0.95rem] font-medium transition-colors duration-200 hover:text-primary relative group">
		{@render children()}
		<span class="absolute -bottom-1 left-0 w-0 h-0.5 bg-accent transition-all duration-200 group-hover:w-full"></span>
	</a>
</li>
