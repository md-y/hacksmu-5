<script lang="ts">
	import type { Asset } from '../../../types';
	import type { AEntity } from 'aframe';
	import { currentAsset } from './panelstore';

	export let asset: Asset;
	// currentAsset.set(asset);

	let parentEntity: AEntity;

	const bgColor = '#262626';
</script>

<a-entity
	gps-new-entity-place="latitude: {asset.lat}; longitude: {asset.long}"
	look-at-id="camera"
	material="opacity: 0.75; color: {bgColor}"
	geometry="primitive: circle"
	on:click|capture|stopPropagation={() => currentAsset.set(asset)}
>
	<a-entity
		text__name="align: center; baseline: bottom; value: {asset.name}; width: 10"
		position="0 0.1 0.1"
	/>
	<a-entity
		text__id="align: center; baseline: top; value: {asset.id}; width: 5"
		position="0 -0.1 0.1"
	/>
</a-entity>
