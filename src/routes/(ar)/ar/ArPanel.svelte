<script lang="ts">
	import type { Asset } from '../../../types';
	import { currentAsset } from './panelstore';

	export let asset: Asset;
	currentAsset.set(asset);

	// https://colordesigner.io/gradient-generator/?mode=lch#4A7646-C65E5E
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
	let bgColor = bgColors[asset['Criticality Level']];

	const eyeLevel = 5;
	let assetHeight = (asset['Height From Floor'] - eyeLevel) / 3.281;
</script>

<a-entity
	gps-new-entity-place="latitude: {asset.location.coordinates[1]}; longitude: {asset.location
		.coordinates[0]}"
	look-at-id="camera"
	material="opacity: 0.75; color: {bgColor}"
	geometry="primitive: circle"
	on:click|capture|stopPropagation={() => currentAsset.set(asset)}
	role="none"
	scale="0.5 0.5 1"
	position="0 {assetHeight} 0"
>
	<a-entity
		text__name="align: center; baseline: bottom; value: {asset['Asset Type']}; width: 10"
		position="0 0.1 0.1"
	/>
	<a-entity
		text__id="align: center; baseline: top; value: {asset['Asset ID']}; width: 5"
		position="0 -0.1 0.1"
	/>
</a-entity>
