<script lang="ts">
	import { onMount } from 'svelte';

	let username: string;

	onMount(async () => {
		const url = new URL('/api/whoami', location.origin);
		const res = await fetch(url);
		const json = await res.json();
		username = json.username;
	});
</script>

<div id="header">
	<div id="user">
		{username}
		<div id="user-profile" />
	</div>
</div>

<style>
	#user {
		display: flex;
		justify-content: center;
		align-items: center;
		color: white;
	}
	#user-profile {
		background-color: white;
		border-radius: 50%;
		width: 20px;
		height: 20px;
		margin: 5px;
	}
	#header {
		display: flex;
		width: 100%;
		height: 4.375rem;
		justify-content: right;
		background-color: #242325;
	}
</style>
