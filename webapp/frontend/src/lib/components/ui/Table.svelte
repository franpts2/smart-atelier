<script lang="ts" generics="T">
	import type { Snippet } from "svelte";

	interface Props<T> {
		items: T[];
		header: Snippet;
		row: Snippet<[T]>;
		class?: string;
		containerClass?: string;
	}

	let {
		items,
		header,
		row,
		class: tableClass = "",
		containerClass = "",
	}: Props<T> = $props();
</script>

<div class="w-full overflow-x-auto rounded-xl mt-8 {containerClass}">
	<table class="w-full text-sm border-collapse {tableClass}">
		<thead>
			<tr
				class="border-b border-border bg-surface-2/40 text-text-muted text-xs uppercase tracking-wider"
			>
				{@render header()}
			</tr>
		</thead>
		<tbody class="divide-y divide-border">
			{#each items as item}
				<tr class="hover:bg-surface-2/20 transition-colors group">
					{@render row(item)}
				</tr>
			{/each}

			{#if items.length === 0}
				<tr>
					<td
						colspan="100%"
						class="py-12 text-center text-text-muted italic"
					>
						No data available to display in this table.
					</td>
				</tr>
			{/if}
		</tbody>
	</table>
</div>
