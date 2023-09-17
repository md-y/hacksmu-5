<script lang="ts">
	import type { Asset } from '../../../types';

	let results: Asset[] = [];

	async function onSearch(target: EventTarget & HTMLInputElement) {
		const query = target.value;
		if (!query) return;

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
</script>

<div id="page">
	<div id="search-area">
		<input
			id="search-input"
			type="text"
			placeholder="Search assets..."
			on:keydown={(ev) => {
				if (ev.key === 'Enter') onSearch(ev.currentTarget);
			}}
		/>
	</div>
	<div id="results-area">
		{#each results as res}
			<a class="result" style:border-color={getColor(res)} href="/info/{res['_id']}">
				<h3><b>{res['Asset Type']}</b> - #{res['Asset ID']}</h3>
				<h3>{res['Installation Date']}</h3>
			</a>
		{/each}
	</div>
</div>

<style lang="scss">
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
		text-decoration: none;

		display: flex;
		justify-content: space-between;

		h3 {
			display: inline-flex;
		}
	}
</style>
