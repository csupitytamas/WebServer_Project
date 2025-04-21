<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import FormGeneratorv2 from '$lib/components/FormGeneratorv2.svelte';
	import { accessToken } from '$lib/stores/auth';
	import axios from 'axios';
	import { onMount } from 'svelte';

	let usersData: any[] = [];

	const userFields = [
		{ databaseName: 'user_id', label: 'User ID', placeholder: 'User ID', type: 'number' },
		{ databaseName: 'nev', label: 'Név', placeholder: 'Név', type: 'string' },
		{ databaseName: 'email', label: 'Email', placeholder: 'Email', type: 'string' },
		{ databaseName: 'szerep', label: 'Szerep', placeholder: 'Szerep', type: 'number' }
	];

	let inputUsers = userFields.map((field) => ({
		...field,
		value: field.type === 'number' ? '' : ''
	}));

	async function onMountLoading() {
		try {
			const response = await axios.get(`${PUBLIC_API_URL}/users?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			});
			usersData = response.data.map((item: any) =>
				userFields.map((field) => ({
					value: item[field.databaseName],
					label: field.databaseName,
					placeholder: ''
				}))
			);
		} catch (error) {
			console.error('Hiba a userek lekérésekor:', error);
			usersData = [];
		}
	}

	onMount(onMountLoading);
</script>

<FormGeneratorv2
	title="Felhasználó létrehozás"
	inputs={inputUsers}
	data={usersData}
	updateEndpoint={`${PUBLIC_API_URL}/api/update_user`}
	deleteEndpoint={`${PUBLIC_API_URL}/api/delete_user`}
	addEndpoint={`${PUBLIC_API_URL}/api/create_user`}
	primaryKey="user_id"
	onMountFunctions={onMountLoading}
/>
