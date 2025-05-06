<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import Plan from '$lib/components/Plan.svelte';
	import { accessToken } from '$lib/stores/auth';
	import { plans } from '$lib/stores/plans';
	import axios from 'axios';
	import { onMount } from 'svelte';

	let stage = $state(1);

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

		suggestPlan();
	});

	$inspect($plans);

	let selectedPlanId: Number | null = $state(null);

	function updateSelectedPlanId(id: Number) {
		selectedPlanId = id;
	}

	let domainsInputs: string[] = $state([]);
	function addDomainInput() {
		domainsInputs = [...domainsInputs, ''];
	}

	function createInvoice() {
		axios
			.post(
				`${PUBLIC_API_URL}/api/vasarlas?token=${$accessToken}`,
				{
					dijcsomag_id: selectedPlanId,
					domain_id: domainsInputs,
					meret: 0
				},
				{
					headers: {
						Authorization: `Bearer ${$accessToken}`,
						'Content-Type': 'application/json'
					}
				}
			)
			.then((response) => {
				if (response.data.message) {
					alert(response.data.message + ' A számlát kiállítottuk.');
				} else {
					alert('Hiba történt fizetéskor!');
				}
			});
	}

	let suggestedPlan = $state(null);

	function suggestPlan() {
		axios
			.get(`${PUBLIC_API_URL}/api/ajanlas?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				if (suggestedPlan.detail !== undefined) {
					alert(suggestedPlan.detail);
				} else {
					suggestedPlan = response.data;
				}
			});
	}
</script>

{#if stage === 1}
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

	{#if suggestedPlan !== null}
		<div
			class="fixed bottom-4 right-4 rounded-md bg-yellow-500 px-4 py-2 text-white hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-75"
		>
			<p class="text-lg font-bold">Ajánlott díjcsomag: {suggestedPlan}</p>
		</div>
	{/if}

	{#if selectedPlanId !== null}
		<p class="mt-4 text-center text-lg font-bold">
			Kiválasztott díjcsomag neve: {$plans?.find((e) => e.d_id == selectedPlanId)?.neve}
		</p>
		<button
			class="fixed bottom-4 right-4 rounded-md bg-green-500 px-4 py-2 text-white hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75"
			onclick={() => {
				stage = 2;
			}}
		>
			Tovább a fizetéshez
		</button>
	{/if}
{/if}
{#if stage === 2}
	<div class="flex h-full flex-wrap items-center justify-center gap-4">
		{#each $plans ?? [] as plan (plan.d_id)}
			{#if plan.d_id == selectedPlanId}
				{#if plan.max_domain > 0}
					{#each Array(plan.max_domain) as _, index}
						<div class="mb-4 flex flex-col items-center justify-center gap-2">
							<label for="domain-{index}" class="text-lg font-bold">Domain {index + 1}:</label>
							<input
								type="text"
								id="domain-{index}"
								class="w-full rounded-md border border-gray-300 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
								bind:value={domainsInputs[index]}
							/>
						</div>
					{/each}
					<button
						class="fixed bottom-4 right-4 rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
						onclick={() => {
							stage = 3;
						}}
					>
						Domain hozzáadása
					</button>
				{:else}
					<p class="text-lg font-bold">Nincs lehetőség domain hozzáadására.</p>
					<button
						class="fixed bottom-4 right-4 rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
						onclick={() => {
							stage = 3;
						}}
					>
						Tovább a fizetéshez
					</button>
				{/if}
			{/if}
		{/each}
	</div>
{/if}
{#if stage === 3}
	<div class="flex h-full flex-wrap items-center justify-center gap-4">
		<p class="text-lg font-bold">Fizetési információk:</p>
		<br />
		<p class="text-lg font-bold">
			Kiválasztott díjcsomag neve: {$plans?.find((e) => e.d_id == selectedPlanId)?.neve}
		</p>
		<br />
		<p class="text-lg font-bold">Kiválasztott domain neve: {domainsInputs.join(', ')}</p>
		<br />
		<p class="text-lg font-bold">
			Összeg: {$plans?.find((e) => e.d_id == selectedPlanId)?.ar} Ft
		</p>

		<button
			class="fixed bottom-4 right-4 rounded-md bg-green-500 px-4 py-2 text-white hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75"
			onclick={() => {
				createInvoice();
			}}
		>
			Fizetés
		</button>
	</div>
{/if}
