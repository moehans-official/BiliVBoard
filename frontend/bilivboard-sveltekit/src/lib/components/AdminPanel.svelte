<script>
  import { onMount } from 'svelte';

  let activeSection = $state('announcements');
  let announcements = $state([]);
  let nominations = $state([]);
  let charts = $state([]);
  let loading = $state(false);
  let message = $state('');

  // Announcement form
  let annTitle = $state('');
  let annContent = $state('');

  onMount(() => {
    loadAnnouncements();
    loadNominations();
    loadCharts();
  });

  async function loadAnnouncements() {
    const res = await fetch('/api/admin/announcements');
    if (res.ok) announcements = await res.json();
  }

  async function loadNominations() {
    const res = await fetch('/api/admin/nominations');
    if (res.ok) nominations = await res.json();
  }

  async function loadCharts() {
    const res = await fetch('/api/admin/charts');
    if (res.ok) charts = await res.json();
  }

  async function createAnnouncement() {
    if (!annTitle.trim()) return;
    const res = await fetch('/api/admin/announcements', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: annTitle, content: annContent })
    });
    if (res.ok) {
      annTitle = '';
      annContent = '';
      message = '公告已发布';
      setTimeout(() => message = '', 2000);
      await loadAnnouncements();
    }
  }

  async function toggleAnnouncement(id, currentActive) {
    await fetch(`/api/admin/announcements/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_active: currentActive ? 0 : 1 })
    });
    await loadAnnouncements();
  }

  async function deleteAnnouncement(id) {
    if (!confirm('确定删除这条公告？')) return;
    await fetch(`/api/admin/announcements/${id}`, { method: 'DELETE' });
    await loadAnnouncements();
  }

  async function parseNomination(id) {
    loading = true;
    const res = await fetch(`/api/admin/nominations/${id}/parse`, { method: 'POST' });
    if (res.ok) {
      message = '解析完成';
      setTimeout(() => message = '', 2000);
      await loadNominations();
    }
    loading = false;
  }

  async function reviewNomination(id, status) {
    const reason = status === 'rejected' ? prompt('拒绝原因：') : '';
    await fetch(`/api/admin/nominations/${id}/review`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, reason: reason || '' })
    });
    message = status === 'approved' ? '已批准' : '已拒绝';
    setTimeout(() => message = '', 2000);
    await loadNominations();
  }

  async function deleteNomination(id) {
    if (!confirm('确定删除这条提名？')) return;
    await fetch(`/api/admin/nominations/${id}`, { method: 'DELETE' });
    await loadNominations();
  }

  function formatNumber(num) {
    if (!num) return '-';
    if (num >= 10000) return (num / 10000).toFixed(1) + '万';
    return num.toLocaleString();
  }

  function statusLabel(s) {
    if (s === 'pending') return '待审核';
    if (s === 'approved') return '已批准';
    if (s === 'rejected') return '已拒绝';
    return s;
  }
</script>

<section class="admin">
  <div class="admin-header">
    <div class="admin-icon">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
    </div>
    <div>
      <h2>管理后台</h2>
      <p class="admin-desc">公告、提名、榜单管理</p>
    </div>
  </div>

  {#if message}
    <div class="toast">{message}</div>
  {/if}

  <div class="section-tabs">
    <button class="section-tab" class:active={activeSection === 'announcements'} onclick={() => activeSection = 'announcements'}>
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 11 18-5v12L3 13v-2z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/></svg>
      公告管理
    </button>
    <button class="section-tab" class:active={activeSection === 'nominations'} onclick={() => activeSection = 'nominations'}>
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="m9 14 2 2 4-4"/></svg>
      提名审核
    </button>
    <button class="section-tab" class:active={activeSection === 'charts'} onclick={() => activeSection = 'charts'}>
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
      榜单列表
    </button>
  </div>

  {#if activeSection === 'announcements'}
    <div class="card">
      <h3>发布公告</h3>
      <div class="form-row">
        <input type="text" placeholder="公告标题" bind:value={annTitle} class="input" />
      </div>
      <div class="form-row">
        <textarea placeholder="公告内容（可选）" bind:value={annContent} class="input textarea"></textarea>
      </div>
      <button class="btn" onclick={createAnnouncement} disabled={!annTitle.trim()}>发布</button>
    </div>

    <div class="card">
      <h3>已有公告</h3>
      {#if announcements.length === 0}
        <p class="empty">暂无公告</p>
      {:else}
        <div class="list">
          {#each announcements as ann}
            <div class="list-item">
              <div class="item-info">
                <span class="item-title">{ann.title}</span>
                {#if ann.content}
                  <span class="item-sub">{ann.content}</span>
                {/if}
                <span class="item-meta">{ann.created_at}</span>
              </div>
              <div class="item-actions">
                <button class="btn-sm" class:active={ann.is_active} onclick={() => toggleAnnouncement(ann.id, ann.is_active)}>
                  {ann.is_active ? '已发布' : '已隐藏'}
                </button>
                <button class="btn-sm danger" onclick={() => deleteAnnouncement(ann.id)}>删除</button>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}

  {#if activeSection === 'nominations'}
    <div class="card">
      <h3>提名列表</h3>
      {#if nominations.length === 0}
        <p class="empty">暂无提名</p>
      {:else}
        <div class="list">
          {#each nominations as nom}
            <div class="list-item">
              <div class="item-cover">
                {#if nom.cover_url && nom.cover_url !== 'https://i0.hdslb.com/bfs/archive/transparent.png'}
                  <img src={nom.cover_url} alt={nom.title || nom.bvid} />
                {:else}
                  <div class="cover-placeholder">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  </div>
                {/if}
              </div>
              <div class="item-info">
                <span class="item-title">{nom.title || nom.bvid}</span>
                {#if nom.name}
                  <span class="item-sub">{nom.name}</span>
                {/if}
                <span class="item-meta">
                  {nom.bvid}
                  {#if nom.view} | {formatNumber(nom.view)} 播放{/if}
                  {#if nom.like_count} | {formatNumber(nom.like_count)} 点赞{/if}
                </span>
              </div>
              <div class="item-actions">
                <span class="status-tag {nom.status}">{statusLabel(nom.status)}</span>
                {#if nom.status === 'pending'}
                  {#if !nom.title}
                    <button class="btn-sm" onclick={() => parseNomination(nom.id)} disabled={loading}>解析</button>
                  {/if}
                  <button class="btn-sm success" onclick={() => reviewNomination(nom.id, 'approved')}>批准</button>
                  <button class="btn-sm danger" onclick={() => reviewNomination(nom.id, 'rejected')}>拒绝</button>
                {/if}
                <button class="btn-sm danger" onclick={() => deleteNomination(nom.id)}>删除</button>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}

  {#if activeSection === 'charts'}
    <div class="card">
      <h3>榜单列表</h3>
      {#if charts.length === 0}
        <p class="empty">暂无榜单。运行 <code>python3 start_make.py</code> 创建榜单。</p>
      {:else}
        <div class="list">
          {#each charts as chart}
            <div class="list-item">
              <div class="item-info">
                <span class="item-title">#{String(chart.id).padStart(3, '0')}</span>
                <span class="item-sub">{chart.formula} | {chart.video_count} 首</span>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</section>

<style>
  .admin {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .admin-header {
    display: flex;
    align-items: center;
    gap: 16px;
    background: #ffffff;
    padding: 24px 28px;
    border-radius: 20px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.04);
  }

  .admin-icon {
    width: 48px;
    height: 48px;
    background: #1a1a2e;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    flex-shrink: 0;
  }

  h2 {
    color: #1a1a2e;
    font-size: 1.25rem;
    margin: 0 0 4px 0;
    font-weight: 700;
  }

  .admin-desc {
    color: #8e8ea0;
    font-size: 0.875rem;
    margin: 0;
  }

  .toast {
    background: #2e7d32;
    color: #fff;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 0.875rem;
    font-weight: 600;
    text-align: center;
    animation: fadeIn 0.2s ease-out;
  }

  .section-tabs {
    display: flex;
    gap: 8px;
    background: #ffffff;
    padding: 8px;
    border-radius: 16px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.04);
  }

  .section-tab {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 16px;
    font-size: 0.8125rem;
    font-weight: 600;
    color: #8e8ea0;
    border-radius: 12px;
    transition: all 0.2s ease;
  }

  .section-tab:hover {
    color: #1a1a2e;
    background: #f5f5f7;
  }

  .section-tab.active {
    color: #1a1a2e;
    background: #f0f0f5;
  }

  .card {
    background: #ffffff;
    border-radius: 20px;
    padding: 24px 28px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.04);
  }

  h3 {
    color: #1a1a2e;
    font-size: 1rem;
    margin: 0 0 16px 0;
    font-weight: 700;
  }

  .form-row {
    margin-bottom: 12px;
  }

  .input {
    width: 100%;
    padding: 12px 16px;
    border: 1.5px solid #e5e5ea;
    border-radius: 12px;
    font-size: 0.875rem;
    font-family: inherit;
    color: #1a1a2e;
    background: #fafafa;
    transition: all 0.2s ease;
    box-sizing: border-box;
  }

  .input:focus {
    outline: none;
    border-color: #1a1a2e;
    background: #ffffff;
    box-shadow: 0 0 0 3px rgba(26, 26, 46, 0.08);
  }

  .textarea {
    min-height: 80px;
    resize: vertical;
  }

  .btn {
    padding: 10px 24px;
    background: #1a1a2e;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    font-size: 0.875rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn:hover:not(:disabled) {
    background: #2a2a3e;
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .empty {
    color: #8e8ea0;
    font-size: 0.875rem;
    text-align: center;
    padding: 24px;
  }

  .empty code {
    background: #f0f0f5;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.8125rem;
  }

  .list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .list-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    background: #fafafa;
    border-radius: 14px;
    transition: background 0.2s ease;
  }

  .list-item:hover {
    background: #f5f5f7;
  }

  .item-cover {
    width: 48px;
    height: 36px;
    border-radius: 8px;
    overflow: hidden;
    flex-shrink: 0;
    background: #e5e5ea;
  }

  .item-cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .cover-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #a0a0b0;
  }

  .item-info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .item-title {
    color: #1a1a2e;
    font-size: 0.875rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .item-sub {
    color: #8e8ea0;
    font-size: 0.75rem;
  }

  .item-meta {
    color: #a0a0b0;
    font-size: 0.6875rem;
  }

  .item-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }

  .btn-sm {
    padding: 6px 12px;
    border: 1.5px solid #e5e5ea;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s ease;
    background: #ffffff;
    color: #1a1a2e;
  }

  .btn-sm:hover {
    border-color: #1a1a2e;
  }

  .btn-sm.active {
    background: #2e7d32;
    color: #fff;
    border-color: #2e7d32;
  }

  .btn-sm.success {
    background: #2e7d32;
    color: #fff;
    border-color: #2e7d32;
  }

  .btn-sm.success:hover {
    background: #1b5e20;
  }

  .btn-sm.danger {
    color: #c62828;
    border-color: #ffcdd2;
  }

  .btn-sm.danger:hover {
    background: #ffebee;
    border-color: #c62828;
  }

  .status-tag {
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.6875rem;
    font-weight: 600;
  }

  .status-tag.pending {
    background: #fff3e0;
    color: #e65100;
  }

  .status-tag.approved {
    background: #e8f5e9;
    color: #2e7d32;
  }

  .status-tag.rejected {
    background: #ffebee;
    color: #c62828;
  }

  @media (max-width: 640px) {
    .admin-header {
      padding: 20px;
    }

    .card {
      padding: 20px;
      border-radius: 16px;
    }

    .section-tab {
      padding: 10px 12px;
      font-size: 0.75rem;
    }

    .section-tab svg {
      width: 14px;
      height: 14px;
    }

    .list-item {
      flex-wrap: wrap;
    }

    .item-actions {
      width: 100%;
      justify-content: flex-end;
      margin-top: 8px;
    }
  }
</style>
