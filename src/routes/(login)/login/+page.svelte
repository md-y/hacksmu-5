<div>
	<form method="POST">
		<h1>Facilitrack</h1>
		<input placeholder="Username" name="username" type="username" required />
		<input placeholder="Password" name="password" type="password" required />
		<button type="submit">Sign In</button>
	</form>
</div>

<svelte:head>
	<link
		href="https://fonts.googleapis.com/css?family=Roboto:regular&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<style lang="scss">
	:global(body) {
		background-color: #242325;
	}

	div {
		display: flex;
		justify-content: center;
		align-items: end;

		height: 50vh;

		form {
			display: flex;
			flex-direction: column;
			width: 50%;

			h1 {
				color: white;
				font-family: 'Roboto', sans-serif;
			}

			input,
			button {
				height: 2em;
				margin-bottom: 0.5em;
				text-align: start;
			}
		}
	}
</style>
