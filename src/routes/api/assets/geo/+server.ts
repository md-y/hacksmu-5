import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getCBRECollection } from '../../mongoclient';

export const GET: RequestHandler = async (event) => {
	const params = event.url.searchParams;
	const long = params.get('long');
	const lat = params.get('lat');
	if (!long || !lat) {
		throw error(400, {
			message: 'Missing long/lat parameters'
		});
	}

	const collection = await getCBRECollection();

	const indexExists = await collection.indexExists('location_2dsphere');
	if (!indexExists) {
		await collection.createIndex({ location: '2dsphere' });
	}

	const cursor = await collection.find({
		location: {
			$near: {
				$geometry: { type: 'Point', coordinates: [parseFloat(long), parseFloat(lat)] },
				$maxDistance: 1000
			}
		}
	});
	const data = await cursor.toArray();
	return json(data ?? {});
};
