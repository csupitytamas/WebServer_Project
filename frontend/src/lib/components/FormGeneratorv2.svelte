<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import Input from '$lib/components/ui/input/input.svelte';
	import axios from 'axios';
	import { accessToken } from '$lib/stores/auth';

	let {
		title,
		inputs,
		data,
		updateEndpoint,
		deleteEndpoint,
		addEndpoint,
		primaryKey,
		onMountFunctions
	}: {
		title: string;
		inputs: Array<{ label: string; placeholder: string; value: string | number }>;
		data: Array<Array<{ value: string }>>;
		updateEndpoint: string;
		deleteEndpoint: string;
		addEndpoint: string;
		primaryKey: string;
		onMountFunctions: () => void;
	} = $props();

	let currentState: 'ADD' | 'MODIFY' = $state('ADD');

	let currentItem: Array<{ value: string }> = $state([]);

	function deleteItem(item: Array<{ value: string }>) {
		const primaryKeyIndex = inputs.findIndex(
			(input) => input.databaseName.toLowerCase() === primaryKey.toLowerCase()
		);
		if (primaryKeyIndex !== -1) {
			const primaryKeyValue = item[primaryKeyIndex].value;
			axios
				.delete(deleteEndpoint + `/${primaryKeyValue}?token=${$accessToken}`, {
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${$accessToken}`
					}
				})
				.then((response) => {
					if (response.status === 200) {
						alert('Sikeres törlés!');
						onMountFunctions();
					} else {
						alert('Hiba történt a törlés során!');
					}
				});
		}
	}

	function findPrimaryKeyIndexValue() {
		const primaryKeyIndex = inputs.findIndex(
			(input) => input.databaseName.toLowerCase() === primaryKey.toLowerCase()
		);
		if (primaryKeyIndex !== -1) {
			return currentItem[primaryKeyIndex].value;
		}
		return null;
	}

	function modifyItem() {
		axios
			.put(
				updateEndpoint + `/${findPrimaryKeyIndexValue()}?token=${$accessToken}`,
				transformInput(inputs),
				{
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${$accessToken}`
					}
				}
			)
			.then((response) => {
				if (response.status === 200) {
					alert('Sikeres módosítás!');
					onMountFunctions();
				} else {
					alert('Hiba történt a módosítás során! Tölts ki minden mezőt!');
				}
			});
	}

	function transformInput(inputArray: any) {
		if (!Array.isArray(inputArray)) {
			throw new Error('A bemenetnek tömbnek kell lennie!');
		}

		const result: Record<string, string | null | Number> = {};

		inputArray.forEach((item) => {
			if (item.databaseName !== undefined) {
				if (item.value !== undefined) {
					if (typeof item.type === 'string') {
						if (item.length === 0) {
							result[item.databaseName] = '';
						} else {
							result[item.databaseName] = item.value;
						}
					} else if (typeof item.type === 'number') {
						if (typeof item.value === 'string') {
							result[item.databaseName] = 0;
						} else {
							result[item.databaseName] = item.value;
						}
					} else {
						result[item.databaseName] = null;
					}
				}
			}
		});

		return result;
	}

	function addItem() {
		currentState = 'ADD';
		axios
			.post(addEndpoint + `?token=${$accessToken}`, transformInput(inputs), {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${$accessToken}`
				}
			})
			.then((response) => {
				if (response.status === 200) {
					alert('Sikeres hozzáadás!');
					inputs = inputs.map((input) => {
						return {
							...input,
							value: ''
						};
					});
					onMountFunctions();
				} else {
					alert('Hiba történt a hozzáadás során! Tölts ki minden mezőt!');
				}
			});
	}

	function changeModifyState(item: Array<{ value: string }>) {
		currentState = 'MODIFY';
		currentItem = item;
		inputs = inputs.map((input, index) => {
			return {
				...input,
				value: item[index]?.value || ''
			};
		});
	}

	function changeAddState() {
		currentState = 'ADD';
		inputs = inputs.map((input) => {
			return {
				...input,
				value: ''
			};
		});
	}
</script>

<div class="mt-4">
	<h1 class="mb-5 flex items-center justify-center text-2xl font-bold">{title}</h1>
	<div class=" flex items-center justify-center">
		<div class="grid grid-cols-2 gap-2 px-4 md:w-2/4 md:gap-4 md:px-0">
			{#each inputs as input, i (i)}
				{input.label}
				<Input placeholder={input.placeholder} bind:value={input.value} />
			{/each}
			<div class=""></div>
			<div>
				{#if currentState === 'ADD'}
					<Button class="bg-green-500 text-white" onclick={() => addItem()}
						>Új elem hozzáadása</Button
					>
				{:else if currentState === 'MODIFY'}
					<Button class="bg-blue-500 text-white" onclick={() => modifyItem()}>Módosítás</Button>
					<Button class="bg-red-500 text-white" onclick={() => changeAddState()}>Mégse</Button>
				{/if}
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
							<Button class="bg-blue-500" onclick={() => changeModifyState(item)}
								>Betöltés módosításra</Button
							>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
