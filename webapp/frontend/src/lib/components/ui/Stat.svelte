<script lang="ts">
	interface Props {
		label: string;
		value: string | number;
		valueClass?: string;
	}

	let { label, value, valueClass = '' }: Props = $props();
</script>

<div class="p-4 bg-surface-1 rounded border border-border">
	<p class="text-xs text-text-muted uppercase tracking-wider font-bold mb-1">{label}</p>
	<p class="text-xl font-heading {valueClass}">{value}</p>
</div>
