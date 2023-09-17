export type Asset = {
	_id: string;
	'Asset ID': number;
	'Asset Type': string;
	Floor: number;
	Room: number;
	'Installation Date': string;
	Manufacturer: string;
	'Operational Time (hrs)': string;
	'Criticality Level': number;
	'Time Between Services': number;
	Cost: number;
	'Energy Efficiency': number;
	Weight: number;
	'Height From Floor': number;
	location: {
		type: 'Point';
		coordinates: [number, number];
	};
};
