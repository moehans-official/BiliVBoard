<script>
	let formulasOpen = [true, false, false];

	function toggleFormula(index) {
		formulasOpen[index] = !formulasOpen[index];
		formulasOpen = [...formulasOpen];
	}
</script>

<section class="about">
	<div class="card">
		<h2>关于</h2>
		<p class="desc">BiliVBoard 是一个B站视频数据采集与智能评分系统，支持多种评分算法。</p>

		<div class="formulas">
			{#each [
				{
					name: 'V3 Normal / 普通版',
					desc: '基础热度 × 互动增强 × 时间衰减 × 放大系数',
					formula: 'Score = 10000 + ln(P+1) × (1 + 0.3×ln(C+1)) × (1 + 1.5×I_rate) × e^(-T/30) × 800',
					halfLife: '半衰期约 20.79 天'
				},
				{
					name: 'V3 Radical / 激进版',
					desc: '更短的半衰期，更强的互动权重',
					formula: 'Score = 10000 + ln(P+1) × (1 + 3×I_rate) × e^(-T/10) × 500',
					halfLife: '半衰期约 6.93 天'
				},
				{
					name: 'V3 E SP / 无时间衰减版',
					desc: '去掉时间衰减因子，适用于长期评估',
					formula: 'Score = 10000 + ln(P+1) × (1 + 0.3×ln(C+1)) × (1 + 1.5×I_rate) × 800',
					halfLife: '无时间衰减'
				}
			] as algo, i}
				<div class="algo-item">
					<button class="algo-header" on:click={() => toggleFormula(i)}>
						<span class="algo-name">{algo.name}</span>
						<span class="chevron" class:open={formulasOpen[i]}>
							<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<polyline points="6 9 12 15 18 9"/>
							</svg>
						</span>
					</button>
					{#if formulasOpen[i]}
						<div class="algo-body">
							<p class="algo-desc">{algo.desc}</p>
							<pre class="formula">{algo.formula}</pre>
							<span class="half-life">{algo.halfLife}</span>
						</div>
					{/if}
				</div>
			{/each}
		</div>

		<div class="contact">
			<h3>联系我们</h3>
			<div class="contact-links">
				<a href="https://github.com/moehans-official/BiliVBoard" target="_blank" rel="noopener" class="contact-link">
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>
					</svg>
					GitHub
				</a>
				<a href="mailto:contact@moehans.com" class="contact-link">
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
						<polyline points="22,6 12,13 2,6"/>
					</svg>
					contact@moehans.com
				</a>
			</div>
		</div>

		<div class="intro">
			<h3>项目介绍</h3>
			<p>BiliVBoard 是一个面向B站术力口（VOCALOID等音声合成引擎制作歌曲）领域的视频排行榜系统。通过自动化数据采集与多维度评分算法，为创作者和爱好者提供透明、客观的排名参考，记录每一首术曲的影响力。</p>
		</div>

		<div class="disclaimer">
			<h3>参考项目</h3>
			<p>本项目设计参考了 <a href="https://biliboard.uk/" target="_blank" rel="noopener">BiliBoard</a> 的榜单展示理念，所有评分算法与数据来源均为独立开发。</p>
		</div>
	</div>
</section>

<style>
	.about {
		max-width: 640px;
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
		margin: 0 0 28px 0;
	}

	.formulas {
		display: flex;
		flex-direction: column;
		gap: 8px;
		margin-bottom: 28px;
	}

	.algo-item {
		border: 1px solid #f0f0f5;
		border-radius: 12px;
		overflow: hidden;
		transition: border-color 0.2s;
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

	.algo-name {
		color: #1a1a2e;
		font-size: 0.875rem;
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
		color: #8e8ea0;
		font-size: 0.75rem;
		margin: 0 0 10px 0;
	}

	.formula {
		color: #1a1a2e;
		font-size: 0.75rem;
		background: #f5f5fa;
		padding: 12px;
		border-radius: 8px;
		overflow-x: auto;
		margin: 0 0 8px 0;
		font-family: 'SF Mono', Monaco, monospace;
		line-height: 1.6;
	}

	.half-life {
		display: block;
		color: #a0a0b0;
		font-size: 0.6875rem;
	}

	.contact {
		padding-top: 24px;
		margin-bottom: 24px;
		border-top: 1px solid #f0f0f5;
	}

	.contact h3 {
		color: #1a1a2e;
		font-size: 0.875rem;
		margin: 0 0 12px 0;
		font-weight: 600;
	}

	.contact-links {
		display: flex;
		gap: 10px;
	}

	.contact-link {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 10px 16px;
		background: #f5f5fa;
		color: #1a1a2e;
		text-decoration: none;
		border-radius: 10px;
		font-size: 0.8125rem;
		font-weight: 500;
		transition: all 0.2s ease;
	}

	.contact-link:hover {
		background: #e5e5ea;
		transform: translateY(-1px);
	}

	.intro {
		padding-top: 24px;
		margin-bottom: 24px;
		border-top: 1px solid #f0f0f5;
	}

	.intro h3 {
		color: #1a1a2e;
		font-size: 0.875rem;
		margin: 0 0 8px 0;
		font-weight: 600;
	}

	.intro p {
		color: #6b7280;
		font-size: 0.8125rem;
		line-height: 1.6;
		margin: 0;
	}

	.disclaimer {
		padding-top: 24px;
		border-top: 1px solid #f0f0f5;
	}

	.disclaimer h3 {
		color: #1a1a2e;
		font-size: 0.875rem;
		margin: 0 0 8px 0;
		font-weight: 600;
	}

	.disclaimer p {
		color: #6b7280;
		font-size: 0.8125rem;
		line-height: 1.6;
		margin: 0;
	}

	.disclaimer a {
		color: #1a1a2e;
		text-decoration: underline;
		font-weight: 500;
	}

	@media (max-width: 640px) {
		.card {
			padding: 20px;
			border-radius: 12px;
		}

		.contact-links {
			flex-direction: column;
			gap: 8px;
		}

		.contact-link {
			justify-content: center;
			padding: 12px;
		}

		.formula {
			font-size: 0.6875rem;
			padding: 10px;
		}
	}
</style>
