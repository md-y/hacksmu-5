import { json } from '@sveltejs/kit';
import { getCBRECollection } from '../../mongoclient';
import type { RequestHandler } from './$types';

const demoAssets = [
	{
		'Asset Type': 'Fire Extinguisher',
		'Asset ID': 1000002,
		floor: 1,
		room: 22,
		location: {
			type: 'Point',
			coordinates: [-96.7834767, 32.8436381]
		},
		'Height From Floor': 6,
		'Criticality Level': 8
	},
	{
		'Asset Type': 'Bleed Kit',
		'Asset ID': 1000003,
		location: {
			type: 'Point',
			coordinates: [-96.7834756, 32.843647]
		},
		'Height From Floor': 6,
		'Criticality Level': 3
	},
	{
		'Asset Type': 'Defibrillator',
		'Asset ID': 1000004,
		floor: 1,
		room: 22,
		location: {
			type: 'Point',
			coordinates: [-96.7834946, 32.8436494]
		},
		'Height From Floor': 6,
		'Criticality Level': 1
	},
	{
		'Asset Type': 'Elevator',
		'Asset ID': 1000005,
		floor: 1,
		room: 22,
		location: {
			type: 'Point',
			coordinates: [-96.7834388, 32.8436487]
		},
		'Height From Floor': 5,
		'Criticality Level': 0
	}
];

const example = {
	Floor: 1,
	Room: 83,
	'Installation Date': '7/12/2015',
	Manufacturer: 'Manufacturer_4',
	'Operational Time (hrs)': '21609',
	'Error Logs': [
		{
			'Logger Name': 'Sam',
			'Log Description': 'This is a random operational log',
			'Log Date': '4/25/2016'
		},
		{
			'Logger Name': 'Automated Error Logging',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/28/2017'
		},
		{
			'Logger Name': 'Jerry',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/11/2018'
		},
		{
			'Logger Name': 'Automated Error Logging',
			'Log Description': 'This is a random operational log',
			'Log Date': '7/24/2018'
		},
		{
			'Logger Name': 'Jerry',
			'Log Description': 'This is a random operational log',
			'Log Date': '8/3/2019'
		},
		{
			'Logger Name': 'Nevin',
			'Log Description': 'This is a random operational log',
			'Log Date': '4/1/2020'
		},
		{
			'Logger Name': 'Nevin',
			'Log Description': 'This is a random operational log',
			'Log Date': '4/19/2020'
		},
		{
			'Logger Name': 'Automated Error Logging',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/8/2022'
		},
		{
			'Logger Name': 'Nevin',
			'Log Description': 'This is a random operational log',
			'Log Date': '10/26/2022'
		}
	],
	'Operational Logs': [
		{
			'Logger Name': 'Charlene',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/8/2023'
		},
		{
			'Logger Name': 'Nevin',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/9/2023'
		},
		{
			'Logger Name': 'Dolly',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/9/2023'
		},
		{
			'Logger Name': 'Sam',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/9/2023'
		},
		{
			'Logger Name': 'Nevin',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/10/2023'
		},
		{
			'Logger Name': 'Sam',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/12/2023'
		},
		{
			'Logger Name': 'Dolly',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/12/2023'
		},
		{
			'Logger Name': 'Jerry',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/12/2023'
		},
		{
			'Logger Name': 'Nevin',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/12/2023'
		},
		{
			'Logger Name': 'Jerry',
			'Log Description': 'This is a random operational log',
			'Log Date': '6/15/2023'
		}
	],
	'Service Reports': [
		{
			'Servicer Name': 'Bob',
			'Service Description': 'This is a random service description',
			'Date Serviced': '5/3/2016',
			Cost: 18841,
			'Service Reason': 'This is a random service reason'
		},
		{
			'Servicer Name': 'Bob',
			'Service Description': 'This is a random service description',
			'Date Serviced': '7/7/2017',
			Cost: 5661,
			'Service Reason': 'This is a random service reason'
		},
		{
			'Servicer Name': 'Dolly',
			'Service Description': 'This is a random service description',
			'Date Serviced': '6/19/2018',
			Cost: 25978,
			'Service Reason': 'This is a random service reason'
		},
		{
			'Servicer Name': 'Bob',
			'Service Description': 'This is a random service description',
			'Date Serviced': '7/31/2018',
			Cost: 13473,
			'Service Reason': 'This is a random service reason'
		},
		{
			'Servicer Name': 'Charlene',
			'Service Description': 'This is a random service description',
			'Date Serviced': '8/11/2019',
			Cost: 1319,
			'Service Reason': 'This is a random service reason'
		},
		{
			'Servicer Name': 'Nevin',
			'Service Description': 'This is a random service description',
			'Date Serviced': '4/3/2020',
			Cost: 769,
			'Service Reason': 'This is a random service reason'
		},
		{
			'Servicer Name': 'Jerry',
			'Service Description': 'This is a random service description',
			'Date Serviced': '4/27/2020',
			Cost: 18215,
			'Service Reason': 'This is a random service reason'
		},
		{
			'Servicer Name': 'Dolly',
			'Service Description': 'This is a random service description',
			'Date Serviced': '6/12/2022',
			Cost: 18784,
			'Service Reason': 'This is a random service reason'
		},
		{
			'Servicer Name': 'David',
			'Service Description': 'This is a random service description',
			'Date Serviced': '11/2/2022',
			Cost: 11529,
			'Service Reason': 'This is a random service reason'
		}
	],
	'Time Between Services': 8760,
	'Work Orders': [
		{
			'Filer Name': 'Jayesh',
			'File Date': '5/1/2016',
			'Completion Date': '5/3/2016',
			Description: 'This is a random work order description'
		},
		{
			'Filer Name': 'Charlene',
			'File Date': '7/5/2017',
			'Completion Date': '7/7/2017',
			Description: 'This is a random work order description'
		},
		{
			'Filer Name': 'Bob',
			'File Date': '6/12/2018',
			'Completion Date': '6/19/2018',
			Description: 'This is a random work order description'
		},
		{
			'Filer Name': 'David',
			'File Date': '7/26/2018',
			'Completion Date': '7/31/2018',
			Description: 'This is a random work order description'
		},
		{
			'Filer Name': 'Nevin',
			'File Date': '8/10/2019',
			'Completion Date': '8/11/2019',
			Description: 'This is a random work order description'
		},
		{
			'Filer Name': 'Charlene',
			'File Date': '4/3/2020',
			'Completion Date': '4/3/2020',
			Description: 'This is a random work order description'
		},
		{
			'Filer Name': 'Nevin',
			'File Date': '4/21/2020',
			'Completion Date': '4/27/2020',
			Description: 'This is a random work order description'
		},
		{
			'Filer Name': 'David',
			'File Date': '6/10/2022',
			'Completion Date': '6/12/2022',
			Description: 'This is a random work order description'
		},
		{
			'Filer Name': 'Nevin',
			'File Date': '10/27/2022',
			'Completion Date': '11/2/2022',
			Description: 'This is a random work order description'
		}
	],
	Cost: 696969,
	'Energy Efficiency': 4,
	Weight: 5000,
	location: {
		type: 'Point',
		coordinates: [0, 0]
	}
};

export const GET: RequestHandler = async () => {
	const collection = await getCBRECollection();

	await collection.deleteMany({ Cost: 696969 });
	await collection.insertMany(demoAssets.map((obj) => ({ ...example, ...obj })));

	return json({ 'Demo Items': await collection.countDocuments({ Cost: 696969 }) });
};
