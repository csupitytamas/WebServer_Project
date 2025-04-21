<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import FormGeneratorv2 from '$lib/components/FormGeneratorv2.svelte';
	import { accessToken } from '$lib/stores/auth';
	import axios from 'axios';
	import { onMount } from 'svelte';

	let domainsData: any[] = [];

	const domainFields = [
		{ databaseName: 'd_id', label: 'D_ID', placeholder: 'D_ID', type: 'number' },
		{ databaseName: 'allapot', label: 'Allapot', placeholder: 'Allapot', type: 'number' },
		{ databaseName: 'domain_nev', label: 'Domain név', placeholder: 'Domain név', type: 'string' },
		{
			databaseName: 'megtekintes',
			label: 'Megtekintés',
			placeholder: 'Megtekintés',
			type: 'number'
		},
		{ databaseName: 'u_id', label: 'UID', placeholder: 'UID', type: 'number' },
		{ databaseName: 'dij_id', label: 'Dij ID', placeholder: 'Dij ID', type: 'number' }
	];

	let inputDomains = domainFields.map((field) => ({
		...field,
		value: field.type === 'number' ? '' : ''
	}));

	async function onMountLoading() {
		try {
			const response = await axios.get(`${PUBLIC_API_URL}/api/get_domains`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			});
			domainsData = response.data.map((item: any) =>
				domainFields.map((field) => ({
					value: item[field.databaseName],
					label: field.databaseName,
					placeholder: ''
				}))
			);
		} catch (error) {
			console.error('Hiba a domainek lekérésekor:', error);
			domainsData = [];
		}
	}

	onMount(onMountLoading);
</script>

<FormGeneratorv2
	title="Domain létrehozás"
	inputs={inputDomains}
	data={domainsData}
	updateEndpoint={`${PUBLIC_API_URL}/api/update_domain`}
	deleteEndpoint={`${PUBLIC_API_URL}/api/delete_domain`}
	addEndpoint={`${PUBLIC_API_URL}/api/create_domain`}
	primaryKey="d_id"
	onMountFunctions={onMountLoading}
/>
