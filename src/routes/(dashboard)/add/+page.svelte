<script>
	// @ts-nocheck

	let asset_id = 0;
	let asset_name = '';
	let floor = 0;
	let room = 0;
	let installation_date = '';
	let manufacturer = '';
	let operational_time = '';
	let criticality = 0;
	let time_between_services = 0;
	let cost = 0;
	let energy_efficiency = 0;
	let weight = 0;
	let height_from_floor = 0;
	let cord_x = 0;
	let cord_y = 0;

	let error_logs = {};
	let operational_logs = {};
	let service_reports = {};
	let work_orders = {};

	async function submit() {
		console.log('submitted');
		let push = await fetch(`http://localhost:5173/api/assets/update`, {
			method: 'POST',
			body: JSON.stringify({
				'Asset ID': asset_id,
				'Asset Type': asset_name,
				Cost: cost,
				'Criticality Level': criticality,
				'Energy Efficiency': energy_efficiency,
				'Error Logs': error_logs,
				Floor: floor,
				'Height From Floor': height_from_floor,
				'Installation Date': installation_date,
				Manufacturer: manufacturer,
				'Operational Logs': operational_logs,
				'Operational Time (hrs)': operational_time,
				Room: room,
				'Service Reports': service_reports,
				'Time Between Services': time_between_services,
				Weight: weight,
				'Work Orders': work_orders,
				location: {
					coordinates: [cord_x, cord_y],
					type: 'Point'
				}
			})
		});
		push = await push.json();
	}

	async function getNewId() {
		//fetch the new id
		let new_id = await fetch(`http://127.0.0.1:5000/next_asset`);
		new_id = await new_id.json();
		asset_id = new_id['response'];
	}

	async function changeID() {
		//check for asset
		let asset = await fetch(`http://127.0.0.1:5000/asset?id=${asset_id}`);
		asset = await asset.json();
		console.log(asset);

		asset_name = asset['Asset Type'];
		floor = asset['Floor'];
		room = asset['Room'];
		installation_date = asset['Installation Date'];
		manufacturer = asset['Manufacturer'];
		operational_time = asset['Operational Time (hrs)'];
		criticality = asset['Criticality Level'];
		time_between_services = asset['Time Between Services'];
		cost = asset['Cost'];
		energy_efficiency = asset['Energy Efficiency'];
		weight = asset['Weight'];
		height_from_floor = asset['Height From Floor'];
		cord_x = asset['location']['coordinates'][0];
		cord_y = asset['location']['coordinates'][1];
		error_logs = asset['Error Logs'];
		operational_logs = asset['Operational Logs'];
		service_reports = asset['Service Reports'];
		work_orders = asset['Work Orders'];
	}
</script>

<form>
	<span>Asset Id</span>
	<input on:change={changeID} bind:value={asset_id} />
	<button on:click={getNewId}>Get New Id</button>
	<br />

	<span>Asset Name</span>
	<input bind:value={asset_name} />
	<br />

	<span>Floor</span>
	<input bind:value={floor} />
	<br />

	<span>Room</span>
	<input bind:value={room} />
	<br />

	<span>Installation Date</span>
	<input bind:value={installation_date} />
	<br />

	<span>Manufacturer</span>
	<input bind:value={manufacturer} />
	<br />

	<span>Operational Time</span>
	<input bind:value={operational_time} />
	<br />

	<span>Criticality Level</span>
	<input bind:value={criticality} />
	<br />

	<span>Time Between Services</span>
	<input bind:value={time_between_services} />
	<br />

	<span>Cost</span>
	<input bind:value={cost} />
	<br />

	<span>Energy Efficiency</span>
	<input bind:value={energy_efficiency} />
	<br />

	<span>Weight</span>
	<input bind:value={weight} />
	<br />

	<span>Height From Floor</span>
	<input bind:value={height_from_floor} />
	<br />

	<span>X Cord</span>
	<input bind:value={cord_x} />
	<br />

	<span>Y Cord</span>
	<input bind:value={cord_y} />
	<br />

	<button on:click={submit}>SUBMIT</button>
</form>

<style>
	form {
		margin: 1em;
		padding: 1em;
	}
	span {
		color: white;
	}
</style>
