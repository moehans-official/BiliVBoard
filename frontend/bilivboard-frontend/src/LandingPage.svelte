<script>
	let name = 'BiliVBoard';
</script>

<main>
	<div class="content">
		<img src="/logo.png" alt="BiliVBoard Logo" class="logo" />
		<h1>{name}</h1>
		<p class="subtitle">B站视频数据采集与智能评分系统</p>
		<div class="status">
			<span class="dot"></span>
			<span>维护中</span>
		</div>
	</div>
</main>

<style>
	main {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 100vh;
		background-color: #ffffff;
		padding: 16px;
	}

	.content {
		text-align: center;
	}

	.logo {
		width: 100px;
		height: 100px;
		object-fit: contain;
		margin-bottom: 32px;
	}

	h1 {
		color: #111111;
		font-size: 2.5rem;
		margin: 0 0 12px 0;
		font-weight: 600;
		letter-spacing: 2px;
	}

	.subtitle {
		color: #666666;
		font-size: 0.875rem;
		margin: 0 0 48px 0;
		letter-spacing: 1px;
	}

	.status {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		color: #999999;
		font-size: 0.75rem;
		letter-spacing: 2px;
		text-transform: uppercase;
	}

	.dot {
		width: 6px;
		height: 6px;
		background-color: #999999;
		border-radius: 50%;
		animation: pulse 2s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% {
			opacity: 0.4;
		}
		50% {
			opacity: 1;
		}
	}
</style>
