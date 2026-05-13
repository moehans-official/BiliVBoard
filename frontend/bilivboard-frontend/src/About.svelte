<section class="about">
	<h2>关于</h2>
	<p class="desc">BiliVBoard 是一个B站视频数据采集与智能评分系统，支持多种评分算法。</p>

	<div class="algorithms">
		<div class="algo">
			<h3>V3 Normal / 普通版</h3>
			<p class="algo-desc">基础热度 × 互动增强 × 时间衰减 × 放大系数</p>
			<pre class="formula">Score = 10000 + ln(P+1) × (1 + 0.3×ln(C+1)) × (1 + 1.5×I_rate) × e^(-T/30) × 800</pre>
		</div>

		<div class="algo">
			<h3>V3 Radical / 激进版</h3>
			<p class="algo-desc">更短的半衰期（6.93天），更强的互动权重</p>
			<pre class="formula">Score = 10000 + ln(P+1) × (1 + 3×I_rate) × e^(-T/10) × 500</pre>
		</div>

		<div class="algo">
			<h3>V3 E SP / 无时间衰减版</h3>
			<p class="algo-desc">去掉时间衰减因子，适用于长期评估</p>
			<pre class="formula">Score = 10000 + ln(P+1) × (1 + 0.3×ln(C+1)) × (1 + 1.5×I_rate) × 800</pre>
		</div>
	</div>

	<div class="contact">
		<h3>联系我们</h3>
		<p>GitHub: <a href="https://github.com/moehans-official/BiliVBoard" target="_blank" rel="noopener">moehans-official/BiliVBoard</a></p>
		<p>邮箱: <a href="mailto:contact@moehans.com">contact@moehans.com</a></p>
	</div>

	<div class="disclaimer">
		<h3>声明</h3>
		<p>BiliVBoard术力口周榜周榜首刊于2026年5月17日，收录包括但不限于使用VOCALOID、UTAU、SynthesizerV、CEVIO、初音ミクNT等音声合成引擎制作的歌曲（统称"术曲"）</p>
	</div>
</section>

<style>
	.about {
		max-width: 640px;
		margin: 0 auto;
	}

	h2 {
		color: #111111;
		font-size: 1.25rem;
		margin: 0 0 8px 0;
		font-weight: 500;
		letter-spacing: 1px;
		text-align: center;
	}

	.desc {
		color: #666666;
		font-size: 0.875rem;
		margin: 0 0 40px 0;
		text-align: center;
	}

	.algorithms {
		display: flex;
		flex-direction: column;
		gap: 16px;
		margin-bottom: 40px;
	}

	.algo {
		padding: 20px;
		background-color: #f8f8f8;
		border-radius: 8px;
	}

	.algo h3 {
		color: #111111;
		font-size: 0.875rem;
		margin: 0 0 8px 0;
		font-weight: 500;
	}

	.algo-desc {
		color: #666666;
		font-size: 0.75rem;
		margin: 0 0 12px 0;
	}

	.formula {
		color: #111111;
		font-size: 0.75rem;
		background-color: #ffffff;
		padding: 12px;
		border-radius: 4px;
		overflow-x: auto;
		margin: 0;
		font-family: 'SF Mono', Monaco, monospace;
		line-height: 1.6;
	}

	.contact {
		padding: 24px 0;
		border-top: 1px solid #eeeeee;
		margin-bottom: 24px;
	}

	.contact h3 {
		color: #111111;
		font-size: 0.875rem;
		margin: 0 0 8px 0;
		font-weight: 500;
	}

	.contact p {
		color: #666666;
		font-size: 0.875rem;
		margin: 0;
	}

	.contact a {
		color: #111111;
		text-decoration: underline;
	}

	.disclaimer {
		padding: 24px 0;
		border-top: 1px solid #eeeeee;
	}

	.disclaimer h3 {
		color: #111111;
		font-size: 0.875rem;
		margin: 0 0 8px 0;
		font-weight: 500;
	}

	.disclaimer p {
		color: #666666;
		font-size: 0.875rem;
		line-height: 1.6;
		margin: 0;
	}
</style>
