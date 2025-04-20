<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import type { MouseEventHandler } from 'svelte/elements';

	import Button from './ui/button/button.svelte';
	import Input from './ui/input/input.svelte';
	import { accessToken } from '$lib/stores/auth';
	import axios from 'axios';

	export interface InputProps {
		placeholder: string;
		value: string;
		class?: string;
		type?: 'text' | 'password' | 'number' | 'email' | 'date';
		required?: boolean;
		label?: string;
	}
	export interface ButtonProps {
		text: string;
		onclick?: MouseEventHandler<HTMLButtonElement> | null;
		href?: string;
		class?: string;
		type?: 'button' | 'submit';
		look?: 'primary' | 'cta';
		large?: boolean;
	}
	export interface FormProps {
		data: InputProps[][];
		inputs: InputProps[];
		button: ButtonProps;
		title: string;
		apiValue: string;
		primaryKey: string;
	}

	let { inputs = $bindable([]), button, title, data, apiValue, primaryKey }: FormProps = $props();

	async function deleteItem(item: InputProps[]) {
		let primaryKey = item[findPrimaryKeyIndex(item)];
		const response = await axios
			.delete(`${PUBLIC_API_URL}/api/${apiValue}/${primaryKey.value}/?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				if (response.status === 200) {
					alert('Sikeres törlés');
					return response;
				} else {
					throw new Error('Hiba történt a törlés során');
				}
			})
			.catch((error) => {
				console.error(error);
				return null;
			});
	}

	function findPrimaryKeyIndex(item: InputProps[]) {
		return item.findIndex((i) => i.label?.toLowerCase() === primaryKey.toLowerCase());
	}
</script>

<div class="mt-16 md:mt-40">
	<h1 class="mb-5 flex items-center justify-center text-2xl font-bold">{title}</h1>
	<div class=" flex items-center justify-center">
		<div class="grid grid-cols-2 gap-2 px-4 md:w-2/4 md:gap-4 md:px-0">
			{#each inputs as input, i (i)}
				<Input placeholder={input.placeholder} bind:value={input.value} />
				{input.label}
			{/each}
			<div class=""></div>
			<div>
				<Button class={button.class} onclick={() => button.onclick}>
					{button.text}
				</Button>
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
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
