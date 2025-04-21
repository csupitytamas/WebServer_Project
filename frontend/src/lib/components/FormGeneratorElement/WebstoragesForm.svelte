<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import FormGeneratorv2 from '$lib/components/FormGeneratorv2.svelte';
	import { accessToken } from '$lib/stores/auth';
	import axios from 'axios';
	import { onMount } from 'svelte';

	let webstoragesData: any[] = [];

	const webstorageFields = [
		{ databaseName: 'w_id', label: 'W_ID', placeholder: 'W_ID', type: 'number' },
		{ databaseName: 'allapot', label: 'Allapot', placeholder: 'Allapot', type: 'number' },
		{ databaseName: 'meret', label: 'Méret', placeholder: 'Méret', type: 'number' },
		{ databaseName: 'd_id', label: 'Dij ID', placeholder: 'Dij ID', type: 'number' },
		{ databaseName: 'u_id', label: 'UID', placeholder: 'UID', type: 'number' }
	];

	let inputWebstorages = webstorageFields.map((field) => ({
		...field,
		value: field.type === 'number' ? '' : ''
	}));

	async function onMountLoading() {
		try {
			const response = await axios.get(`${PUBLIC_API_URL}/api/get_webtarhelyek`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			});
			webstoragesData = response.data.map((item: any) =>
				webstorageFields.map((field) => ({
					value: item[field.databaseName],
					label: field.databaseName,
					placeholder: ''
				}))
			);
		} catch (error) {
			console.error('Hiba a webstoragek lekérésekor:', error);
			webstoragesData = [];
		}
	}

	onMount(onMountLoading);
</script>

<FormGeneratorv2
	title="Webstorage létrehozás"
	inputs={inputWebstorages}
	data={webstoragesData}
	updateEndpoint={`${PUBLIC_API_URL}/api/update_webtarhely`}
	deleteEndpoint={`${PUBLIC_API_URL}/api/delete_webtarhely`}
	addEndpoint={`${PUBLIC_API_URL}/api/create_webtarhely`}
	primaryKey="w_id"
	onMountFunctions={onMountLoading}
/>
