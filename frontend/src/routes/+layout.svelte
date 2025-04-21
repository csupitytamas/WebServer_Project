<script lang="ts">
	import { goto } from '$app/navigation';
	import { accessToken } from '$lib/stores/auth';
	import { get } from 'svelte/store';
	import '../app.css';
	let { children } = $props();

	$effect(() => {
		if ($accessToken && $accessToken !== null && !isExpired($accessToken)) {
		} else {
			goto('/login', { replaceState: true });
		}
	});

	function decodeJWT(token: string) {
		const payload = token.split('.')[1];
		const decodedPayload = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
		return JSON.parse(decodedPayload);
	}

	function getTokenExpirationDate(token: string) {
		const decodedToken = decodeJWT(token);
		if (decodedToken.exp) {
			return new Date(decodedToken.exp * 1000);
		}
		return null;
	}

	function isExpired(token: string) {
		const expirationDate = getTokenExpirationDate(token);
		if (expirationDate) {
			return expirationDate < new Date();
		}
		return false;
	}
</script>

{@render children()}
