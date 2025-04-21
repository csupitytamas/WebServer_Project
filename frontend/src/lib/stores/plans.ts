import { writable, type Writable } from 'svelte/store';

export interface Plan {
	d_id: Number;
	ar: Number;
	neve: string;
	max_domain: Number;
	max_meret: Number;
}

export const plans: Writable<Plan[] | null> = writable(null);
