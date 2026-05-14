<script>
  import '../app.css';
</script>

<div class="app">
  <header>
    <div class="header-content">
      <a href="/" class="logo">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
        <span>BiliVBoard</span>
      </a>
    </div>
  </header>

  <main>
    <slot />
  </main>

  <footer>
    <p>BiliVBoard - B站术力口视频数据采集与智能评分系统</p>
    <p class="contact">联系: contact@moehans.com</p>
  </footer>
</div>

<style>
  .app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: #f8f9fa;
  }

  header {
    background: #ffffff;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
    background: rgba(255, 255, 255, 0.95);
  }

  .header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: #1a1a2e;
    font-weight: 800;
    font-size: 1.125rem;
    letter-spacing: -0.02em;
  }

  .logo svg {
    color: #1a1a2e;
  }

  main {
    flex: 1;
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    padding: 32px 24px;
  }

  footer {
    background: #ffffff;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
    padding: 24px;
    text-align: center;
  }

  footer p {
    margin: 0;
    color: #8e8ea0;
    font-size: 0.8125rem;
    font-weight: 500;
    line-height: 1.6;
  }

  .contact {
    color: #b0b0c0 !important;
    font-size: 0.75rem !important;
  }

  @media (max-width: 640px) {
    .header-content {
      padding: 12px 16px;
    }

    .logo span {
      font-size: 1rem;
    }

    main {
      padding: 16px;
    }

    footer {
      padding: 16px;
    }
  }
</style>
