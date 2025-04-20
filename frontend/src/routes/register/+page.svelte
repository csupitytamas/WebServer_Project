<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { PUBLIC_API_URL } from '$env/static/public';
	import axios from 'axios';
	import { accessToken } from '$lib/stores/auth';

	let username: string = $state('');
	let email: string = $state('');
	let password: string = $state('');
	let password2: string = $state('');

	function handleRegister() {
		if (password !== password2) {
			alert('A jelszavak nem egyeznek meg!');
			return;
		}

		if (!username || !email || !password) {
			alert('Kérlek töltsd ki az összes mezőt!');
			return;
		}

		const data = {
			nev: username,
			email: email,
			jelszo: password
		};

		axios
			.post(`${PUBLIC_API_URL}/auth/register`, JSON.stringify(data), {
				headers: {
					'Content-Type': 'application/json'
				}
			})
			.then((res) => {
				console.log(res);
				if (res.status === 200) {
					if (res.data.access_token) {
						$accessToken = res.data.access_token;
						window.location.href = '/home';
					}
				} else {
					alert('Hiba történt a bejelentkezés során!');
				}
			})
			.catch((error) => {
				console.error('Error:', error);
				alert('Hiba történt a bejelentkezés során!');
			});
	}
</script>

<div class="mt-32 flex flex-col items-center justify-center gap-6">
	<div class="flex w-full max-w-sm flex-col gap-1.5">
		<Label for="username">Név</Label>
		<Input type="név" id="username" placeholder="Név" bind:value={username} />
		<p class="text-sm text-muted-foreground">Add meg a neved</p>
	</div>

	<div class="flex w-full max-w-sm flex-col gap-1.5">
		<Label for="email-2">Email</Label>
		<Input type="email" id="email-2" placeholder="Email" bind:value={email} />
		<p class="text-sm text-muted-foreground">Add meg az email címedet</p>
	</div>

	<div class="flex w-full max-w-sm flex-col gap-1.5">
		<Label for="password">Jelszó</Label>
		<Input type="password" id="password" placeholder="Jelszó" bind:value={password} />
		<p class="text-sm text-muted-foreground">Add meg a jelszavad</p>
	</div>

	<div class="flex w-full max-w-sm flex-col gap-1.5">
		<Label for="password2">Jelszó mégegyszer</Label>
		<Input type="password" id="password2" placeholder="Jelszó mégegyszer" bind:value={password2} />
		<p class="text-sm text-muted-foreground">Add meg a jelszavad ismét</p>
	</div>

	<div class="flex flex-col items-center justify-center gap-2">
		<Button onclick={handleRegister}>Regisztráció</Button>
		<a href="/login" class="text-blue-400 underline">Van már felhasználód?</a>
	</div>
</div>
