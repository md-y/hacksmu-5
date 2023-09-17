<script lang="ts">
	import { onMount } from 'svelte';
	import ArPanel from './ArPanel.svelte';
	import { currentAsset } from './panelstore';
	import { fly } from 'svelte/transition';
	import type { Asset } from '../../../types';

	// https://github.com/sectorxusa/svelte-aframe-arjs/blob/master/src/routes/index.svelte

	const libraryCount = 4;

	let loadCount = 0;
	let assets: Asset[] | null = null;
	let mounted = false;
	let ready = false;
	$: ready = loadCount === libraryCount && mounted && assets != null;

	function onLibraryLoad() {
		loadCount++;
		console.log('load count:', loadCount);
	}

	onMount(() => {
		loadCount = 0;
		mounted = true;

		navigator.geolocation.getCurrentPosition(async (position) => {
			const url = new URL('/api/assets/geo', location.origin);
			url.searchParams.set('lat', position.coords.latitude.toString());
			url.searchParams.set('long', position.coords.longitude.toString());
			console.log(url);
			const req = await fetch(url);
			assets = (await req.json()) as Asset[];
			console.log('Loaded', assets.length, 'assets');
		});
	});
</script>

<svelte:head>
	<link
		href="https://fonts.googleapis.com/css?family=Roboto:regular,black&display=swap"
		rel="stylesheet"
	/>
	<title>Asset Finder</title>
	{#if mounted}
		<script src="https://aframe.io/releases/1.3.0/aframe.min.js" on:load={onLibraryLoad}></script>
		{#if loadCount >= 1}
			<script
				type="text/javascript"
				src="https://raw.githack.com/AR-js-org/AR.js/master/three.js/build/ar-threex-location-only.js"
				on:load={onLibraryLoad}
			></script>
			<script
				type="text/javascript"
				src="https://raw.githack.com/AR-js-org/AR.js/master/aframe/build/aframe-ar.js"
				on:load={onLibraryLoad}
			></script>
			<script type="text/javascript" src="/ar_addon.js" on:load={onLibraryLoad}></script>
		{/if}
	{/if}
</svelte:head>

{#if ready}
	<a-scene
		vr-mode-ui="enabled: false"
		arjs="sourceType: webcam; videoTexture: true; debugUIEnabled: false"
		renderer="antialias: true; alpha: true"
	>
		<a-camera
			id="camera"
			gps-new-camera="gpsMinDistance: 5;"
			arjs-device-orientation-controls="smoothingFactor: 0.1"
			cursor="rayOrigin: mouse"
		>
			<a-entity
				cursor="fuse: true; fuseTimeout: 1"
				position="0 0 -1"
				geometry="primitive: ring; radiusInner: 0.02; radiusOuter: 0.03"
				material="color: white; shader: flat"
			/>
		</a-camera>
		{#if assets !== null}
			{#each assets as asset}
				<ArPanel {asset} />
			{/each}
		{/if}
	</a-scene>
	<div id="ar-overlay">
		<div class="header">
			<a href="/">
				<svg xmlns="http://www.w3.org/2000/svg" height="2em" viewBox="0 0 576 512">
					<!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
					<path
						fill="white"
						d="M575.8 255.5c0 18-15 32.1-32 32.1h-32l.7 160.2c0 2.7-.2 5.4-.5 8.1V472c0 22.1-17.9 40-40 40H456c-1.1 0-2.2 0-3.3-.1c-1.4 .1-2.8 .1-4.2 .1H416 392c-22.1 0-40-17.9-40-40V448 384c0-17.7-14.3-32-32-32H256c-17.7 0-32 14.3-32 32v64 24c0 22.1-17.9 40-40 40H160 128.1c-1.5 0-3-.1-4.5-.2c-1.2 .1-2.4 .2-3.6 .2H104c-22.1 0-40-17.9-40-40V360c0-.9 0-1.9 .1-2.8V287.6H32c-18 0-32-14-32-32.1c0-9 3-17 10-24L266.4 8c7-7 15-8 22-8s15 2 21 7L564.8 231.5c8 7 12 15 11 24z"
					/>
				</svg>
			</a>
		</div>
		{#if $currentAsset !== null}
			<div
				class="footer"
				transition:fly={{
					duration: 300,
					y: 500
				}}
			>
				<div class="close">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						height="2em"
						viewBox="0 0 384 512"
						on:click={() => currentAsset.set(null)}
						on:keyup={() => currentAsset.set(null)}
						role="button"
						tabindex="0"
					>
						<!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
						<path
							fill="white"
							d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"
						/>
					</svg>
				</div>
				<div class="body">
					<h1>{$currentAsset['Asset Type']}</h1>
					<h2><b>ID</b> {$currentAsset['Asset ID']}</h2>
					<h2><b>Install Date</b> {$currentAsset['Installation Date']}</h2>
					<h2><b>Operation Time</b> {$currentAsset['Operational Time (hrs)']}hrs</h2>
					<h2><b>Criticality Level</b> {$currentAsset['Criticality Level']}/10</h2>
					<h2><b>Time Between Service</b> {$currentAsset['Time Between Services']}hrs</h2>
					<h2><b>Cost</b> ${$currentAsset['Cost']}</h2>
					<h2><b>Manufacturer</b> {$currentAsset['Manufacturer']}</h2>
					<h2><b>Floor</b> {$currentAsset['Floor']}</h2>
					<h2><b>Room</b> {$currentAsset['Room']}</h2>
					<h2><b>Energy Efficiency</b> {$currentAsset['Energy Efficiency']}</h2>
					<h2><b>Weight</b> {$currentAsset['Weight']}</h2>
					<span class="spacer" />
				</div>
			</div>
		{/if}
	</div>
{:else}
	<img
		src="https://upload.wikimedia.org/wikipedia/commons/9/92/Loading_icon_cropped.gif"
		alt="loading icon"
	/>
{/if}

<style lang="scss">
	#ar-overlay {
		position: absolute;
		left: 0;
		top: 0;

		width: 100vw;
		height: 100vh;

		color: white;

		font-family: 'Roboto', sans-serif;

		b {
			font-weight: 900;
		}

		h2 {
			font-weight: 400;
		}

		.header {
			padding: 1em;
		}

		.footer {
			position: absolute;
			top: 60vh;
			left: 0;
			width: 100%;

			padding: 1em;
			background-color: rgba(0, 0, 0, 0.5);

			.close {
				position: absolute;
				right: 3em;
				top: 1em;
			}

			.body {
				overflow-y: auto;
				height: 40vh;
			}

			.spacer {
				display: block;
				width: 100%;
				height: 10vh;
			}
		}
	}
</style>
