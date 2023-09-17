import { json } from '@sveltejs/kit';
import { getCBRECollection } from '../../mongoclient';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async (event) => {
	const asset = await event.request.json();

	const collection = await getCBRECollection();

	console.log(asset['Room']);
	const data = await collection.updateOne(
		{ 'Asset ID': asset['Asset ID'] },
		{ $set: asset },
		{
			upsert: true
		}
	);

	console.log({ $set: asset });
	return json(data);
};
