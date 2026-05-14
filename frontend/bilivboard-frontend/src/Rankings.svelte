<script>
	import { onMount } from 'svelte';

	let animatedScores = {};
	let selectedItem = null;

	let rankings = Array.from({ length: 20 }, (_, i) => {
		const rate = (Math.random() * 40 - 10).toFixed(1);
		const rankChange = Math.floor(Math.random() * 10) - 3;
		return {
			rank: i + 1,
			bvid: `BV1xxxxx${i + 1}`,
			title: `视频标题 ${i + 1} - 这是一个示例标题`,
			author: `UP主 ${i + 1}`,
			score: Math.floor(Math.random() * 100),
			cover: `https://picsum.photos/640/360?random=${i + 1}`,
			views: Math.floor(Math.random() * 1000000),
			likes: Math.floor(Math.random() * 100000),
			coins: Math.floor(Math.random() * 50000),
			favorites: Math.floor(Math.random() * 30000),
			shares: Math.floor(Math.random() * 10000),
			danmaku: Math.floor(Math.random() * 5000),
			rate: parseFloat(rate),
			rankChange: rankChange,
			lastRank: i + 1 + rankChange,
			timesOnChart: Math.floor(Math.random() * 20) + 1,
			weeksOnChart: Math.floor(Math.random() * 12) + 1
		};
	});

	onMount(() => {
		rankings.forEach((item, index) => {
			animatedScores[item.rank] = 0;
			setTimeout(() => {
				animateScore(item.rank, item.score);
			}, index * 80);
		});
	});

	function animateScore(rank, target) {
		const duration = 800;
		const steps = 24;
		const increment = target / steps;
		let current = 0;
		let step = 0;

		const timer = setInterval(() => {
			step++;
			current = Math.min(Math.round(increment * step), target);
			animatedScores[rank] = current;
			animatedScores = { ...animatedScores };

			if (step >= steps) {
				clearInterval(timer);
				animatedScores[rank] = target;
				animatedScores = { ...animatedScores };
			}
		}, duration / steps);
	}

	function formatNumber(num) {
		if (num >= 10000) {
			return (num / 10000).toFixed(1) + '万';
		}
		return num.toLocaleString();
	}

	function openDetail(item) {
		selectedItem = item;
	}

	function closeDetail() {
		selectedItem = null;
	}

	function getRankClass(rank) {
		if (rank === 1) return 'gold';
		if (rank === 2) return 'silver';
		if (rank === 3) return 'bronze';
		return '';
	}
</script>

<section class="ranking">
	<div class="section-header">
		<div class="header-left">
			<h2>TOP 20</h2>
			<span class="period">第 12 期</span>
		</div>
		<span class="count">{rankings.length} 条目</span>
	</div>
	<div class="grid">
		{#each rankings as item, index}
			<div class="card" class:top3={item.rank <= 3} on:click={() => openDetail(item)}>
				<div class="cover-wrapper">
					<img src={item.cover} alt={item.title} class="cover" />
					<div class="cover-overlay" />
					<div class="rank-badge {getRankClass(item.rank)}">
						<span class="rank-num">#{item.rank}</span>
					</div>
					<div class="score-overlay">
						<span class="score">{animatedScores[item.rank] ?? 0}</span>
					</div>
				</div>
				<div class="card-body">
					<div class="info">
						<span class="title">{item.title}</span>
						<span class="author">{item.author}</span>
					</div>
					<div class="stats-row">
						<span class="stat">
							<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
							{formatNumber(item.views)}
						</span>
						<span class="stat">
							<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10h10"/><path d="M7 14h6"/><path d="M12 18H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6"/><path d="M22 18H12a2 2 0 0 0-2 2v0a2 2 0 0 0 2 2h10"/></svg>
							{formatNumber(item.likes)}
						</span>
						<span class="stat">
							<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M15 9.5a3 3 0 0 0-6 0"/></svg>
							{formatNumber(item.coins)}
						</span>
						<span class="stat">
							<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
							{formatNumber(item.favorites)}
						</span>
					</div>
					<div class="bottom-row">
						<span class="rate-badge" class:up={item.rate > 0} class:down={item.rate < 0} class:zero={item.rate === 0}>
							{#if item.rate > 0}
								<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>
							{:else if item.rate < 0}
								<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
							{:else}
								<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/></svg>
							{/if}
							<span class="rate-value">{item.rate > 0 ? '+' : ''}{item.rate}%</span>
						</span>
						<span class="rank-change-badge" class:up={item.rankChange > 0} class:down={item.rankChange < 0} class:same={item.rankChange === 0}>
							{#if item.rankChange > 0}
								<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>
							{:else if item.rankChange < 0}
								<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
							{:else}
								<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/></svg>
							{/if}
							{Math.abs(item.rankChange)}
						</span>
					</div>
				</div>
			</div>
		{/each}
	</div>
</section>

{#if selectedItem}
	<div class="overlay" on:click={closeDetail}>
		<div class="modal" on:click|stopPropagation>
			<button class="close" on:click={closeDetail}>
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
			</button>
			<div class="modal-cover-wrapper">
				<img src={selectedItem.cover} alt={selectedItem.title} class="modal-cover" />
				<div class="modal-score">
					<span class="score-label">评分</span>
					<span class="score-value-modal">{selectedItem.score}</span>
				</div>
			</div>
			<div class="detail">
				<h3>{selectedItem.title}</h3>
				<p class="modal-author">{selectedItem.author}</p>
				<div class="stats-grid">
					<div class="stat-item">
						<div class="stat-icon">
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.views)}</span>
						<span class="stat-label">播放</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon">
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10h10"/><path d="M7 14h6"/><path d="M12 18H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6"/><path d="M22 18H12a2 2 0 0 0-2 2v0a2 2 0 0 0 2 2h10"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.likes)}</span>
						<span class="stat-label">点赞</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon">
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M15 9.5a3 3 0 0 0-6 0"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.coins)}</span>
						<span class="stat-label">投币</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon">
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.favorites)}</span>
						<span class="stat-label">收藏</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon">
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 8h.01"/><path d="M6 6h16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2Z"/><path d="M6 6V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.shares)}</span>
						<span class="stat-label">转发</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon">
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.danmaku)}</span>
						<span class="stat-label">弹幕</span>
					</div>
				</div>
				<div class="rank-info">
					<div class="rank-item">
						<span class="rank-value">#{selectedItem.lastRank}</span>
						<span class="rank-label">上次排名</span>
					</div>
					<div class="rank-item">
						<span class="rank-value">{selectedItem.timesOnChart}</span>
						<span class="rank-label">上榜次数</span>
					</div>
					<div class="rank-item">
						<span class="rank-value">{selectedItem.weeksOnChart}周</span>
						<span class="rank-label">上榜周数</span>
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.ranking {
		background: #ffffff;
		border-radius: 20px;
		padding: 28px;
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
	}

	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 24px;
	}

	.header-left {
		display: flex;
		align-items: baseline;
		gap: 12px;
	}

	h2 {
		color: #1a1a2e;
		font-size: 1.25rem;
		margin: 0;
		font-weight: 700;
		letter-spacing: -0.02em;
	}

	.period {
		color: #8e8ea0;
		font-size: 0.875rem;
		font-weight: 500;
	}

	.count {
		color: #b0b0c0;
		font-size: 0.8125rem;
		font-weight: 500;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
		gap: 20px;
	}

	.card {
		background-color: #fafafa;
		border-radius: 16px;
		overflow: hidden;
		cursor: pointer;
		transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
		animation: slideUp 0.4s ease-out backwards;
		position: relative;
		border: 1px solid rgba(0, 0, 0, 0.04);
	}

	.card:hover {
		transform: translateY(-4px);
		box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04);
		border-color: transparent;
	}

	.card.top3 {
		background-color: #f5f5f5;
	}

	.card.top3:hover {
		box-shadow: 0 12px 28px rgba(0, 0, 0, 0.1), 0 4px 12px rgba(0, 0, 0, 0.05);
	}

	.cover-wrapper {
		position: relative;
		width: 100%;
		aspect-ratio: 16 / 9;
		overflow: hidden;
	}

	.cover {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
	}

	.card:hover .cover {
		transform: scale(1.06);
	}

	.cover-overlay {
		position: absolute;
		inset: 0;
		background: linear-gradient(to top, rgba(0,0,0,0.35) 0%, transparent 50%);
		pointer-events: none;
	}

	.rank-badge {
		position: absolute;
		top: 12px;
		left: 12px;
		background: rgba(255, 255, 255, 0.92);
		backdrop-filter: blur(8px);
		padding: 5px 12px;
		border-radius: 10px;
		display: flex;
		align-items: center;
		gap: 5px;
		z-index: 1;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
	}

	.rank-badge.gold {
		background: rgba(26, 26, 46, 0.85);
		color: #fff;
	}

	.rank-badge.silver {
		background: rgba(100, 100, 120, 0.85);
		color: #fff;
	}

	.rank-badge.bronze {
		background: rgba(160, 160, 176, 0.85);
		color: #fff;
	}

	.rank-num {
		font-size: 0.8125rem;
		font-weight: 700;
		letter-spacing: -0.01em;
	}

	.score-overlay {
		position: absolute;
		bottom: 12px;
		right: 12px;
		background: rgba(0, 0, 0, 0.75);
		backdrop-filter: blur(8px);
		color: #fff;
		padding: 5px 14px;
		border-radius: 10px;
		font-size: 1.25rem;
		font-weight: 800;
		font-variant-numeric: tabular-nums;
		letter-spacing: -0.02em;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
	}

	.card-body {
		padding: 16px;
	}

	.info {
		display: flex;
		flex-direction: column;
		gap: 4px;
		margin-bottom: 10px;
	}

	.title {
		color: #1a1a2e;
		font-size: 0.9375rem;
		font-weight: 600;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		line-height: 1.4;
	}

	.author {
		color: #a0a0b0;
		font-size: 0.8125rem;
		font-weight: 500;
	}

	.stats-row {
		display: flex;
		gap: 14px;
		padding-bottom: 10px;
		margin-bottom: 10px;
		border-bottom: 1px solid rgba(0, 0, 0, 0.05);
	}

	.stat {
		display: flex;
		align-items: center;
		gap: 5px;
		color: #1a1a2e;
		font-size: 0.8125rem;
		font-weight: 700;
		font-variant-numeric: tabular-nums;
	}

	.stat svg {
		color: #a0a0b0;
		flex-shrink: 0;
	}

	.bottom-row {
		display: flex;
		justify-content: flex-end;
		gap: 8px;
		align-items: center;
	}

	.rate-badge {
		display: inline-flex;
		align-items: center;
		gap: 3px;
		padding: 4px 10px;
		border-radius: 8px;
		font-size: 0.75rem;
		font-weight: 700;
		font-variant-numeric: tabular-nums;
		letter-spacing: -0.01em;
		transition: all 0.2s ease;
	}

	.rate-badge.up {
		background: #e8f5e9;
		color: #2e7d32;
	}

	.rate-badge.down {
		background: #ffebee;
		color: #c62828;
	}

	.rate-badge.zero {
		background: #f1f5f9;
		color: #64748b;
	}

	.rank-change-badge {
		display: inline-flex;
		align-items: center;
		gap: 3px;
		padding: 4px 10px;
		border-radius: 8px;
		font-size: 0.75rem;
		font-weight: 700;
		font-variant-numeric: tabular-nums;
		transition: all 0.2s ease;
	}

	.rank-change-badge.up {
		background: #e8f5e9;
		color: #2e7d32;
	}

	.rank-change-badge.down {
		background: #ffebee;
		color: #c62828;
	}

	.rank-change-badge.same {
		background: #f1f5f9;
		color: #94a3b8;
	}

	/* Modal */
	.overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.65);
		backdrop-filter: blur(6px);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
		padding: 16px;
		animation: fadeIn 0.2s ease-out;
	}

	.modal {
		background-color: #ffffff;
		border-radius: 20px;
		max-width: 520px;
		width: 100%;
		overflow: hidden;
		position: relative;
		animation: scaleIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
		box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.3);
	}

	.close {
		position: absolute;
		top: 16px;
		right: 16px;
		background: rgba(255, 255, 255, 0.95);
		color: #1a1a2e;
		border: none;
		width: 36px;
		height: 36px;
		border-radius: 50%;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 2;
		transition: all 0.2s ease;
		box-shadow: 0 2px 12px rgba(0, 0, 0, 0.12);
	}

	.close:hover {
		transform: scale(1.1) rotate(90deg);
		background: #ffffff;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
	}

	.modal-cover-wrapper {
		position: relative;
		width: 100%;
		aspect-ratio: 16 / 9;
	}

	.modal-cover {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.modal-score {
		position: absolute;
		bottom: 16px;
		right: 16px;
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(8px);
		padding: 6px 16px;
		border-radius: 12px;
		display: flex;
		align-items: baseline;
		gap: 6px;
	}

	.score-label {
		color: rgba(255, 255, 255, 0.7);
		font-size: 0.75rem;
		font-weight: 600;
	}

	.score-value-modal {
		color: #ffffff;
		font-size: 1.5rem;
		font-weight: 800;
		font-variant-numeric: tabular-nums;
		letter-spacing: -0.02em;
	}

	.detail {
		padding: 24px;
	}

	.detail h3 {
		color: #1a1a2e;
		font-size: 1.125rem;
		margin: 0 0 4px 0;
		font-weight: 700;
		line-height: 1.4;
	}

	.modal-author {
		color: #8e8ea0;
		font-size: 0.875rem;
		font-weight: 500;
		margin: 0 0 24px 0;
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 12px;
		margin-bottom: 20px;
		padding-bottom: 20px;
		border-bottom: 1px solid #f0f0f5;
	}

	.stat-item {
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 6px;
		padding: 8px;
		border-radius: 12px;
		transition: background 0.2s ease;
	}

	.stat-item:hover {
		background: #f5f5f7;
	}

	.stat-icon {
		width: 32px;
		height: 32px;
		border-radius: 10px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #ffffff;
		background: #1a1a2e;
	}

	.stat-value {
		color: #1a1a2e;
		font-size: 0.9375rem;
		font-weight: 800;
		font-variant-numeric: tabular-nums;
		letter-spacing: -0.01em;
	}

	.stat-label {
		color: #a0a0b0;
		font-size: 0.6875rem;
		font-weight: 500;
	}

	.rank-info {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 12px;
	}

	.rank-item {
		text-align: center;
		padding: 12px;
		border-radius: 12px;
		background: #fafafa;
	}

	.rank-value {
		display: block;
		color: #1a1a2e;
		font-size: 1.0625rem;
		font-weight: 800;
		font-variant-numeric: tabular-nums;
		letter-spacing: -0.01em;
		margin-bottom: 2px;
	}

	.rank-label {
		color: #a0a0b0;
		font-size: 0.6875rem;
		font-weight: 500;
	}

	@media (max-width: 640px) {
		.ranking {
			padding: 16px;
			border-radius: 16px;
		}

		.grid {
			grid-template-columns: 1fr;
			gap: 16px;
		}

		.card {
			border-radius: 14px;
		}

		.card-body {
			padding: 14px;
		}

		.info {
			gap: 3px;
		}

		.title {
			font-size: 0.875rem;
		}

		.author {
			font-size: 0.75rem;
		}

		.stats-row {
			gap: 10px;
			padding-bottom: 8px;
			margin-bottom: 8px;
		}

		.stat {
			font-size: 0.75rem;
		}

		.stat svg {
			width: 12px;
			height: 12px;
		}

		.bottom-row {
			gap: 6px;
		}

		.rate-badge, .rank-change-badge {
			font-size: 0.6875rem;
			padding: 3px 7px;
		}

		.rate-badge svg, .rank-change-badge svg {
			width: 9px;
			height: 9px;
		}

		.score-overlay {
			font-size: 0.9375rem;
			padding: 4px 10px;
		}

		.rank-badge {
			padding: 4px 10px;
		}

		.rank-num {
			font-size: 0.6875rem;
		}

		.modal {
			max-width: 100%;
			border-radius: 20px 20px 0 0;
			max-height: 90vh;
			overflow-y: auto;
			position: fixed;
			bottom: 0;
			left: 0;
			right: 0;
		}

		.close {
			top: 12px;
			right: 12px;
			width: 32px;
			height: 32px;
		}

		.detail {
			padding: 16px;
		}

		.detail h3 {
			font-size: 0.9375rem;
		}

		.stats-grid {
			grid-template-columns: repeat(3, 1fr);
			gap: 8px;
			padding-bottom: 16px;
			margin-bottom: 16px;
		}

		.stat-icon {
			width: 28px;
			height: 28px;
			border-radius: 8px;
		}

		.stat-icon svg {
			width: 14px;
			height: 14px;
		}

		.stat-value {
			font-size: 0.8125rem;
		}

		.stat-label {
			font-size: 0.625rem;
		}

		.rank-info {
			gap: 8px;
		}

		.rank-item {
			padding: 10px;
		}

		.rank-value {
			font-size: 0.875rem;
		}

		.rank-label {
			font-size: 0.625rem;
		}

		.score-value-modal {
			font-size: 1.25rem;
		}

		.score-label {
			font-size: 0.6875rem;
		}
	}
</style>
