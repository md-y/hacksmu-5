<script lang="ts">
	import { onMount } from 'svelte';

	// https://github.com/sectorxusa/svelte-aframe-arjs/blob/master/src/routes/index.svelte
	let loadCount = 0;
	let mounted = false;
	let ready = false;
	$: ready = loadCount === 3 && mounted;

	function onLibraryLoad() {
		loadCount++;
		console.log('load count:', loadCount);
	}

	onMount(() => {
		loadCount = 0;
		mounted = true;
	});
</script>

<svelte:head>
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
		{/if}
	{/if}
</svelte:head>

{#if ready}
	<a-scene
		vr-mode-ui="enabled: false"
		arjs="sourceType: webcam; videoTexture: true; debugUIEnabled: false"
		renderer="antialias: true; alpha: true"
	>
		<a-camera gps-new-camera="gpsMinDistance: 5" />
		<a-entity
			material="color: red"
			geometry="primitive: box"
			gps-new-entity-place="latitude: 32.8434832; longitude: -96.7833988"
			scale="10 10 10"
		/>
	</a-scene>
{:else}
	<h1>Loading libraries {loadCount}/3...</h1>
{/if}
