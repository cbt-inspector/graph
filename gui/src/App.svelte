<script>
	import Pic from "./Pic.svelte";
	let size = 5;
	let percentage = 30;
	let type;
	let colored;
	let plot = false;
	let plotType

	let pics = []
	
	function typeChange(event) {
		type = event.currentTarget.value;
	}
	function plotChange(event) {
		plotType = event.currentTarget.value;
	}

	function handleSubmission() {
		let link;
		if (!plot) {
			link = "http://localhost:5000/graph?size="+size+"&percentage="+percentage+"&type="+type+"&coloredClusters="+colored
		} else {
			link = "http://localhost:5000/plot?size="+size+"&type="+type+"&plotType="+plotType
		}
		
		pics = [...pics, link]
	}
</script>

<main>
	<div>
		{#each pics as url}
			<Pic link={url}/>
		{/each}
	</div>
	<hr>
	<form on:submit|preventDefault={handleSubmission}>
		<div class="flexOutside">
			<label for="size" class="centered">Size</label>
			<input type="number" name="size" id="size" class="centered" bind:value={size}>

			<label for="percentage" class="centered">Percentage</label>
			{#if plot == false}
			<input type="number" class="centered" bind:value={percentage}>
			{:else}
			<input type="number" class="centered" bind:value={percentage} disabled>
			{/if}
			
			<div class="flexInside">
				<input type="radio" class="radio" name="type" value="triangular" on:change={typeChange}>
				<label for="triangular">Triangular</label>
			</div>
			<div class="flexInside">
				<input type="radio" class="radio" name="type" value="square" on:change={typeChange}>
				<label for="square">Square</label>
			</div>
			<div class="flexInside">
				<input type="radio" class="radio" name="type" value="hexagonal" on:change={typeChange}>
				<label for="hexagonal">Hexagonal</label>
			</div>
			<div class="flexInside"
				style="margin-top: 5px"
			>
				{#if plot == false}
				<input type="checkbox" class="radio" bind:checked={colored}>
				{:else}
				<input type="checkbox" class="radio" disabled>
				{/if}
				<label for="coloredClusters">Colored clusters</label>
			</div>
			
			<div class="flexInside"
				style="margin-top: 5px"
			>	
				<input type="checkbox" class="radio" bind:checked={plot}>
				<label for="coloredClusters">Plot?</label>
			</div>
			{#if plot == true}
			<div class="flexInside">
				<input type="radio" class="radio" name="plotType" value="line" on:change={plotChange}>
				<label for="line">Line plot</label>
			</div>
			<div class="flexInside">
				<input type="radio" class="radio" name="plotType" value="scatter" on:change={plotChange}>
				<label for="scatter">Scatter plot</label>
			</div>
			{/if}
		</div>
		<button type="submit" style="margin-top: 15px">
			{#if plot == false}
				Create Graph
			{:else}
				Create Plot
			{/if}
		</button>
	</form>
	
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}
	form {
		margin-left: auto;
		margin-right: auto;
	}
	.flexOutside {
		display: flex;
		flex-direction: column;
	}
	.flexInside {
		display: flex;
	}
	.radio {
		width: 3ch;
		margin-top: auto;
		margin-bottom: auto;
	}
	.centered {
		margin-left: auto;
		margin-right: auto;
	}
</style>