<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Chart, registerables } from 'chart.js';
	import type { DistributionItem } from '$lib/types/analytics';
	import { THEME_COLORS } from '$lib/constants';

	Chart.register(...registerables);

	interface Props {
		data: DistributionItem[];
	}

	let { data }: Props = $props();

	let chart: Chart | null = null;
	let observer: ResizeObserver | null = null;

	$effect(() => {
		if (chart && data) {
			chart.data.labels = data.map((d) => d.label);
			chart.data.datasets[0].data = data.map((d) => d.count);
			chart.data.datasets[0].backgroundColor = THEME_COLORS.slice(0, data.length);
			chart.update();
		}
	});

	function buildConfig() {
		return {
			type: 'doughnut' as const,
			data: {
				labels: data.map((d) => d.label),
				datasets: [{
					data: data.map((d) => d.count),
					backgroundColor: THEME_COLORS.slice(0, data.length),
					borderWidth: 0
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: {
						position: 'bottom' as const,
						labels: { padding: 20, usePointStyle: true }
					}
				}
			}
		};
	}

	function createChart(node: HTMLCanvasElement) {
		const parent = node.parentElement!;
		if (parent.clientWidth === 0 || parent.clientHeight === 0) return false;
		chart?.destroy();
		chart = new Chart(node, buildConfig());
		return true;
	}

	function mount(node: HTMLCanvasElement) {
		if (!createChart(node)) {
			observer = new ResizeObserver(() => {
				if (createChart(node)) observer?.disconnect();
			});
			observer.observe(node.parentElement!);
		}
		return {
			destroy() {
				chart?.destroy();
				observer?.disconnect();
			}
		};
	}

	onDestroy(() => {
		chart?.destroy();
		observer?.disconnect();
	});
</script>

<div class="relative h-72 w-full">
	<canvas use:mount class="block w-full h-full"></canvas>
</div>
