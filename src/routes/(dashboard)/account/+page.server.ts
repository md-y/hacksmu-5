import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions = {
	default: async (event) => {
		event.cookies.delete('auth');
		throw redirect(303, '/login');
	}
} satisfies Actions;
