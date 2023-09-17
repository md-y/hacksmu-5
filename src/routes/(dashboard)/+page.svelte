<script>
    let selected_asset = 0;
    let assetInfo = "";
	let prompt = "";
    async function getAsset(){
        //fetch assetInfo
        const response = await fetch(`http://127.0.0.1:5000/asset?id=${selected_asset}`);
        assetInfo = await response.json();
        console.log(assetInfo);
    }

	function getAssistance(){
		//make request to backend for the promt data
	}
</script>

<div id="chatbot">
	<div style="width:99%">
		<p>Ask me a question about the data!</p>
	</div>
	<div style="width:99%">
		<form on:submit={(e) => getAssistance()}>
			<input bind:value={prompt} placeholder="Type your question here"/>
		</form>
	</div>

</div>
<iframe title="dashboard" src="http://localhost:8501/"></iframe>

<style>
    iframe{
        width:99%;
        height: 90%;
		border: none;
    }
	#chatbot{
		width: 99%;
		height: 25%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		color: white;
		text-align: center;
	}
	input{
		width:99%;
		background: none;
		color: rgb(181, 160, 160);
		height: 100%;
		text-align: center;
		margin-block-start: 1em;
		margin-block-end: 1em;
		margin-inline-start: 0px;
		margin-inline-end: 0px;

		border: none;
  		outline: none;
	}
</style>

<!-- <input bind:value={selected_asset}/>
<button on:click={getAsset}>CLICK ME</button>
{#if assetInfo != ""}
    <p>{JSON.stringify(assetInfo)}</p>
{:else}
    <p>...</p>
{/if} -->


