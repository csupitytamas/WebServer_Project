<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import { accessToken } from '$lib/stores/auth';
	import { plans } from '$lib/stores/plans';
	import axios from 'axios';
	import { onMount } from 'svelte';

	let topPayingUsers = $state([
		{
			felhasznalo: 'string',
			osszeg: 0
		}
	]);

	let monthlyRevenue = $state([
		{
			honap: 'string',
			bevetel: 0
		}
	]);

	let mostVisitedDomains = $state([
		{
			domain: 'string',
			tulajdonos: 'string',
			megtekintes: 0
		}
	]);

	let mostActiveUsers = $state([
		{
			felhasznalo: 'string',
			domainek: 0,
			webtarhelyek: 0,
			szamlak: 0
		}
	]);
	onMount(() => {
		axios
			.get(`${PUBLIC_API_URL}/api/stats/havi-bevetel?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				monthlyRevenue = response.data;
			});

		axios
			.get(`${PUBLIC_API_URL}/api/stats/legtobbet-fizetok?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				topPayingUsers = response.data;
			});

		axios
			.get(`${PUBLIC_API_URL}/api/stats/legnezettebb-domain?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				mostVisitedDomains = response.data;
			});

		axios
			.get(`${PUBLIC_API_URL}/api/stats/legaktivabb-felhasznalok?token=${$accessToken}`, {
				headers: {
					Authorization: `Bearer ${$accessToken}`,
					'Content-Type': 'application/json'
				}
			})
			.then((response) => {
				mostActiveUsers = response.data;
			});
	});
</script>

<!-- print all data-->

<div class="flex flex-col gap-4 p-4">
	<h1 class="text-2xl font-bold">Statisztikák</h1>
	<div class="flex flex-col gap-4">
		<h2 class="text-xl font-bold">Havi bevétel</h2>
		<table class="table-auto border-collapse border border-gray-300">
			<thead>
				<tr>
					<th class="border border-gray-300 px-4 py-2">Hónap</th>
					<th class="border border-gray-300 px-4 py-2">Bevétel</th>
				</tr>
			</thead>
			<tbody>
				{#each monthlyRevenue as { honap, bevetel }}
					<tr>
						<td class="border border-gray-300 px-4 py-2">{honap}</td>
						<td class="border border-gray-300 px-4 py-2">{bevetel} Ft</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	<div class="flex flex-col gap-4">
		<h2 class="text-xl font-bold">Legtöbbet fizetők</h2>
		<table class="table-auto border-collapse border border-gray-300">
			<thead>
				<tr>
					<th class="border border-gray-300 px-4 py-2">Felhasználó</th>
					<th class="border border-gray-300 px-4 py-2">Összeg</th>
				</tr>
			</thead>
			<tbody>
				{#each topPayingUsers as { felhasznalo, osszeg }}
					<tr>
						<td class="border border-gray-300 px-4 py-2">{felhasznalo}</td>
						<td class="border border-gray-300 px-4 py-2">{osszeg} Ft</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	<div class="flex flex-col gap-4">
		<h2 class="text-xl font-bold">Legnézettebb domain</h2>
		<table class="table-auto border-collapse border border-gray-300">
			<thead>
				<tr>
					<th class="border border-gray-300 px-4 py-2">Domain</th>
					<th class="border border-gray-300 px-4 py-2">Tulajdonos</th>
					<th class="border border-gray-300 px-4 py-2">Megtekintés</th>
				</tr>
			</thead>
			<tbody>
				{#each mostVisitedDomains as { domain, tulajdonos, megtekintes }}
					<tr>
						<td class="border border-gray-300 px-4 py-2">{domain}</td>
						<td class="border border-gray-300 px-4 py-2">{tulajdonos}</td>
						<td class="border border-gray-300 px-4 py-2">{megtekintes}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	<div class="flex flex-col gap-4">
		<h2 class="text-xl font-bold">Legaktívabb felhasználók</h2>
		<table class="table-auto border-collapse border border-gray-300">
			<thead>
				<tr>
					<th class="border border-gray-300 px-4 py-2">Felhasználó</th>
					<th class="border border-gray-300 px-4 py-2">Domainjeim</th>
					<th class="border border-gray-300 px-4 py-2">Webtárhelyeim</th>
					<th class="border border-gray-300 px-4 py-2">Számláim</th>
				</tr>
			</thead>
			<tbody>
				{#each mostActiveUsers as { felhasznalo, domainjeim, webtarhelyeim, szamlak }}
					<tr>
						<td class="border border-gray-300 px-4 py-2">{felhasznalo}</td>
						<td class="border border-gray-300 px-4 py-2">{domainjeim}</td>
						<td class="border border-gray-300 px-4 py-2">{webtarhelyeim}</td>
						<td class="border border-gray-300 px-4 py-2">{szamlak}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
