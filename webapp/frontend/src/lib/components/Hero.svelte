<script lang="ts">
	import type { Snippet } from "svelte";
	import Badge from "./ui/Badge.svelte";

	interface Props {
		badge: string;
		title: Snippet;
		subtitle: string;
		children: Snippet;
	}

	let { badge, title, subtitle, children }: Props = $props();
</script>

<section class="text-center max-w-[900px] flex flex-col items-center gap-6">
	<Badge>{badge}</Badge>
	<h1
		class="text-[clamp(2.5rem,8vw,4rem)] leading-[1.1] tracking-[-1px] font-heading text-primary font-bold"
	>
		{@render title()}
	</h1>
	<p class="text-xl text-text-muted max-w-[600px] mb-4">
		{subtitle}
	</p>

	<div class="flex gap-4 mt-4">
		{@render children()}
	</div>
</section>
