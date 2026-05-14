<script>
  import { onMount } from 'svelte';

  let rankings = $state([]);
  let total = $state(0);
  let period = $state(null);
  let loading = $state(true);
  let error = $state(null);
  let animatedScores = $state({});
  let selectedItem = $state(null);
  let selectedItemDetail = $state(null);

  onMount(async () => {
    try {
      const res = await fetch('/api/rankings?limit=20');
      if (!res.ok) throw new Error('加载失败');
      const data = await res.json();
      rankings = data.items;
      total = data.total;
      period = data.period;

      rankings.forEach((item, index) => {
        animatedScores[item.bvid] = 0;
        setTimeout(() => {
          animateScore(item.bvid, item.score);
        }, index * 80);
      });
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  });

  function animateScore(bvid, target) {
    const duration = 800;
    const steps = 24;
    const increment = target / steps;
    let current = 0;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current = Math.min(Math.round(increment * step), target);
      animatedScores[bvid] = current;
      animatedScores = { ...animatedScores };

      if (step >= steps) {
        clearInterval(timer);
        animatedScores[bvid] = target;
        animatedScores = { ...animatedScores };
      }
    }, duration / steps);
  }

  function formatNumber(num) {
    if (!num) return '0';
    if (num >= 10000) {
      return (num / 10000).toFixed(1) + '万';
    }
    return num.toLocaleString();
  }

  function getRankClass(rank) {
    if (rank === 1) return 'gold';
    if (rank === 2) return 'silver';
    if (rank === 3) return 'bronze';
    return '';
  }

  async function openDetail(item) {
    selectedItem = item;
    selectedItemDetail = null;
    try {
      const res = await fetch(`/api/rankings/${item.bvid}`);
      if (res.ok) {
        selectedItemDetail = await res.json();
      }
    } catch (e) {}
  }

  function openModal(e) {
    e.stopPropagation();
  }

  function closeDetail() {
    selectedItem = null;
    selectedItemDetail = null;
  }
</script>

<section class="ranking">
  <div class="section-header">
    <div class="header-left">
      <h2>TOP 20</h2>
      {#if period}
        <span class="period">共 {period.total_videos || total} 首 | {period.formula}</span>
      {/if}
    </div>
  </div>

  {#if loading}
    <div class="loading">
      <div class="spinner"></div>
      <span>加载中...</span>
    </div>
  {:else if error}
    <div class="error">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <span>{error}</span>
    </div>
  {:else}
    <div class="grid">
      {#each rankings as item}
        <div class="card" class:top3={item.rank <= 3} onclick={() => openDetail(item)}>
          <div class="cover-wrapper">
            {#if item.cover_path || item.cover_url}
              <img
                src={item.cover_path || item.cover_url}
                alt={item.title}
                class="cover"
                loading="lazy"
                onerror={(e) => e.target.style.display = 'none'}
              />
            {/if}
            <div class="cover-overlay"></div>
            <div class="rank-badge {getRankClass(item.rank)}">
              <span class="rank-num">#{item.rank}</span>
            </div>
            <div class="score-overlay">
              <span class="score">{animatedScores[item.bvid] ?? 0}</span>
            </div>
          </div>
          <div class="card-body">
            <div class="info">
              <span class="title">{item.title}</span>
              <span class="author">{item.name}</span>
            </div>
            <div class="stats-row">
              <span class="stat">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                {formatNumber(item.view)}
              </span>
              <span class="stat">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10h10"/><path d="M7 14h6"/><path d="M12 18H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6"/><path d="M22 18H12a2 2 0 0 0-2 2v0a2 2 0 0 0 2 2h10"/></svg>
                {formatNumber(item.like_count)}
              </span>
              <span class="stat">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M15 9.5a3 3 0 0 0-6 0"/></svg>
                {formatNumber(item.coin)}
              </span>
              <span class="stat">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                {formatNumber(item.favorite)}
              </span>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</section>

{#if selectedItem}
  <div class="overlay" onclick={closeDetail}>
    <div class="modal" onclick={openModal}>
      <button class="close" onclick={closeDetail}>
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
      </button>
      <div class="modal-cover-wrapper">
        <img
          src={selectedItem.cover_path || selectedItem.cover_url}
          alt={selectedItem.title}
          class="modal-cover"
          onerror={(e) => e.target.src = selectedItem.cover_url}
        />
        <div class="modal-score">
          <span class="score-label">评分</span>
          <span class="score-value-modal">{(selectedItemDetail?.score || selectedItem.score)?.toLocaleString()}</span>
        </div>
      </div>
      <div class="detail">
        <h3>{selectedItem.title}</h3>
        <p class="modal-author">UP主: {selectedItem.name}</p>
        <p class="modal-date">{selectedItemDetail?.pubdate || ''}</p>

        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            </div>
            <span class="stat-value">{formatNumber(selectedItem.view)}</span>
            <span class="stat-label">播放</span>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10h10"/><path d="M7 14h6"/><path d="M12 18H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6"/><path d="M22 18H12a2 2 0 0 0-2 2v0a2 2 0 0 0 2 2h10"/></svg>
            </div>
            <span class="stat-value">{formatNumber(selectedItem.like_count)}</span>
            <span class="stat-label">点赞</span>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M15 9.5a3 3 0 0 0-6 0"/></svg>
            </div>
            <span class="stat-value">{formatNumber(selectedItem.coin)}</span>
            <span class="stat-label">投币</span>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <span class="stat-value">{formatNumber(selectedItem.favorite)}</span>
            <span class="stat-label">收藏</span>
          </div>
          <div class="stat-item">
            <div class="stat-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 8h.01"/><path d="M6 6h16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2Z"/><path d="M6 6V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2"/></svg>
            </div>
            <span class="stat-value">{formatNumber(selectedItem.share)}</span>
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
            <span class="rank-value">#{selectedItem.rank}</span>
            <span class="rank-label">排名</span>
          </div>
          <div class="rank-item">
            <span class="rank-value">{formatNumber(selectedItem.reply)}</span>
            <span class="rank-label">评论</span>
          </div>
        </div>

        <a
          href={selectedItemDetail?.bilibili_url || selectedItem.bilibili_url}
          target="_blank"
          rel="noopener"
          class="bilibili-link"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
          在B站查看原视频
        </a>
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

  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 48px;
    color: #8e8ea0;
    font-size: 0.875rem;
  }

  .spinner {
    width: 24px;
    height: 24px;
    border: 3px solid #f0f0f5;
    border-top-color: #1a1a2e;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .error {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 48px;
    color: #c62828;
    font-size: 0.875rem;
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

  .cover-wrapper {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    background: #f0f0f5;
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
    padding-top: 10px;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
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
    margin: 0 0 2px 0;
  }

  .modal-date {
    color: #b0b0c0;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0 0 20px 0;
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
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 20px;
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

  .bilibili-link {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    padding: 14px 24px;
    background: #1a1a2e;
    color: #ffffff;
    border-radius: 12px;
    font-size: 0.9375rem;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s ease;
  }

  .bilibili-link:hover {
    background: #2a2a3e;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(26, 26, 46, 0.2);
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

    .card-body {
      padding: 14px;
    }

    .title {
      font-size: 0.875rem;
    }

    .author {
      font-size: 0.75rem;
    }

    .stats-row {
      gap: 10px;
    }

    .stat {
      font-size: 0.75rem;
    }

    .stat svg {
      width: 12px;
      height: 12px;
    }

    .score-overlay {
      font-size: 0.9375rem;
      padding: 4px 10px;
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

    .detail {
      padding: 16px;
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

    .bilibili-link {
      padding: 12px 20px;
      font-size: 0.875rem;
    }
  }
</style>
