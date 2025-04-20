<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import type { Plan } from '$lib/stores/plans';
	let { plan, updateSelectedPlanId }: { plan: Plan; updateSelectedPlanId: any } = $props();
</script>

<Card.Root
	class="w-80 bg-white shadow-md transition-shadow duration-300 ease-in-out hover:shadow-lg "
>
	<Card.Header>
		<Card.Title>{plan.neve}</Card.Title>
		<Card.Description
			><p class="font-bold">{plan.ar} <span class="text-green-500">HUF</span></p></Card.Description
		>
	</Card.Header>

	<Card.Content>
		{#if plan.max_domain !== null}
			<p class=" font-bold">Maximum domain címek:</p>
			<p>{plan.max_domain} darab</p>
		{/if}
		{#if plan.max_meret !== null}
			<p class=" font-bold">Webtárhely mérete:</p>
			<p>{plan.max_meret} MB</p>
		{/if}
	</Card.Content>
	<!-- svelte-ignore a11y_consider_explicit_label -->
	<button
		class={`w-full rounded-md  bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75`}
		onclick={() => updateSelectedPlanId(plan.d_id)}
	>
		Kiválasztás
	</button>
</Card.Root>
