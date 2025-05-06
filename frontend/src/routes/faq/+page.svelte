<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import { accessToken } from '$lib/stores/auth';
	import { plans } from '$lib/stores/plans';
	import axios from 'axios';
	import { onMount } from 'svelte';

	/**
	[
  {
    "t_id": 0,
    "kategoria": 0,
    "kerdes_szoveg": "string",
    "valasz_szoveg": "string"
  }
]*/
	let questions = $state([
		{
			t_id: 0,
			kategoria: 0,
			kerdes_szoveg: 'string',
			valasz_szoveg: 'string'
		}
	]);
	onMount(() => {
		axios
			.get(`${PUBLIC_API_URL}/api/tudastar`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				questions = response.data;
			});
	});
</script>

<div class="mx-auto flex justify-center">
	<div class="w-lg w-full rounded-lg bg-white p-6 shadow-md">
		<div>
			<h2 class="text-2xl font-bold">Gyakori kérdések</h2>
			{#if questions}
				{#each questions as question}
					<div class="mb-4">
						<h3 class="text-xl font-semibold">{question.kerdes_szoveg}</h3>
						<p>{question.valasz_szoveg}</p>
					</div>
				{/each}
			{:else}
				<p>Nincsenek kérdések.</p>
			{/if}
		</div>
	</div>
</div>
