<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import FormGeneratorv2 from '$lib/components/FormGeneratorv2.svelte';
	import { accessToken } from '$lib/stores/auth';
	import axios from 'axios';
	import { onMount } from 'svelte';

	let invoicesData: any[] = [];

	const invoiceFields = [
		{ databaseName: 'sz_id', label: 'Számla ID', placeholder: 'Számla ID', type: 'number' },
		{ databaseName: 'osszeg', label: 'Összeg', placeholder: 'Összeg', type: 'number' },
		{
			databaseName: 'letrehozas_datuma',
			label: 'Létrehozás dátuma',
			placeholder: 'Létrehozás dátuma',
			type: 'string'
		},
		{ databaseName: 'u_id', label: 'UID', placeholder: 'UID', type: 'number' },
		{ databaseName: 'all_id', label: 'All ID', placeholder: 'All ID', type: 'number' }
	];

	let inputInvoices = invoiceFields.map((field) => ({
		...field,
		value: field.type === 'number' ? '' : ''
	}));

	async function onMountLoading() {
		try {
			const response = await axios.get(`${PUBLIC_API_URL}/api/get_szamlak?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			});
			invoicesData = response.data.map((item: any) =>
				invoiceFields.map((field) => ({
					value: item[field.databaseName],
					label: field.databaseName,
					placeholder: ''
				}))
			);
		} catch (error) {
			console.error('Hiba a számlák lekérésekor:', error);
			invoicesData = [];
		}
	}

	onMount(onMountLoading);
</script>

<FormGeneratorv2
	title="Számla létrehozás"
	inputs={inputInvoices}
	data={invoicesData}
	updateEndpoint={`${PUBLIC_API_URL}/api/update_szamla`}
	deleteEndpoint={`${PUBLIC_API_URL}/api/delete_szamla`}
	addEndpoint={`${PUBLIC_API_URL}/api/create_szamla`}
	primaryKey="sz_id"
	onMountFunctions={onMountLoading}
/>
