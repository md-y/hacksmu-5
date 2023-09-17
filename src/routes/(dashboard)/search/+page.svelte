<script lang="ts">
	import type { Asset } from '../../../types';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	let results: Asset[] = [];
	let currentAsset: any = undefined;
	let showErrorLogs = false;
	let showWorkOrders = false;
	let showServiceReports = false;
	let showOperationalLogs = false;
	let anomolyDetected: any = undefined;
	let serviceDateCalculated: any = undefined;
	
	function onSearch(target: EventTarget & HTMLInputElement) {
		if (target.value) search(target.value);
	}

	async function search(query: string) {
		currentAsset = undefined;
		const url = new URL('/api/assets/search', location.origin);
		url.searchParams.set('query', query);

		const res = await fetch(url);
		results = await res.json();
	}

	function getColor(asset: Asset) {
		const bgColors = [
			'#4a7646',
			'#5a763d',
			'#697536',
			'#797431',
			'#88712f',
			'#976e31',
			'#a56a38',
			'#b26641',
			'#bd624e',
			'#c65e5e'
		];
		return bgColors[asset['Criticality Level']];
	}

	async function onResultClick(asset: Asset) {
		//bind crap
		currentAsset = asset;
		console.log(currentAsset);

		anomolyDetected = undefined;
		serviceDateCalculated = undefined;

		//check for anomaly
		let anomaly: any = await fetch(`http://127.0.0.1:5000/anomaly?id=${asset["Asset ID"]}`);
        anomaly = await anomaly.json();
		anomolyDetected = anomaly.response;

		//check for next service date
		let serviced: any = await fetch(`http://127.0.0.1:5000/serviceRegression?id=${asset["Asset ID"]}`);
        serviced = await serviced.json();
		serviceDateCalculated = serviced.response;
	}

	function toggleErrorLogs(){
		showErrorLogs = !showErrorLogs;
	}

	function toggleWorkOrders(){
		showWorkOrders = !showWorkOrders;
	}

	function toggleServiceReports(){
		showServiceReports = !showServiceReports;
	}

	function toggleOperationalLogs(){
		showOperationalLogs = !showOperationalLogs;
	}

	onMount(() => {
		if ($page.url.searchParams.has('query')) {
			search($page.url.searchParams.get('query')!);
		}
	});
</script>

<div id="page">
	<div id="search-area">
		<input
			id="search-input"
			type="text"
			placeholder="Search asset_id..."
			on:keydown={(ev) => {
				if (ev.key === 'Enter') onSearch(ev.currentTarget);
			}}
		/>
	</div>
	{#if currentAsset == undefined}
		<div id="results-area">
			{#each results as res, i}
				<div
					class="result"
					style:border-color={getColor(res)}
					on:click={() => onResultClick(res)}
					on:keydown={() => onResultClick(res)}
					role="button"
					tabindex={i}
				>
					<h3><b>{res['Asset Type']}</b> - #{res['Asset ID']}</h3>
					<h3>{res['Installation Date']}</h3>
				</div>
			{/each}
		</div>
	{:else}
		<div id="asset-info">
			{#if anomolyDetected === undefined}
				<h4>Anomoly Detected:  (Detecting...)</h4>
			{:else}
				<h4>Anomoly Detected:  {anomolyDetected}</h4>
			{/if}

			{#if serviceDateCalculated === undefined}
				<h4>Next Predicted Service Date: (Calculating...)</h4>
			{:else}
				<h4>Next Predicted Service Date: {serviceDateCalculated}</h4>
			{/if}

			<h4>Asset ID: {currentAsset["Asset ID"]}</h4>
			<h4>Asset Type: {currentAsset["Asset Type"]}</h4>
			<h4>Cost: {currentAsset["Cost"]}</h4>
			<h4>Criticality Level: {currentAsset["Criticality Level"]} / 10</h4>
			<h4>Energy Efficiency: {currentAsset["Criticality Level"]} / 10</h4>
			<h4>Floor: {currentAsset["Floor"]}</h4>
			<h4>Installation Date: {currentAsset["Installation Date"]}</h4>
			<h4>Manufacturer: {currentAsset["Manufacturer"]}</h4>
			<h4>Operational Time: {currentAsset["Operational Time (hrs)"]} Hours</h4>
			<h4>Room: {currentAsset["Room"]}</h4>
			<h4>Time Between Services: {currentAsset["Time Between Services"]} Hours</h4>
			<h4>Weight: {currentAsset["Weight"]} lbs</h4>
				{#if showOperationalLogs}
					<h4>Operational Logs: <svg on:click={toggleOperationalLogs} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg></h4>
					{#each currentAsset["Operational Logs"] as log}
						<h4>Logger Name: {log["Logger Name"]}</h4>
						<h4>Log Date: {log["Log Date"]}</h4>
						<h4>Log Description: {log["Log Description"]}</h4>
						<br/>
					{/each}
				{:else}
					<h4>Operational Logs: <svg on:click={toggleOperationalLogs} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M201.4 137.4c12.5-12.5 32.8-12.5 45.3 0l160 160c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L224 205.3 86.6 342.6c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l160-160z"/></svg></h4>
				{/if}

				{#if showErrorLogs}
					<h4>Error Logs: <svg on:click={toggleErrorLogs} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg></h4>
					{#each currentAsset["Error Logs"] as log}
						<h4>Logger Name: {log["Logger Name"]}</h4>
						<h4>Log Date: {log["Log Date"]}</h4>
						<h4>Log Description: {log["Log Description"]}</h4>
						<br/>
					{/each}
				{:else}
					<h4>Error Logs: <svg on:click={toggleErrorLogs} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M201.4 137.4c12.5-12.5 32.8-12.5 45.3 0l160 160c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L224 205.3 86.6 342.6c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l160-160z"/></svg></h4>
				{/if}

				{#if showWorkOrders}
					<h4>Work Orders: <svg on:click={toggleWorkOrders} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg></h4>
					{#each currentAsset["Work Orders"] as log}
						<h4>Filer Name: {log["Filer Name"]}</h4>
						<h4>Description: {log["Description"]}</h4>
						<h4>File Date: {log["File Date"]}</h4>
						<h4>Completion Description: {log["Completion Description"]}</h4>
						<br/>
					{/each}
				{:else}
					<h4>Work Orders: <svg on:click={toggleWorkOrders} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M201.4 137.4c12.5-12.5 32.8-12.5 45.3 0l160 160c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L224 205.3 86.6 342.6c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l160-160z"/></svg></h4>
				{/if}

				{#if showServiceReports}
					<h4>Service Reports: <svg on:click={toggleServiceReports} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg></h4>
					{#each currentAsset["Service Reports"] as log}
						<h4>Servicer Name: {log["Servicer Name"]}</h4>
						<h4>Service Reason: {log["Service Reason"]}</h4>
						<h4>Service Description: {log["Service Description"]}</h4>
						<h4>Date Serviced: {log["Date Serviced"]}</h4>
						<h4>Cost: {log["Cost"]}</h4>
						<br/>
					{/each}
				{:else}
					<h4>Service Reports: <svg on:click={toggleServiceReports} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M201.4 137.4c12.5-12.5 32.8-12.5 45.3 0l160 160c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L224 205.3 86.6 342.6c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l160-160z"/></svg></h4>
				{/if}
		</div>
	{/if}
</div>

<style lang="scss">
	svg{
		background-color: #242325;
		border-radius: 50%;
		padding: 5px;
		position: relative;
    	bottom: -8px;
	}
	svg:hover{
		cursor:grab
	}
	#page {
		overflow: hidden;
		height: 90vh;
	}

	#search-area {
		display: flex;
		flex-direction: row;
		justify-content: center;

		#search-input {
			display: block;
			width: 80%;
			height: 3em;
			margin-top: 2em;
			background-color: #242325;
			color: white;
			border: none;
			padding: 0.75em;
		}
	}

	#asset-info {
		overflow: scroll;
		height: 80%;
		color: white;
		padding: .5em;
		margin: 1.5em;
	}
	/* Hide scrollbar for Chrome, Safari and Opera */
	#asset-info::-webkit-scrollbar {
		display: none;
	}
	/* Hide scrollbar for IE, Edge and Firefox */
	#asset-info {
		-ms-overflow-style: none;  /* IE and Edge */
		scrollbar-width: none;  /* Firefox */
	}

	#results-area {
		height: 100%;
		overflow-y: auto;
	}

	.result {
		background-color: #242325;
		border-radius: 10px;
		border-width: 2px;
		border-style: solid;
		border-color: transparent;
		margin: 1.5em;
		padding: 0.5em;

		color: white;
		cursor: pointer;

		display: flex;
		justify-content: space-between;

		h3 {
			display: inline-flex;
		}
	}
</style>
