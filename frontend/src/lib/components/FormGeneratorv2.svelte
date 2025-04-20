<script lang="ts">
	import { onMount } from 'svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import Input from '$lib/components/ui/input/input.svelte';
	import { PUBLIC_API_URL } from '$env/static/public';

	export let title: string;
	export let inputs: Array<{ label: string; placeholder: string; value: string }>;
	export let data: Array<Array<{ value: string }>>;

	function deleteItem(item: Array<{ value: string }>) {
		// Implement the delete logic here
		console.log('Deleting item:', item);
	}

	function modifyItem(item: Array<{ value: string }>) {
		inputs = inputs.map((input, index) => {
			return {
				...input,
				value: item[index]?.value || ''
			};
		});
		console.log('Modifying item:', item);
	}

	function addItem() {
		// Implement the add logic here
		console.log('Adding item:', inputs);
	}
</script>

<div class="mt-16 md:mt-40">
	<h1 class="mb-5 flex items-center justify-center text-2xl font-bold">{title}</h1>
	<div class=" flex items-center justify-center">
		<div class="grid grid-cols-2 gap-2 px-4 md:w-2/4 md:gap-4 md:px-0">
			{#each inputs as input, i (i)}
				{input.label}
				<Input placeholder={input.placeholder} bind:value={input.value} />
			{/each}
			<div class=""></div>
			<div>
				<Button class="bg-green-500 text-white" onclick={() => addItem}>Új elem hozzáadása</Button>
			</div>
		</div>
	</div>
	<div class="mt-16">
		<table class="mx-10 mt-10 w-full table-auto">
			<thead>
				<tr>
					{#each inputs as input, i (i)}
						<th class="px-4 py-2">{input.label}</th>
					{/each}
					<th>Műveletek</th>
				</tr>
			</thead>
			<tbody>
				{#each data as item, i (i)}
					<tr>
						{#each item as value, i (i)}
							<td class="border px-4 py-2">{value.value}</td>
						{/each}
						<td class="border px-2 py-2">
							<Button class="bg-red-500" onclick={() => deleteItem(item)}>Törlés</Button>
							<Button class="bg-blue-500" onclick={() => modifyItem(item)}>Módosítás</Button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
