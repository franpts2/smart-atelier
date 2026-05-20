<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Chart, registerables } from 'chart.js';
	import type { ModelMetric } from '$lib/types/analytics';

	Chart.register(...registerables);

	interface Props {
		data: ModelMetric[];
	}

	let { data }: Props = $props();

	let chart: Chart | null = null;
	let observer: ResizeObserver | null = null;

	const metricColors = ['#6C4060', '#7B9DBF', '#0F172A', '#64748B'];

	$effect(() => {
		if (chart && data) {
			chart.data.labels = data.map((d) => d.name);
			chart.data.datasets[0].data = data.map((d) => d.accuracy);
			chart.data.datasets[1].data = data.map((d) => d.precision);
			chart.data.datasets[2].data = data.map((d) => d.recall);
			chart.data.datasets[3].data = data.map((d) => d.f1_score);
			chart.update();
		}
	});

	function buildConfig() {
		return {
			type: 'bar' as const,
			data: {
				labels: data.map((d) => d.name),
				datasets: [
					{
						label: 'Accuracy',
						data: data.map((d) => d.accuracy),
						backgroundColor: metricColors[0],
						borderRadius: 4
					},
					{
						label: 'Precision',
						data: data.map((d) => d.precision),
						backgroundColor: metricColors[1],
						borderRadius: 4
					},
					{
						label: 'Recall',
						data: data.map((d) => d.recall),
						backgroundColor: metricColors[2],
						borderRadius: 4
					},
					{
						label: 'F1 Score',
						data: data.map((d) => d.f1_score),
						backgroundColor: metricColors[3],
						borderRadius: 4
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: {
						position: 'bottom' as const,
						labels: { padding: 20, usePointStyle: true }
					}
				},
				scales: {
					y: { beginAtZero: true, max: 0.7, grid: { color: '#F1F5F9' } },
					x: { grid: { display: false } }
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
