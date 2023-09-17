import { error, json } from '@sveltejs/kit';
import { getClient } from '../mongoclient';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async (ev) => {
	const authCookie = ev.cookies.get('auth');
	if (!authCookie)
		throw error(403, {
			message: 'Not authenticated'
		});

	const client = await getClient();
	const collection = client.db('CBREData').collection('users');
	const data = await collection.findOne({ token: authCookie });
	if (!data) throw error(404);

	return json({ username: data.username });
};
