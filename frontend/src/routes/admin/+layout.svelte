<script>
	import { goto } from '$app/navigation';
	import Menu from '$lib/components/Menu.svelte';
	import { isAdmin } from '$lib/stores/auth';

	$effect(() => {
		if (!$isAdmin) {
			goto('/home');
		}
	});
</script>

<Menu />

<slot />
