<script>
	let formulasOpen = [true, false, false];

	function toggleFormula(index) {
		formulasOpen[index] = !formulasOpen[index];
		formulasOpen = [...formulasOpen];
	}
</script>

<section class="about">
	<div class="hero-card">
		<div class="hero-header">
			<div class="hero-icon">
				<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>
			</div>
			<div class="hero-text">
				<h2>关于 BiliVBoard</h2>
				<p class="desc">B站术力口视频数据采集与智能评分系统</p>
			</div>
		</div>
		<p class="intro">BiliVBoard 是一个面向B站术力口（VOCALOID等音声合成引擎制作歌曲）领域的视频排行榜系统。通过自动化数据采集与多维度评分算法，为创作者和爱好者提供透明、客观的排名参考，记录每一首术曲的影响力。</p>
	</div>

	<div class="card">
		<div class="section-header">
			<h3>评分算法</h3>
			<span class="section-tag">3 种公式</span>
		</div>

		<div class="formulas">
			{#each [
				{
					name: 'V3 Normal',
					subtitle: '普通版',
					desc: '基础热度 × 互动增强 × 时间衰减 × 放大系数',
					formula: 'Score = 10000 + ln(P+1) × (1 + 0.3×ln(C+1)) × (1 + 1.5×I_rate) × e^(-T/30) × 800',
					halfLife: '半衰期约 20.79 天'
				},
				{
					name: 'V3 Radical',
					subtitle: '激进版',
					desc: '更短的半衰期，更强的互动权重',
					formula: 'Score = 10000 + ln(P+1) × (1 + 3×I_rate) × e^(-T/10) × 500',
					halfLife: '半衰期约 6.93 天'
				},
				{
					name: 'V3 E SP',
					subtitle: '无时间衰减版',
					desc: '去掉时间衰减因子，适用于长期评估',
					formula: 'Score = 10000 + ln(P+1) × (1 + 0.3×ln(C+1)) × (1 + 1.5×I_rate) × 800',
					halfLife: '无时间衰减'
				}
			] as algo, i}
				<div class="algo-item">
					<button class="algo-header" on:click={() => toggleFormula(i)}>
						<div class="algo-info">
						<div class="algo-badge">
							{algo.name}
						</div>
							<span class="algo-subtitle">{algo.subtitle}</span>
						</div>
						<span class="chevron" class:open={formulasOpen[i]}>
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
						</span>
					</button>
					{#if formulasOpen[i]}
						<div class="algo-body">
							<p class="algo-desc">{algo.desc}</p>
							<pre class="formula">{algo.formula}</pre>
							<div class="algo-meta">
								<span class="half-life">
									<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
									{algo.halfLife}
								</span>
							</div>
						</div>
					{/if}
				</div>
			{/each}
		</div>
	</div>

	<div class="card">
		<div class="section-header">
			<h3>联系我们</h3>
		</div>
		<div class="contact-links">
			<a href="https://github.com/moehans-official/BiliVBoard" target="_blank" rel="noopener" class="contact-link">
				<div class="contact-icon github">
					<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 2.183-.322 1.176 0 2.37.302 2.37.302 1.315.302 1.58 1.62 1.58 1.62 1.005 2.72 2.62 1.95 3.26 1.49.093-.725.395-1.95.715-2.405-2.51-.285-5.155-1.255-5.155-5.585 0-1.23.44-2.235 1.155-3.025-.115-.285-.5-1.435.11-2.99 0 0 .88-.28 2.88-2.88 1.365-.38 2.85-.38 4.215 0 1.995 2.6 2.865 2.88 2.865 2.88.615 1.555.225 2.705.11 2.99.72.79 1.155 1.795 1.155 3.025 0 4.34-2.65 5.3-5.16 5.58.405.35.765 1.045.765 2.11 0 1.525-.015 2.755-.015 3.13 0 .32.225.695.825.577C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
				</div>
				<span>GitHub</span>
			</a>
			<a href="mailto:contact@moehans.com" class="contact-link">
				<div class="contact-icon email">
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
						<polyline points="22,6 12,13 2,6"/>
					</svg>
				</div>
				<span>contact@moehans.com</span>
			</a>
		</div>
	</div>

	<div class="disclaimer-card">
		<div class="disclaimer-header">
			<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
				<circle cx="12" cy="12" r="10"/>
				<line x1="12" y1="8" x2="12" y2="12"/>
				<line x1="12" y1="16" x2="12.01" y2="16"/>
			</svg>
			<span>参考声明</span>
		</div>
		<p>本项目设计参考了 <a href="https://biliboard.uk/" target="_blank" rel="noopener">BiliBoard</a> 的榜单展示理念，所有评分算法与数据来源均为独立开发。</p>
	</div>
</section>

<style>
	.about {
		max-width: 640px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.hero-card {
		background: #1a1a2e;
		border-radius: 20px;
		padding: 32px;
		color: #ffffff;
		animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
	}

	.hero-header {
		display: flex;
		align-items: center;
		gap: 16px;
		margin-bottom: 20px;
	}

	.hero-icon {
		width: 52px;
		height: 52px;
		border-radius: 14px;
		background: rgba(255, 255, 255, 0.15);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.hero-text h2 {
		font-size: 1.375rem;
		margin: 0 0 4px 0;
		font-weight: 700;
		letter-spacing: -0.02em;
	}

	.desc {
		font-size: 0.875rem;
		opacity: 0.85;
		font-weight: 500;
		margin: 0;
	}

	.intro {
		font-size: 0.9375rem;
		line-height: 1.7;
		opacity: 0.9;
		margin: 0;
	}

	.card {
		background: #ffffff;
		border-radius: 20px;
		padding: 28px;
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
		border: 1px solid rgba(0, 0, 0, 0.04);
		animation: slideUp 0.4s ease-out backwards;
	}

	.card:nth-child(2) { animation-delay: 0.1s; }
	.card:nth-child(3) { animation-delay: 0.15s; }

	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20px;
	}

	.section-header h3 {
		color: #1a1a2e;
		font-size: 1rem;
		margin: 0;
		font-weight: 700;
	}

	.section-tag {
		color: #8e8ea0;
		font-size: 0.75rem;
		font-weight: 500;
		background: #f5f5f7;
		padding: 3px 10px;
		border-radius: 6px;
	}

	.formulas {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.algo-item {
		border: 1.5px solid #f0f0f5;
		border-radius: 14px;
		overflow: hidden;
		transition: all 0.2s ease;
	}

	.algo-item:hover {
		border-color: #e0e0ea;
	}

	.algo-header {
		width: 100%;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 14px 16px;
		background: transparent;
		border: none;
		cursor: pointer;
		font-family: inherit;
	}

	.algo-info {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.algo-badge {
		font-size: 0.8125rem;
		font-weight: 700;
		color: #ffffff;
		padding: 3px 10px;
		border-radius: 6px;
		background: #1a1a2e;
	}

	.algo-subtitle {
		color: #8e8ea0;
		font-size: 0.8125rem;
		font-weight: 500;
	}

	.chevron {
		color: #a0a0b0;
		transition: transform 0.25s ease;
	}

	.chevron.open {
		transform: rotate(180deg);
	}

	.algo-body {
		padding: 0 16px 16px;
		animation: fadeIn 0.3s ease-out;
	}

	.algo-desc {
		color: #6b7280;
		font-size: 0.8125rem;
		margin: 0 0 12px 0;
		line-height: 1.5;
	}

	.formula {
		color: #1a1a2e;
		font-size: 0.8125rem;
		background: #f5f5fa;
		padding: 14px;
		border-radius: 10px;
		overflow-x: auto;
		margin: 0 0 10px 0;
		font-family: 'SF Mono', Monaco, monospace;
		line-height: 1.6;
		border: 1px solid rgba(0, 0, 0, 0.04);
	}

	.algo-meta {
		display: flex;
		gap: 16px;
	}

	.half-life {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		color: #a0a0b0;
		font-size: 0.75rem;
		font-weight: 500;
	}

	.half-life svg {
		flex-shrink: 0;
	}

	.contact-links {
		display: flex;
		gap: 12px;
	}

	.contact-link {
		display: inline-flex;
		align-items: center;
		gap: 10px;
		padding: 12px 16px;
		background: #f5f5fa;
		color: #1a1a2e;
		text-decoration: none;
		border-radius: 12px;
		font-size: 0.8125rem;
		font-weight: 600;
		transition: all 0.2s ease;
		flex: 1;
		justify-content: center;
	}

	.contact-link:hover {
		background: #e5e5ea;
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
	}

	.contact-icon {
		width: 32px;
		height: 32px;
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.contact-icon.github {
		background: #1a1a2e;
		color: #ffffff;
	}

	.contact-icon.email {
		background: #1a1a2e;
		color: #ffffff;
	}

	.disclaimer-card {
		background: #fafafa;
		border: 1px solid #f0f0f5;
		border-radius: 16px;
		padding: 20px;
		animation: slideUp 0.4s ease-out 0.2s backwards;
	}

	.disclaimer-header {
		display: flex;
		align-items: center;
		gap: 6px;
		color: #a0a0b0;
		font-size: 0.75rem;
		font-weight: 600;
		margin-bottom: 8px;
	}

	.disclaimer-card p {
		color: #6b7280;
		font-size: 0.8125rem;
		line-height: 1.6;
		margin: 0;
	}

	.disclaimer-card a {
		color: #1a1a2e;
		text-decoration: underline;
		font-weight: 600;
	}

	@media (max-width: 640px) {
		.about {
			gap: 16px;
		}

		.hero-card {
			padding: 24px;
			border-radius: 16px;
		}

		.hero-text h2 {
			font-size: 1.25rem;
		}

		.intro {
			font-size: 0.875rem;
		}

		.card {
			padding: 20px;
			border-radius: 16px;
		}

		.contact-links {
			flex-direction: column;
			gap: 8px;
		}

		.contact-link {
			padding: 12px;
		}

		.formula {
			font-size: 0.6875rem;
			padding: 10px;
		}

		.algo-badge {
			font-size: 0.75rem;
			padding: 2px 8px;
		}
	}
</style>
