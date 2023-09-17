import type { Handle } from '@sveltejs/kit';
import { getClient } from './routes/api/mongoclient';

const tokenCache: string[] = [];

export const handle: Handle = async ({ event, resolve }) => {
	if (event.url.pathname !== '/login') {
		const authCookie = event.cookies.get('auth');
		if (!authCookie) {
			return Response.redirect(new URL('/login', event.url.origin), 303);
		} else if (!tokenCache.includes(authCookie)) {
			const client = await getClient();
			const collection = client.db('CBREData').collection('users');
			const data = await collection.findOne({ token: authCookie });
			if (!data) {
				event.cookies.delete('auth');
				return Response.redirect(new URL('/login', event.url.origin), 303);
			} else {
				tokenCache.push(data.token);
			}
		}
	}

	const response = await resolve(event);
	return response;
};
