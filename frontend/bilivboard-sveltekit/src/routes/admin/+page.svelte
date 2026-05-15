<script>
  import { onMount } from 'svelte';
  import AdminPanel from '$lib/components/AdminPanel.svelte';

  let password = $state('');
  let authenticated = $state(false);
  let error = $state('');

  const ADMIN_PASSWORD = 'bilivboard2024';

  onMount(() => {
    if (sessionStorage.getItem('admin_auth') === '1') {
      authenticated = true;
    }
  });

  function login() {
    if (password === ADMIN_PASSWORD) {
      authenticated = true;
      sessionStorage.setItem('admin_auth', '1');
      error = '';
    } else {
      error = '密码错误';
      password = '';
    }
  }
</script>

<svelte:head>
  <title>管理后台 - BiliVBoard</title>
</svelte:head>

{#if !authenticated}
  <div class="login-wrapper">
    <div class="login-card">
      <div class="login-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      </div>
      <h2>管理后台</h2>
      <p class="login-desc">请输入管理员密码</p>
      <form onsubmit={(e) => { e.preventDefault(); login(); }}>
        <input
          type="password"
          placeholder="密码"
          bind:value={password}
          class="login-input"
        />
        {#if error}
          <p class="login-error">{error}</p>
        {/if}
        <button type="submit" class="login-btn">进入</button>
      </form>
    </div>
  </div>
{:else}
  <AdminPanel />
{/if}

<style>
  .login-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 60vh;
  }

  .login-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 40px;
    width: 100%;
    max-width: 380px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.04);
    text-align: center;
  }

  .login-icon {
    width: 56px;
    height: 56px;
    background: #1a1a2e;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    margin: 0 auto 20px;
  }

  h2 {
    color: #1a1a2e;
    font-size: 1.25rem;
    margin: 0 0 8px 0;
    font-weight: 700;
  }

  .login-desc {
    color: #8e8ea0;
    font-size: 0.875rem;
    margin: 0 0 24px 0;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .login-input {
    width: 100%;
    padding: 14px 16px;
    border: 1.5px solid #e5e5ea;
    border-radius: 12px;
    font-size: 0.9375rem;
    font-family: inherit;
    color: #1a1a2e;
    background: #fafafa;
    transition: all 0.2s ease;
    box-sizing: border-box;
    text-align: center;
    letter-spacing: 4px;
  }

  .login-input:focus {
    outline: none;
    border-color: #1a1a2e;
    background: #ffffff;
    box-shadow: 0 0 0 3px rgba(26, 26, 46, 0.08);
  }

  .login-input::placeholder {
    letter-spacing: normal;
    color: #b0b0c0;
  }

  .login-error {
    color: #c62828;
    font-size: 0.8125rem;
    margin: 0;
    background: #ffebee;
    padding: 8px 12px;
    border-radius: 8px;
  }

  .login-btn {
    padding: 14px 24px;
    background: #1a1a2e;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    font-size: 0.9375rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .login-btn:hover {
    background: #2a2a3e;
  }
</style>
