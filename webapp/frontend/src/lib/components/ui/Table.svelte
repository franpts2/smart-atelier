<script lang="ts" generics="T">
	import type { Snippet } from 'svelte';

	interface Props<T> {
		/** Array of data items to display */
		items: T[];
		/** Snippet to render the table header columns (e.g. <th> elements) */
		header: Snippet;
		/** Snippet to render each row's cells (e.g. <td> elements) */
		row: Snippet<[T]>;
		/** Additional classes for the table element */
		class?: string;
		/** Additional classes for the outer overflow container */
		containerClass?: string;
	}

	let { 
		items, 
		header, 
		row, 
		class: tableClass = '',
		containerClass = ''
	}: Props<T> = $props();
</script>

<div class="w-full overflow-x-auto rounded-xl border border-border bg-surface-1 {containerClass}">
	<table class="w-full text-sm border-collapse {tableClass}">
		<thead>
			<tr class="border-b border-border bg-surface-2/40 text-text-muted text-xs uppercase tracking-wider">
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
					<td colspan="100%" class="py-12 text-center text-text-muted italic">
						No data available to display in this table.
					</td>
				</tr>
			{/if}
		</tbody>
	</table>
</div>
