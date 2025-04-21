<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import FormGeneratorv2 from '$lib/components/FormGeneratorv2.svelte';
	import { accessToken } from '$lib/stores/auth';
	import axios from 'axios';
	import { onMount } from 'svelte';

	/**  {
    "kategoria": 0,
    "kerdes_szoveg": "string",
    "valasz_szoveg": "string"
  }
   */

	let faqsData: any[] = [];

	const faqFields = [
		{ databaseName: 't_id', label: 'T_ID', placeholder: 'T_ID', type: 'number' },
		{ databaseName: 'kategoria', label: 'Kategória', placeholder: 'Kategória', type: 'number' },
		{
			databaseName: 'kerdes_szoveg',
			label: 'Kérdés szöveg',
			placeholder: 'Kérdés szöveg',
			type: 'string'
		},
		{
			databaseName: 'valasz_szoveg',
			label: 'Válasz szöveg',
			placeholder: 'Válasz szöveg',
			type: 'string'
		}
	];

	let inputFaqs = faqFields.map((field) => ({
		...field,
		value: field.type === 'number' ? '' : ''
	}));

	async function onMountLoading() {
		try {
			const response = await axios.get(`${PUBLIC_API_URL}/api/tudastar`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			});
			faqsData = response.data.map((item: any) =>
				faqFields.map((field) => ({
					value: item[field.databaseName],
					label: field.databaseName,
					placeholder: ''
				}))
			);
		} catch (error) {
			console.error('Hiba a kérdések lekérésekor:', error);
			faqsData = [];
		}
	}

	onMount(onMountLoading);
</script>

<FormGeneratorv2
	title="Kérdések létrehozás"
	inputs={inputFaqs}
	data={faqsData}
	updateEndpoint={`${PUBLIC_API_URL}/api/tudastar`}
	deleteEndpoint={`${PUBLIC_API_URL}/api/tudastar`}
	addEndpoint={`${PUBLIC_API_URL}/api/tudastar`}
	primaryKey="t_id"
	onMountFunctions={onMountLoading}
/>
