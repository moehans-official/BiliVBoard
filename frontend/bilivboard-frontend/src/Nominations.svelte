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
		<div class="header">
			<div class="header-icon">
				<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
			</div>
			<div class="header-text">
				<h2>提名</h2>
				<p class="desc">提交B站视频BV号进行提名</p>
			</div>
		</div>

		{#if submitted}
			<div class="success">
				<div class="success-icon">
					<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
						<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
						<polyline points="22 4 12 14.01 9 11.01"/>
					</svg>
				</div>
				<span>提交成功</span>
			</div>
		{:else}
			<div class="form">
				<div class="form-group">
					<label class="form-label">视频BV号</label>
					<div class="input-wrapper">
						<svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
						<input
							type="text"
							class="bvid-input"
							placeholder="BV1xx411c7mD"
							bind:value={bvid}
						/>
					</div>
				</div>

				<div class="form-group">
					<label class="form-label">验证码</label>
					<div class="captcha-row">
						<div class="input-wrapper captcha-input-wrapper">
							<svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
							<input
								type="text"
								class="captcha-input"
								placeholder="输入验证码"
								bind:value={captchaInput}
							/>
						</div>
						<canvas id="captcha-canvas" width="120" height="44" on:click={refreshCaptcha}></canvas>
						<button class="refresh-btn" on:click={refreshCaptcha}>
							<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path d="M23 4v6h-6M1 20v-6h6"/>
								<path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
							</svg>
						</button>
					</div>
				</div>

				<button class="submit-btn" on:click={submit}>
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<line x1="22" y1="2" x2="11" y2="13"/>
						<polygon points="22 2 15 22 11 13 2 9 22 2"/>
					</svg>
					提交提名
				</button>
			</div>
		{/if}
	</div>
</section>

<style>
	.nominations {
		max-width: 520px;
		margin: 0 auto;
	}

	.card {
		background: #ffffff;
		border-radius: 20px;
		padding: 32px;
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
		animation: fadeIn 0.4s ease-out;
		border: 1px solid rgba(0, 0, 0, 0.04);
	}

	.header {
		display: flex;
		align-items: center;
		gap: 16px;
		margin-bottom: 28px;
	}

	.header-icon {
		width: 48px;
		height: 48px;
		border-radius: 14px;
		background: #1a1a2e;
		color: #ffffff;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.header-text h2 {
		color: #1a1a2e;
		font-size: 1.25rem;
		margin: 0 0 2px 0;
		font-weight: 700;
	}

	.desc {
		color: #8e8ea0;
		font-size: 0.8125rem;
		font-weight: 500;
		margin: 0;
	}

	.form {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.form-label {
		color: #1a1a2e;
		font-size: 0.875rem;
		font-weight: 600;
	}

	.input-wrapper {
		position: relative;
	}

	.input-icon {
		position: absolute;
		left: 14px;
		top: 50%;
		transform: translateY(-50%);
		color: #a0a0b0;
		pointer-events: none;
		transition: color 0.2s ease;
	}

	.input-wrapper:focus-within .input-icon {
		color: #1a1a2e;
	}

	.bvid-input {
		width: 100%;
		padding: 12px 16px 12px 44px;
		background: #f5f5fa;
		border: 1.5px solid transparent;
		border-radius: 12px;
		font-size: 0.875rem;
		font-family: inherit;
		outline: none;
		transition: all 0.2s ease;
	}

	.bvid-input:focus {
		background: #ffffff;
		border-color: #1a1a2e;
		box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.06);
	}

	.captcha-row {
		display: flex;
		align-items: center;
		gap: 12px;
	}

	.captcha-input-wrapper {
		flex: 1;
	}

	.captcha-input {
		width: 100%;
		padding: 12px 16px 12px 44px;
		background: #f5f5fa;
		border: 1.5px solid transparent;
		border-radius: 12px;
		font-size: 0.875rem;
		font-family: 'MiSans', monospace;
		letter-spacing: 4px;
		outline: none;
		transition: all 0.2s ease;
	}

	.captcha-input:focus {
		background: #ffffff;
		border-color: #1a1a2e;
		box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.06);
	}

	#captcha-canvas {
		border-radius: 10px;
		cursor: pointer;
		flex-shrink: 0;
		border: 1.5px solid rgba(0, 0, 0, 0.06);
		transition: all 0.2s ease;
	}

	#captcha-canvas:hover {
		border-color: rgba(0, 0, 0, 0.12);
	}

	.refresh-btn {
		width: 44px;
		height: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #f5f5fa;
		border: 1.5px solid transparent;
		border-radius: 12px;
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
		padding: 14px;
		background: #1a1a2e;
		color: #ffffff;
		border: none;
		border-radius: 12px;
		font-size: 0.9375rem;
		font-weight: 600;
		font-family: inherit;
		cursor: pointer;
		transition: all 0.25s ease;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
	}

	.submit-btn:hover {
		background: #2d2d44;
		transform: translateY(-2px);
		box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
	}

	.submit-btn:active {
		transform: translateY(0);
	}

	.success {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 12px;
		padding: 24px;
		color: #2e7d32;
		background: #e8f5e9;
		border-radius: 14px;
		font-size: 0.9375rem;
		font-weight: 600;
		animation: scaleIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.success-icon {
		width: 40px;
		height: 40px;
		border-radius: 50%;
		background: #22c55e;
		color: #ffffff;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	@media (max-width: 640px) {
		.card {
			padding: 20px;
			border-radius: 16px;
		}

		.header {
			gap: 12px;
			margin-bottom: 24px;
		}

		.header-icon {
			width: 40px;
			height: 40px;
			border-radius: 12px;
		}

		.header-text h2 {
			font-size: 1.125rem;
		}

		.captcha-row {
			gap: 8px;
		}

		.captcha-input {
			padding: 10px 14px 10px 40px;
			font-size: 0.8125rem;
			letter-spacing: 3px;
		}

		#captcha-canvas {
			width: 100px;
			height: 38px;
		}

		.refresh-btn {
			width: 40px;
			height: 40px;
		}

		.input-icon {
			width: 16px;
			height: 16px;
			left: 12px;
		}

		.bvid-input, .captcha-input {
			padding-left: 38px;
		}
	}
</style>
