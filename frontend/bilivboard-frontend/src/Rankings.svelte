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

	function getRankIcon(rank) {
		if (rank === 1) return 'I';
		if (rank === 2) return 'II';
		if (rank === 3) return 'III';
		return null;
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
						{#if item.rank <= 3}
							<span class="rank-icon">{getRankIcon(item.rank)}</span>
						{:else}
							<span class="rank-num">{item.rank}</span>
						{/if}
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
							<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
							{formatNumber(item.views)}
						</span>
						<span class="stat">
							<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z"/></svg>
							{formatNumber(item.likes)}
						</span>
						<span class="stat">
							<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.31-8.86c-1.77-.45-2.34-.94-2.34-1.67 0-.84.79-1.43 2.1-1.43 1.38 0 1.9.66 1.94 1.64h1.71c-.05-1.34-.87-2.57-2.49-2.97V5H10.9v1.69c-1.51.32-2.72 1.3-2.72 2.81 0 1.79 1.49 2.69 3.66 3.21 1.95.46 2.34 1.15 2.34 1.87 0 .53-.39 1.39-2.1 1.39-1.6 0-2.23-.72-2.32-1.64H8.64c.1 1.7 1.36 2.66 2.73 2.97V19h2.34v-1.67c1.52-.29 2.72-1.16 2.73-2.77-.01-2.2-1.9-2.96-3.66-3.42z"/></svg>
							{formatNumber(item.coins)}
						</span>
						<span class="stat">
							<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
							{formatNumber(item.favorites)}
						</span>
					</div>
					<div class="bottom-row">
						<span class="rate-badge" class:up={item.rate > 0} class:down={item.rate < 0} class:zero={item.rate === 0}>
							<svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor">
								{#if item.rate > 0}
									<path d="M7 14l5-5 5 5z"/>
								{:else if item.rate < 0}
									<path d="M7 10l5 5 5-5z"/>
								{:else}
									<path d="M5 11h14v2H5z"/>
								{/if}
							</svg>
							<span class="rate-value">{item.rate > 0 ? '+' : ''}{item.rate}%</span>
						</span>
						<span class="rank-change-badge" class:up={item.rankChange > 0} class:down={item.rankChange < 0} class:same={item.rankChange === 0}>
							{#if item.rankChange > 0}
								↑{item.rankChange}
							{:else if item.rankChange < 0}
								↓{Math.abs(item.rankChange)}
							{:else}
								—
							{/if}
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
				<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<path d="M18 6L6 18M6 6l12 12"/>
				</svg>
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
						<div class="stat-icon play">
							<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.views)}</span>
						<span class="stat-label">播放</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon like">
							<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.likes)}</span>
						<span class="stat-label">点赞</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon coin">
							<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.31-8.86c-1.77-.45-2.34-.94-2.34-1.67 0-.84.79-1.43 2.1-1.43 1.38 0 1.9.66 1.94 1.64h1.71c-.05-1.34-.87-2.57-2.49-2.97V5H10.9v1.69c-1.51.32-2.72 1.3-2.72 2.81 0 1.79 1.49 2.69 3.66 3.21 1.95.46 2.34 1.15 2.34 1.87 0 .53-.39 1.39-2.1 1.39-1.6 0-2.23-.72-2.32-1.64H8.64c.1 1.7 1.36 2.66 2.73 2.97V19h2.34v-1.67c1.52-.29 2.72-1.16 2.73-2.77-.01-2.2-1.9-2.96-3.66-3.42z"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.coins)}</span>
						<span class="stat-label">投币</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon fav">
							<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.favorites)}</span>
						<span class="stat-label">收藏</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon share">
							<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/></svg>
						</div>
						<span class="stat-value">{formatNumber(selectedItem.shares)}</span>
						<span class="stat-label">转发</span>
					</div>
					<div class="stat-item">
						<div class="stat-icon danmaku">
							<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
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
		background-color: #fafafa;
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

	.rank-icon {
		font-size: 0.75rem;
		font-weight: 700;
		letter-spacing: 0.05em;
		line-height: 1;
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
		color: #fff;
		background: #1a1a2e;
	}

	.stat-icon.play,
	.stat-icon.like,
	.stat-icon.coin,
	.stat-icon.fav,
	.stat-icon.share,
	.stat-icon.danmaku {
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
