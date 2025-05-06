import { writable, type Writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';

const STORAGE_KEY = 'accessToken';

const initial =
	isBrowser && localStorage.getItem(STORAGE_KEY)
		? (localStorage.getItem(STORAGE_KEY) as string)
		: null;

export const accessToken: Writable<string | null> = writable(initial);
export const isAdmin: Writable<boolean> = writable(false);

if (isBrowser) {
	accessToken.subscribe((value) => {
		localStorage.setItem(STORAGE_KEY, value ?? '');
		decodeJWT(value);
	});
}

function decodeJWT(token: string | null) {
	if (token) {
		const payload = token.split('.')[1];
		if (payload) {
			const decodedPayload = JSON.parse(atob(payload));
			isAdmin.set(decodedPayload.role);
		}
	} else {
		isAdmin.set(false);
	}
}
