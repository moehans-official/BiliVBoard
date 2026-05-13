<script>
	import { onMount } from 'svelte';

	let submitted = false;
	let bvid = '';
	let captchaInput = '';
	let captchaCode = '';

	function generateCaptcha() {
		const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
		let code = '';
		for (let i = 0; i < 4; i++) {
			code += chars.charAt(Math.floor(Math.random() * chars.length));
		}
		captchaCode = code;
		return code;
	}

	generateCaptcha();

	function drawCaptcha(canvas, code) {
		const ctx = canvas.getContext('2d');
		const width = canvas.width;
		const height = canvas.height;

		ctx.fillStyle = '#f5f5fa';
		ctx.fillRect(0, 0, width, height);

		for (let i = 0; i < 4; i++) {
			ctx.strokeStyle = `rgba(${Math.random()*100},${Math.random()*100},${Math.random()*150},0.3)`;
			ctx.beginPath();
			ctx.moveTo(Math.random() * width, Math.random() * height);
			ctx.lineTo(Math.random() * width, Math.random() * height);
			ctx.stroke();
		}

		for (let i = 0; i < 40; i++) {
			ctx.fillStyle = `rgba(${Math.random()*150},${Math.random()*150},${Math.random()*150},0.2)`;
			ctx.fillRect(Math.random() * width, Math.random() * height, 1.5, 1.5);
		}

		ctx.textBaseline = 'middle';
		for (let i = 0; i < code.length; i++) {
			const hue = 220 + Math.random() * 40;
			ctx.fillStyle = `hsl(${hue}, 60%, 35%)`;
			ctx.font = `bold ${26 + Math.random() * 4}px "MiSans", Arial`;
			const x = 18 + i * 26;
			const y = height / 2 + (Math.random() * 6 - 3);
			ctx.save();
			ctx.translate(x, y);
			ctx.rotate((Math.random() - 0.5) * 0.35);
			ctx.fillText(code[i], 0, 0);
			ctx.restore();
		}
	}

	function refreshCaptcha() {
		generateCaptcha();
		const canvas = document.getElementById('captcha-canvas');
		if (canvas) drawCaptcha(canvas, captchaCode);
	}

	function submit() {
		if (!bvid.trim()) return;
		if (captchaInput.toUpperCase() !== captchaCode) {
			alert('验证码错误');
			refreshCaptcha();
			captchaInput = '';
			return;
		}
		submitted = true;
		setTimeout(() => {
			submitted = false;
			bvid = '';
			captchaInput = '';
			refreshCaptcha();
		}, 2000);
	}

	onMount(() => {
		const canvas = document.getElementById('captcha-canvas');
		if (canvas) drawCaptcha(canvas, captchaCode);
	});
</script>

<section class="nominations">
	<div class="card">
		<h2>提名</h2>
		<p class="desc">提交B站视频BV号进行提名</p>

		{#if submitted}
			<div class="success">
				<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
					<polyline points="22 4 12 14.01 9 11.01"/>
				</svg>
				<span>提交成功</span>
			</div>
		{:else}
			<div class="form-group">
				<input
					type="text"
					class="bvid-input"
					placeholder="BV1xx411c7mD"
					bind:value={bvid}
				/>
			</div>

			<div class="captcha-row">
				<input
					type="text"
					class="captcha-input"
					placeholder="验证码"
					bind:value={captchaInput}
				/>
				<canvas id="captcha-canvas" width="120" height="40"></canvas>
				<button class="refresh-btn" on:click={refreshCaptcha}>
					<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M23 4v6h-6M1 20v-6h6"/>
						<path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
					</svg>
				</button>
			</div>

			<button class="submit-btn" on:click={submit}>
				提交提名
			</button>
		{/if}
	</div>
</section>

<style>
	.nominations {
		max-width: 480px;
		margin: 0 auto;
	}

	.card {
		background: #ffffff;
		border-radius: 16px;
		padding: 28px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.06);
		animation: fadeIn 0.4s ease-out;
	}

	h2 {
		color: #1a1a2e;
		font-size: 1.125rem;
		margin: 0 0 8px 0;
		font-weight: 600;
	}

	.desc {
		color: #8e8ea0;
		font-size: 0.8125rem;
		margin: 0 0 24px 0;
	}

	.form-group {
		margin-bottom: 12px;
	}

	.bvid-input {
		width: 100%;
		padding: 12px 16px;
		background: #f5f5fa;
		border: 1.5px solid transparent;
		border-radius: 10px;
		font-size: 0.875rem;
		font-family: inherit;
		outline: none;
		transition: all 0.2s ease;
	}

	.bvid-input:focus {
		background: #ffffff;
		border-color: #1a1a2e;
	}

	.captcha-row {
		display: flex;
		align-items: center;
		gap: 10px;
		margin-bottom: 20px;
	}

	.captcha-input {
		width: 110px;
		padding: 10px 14px;
		background: #f5f5fa;
		border: 1.5px solid transparent;
		border-radius: 10px;
		font-size: 0.875rem;
		font-family: 'MiSans', monospace;
		letter-spacing: 4px;
		outline: none;
		transition: all 0.2s ease;
	}

	.captcha-input:focus {
		background: #ffffff;
		border-color: #1a1a2e;
	}

	#captcha-canvas {
		border-radius: 8px;
		cursor: pointer;
		flex-shrink: 0;
	}

	.refresh-btn {
		width: 40px;
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #f5f5fa;
		border: none;
		border-radius: 10px;
		cursor: pointer;
		color: #6b7280;
		transition: all 0.2s ease;
	}

	.refresh-btn:hover {
		background: #e5e5ea;
		color: #1a1a2e;
	}

	.submit-btn {
		width: 100%;
		padding: 12px;
		background: #1a1a2e;
		color: #ffffff;
		border: none;
		border-radius: 10px;
		font-size: 0.875rem;
		font-weight: 500;
		font-family: inherit;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.submit-btn:hover {
		background: #2d2d44;
		transform: translateY(-1px);
	}

	.submit-btn:active {
		transform: translateY(0);
	}

	.success {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		padding: 16px;
		color: #22c55e;
		background: #f0fdf4;
		border-radius: 10px;
		font-size: 0.875rem;
		font-weight: 500;
		animation: scaleIn 0.3s ease-out;
	}

	@media (max-width: 640px) {
		.card {
			padding: 20px;
			border-radius: 12px;
		}

		.captcha-row {
			gap: 8px;
		}

		.captcha-input {
			width: 90px;
			padding: 10px 12px;
			font-size: 0.8125rem;
			letter-spacing: 3px;
		}

		#captcha-canvas {
			width: 100px;
			height: 36px;
		}

		.refresh-btn {
			width: 36px;
			height: 36px;
		}
	}
</style>
