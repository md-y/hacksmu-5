<p>MY DASHBOARD WOOO!</p>
<iframe title="dashboard" src="http://localhost:8501/"></iframe>

<style>
	iframe {
		width: 99%;
		height: 90%;
		border: none;
	}
</style>

<input bind:value={selected_asset}/>
<button on:click={getAsset}>CLICK ME</button>
{#if assetInfo != ""}
    <p>{JSON.stringify(assetInfo)}</p>
{:else}
    <p>...</p>
{/if}


