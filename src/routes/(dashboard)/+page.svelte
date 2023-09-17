<script>
    let selected_asset = 0;
    let assetInfo = "";

    async function getAsset(){
        //fetch assetInfo
        const response = await fetch(`http://127.0.0.1:5000/asset?id=${selected_asset}`);
        assetInfo = await response.json();
        console.log(assetInfo);
    }
</script>

<p>MY DASHBOARD WOOO!</p>
<iframe title="dashboard" src="http://localhost:8501/"></iframe>

<style>
    iframe{
        width:99%;
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


