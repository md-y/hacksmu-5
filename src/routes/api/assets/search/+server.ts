import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getCBRECollection } from '../../mongoclient';

export const GET: RequestHandler = async (event) => {
	const params = event.url.searchParams;
	const query = params.get('query');
	if (!query) {
		throw error(400, {
			message: 'Missing query parameter'
		});
	}

	const collection = await getCBRECollection();
	let cursor = collection.aggregate([
		{
			$search: {
				index: 'default',
				text: {
					query: query,
					path: {
						wildcard: '*'
					}
				}
			}
		}
	]);
	cursor = cursor.limit(50);
	const data = await cursor.toArray();
	return json(data ?? {});
};
