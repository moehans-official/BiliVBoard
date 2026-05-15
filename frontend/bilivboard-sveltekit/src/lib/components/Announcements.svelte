<script>
  import { onMount } from 'svelte';

  let announcements = $state([]);
  let loading = $state(true);

  onMount(async () => {
    try {
      const res = await fetch('/api/announcements');
      if (res.ok) {
        announcements = await res.json();
      }
    } catch (e) {
    } finally {
      loading = false;
    }
  });
</script>

{#if !loading && announcements.length > 0}
  <div class="announcements">
    {#each announcements as ann}
      <div class="announcement">
        <div class="ann-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 11 18-5v12L3 13v-2z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/></svg>
        </div>
        <div class="ann-content">
          <span class="ann-title">{ann.title}</span>
          {#if ann.content}
            <span class="ann-body">{ann.content}</span>
          {/if}
        </div>
      </div>
    {/each}
  </div>
{/if}

<style>
  .announcements {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 24px;
  }

  .announcement {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 18px;
    background: #ffffff;
    border-radius: 14px;
    border: 1px solid rgba(0, 0, 0, 0.04);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    animation: fadeIn 0.3s ease-out;
  }

  .ann-icon {
    width: 32px;
    height: 32px;
    background: #f0f0f5;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #8e8ea0;
    flex-shrink: 0;
    margin-top: 1px;
  }

  .ann-content {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
  }

  .ann-title {
    color: #1a1a2e;
    font-size: 0.875rem;
    font-weight: 600;
    line-height: 1.4;
  }

  .ann-body {
    color: #6a6a7a;
    font-size: 0.8125rem;
    font-weight: 400;
    line-height: 1.5;
  }

  @media (max-width: 640px) {
    .announcement {
      padding: 12px 14px;
    }

    .ann-icon {
      width: 28px;
      height: 28px;
      border-radius: 7px;
    }

    .ann-title {
      font-size: 0.8125rem;
    }

    .ann-body {
      font-size: 0.75rem;
    }
  }
</style>
