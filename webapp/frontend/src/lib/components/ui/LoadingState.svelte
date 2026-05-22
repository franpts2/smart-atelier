<script lang="ts">
	interface Props {
		message?: string;
		class?: string;
	}

	let { 
		message = 'Loading data...', 
		class: className = '' 
	}: Props = $props();
</script>

<div class="flex flex-col items-center justify-center py-20 {className}">
	<div class="w-10 h-10 border-4 border-accent border-t-transparent rounded-full animate-spin mb-4"></div>
	<p class="text-text-muted text-sm font-medium">{message}</p>
</div>
