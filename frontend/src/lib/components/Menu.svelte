<script lang="ts">
	import { accessToken } from '$lib/stores/auth';

	function logout() {
		$accessToken = '';
		window.location.href = '/login';
	}
</script>

<div class="mb-10 flex h-20 w-full items-center justify-between bg-gray-100 px-4 shadow-md">
	<h1 class="text-lg font-bold">Webtárhely&Domain szolgáltató</h1>
	<div class="flex items-center gap-4">
		<a href="/home" class="text-blue-400 underline">Főoldal</a>
		<a href="/admin" class="text-blue-400 underline">Admin</a>
	</div>
	<button onclick={logout} class="text-blue-400 underline">Kijelentkezés</button>
</div>
