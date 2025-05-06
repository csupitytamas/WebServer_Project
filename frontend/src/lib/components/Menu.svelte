<script lang="ts">
	import { accessToken, isAdmin } from '$lib/stores/auth';

	function logout() {
		$accessToken = '';
		window.location.href = '/login';
	}

	function decodeJwt($accessToken: string | null) {
		if ($accessToken) {
			const payload = $accessToken.split('.')[1];
			const decodedPayload = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
			return JSON.parse(decodedPayload);
		}
		return null;
	}
</script>

<div class="mb-10 flex h-20 w-full items-center justify-between bg-gray-100 px-4 shadow-md">
	<h1 class="text-lg font-bold">Webtárhely&Domain szolgáltató</h1>
	<div class="flex items-center gap-4">
		<a href="/home" class="text-blue-400 underline">Főoldal</a>
		{#if $isAdmin}
			<a href="/admin" class="text-blue-400 underline">Admin</a>
		{/if}
		<a href="/profile" class="text-blue-400 underline">Profil</a>
		<a href="/faq" class="text-blue-400 underline">Gyakori kérdések</a>
	</div>
	<button onclick={logout} class="text-blue-400 underline">Kijelentkezés</button>
</div>
