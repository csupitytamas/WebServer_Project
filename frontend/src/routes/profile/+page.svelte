<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import { accessToken } from '$lib/stores/auth';
	import { plans } from '$lib/stores/plans';
	import axios from 'axios';
	import { onMount } from 'svelte';
	import { jwtDecode } from 'jwt-decode';

	let userData = $state();

	let profileData = $state(null);

	function getUserIdFromJWT(token) {
		const decoded = jwtDecode(token);
		return decoded.sub;
	}

	onMount(() => {
		axios
			.get(`${PUBLIC_API_URL}/api/felhasznaloi_adatok?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				userData = response.data;
			});
		const userId = getUserIdFromJWT($accessToken);

		axios
			.get(`${PUBLIC_API_URL}/api/get_user/${userId}?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				profileData = response.data;
			});
	});

	function payInvoice(ivoiceId: number) {
		console.log(ivoiceId);
		axios
			.put(
				`${PUBLIC_API_URL}/api/fizetes/${ivoiceId}?token=${$accessToken}`,
				{},
				{
					headers: {
						Authorization: `Bearer ${$accessToken}`,
						'Content-Type': 'application/json'
					}
				}
			)
			.then((response) => {
				if (response.data.message) {
					alert(response.data.message + ' A számlát kifizettük.');
				} else {
					alert('Hiba történt a számla kifizetésekor!');
				}
			});
	}
</script>

<div class="w-lg w-full rounded-lg bg-white p-6 shadow-md">
	<div>
		<h2 class="text-2xl font-bold">Profil adatok:</h2>
		{#if profileData}
			<p>Név: {profileData.nev}</p>
			<p>Email: {profileData.email}</p>
			<p>Szerep: {profileData.szerep == '1' ? 'Admin' : 'Felhasználó'}</p>
		{:else}
			<p>Nincsenek profil adataid.</p>
		{/if}
	</div>
</div>
<div class="mx-auto flex justify-center">
	<div class="w-lg w-full rounded-lg bg-white p-6 shadow-md">
		<div>
			<h2 class="text-2xl font-bold">Domainjeid:</h2>
			{#if userData}
				{#each userData.domainjeim as domain}
					<p>{domain}</p>
					<hr />
				{/each}
			{:else}
				<p>Nincsenek domainjeid.</p>
			{/if}
		</div>
	</div>

	<div class="w-lg w-full rounded-lg bg-white p-6 shadow-md">
		<div>
			<h2 class="text-2xl font-bold">Számláid:</h2>
			{#if userData}
				{#each userData.szamlak as szamla}
					<p>Azonosító: {szamla.szamla_id}</p>
					<p>Összeg: {szamla.osszeg} Ft</p>
					<p>Dátum: {szamla.datum}</p>
					<p>Állapot: {szamla.allapot_nev}</p>
					{#if szamla.allapot_id === 1}
						<p class="text-green-500">Fizetve</p>
					{:else if szamla.allapot_id === 2}
						<p class="text-red-500">Nem fizetve</p>
					{:else if szamla.allapot_id === 3}
						<p class="text-yellow-500">Függőben</p>
						<button class="text-blue-500 underline" onclick={() => payInvoice(szamla.szamla_id)}
							>Fizetés</button
						>
					{/if}
					<hr />
				{/each}
			{:else}
				<p>Nincsenek számláid.</p>
			{/if}
		</div>
	</div>

	<div class="w-lg w-full rounded-lg bg-white p-6 shadow-md">
		<div>
			<h2 class="text-2xl font-bold">Előfizetéseid:</h2>
			{#if userData}
				{#each userData.elofizetesek as elofizetes}
					<p>Azonosító: {elofizetes.dijcsomag_id}</p>
					<p>Dátum: {elofizetes.nev}</p>
					<hr />
				{/each}
			{:else}
				<p>Nincsenek előfizetéseid.</p>
			{/if}
		</div>
	</div>
</div>
