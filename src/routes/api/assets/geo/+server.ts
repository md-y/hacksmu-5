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
	const data = await collection.findOne({
		location: {
			$near: {
				$geometry: { type: 'Point', coordinates: [parseFloat(long), parseFloat(lat)] },
				$maxDistance: 400
			}
		}
	});
	return json(data ?? {});
};
