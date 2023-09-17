import { fail, redirect } from '@sveltejs/kit';
import { getClient } from '../../api/mongoclient';
import type { Actions } from './$types';
import { createHash } from 'node:crypto';

export const actions = {
	default: async (event) => {
		const formData = await event.request.formData();
		if (!formData.has('username') || !formData.has('password')) {
			return fail(400);
		}

		const client = await getClient();
		const collection = client.db('CBREData').collection('users');
		const username = formData.get('username') as string;
		const data = await collection.findOne({ username: username });

		if (!data) return fail(400);

		const rawPassword = formData.get('password') as string;
		const hash = createHash('sha256').update(rawPassword).update(username).digest('hex');
		if (data.password != hash) return fail(400);

		event.cookies.set('auth', data.token);
		throw redirect(303, '/');
	}
} satisfies Actions;
