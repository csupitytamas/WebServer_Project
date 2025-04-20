<script lang="ts">
	import { jwtDecode } from 'jwt-decode';
	import { accessToken } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import FormGenerator, {
		type ButtonProps,
		type FormProps,
		type InputProps
	} from '$lib/components/FormGenerator.svelte';
	import { PUBLIC_API_URL } from '$env/static/public';
	import axios from 'axios';

	let dataFlights: InputProps[][] = $state([]);

	onMount(async () => {
		if ($accessToken) {
			const decoded = jwtDecode($accessToken);
			if (decoded.role === 0) {
				window.location.href = '/home';
			}
		}

		// domain fetch

		const domains = await axios.get(`${PUBLIC_API_URL}/api/get_domains`, {
			headers: {
				Authorization: `Bearer ${$accessToken}`,
				'Content-Type': 'application/json'
			}
		});
		dataFlights = domains.data.map((item: any) => {
			return [
				{ value: item.d_id, label: 'D_ID', placeholder: '' },
				{ value: item.allapot, label: 'Allapot', placeholder: '' },
				{ value: item.domain_nev, label: 'Domain név', placeholder: '' },
				{ value: item.megtekintes, label: 'Megtekintés', placeholder: '' },
				{ value: item.u_id, label: 'UID', placeholder: '' },
				{ value: item.dij_id, label: 'Dij ID', placeholder: '' }
			];
		});
	});

	let inputFlights: InputProps[] = $derived([
		{ placeholder: 'D_ID', value: '', label: 'D_ID' },
		{ placeholder: 'Allapot', value: '', label: 'Allapot' },
		{ placeholder: 'Domain név', value: '', label: 'Domain név' },
		{ placeholder: 'Megtekintés', value: '', label: 'Megtekintés' },
		{ placeholder: 'UID', value: '', label: 'UID' },
		{ placeholder: 'Dij ID', value: '', label: 'Dij ID' }
	]);

	let buttonFlight: ButtonProps = $state({
		text: 'Új domain hozzáadása',
		class: 'mt-4 w-full',
		onclick: async () => {
			const response = await fetch(`${PUBLIC_API_URL}/api/create_domain`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					d_id: inputFlights[0].value,
					allapot: inputFlights[1].value,
					domain_nev: inputFlights[2].value,
					megtekintes: inputFlights[3].value,
					u_id: inputFlights[4].value,
					dij_id: inputFlights[5].value
				})
			});

			let errorMessage = '';
			await response
				.json()
				.then((data) => (data?.error != null ? (errorMessage = data.error) : (errorMessage = '')));

			if (response && response.ok) {
				alert('Sikeresen hozzáadva!');
				dataFlights = [
					[
						{ value: inputFlights[0].value, label: 'D_ID', placeholder: '' },
						{ value: inputFlights[1].value, label: 'Allapot', placeholder: '' },
						{ value: inputFlights[2].value, label: 'Domain név', placeholder: '' },
						{ value: inputFlights[3].value, label: 'Megtekintés', placeholder: '' },
						{ value: inputFlights[4].value, label: 'UID', placeholder: '' },
						{ value: inputFlights[5].value, label: 'Dij ID', placeholder: '' }
					],
					...dataFlights
				];
				flushAllValue(inputFlights);
			} else {
				if (errorMessage.length > 0) {
					alert(errorMessage);
				} else {
					alert('Valami hiba történt');
				}
			}
		}
	});

	let formProps: FormProps = $derived({
		title: 'Járatok kezelése',
		inputs: inputFlights,
		button: buttonFlight,
		apiValue: 'delete_domain',
		data: dataFlights,
		primaryKey: 'd_id'
	});

	function flushAllValue(inputs: InputProps[]) {
		inputs.forEach((input) => {
			input.value = '';
		});
	}
</script>

<FormGenerator
	button={formProps.button}
	bind:inputs={formProps.inputs}
	title={formProps.title}
	data={formProps.data}
	apiValue={formProps.apiValue}
	primaryKey={formProps.primaryKey}
/>
