<script lang="ts">
	import { accessToken } from '$lib/stores/auth';

	function logout() {
		$accessToken = '';
		window.location.href = '/login';
	}
</script>

<div class="mb-10 flex h-20 w-full items-center justify-between bg-gray-100 px-4 shadow-md">
	<h1 class="text-2xl font-bold">Díjcsomagok</h1>
	<p class="text-gray-500">Válassza ki az Önnek legjobban megfelelő díjcsomagot.</p>
	<button onclick={logout} class="text-blue-400 underline">Kijelentkezés</button>
</div>
