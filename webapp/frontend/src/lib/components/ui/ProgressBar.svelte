<script lang="ts">
	interface Props {
		label: string;
		value: number;
		maxValue: number;
		color?: string;
		unit?: string;
		class?: string;
	}

	let { 
		label, 
		value, 
		maxValue, 
		color = '#0F172A', 
		unit = 'samples',
		class: className = ''
	}: Props = $props();

	let percentage = $derived(maxValue > 0 ? (value / maxValue) * 100 : 0);
</script>

<div class="space-y-2 {className}">
	<div class="flex items-center justify-between">
		<span class="font-medium text-text">{label}</span>
		<span class="text-text-muted text-sm tabular-nums">{value} {unit}</span>
	</div>
	<div class="w-full h-2.5 bg-surface-2 rounded-full overflow-hidden">
		<div
			class="h-full rounded-full transition-all duration-500"
			style="width: {percentage}%; background-color: {color};"
		></div>
	</div>
</div>
