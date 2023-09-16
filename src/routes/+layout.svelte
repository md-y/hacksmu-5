<script>
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import SideBar from './SideBar.svelte';
	import Header from './Header.svelte';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<div id="wrapper">
	<SideBar/>
	<div id="wrapper-section">
		<Header/>
		<!-- Other Content goes here -->
        <slot/>
	</div>
	
</div>

<style>
	#wrapper{
		display: flex;
	}
	#wrapper-section{
		width: 100%;
	}
	:global(body){
		background-color: #F8F9FC;
		margin: 0;
		font-family: Nunito,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
	}
</style>
