import { MongoClient, ServerApiVersion } from 'mongodb';
import 'dotenv/config';

let clientCache: MongoClient;

export async function getClient() {
	if (clientCache) return clientCache;

	const uri = `mongodb+srv://jayeshpaluru:${process.env.MONGODB_PASSWORD}@clustercbredata.o1vqwld.mongodb.net/?retryWrites=true&w=majority`;

	const client = new MongoClient(uri, {
		serverApi: {
			version: ServerApiVersion.v1,
			strict: true,
			deprecationErrors: true
		}
	});

	await client.connect();

	clientCache = client;
	return client;
}

export async function getCBRECollection() {
	return (await getClient()).db('CBREData').collection('CBREData');
}
