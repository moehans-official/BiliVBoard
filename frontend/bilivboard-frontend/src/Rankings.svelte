<script>
	let selectedItem = null;

	// 占位数据，后续接入真实数据
	let rankings = Array.from({ length: 20 }, (_, i) => {
		const rate = (Math.random() * 40 - 10).toFixed(1);
		const rankChange = Math.floor(Math.random() * 10) - 3;
		return {
			rank: i + 1,
			bvid: `BV1xxxxx${i + 1}`,
			title: `视频标题 ${i + 1} - 这是一个示例标题`,
			author: `UP主 ${i + 1}`,
			score: Math.floor(Math.random() * 100),
			cover: `https://picsum.photos/320/180?random=${i + 1}`,
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

	function openDetail(item) {
		selectedItem = item;
	}

	function closeDetail() {
		selectedItem = null;
	}

	function formatNumber(num) {
		if (num >= 10000) {
			return (num / 10000).toFixed(1) + '万';
		}
		return num.toLocaleString();
	}
</script>

<section class="ranking">
	<h2>TOP 20</h2>
	<div class="list">
		{#each rankings as item}
			<div class="card" on:click={() => openDetail(item)}>
				<span class="rank">{item.rank}</span>
				<img src={item.cover} alt={item.title} class="preview" />
				<div class="info">
					<span class="title">{item.title}</span>
					<span class="author">{item.author}</span>
				</div>
				<div class="right">
					<span class="score">{item.score}</span>
					<span class="rate" class:up={item.rate > 0} class:down={item.rate < 0}>
						{item.rate > 0 ? '+' : ''}{item.rate}%
					</span>
					<span class="rank-change" class:up={item.rankChange > 0} class:down={item.rankChange < 0} class:same={item.rankChange === 0}>
						{#if item.rankChange > 0}
							↑{item.rankChange}
						{:else if item.rankChange < 0}
							↓{Math.abs(item.rankChange)}
						{:else}
							一
						{/if}
					</span>
				</div>
			</div>
		{/each}
	</div>
</section>

{#if selectedItem}
	<div class="overlay" on:click={closeDetail}>
		<div class="modal" on:click|stopPropagation>
			<button class="close" on:click={closeDetail}>×</button>
			<img src={selectedItem.cover} alt={selectedItem.title} class="cover" />
			<div class="detail">
				<h3>{selectedItem.title}</h3>
				<p class="author">{selectedItem.author}</p>
				<div class="stats">
					<div class="stat">
						<span class="label">播放</span>
						<span class="value">{formatNumber(selectedItem.views)}</span>
					</div>
					<div class="stat">
						<span class="label">点赞</span>
						<span class="value">{formatNumber(selectedItem.likes)}</span>
					</div>
					<div class="stat">
						<span class="label">收藏</span>
						<span class="value">{formatNumber(selectedItem.favorites)}</span>
					</div>
					<div class="stat">
						<span class="label">转发</span>
						<span class="value">{formatNumber(selectedItem.shares)}</span>
					</div>
					<div class="stat">
						<span class="label">弹幕</span>
						<span class="value">{formatNumber(selectedItem.danmaku)}</span>
					</div>
				</div>
				<div class="rank-info">
					<div class="rank-item">
						<span class="label">上次排名</span>
						<span class="value">#{selectedItem.lastRank}</span>
					</div>
					<div class="rank-item">
						<span class="label">上榜次数</span>
						<span class="value">{selectedItem.timesOnChart}次</span>
					</div>
					<div class="rank-item">
						<span class="label">上榜周数</span>
						<span class="value">{selectedItem.weeksOnChart}周</span>
					</div>
				</div>
				<div class="final-score">
					<span>综合评分</span>
					<span class="score-value">{selectedItem.score}</span>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.ranking {
		max-width: 800px;
		margin: 0 auto;
	}

	h2 {
		color: #111111;
		font-size: 1.25rem;
		margin: 0 0 24px 0;
		font-weight: 500;
		letter-spacing: 1px;
	}

	.list {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.card {
		display: flex;
		align-items: center;
		padding: 12px;
		background-color: #ffffff;
		border: 1px solid #eeeeee;
		border-radius: 8px;
		gap: 12px;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.card:hover {
		background-color: #f8f8f8;
	}

	.rank {
		width: 24px;
		text-align: center;
		color: #999999;
		font-size: 0.875rem;
		font-weight: 500;
	}

	.preview {
		width: 80px;
		height: 45px;
		object-fit: cover;
		border-radius: 4px;
	}

	.info {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 4px;
		min-width: 0;
	}

	.title {
		color: #111111;
		font-size: 0.875rem;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.author {
		color: #999999;
		font-size: 0.75rem;
	}

	.right {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 4px;
	}

	.score {
		color: #111111;
		font-size: 1rem;
		font-weight: 600;
	}

	.rate {
		font-size: 0.75rem;
		font-weight: 500;
	}

	.rate.up {
		color: #22c55e;
	}

	.rate.down {
		color: #ef4444;
	}

	.rank-change {
		font-size: 0.75rem;
		font-weight: 500;
	}

	.rank-change.up {
		color: #22c55e;
	}

	.rank-change.down {
		color: #ef4444;
	}

	.rank-change.same {
		color: #999999;
	}

	/* Modal */
	.overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
		padding: 16px;
	}

	.modal {
		background-color: #ffffff;
		border-radius: 12px;
		max-width: 480px;
		width: 100%;
		overflow: hidden;
		position: relative;
	}

	.close {
		position: absolute;
		top: 12px;
		right: 12px;
		background: rgba(0, 0, 0, 0.5);
		color: #ffffff;
		border: none;
		width: 32px;
		height: 32px;
		border-radius: 50%;
		font-size: 1.25rem;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1;
	}

	.cover {
		width: 100%;
		aspect-ratio: 16 / 9;
		object-fit: cover;
	}

	.detail {
		padding: 20px;
	}

	.detail h3 {
		color: #111111;
		font-size: 1rem;
		margin: 0 0 4px 0;
		font-weight: 500;
	}

	.detail .author {
		color: #666666;
		font-size: 0.875rem;
		margin: 0 0 20px 0;
	}

	.stats {
		display: flex;
		flex-wrap: wrap;
		gap: 16px;
		margin-bottom: 20px;
	}

	.stat {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.stat .label {
		color: #999999;
		font-size: 0.75rem;
	}

	.stat .value {
		color: #111111;
		font-size: 0.875rem;
		font-weight: 500;
	}

	.rank-info {
		display: flex;
		gap: 24px;
		padding: 16px 0;
		margin-bottom: 16px;
		border-top: 1px solid #eeeeee;
		border-bottom: 1px solid #eeeeee;
	}

	.rank-item {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.rank-item .label {
		color: #999999;
		font-size: 0.75rem;
	}

	.rank-item .value {
		color: #111111;
		font-size: 0.875rem;
		font-weight: 500;
	}

	.final-score {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: 16px;
	}

	.final-score span:first-child {
		color: #666666;
		font-size: 0.875rem;
	}

	.score-value {
		color: #111111;
		font-size: 1.5rem;
		font-weight: 600;
	}
</style>
