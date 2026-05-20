<script lang="ts">
	interface Props {
		size?: number;
		strokeWidth?: number;
		class?: string;
	}

	let { size, strokeWidth = 2, class: className = "" }: Props = $props();
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	width={size}
	height={size}
	viewBox="0 0 24 24"
	fill="none"
	stroke="currentColor"
	stroke-width={strokeWidth}
	stroke-linecap="round"
	stroke-linejoin="round"
	class={className}
>
	<path d="M13 10V3L4 14h7v7l9-11h-7z" />
</svg>
