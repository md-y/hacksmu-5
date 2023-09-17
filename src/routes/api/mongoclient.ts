import { MongoClient, ServerApiVersion } from 'mongodb';
import { readFileSync } from 'node:fs';

let clientCache: MongoClient;

export async function getClient() {
	if (clientCache) return clientCache;

	const uri = `mongodb+srv://clustercbredata.o1vqwld.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority`;
	const credentials = 'X509-cert-6706186085905149183.pem';
	const readFile = readFileSync(credentials);

	const client = new MongoClient(uri, {
		serverApi: ServerApiVersion.v1,
		cert: readFile,
		key: readFile
	});

	await client.connect();

	clientCache = client;
	return client;
}

export async function getCBRECollection() {
	return (await getClient()).db('CBREData').collection('CBREData');
}
