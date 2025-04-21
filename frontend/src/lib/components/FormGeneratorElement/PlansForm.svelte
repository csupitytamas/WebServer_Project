<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import FormGeneratorv2 from '$lib/components/FormGeneratorv2.svelte';
	import { accessToken } from '$lib/stores/auth';
	import axios from 'axios';
	import { onMount } from 'svelte';

	let plansData: any[] = [];

	const planFields = [
		{ databaseName: 'd_id', label: 'D_ID', placeholder: 'D_ID', type: 'number' },
		{ databaseName: 'neve', label: 'Név', placeholder: 'Név', type: 'string' },
		{ databaseName: 'ar', label: 'Ár', placeholder: 'Ár', type: 'number' },
		{ databaseName: 'max_meret', label: 'Max méret', placeholder: 'Max méret', type: 'number' },
		{ databaseName: 'max_domain', label: 'Max domain', placeholder: 'Max domain', type: 'number' }
	];

	let inputPlans = planFields.map((field) => ({
		...field,
		value: field.type === 'number' ? '' : ''
	}));

	async function onMountLoading() {
		try {
			const response = await axios.get(`${PUBLIC_API_URL}/api/get_dijcsomagok`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			});
			plansData = response.data.map((item: any) =>
				planFields.map((field) => ({
					value: item[field.databaseName],
					label: field.databaseName,
					placeholder: ''
				}))
			);
		} catch (error) {
			console.error('Hiba a domainok lekérésekor:', error);
			plansData = [];
		}
	}

	onMount(onMountLoading);
</script>

<FormGeneratorv2
	title="Díjcsomag létrehozás"
	inputs={inputPlans}
	data={plansData}
	updateEndpoint={`${PUBLIC_API_URL}/api/update_dijcsomag`}
	deleteEndpoint={`${PUBLIC_API_URL}/api/delete_dijcsomag`}
	addEndpoint={`${PUBLIC_API_URL}/api/create_dijcsomag`}
	primaryKey="d_id"
	onMountFunctions={onMountLoading}
/>
