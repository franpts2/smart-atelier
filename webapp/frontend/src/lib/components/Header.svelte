<script lang="ts">
	import NavLink from "./ui/NavLink.svelte";
	import Logo from "./Logo.svelte";
</script>

<header
	class="bg-white/80 backdrop-blur-xl border-b border-border py-4 sticky top-0 z-50"
>
	<div class="container">
		<nav class="flex justify-between items-center">
			<Logo />
			<ul class="flex gap-10 list-none">
				<NavLink href="/dashboard">Dashboard</NavLink>
				<NavLink href="/inventory">Inventory</NavLink>
				<NavLink href="/analytics">Analytics</NavLink>
			</ul>
		</nav>
	</div>
</header>
