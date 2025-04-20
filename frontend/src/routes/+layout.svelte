<script lang="ts">
	import { goto } from '$app/navigation';
	import { accessToken } from '$lib/stores/auth';
	import '../app.css';
	let { children } = $props();

	$effect(() => {
		if ($accessToken && $accessToken !== null) {
			goto('/home', { replaceState: true });
		} else {
			goto('/login', { replaceState: true });
		}
	});
</script>

{@render children()}
