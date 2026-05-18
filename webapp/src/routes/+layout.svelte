<script lang="ts">
	import '../app.css';
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
	<title>Smart Atelier</title>
</svelte:head>


<div class="flex flex-col min-h-screen overflow-hidden">
	<Header />

	<main class="flex-grow flex flex-col justify-center">
		<div class="container">
			{@render children()}
		</div>
	</main>

	<Footer />
</div>
