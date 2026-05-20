<script lang="ts">
	import AlertIcon from '$lib/components/icons/AlertIcon.svelte';
	import type { Snippet } from 'svelte';

	interface Props {
		variant?: 'error' | 'warning' | 'info' | 'success';
		children: Snippet;
		class?: string;
	}

	let { variant = 'error', children, class: className = '' }: Props = $props();

	const variants = {
		error: 'bg-red-50 border-red-200 text-red-600',
		warning: 'bg-amber-50 border-amber-200 text-amber-600',
		info: 'bg-blue-50 border-blue-200 text-blue-600',
		success: 'bg-emerald-50 border-emerald-200 text-emerald-600'
	};
</script>

<div class="p-6 rounded-2xl border flex items-center gap-3 {variants[variant]} {className}">
	<AlertIcon class="w-6 h-6 shrink-0" />
	<div class="font-semibold">
		{@render children()}
	</div>
</div>
