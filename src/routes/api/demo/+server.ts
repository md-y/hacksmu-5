import { json } from '@sveltejs/kit';
import type { RequestHandler } from '../$types';
import { getCBRECollection } from '../mongoclient';

export const GET: RequestHandler = async () => {
	const collection = await getCBRECollection();
	const data = await collection.findOne();
	return json(data);
};
