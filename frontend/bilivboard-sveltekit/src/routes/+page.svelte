<script>
  import Rankings from '$lib/components/Rankings.svelte';
  import Nominations from '$lib/components/Nominations.svelte';
  import About from '$lib/components/About.svelte';

  let activeTab = $state('rankings');

  const tabs = [
    { id: 'rankings', label: '排行榜', icon: 'chart' },
    { id: 'nominations', label: '提名', icon: 'edit' },
    { id: 'about', label: '关于', icon: 'info' }
  ];

  function switchTab(tab) {
    activeTab = tab;
  }
</script>

<svelte:head>
  <title>BiliVBoard - B站术力口排行榜</title>
  <meta name="description" content="B站术力口视频数据采集与智能评分系统" />
</svelte:head>

<div class="tabs">
  {#each tabs as tab}
    <button
      class="tab"
      class:active={activeTab === tab.id}
      onclick={() => switchTab(tab.id)}
    >
      {#if tab.icon === 'chart'}
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
      {:else if tab.icon === 'edit'}
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="m9 14 2 2 4-4"/></svg>
      {:else}
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>
      {/if}
      {tab.label}
    </button>
  {/each}
</div>

{#if activeTab === 'rankings'}
  <Rankings />
{:else if activeTab === 'nominations'}
  <Nominations />
{:else}
  <About />
{/if}

<style>
  .tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 24px;
    background: #ffffff;
    padding: 8px;
    border-radius: 16px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.04);
  }

  .tab {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 20px;
    font-size: 0.875rem;
    font-weight: 600;
    color: #8e8ea0;
    border-radius: 12px;
    transition: all 0.2s ease;
  }

  .tab:hover {
    color: #1a1a2e;
    background: #f5f5f7;
  }

  .tab.active {
    color: #1a1a2e;
    background: #f0f0f5;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  }

  .tab svg {
    flex-shrink: 0;
  }

  @media (max-width: 640px) {
    .tabs {
      padding: 6px;
      gap: 6px;
    }

    .tab {
      padding: 10px 16px;
      font-size: 0.8125rem;
    }
  }
</style>
