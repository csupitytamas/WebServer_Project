<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import Plan from '$lib/components/Plan.svelte';
	import { accessToken } from '$lib/stores/auth';
	import { plans } from '$lib/stores/plans';
	import axios from 'axios';
	import { onMount } from 'svelte';

	onMount(() => {
		axios
			.get(`${PUBLIC_API_URL}/api/get_dijcsomagok`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				$plans = response.data;
			});
	});

	let selectedPlanId: Number | null = $state(null);

	function updateSelectedPlanId(id: Number) {
		selectedPlanId = id;
	}
</script>

<div class="flex h-full flex-wrap items-center justify-center gap-4">
	{#if $plans === undefined}
		<p>Betöltés...</p>
	{:else if $plans === null || $plans.length === 0}
		<p>Nincs elérhető díjcsomag.</p>
	{/if}
	{#each $plans ?? [] as plan (plan.d_id)}
		<Plan {plan} {updateSelectedPlanId} />
	{/each}
</div>

{#if selectedPlanId !== null}
	<p class="mt-4 text-center text-lg font-bold">
		Kiválasztott díjcsomag neve: {$plans?.find((e) => e.d_id == selectedPlanId)?.neve}
	</p>
{/if}

<button
	class="fixed bottom-4 right-4 rounded-md bg-green-500 px-4 py-2 text-white hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75"
	onclick={() => (window.location.href = '/')}
>
	Tovább a fizetéshez
</button>
