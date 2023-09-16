import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { MongoClient, ServerApiVersion } from 'mongodb';

export const GET: RequestHandler = async () => {
	const uri =
		'mongodb+srv://jayeshpaluru:S7iYJJrFSXx3MO07@clustercbredata.o1vqwld.mongodb.net/?retryWrites=true&w=majority';

	const client = new MongoClient(uri, {
		serverApi: {
			version: ServerApiVersion.v1,
			strict: true,
			deprecationErrors: true
		}
	});

	let data = { status: 'error' } as unknown;
	try {
		await client.connect();
		data = await client.db('CBREData').collection('CBREData').findOne();
	} finally {
		await client.close();
	}

	return json(data);
};
