<script>
    export let link;

    async function getGraph(url) {
		const result = await fetch(url);
		const text = await result.text();

		if (result.ok) {
			return text;
		} else {
            print(result)
			return "error"
		}
	}
</script>

{#await getGraph(link)}
	<p>generating graph..</p>
{:then graph}
	<img src="http://localhost:5000{graph}.svg" alt="graph" style="width:30vw">
    <button on:click={window.open("http://localhost:5000"+graph+".png", "_blank")}>Download as png</button>
{/await}