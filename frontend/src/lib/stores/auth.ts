import { writable, type Writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';

const STORAGE_KEY = 'accessToken';

const initial =
	isBrowser && localStorage.getItem(STORAGE_KEY)
		? (localStorage.getItem(STORAGE_KEY) as string)
		: null;

export const accessToken: Writable<string | null> = writable(initial);

if (isBrowser) {
	accessToken.subscribe((value) => {
		localStorage.setItem(STORAGE_KEY, value ?? '');
	});
}
