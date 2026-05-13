<script>
	let submitted = false;
	let bvid = '';

	function submit() {
		if (bvid.trim()) {
			submitted = true;
			setTimeout(() => {
				submitted = false;
				bvid = '';
			}, 2000);
		}
	}
</script>

<section class="nominations">
	<h2>提名</h2>
	<p class="desc">提交B站视频BV号进行提名</p>
	
	{#if submitted}
		<div class="success">提交成功</div>
	{:else}
		<div class="form">
			<input 
				type="text" 
				placeholder="输入BV号，如 BV1xx411c7mD" 
				bind:value={bvid}
			/>
			<button on:click={submit}>提交</button>
		</div>
	{/if}
</section>

<style>
	.nominations {
		max-width: 480px;
		margin: 0 auto;
		text-align: center;
	}

	h2 {
		color: #111111;
		font-size: 1.25rem;
		margin: 0 0 8px 0;
		font-weight: 500;
		letter-spacing: 1px;
	}

	.desc {
		color: #666666;
		font-size: 0.875rem;
		margin: 0 0 32px 0;
	}

	.form {
		display: flex;
		gap: 8px;
	}

	input {
		flex: 1;
		padding: 12px 16px;
		border: 1px solid #eeeeee;
		border-radius: 8px;
		font-size: 0.875rem;
		outline: none;
	}

	input:focus {
		border-color: #111111;
	}

	button {
		padding: 12px 24px;
		background-color: #111111;
		color: #ffffff;
		border: none;
		border-radius: 8px;
		font-size: 0.875rem;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	button:hover {
		background-color: #333333;
	}

	.success {
		color: #22c55e;
		font-size: 0.875rem;
	}
</style>
