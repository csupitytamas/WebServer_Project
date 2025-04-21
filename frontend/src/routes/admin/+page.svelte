<script lang="ts">
	import DomainsForm from '$lib/components/FormGeneratorElement/DomainsForm.svelte';
	import FaqForm from '$lib/components/FormGeneratorElement/FaqForm.svelte';
	import InvoicesForm from '$lib/components/FormGeneratorElement/InvoicesForm.svelte';
	import PlansForm from '$lib/components/FormGeneratorElement/PlansForm.svelte';
	import UsersForm from '$lib/components/FormGeneratorElement/UsersForm.svelte';
	import WebstoragesForm from '$lib/components/FormGeneratorElement/WebstoragesForm.svelte';

	let menus = [
		{
			name: 'Domainok',
			component: DomainsForm
		},
		{
			name: 'Díjcsomagok',
			component: PlansForm
		},
		{
			name: 'Felhasználók',
			component: UsersForm
		},
		{
			name: 'Webtárhelyek',
			component: WebstoragesForm
		},
		{
			name: 'Számlák',
			component: InvoicesForm
		},
		{
			name: 'Tudástár',
			component: FaqForm
		}
	];

	let currentMenu = menus[0].component;
</script>

<div class="flex flex-row items-center justify-center gap-2">
	{#each menus as menu}
		<button
			class="rounded bg-blue-500 px-4 py-2 text-white"
			on:click={() => (currentMenu = menu.component)}
		>
			{menu.name}
		</button>
	{/each}
</div>

<div class="p-4">
	<svelte:component this={currentMenu} />
</div>
