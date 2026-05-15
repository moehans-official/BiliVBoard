<script>
  import { onMount } from 'svelte';

  let formulasOpen = $state([true, false, false]);
  let formulaEls = $state([]);

  function toggleFormula(index) {
    formulasOpen[index] = !formulasOpen[index];
    formulasOpen = [...formulasOpen];
    setTimeout(() => renderFormulas(), 0);
  }

  const algorithms = [
    {
      name: 'V3 Normal',
      subtitle: '普通版',
      desc: '综合考虑播放量、互动率和时间因素，适合日常排行参考',
      formula: '\\text{Score} = 10000 + \\ln(P+1) \\times (1 + 0.3 \\cdot \\ln(C+1)) \\times (1 + 1.5 \\cdot I_{\\text{rate}}) \\times e^{-T/30} \\times 800',
      vars: [
        { sym: 'P', desc: '播放量' },
        { sym: 'C', desc: '投币数' },
        { sym: 'I_{\\text{rate}}', desc: '综合互动率' },
        { sym: 'T', desc: '投稿天数' }
      ],
      halfLife: '约 20.79 天'
    },
    {
      name: 'V3 Radical',
      subtitle: '激进版',
      desc: '更强的时间衰减和互动权重，突出近期热门内容',
      formula: '\\text{Score} = 10000 + \\ln(P+1) \\times (1 + 3 \\cdot I_{\\text{rate}}) \\times e^{-T/10} \\times 500',
      vars: [
        { sym: 'P', desc: '播放量' },
        { sym: 'I_{\\text{rate}}', desc: '综合互动率' },
        { sym: 'T', desc: '投稿天数' }
      ],
      halfLife: '约 6.93 天'
    },
    {
      name: 'V3 E SP',
      subtitle: '无时间衰减',
      desc: '去掉时间因子，基于长期累计数据评估视频影响力',
      formula: '\\text{Score} = 10000 + \\ln(P+1) \\times (1 + 0.3 \\cdot \\ln(C+1)) \\times (1 + 1.5 \\cdot I_{\\text{rate}}) \\times 800',
      vars: [
        { sym: 'P', desc: '播放量' },
        { sym: 'C', desc: '投币数' },
        { sym: 'I_{\\text{rate}}', desc: '综合互动率' }
      ],
      halfLife: '无衰减'
    }
  ];

  function renderFormulas() {
    if (typeof katex === 'undefined') return;
    document.querySelectorAll('.katex-formula').forEach(el => {
      try {
        katex.render(el.dataset.formula, el, { displayMode: true, throwOnError: false });
      } catch {}
    });
    document.querySelectorAll('.katex-var').forEach(el => {
      try {
        katex.render(el.dataset.formula, el, { displayMode: false, throwOnError: false });
      } catch {}
    });
  }

  onMount(() => {
    const check = setInterval(() => {
      if (typeof katex !== 'undefined') {
        clearInterval(check);
        renderFormulas();
      }
    }, 100);
    return () => clearInterval(check);
  });
</script>

<section class="about">
  <div class="hero-card">
    <div class="hero-header">
      <div class="hero-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
      </div>
      <div class="hero-text">
        <h2>BiliVBoard</h2>
        <p class="desc">B站术力口视频数据采集与智能评分系统</p>
      </div>
    </div>
    <p class="intro">面向 B 站术力口（VOCALOID、UTAU、Synthesizer V 等音声合成引擎）领域的视频排行榜系统。通过自动化数据采集与多维度评分算法，为创作者和爱好者提供透明、客观的排名参考。</p>
    <div class="stats-row">
      <div class="stat-item">
        <span class="stat-num">10951</span>
        <span class="stat-label">收录视频</span>
      </div>
      <div class="stat-item">
        <span class="stat-num">3</span>
        <span class="stat-label">评分公式</span>
      </div>
      <div class="stat-item">
        <span class="stat-num">6</span>
        <span class="stat-label">互动指标</span>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="section-header">
      <h3>评分算法</h3>
      <span class="section-tag">3 种公式</span>
    </div>
    <div class="formulas">
      {#each algorithms as algo, i}
        <div class="algo-item" class:open={formulasOpen[i]}>
          <button class="algo-header" onclick={() => toggleFormula(i)}>
            <div class="algo-info">
              <div class="algo-badge">{algo.name}</div>
              <span class="algo-subtitle">{algo.subtitle}</span>
            </div>
            <span class="chevron" class:open={formulasOpen[i]}>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
            </span>
          </button>
          {#if formulasOpen[i]}
            <div class="algo-body">
              <p class="algo-desc">{algo.desc}</p>
              <div class="formula-box">
                <div class="katex-formula" data-formula={algo.formula}></div>
              </div>
              <div class="vars-grid">
                {#each algo.vars as v}
                  <div class="var-item">
                    <span class="katex-var" data-formula={v.sym}></span>
                    <span class="var-desc">{v.desc}</span>
                  </div>
                {/each}
              </div>
              <div class="algo-meta">
                <span class="half-life">
                  <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  半衰期 {algo.halfLife}
                </span>
              </div>
            </div>
          {/if}
        </div>
      {/each}
    </div>
  </div>

  <div class="links-row">
    <a href="https://github.com/moehans-official/BiliVBoard" target="_blank" rel="noopener" class="link-card">
      <div class="link-icon github">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65S8.93 17.38 9 18v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
      </div>
      <div class="link-text">
        <span class="link-title">GitHub</span>
        <span class="link-sub">moehans-official/BiliVBoard</span>
      </div>
      <svg class="link-arrow" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17l9.2-9.2M17 17V7H7"/></svg>
    </a>
    <a href="mailto:contact@moehans.com" class="link-card">
      <div class="link-icon email">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
      </div>
      <div class="link-text">
        <span class="link-title">Email</span>
        <span class="link-sub">contact@moehans.com</span>
      </div>
      <svg class="link-arrow" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17l9.2-9.2M17 17V7H7"/></svg>
    </a>
  </div>

  <div class="disclaimer-card">
    <div class="disclaimer-header">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <span>免责声明</span>
    </div>
    <p>本系统仅用于学习和研究目的。所有数据来自公开的 B 站 API，评分结果仅供参考。我们不对数据的准确性和完整性做任何保证，也不对因使用本系统产生的任何后果承担责任。</p>
  </div>
</section>

<style>
  .about {
    display: flex;
    flex-direction: column;
    gap: 20px;
    animation: fadeIn 0.4s ease-out;
  }

  .hero-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.04);
  }

  .hero-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
  }

  .hero-icon {
    width: 56px;
    height: 56px;
    background: #1a1a2e;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    flex-shrink: 0;
  }

  .hero-text { flex: 1; }

  h2 {
    color: #1a1a2e;
    font-size: 1.5rem;
    margin: 0 0 4px 0;
    font-weight: 800;
    letter-spacing: -0.03em;
  }

  .desc {
    color: #8e8ea0;
    font-size: 0.875rem;
    margin: 0;
    font-weight: 500;
  }

  .intro {
    color: #4a4a5a;
    font-size: 0.9375rem;
    line-height: 1.7;
    margin: 0 0 24px 0;
  }

  .stats-row {
    display: flex;
    gap: 4px;
    background: #f5f5f7;
    border-radius: 14px;
    padding: 4px;
  }

  .stat-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 14px 12px;
    border-radius: 12px;
  }

  .stat-num {
    color: #1a1a2e;
    font-size: 1.25rem;
    font-weight: 800;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.02em;
  }

  .stat-label {
    color: #8e8ea0;
    font-size: 0.75rem;
    font-weight: 500;
  }

  .card {
    background: #ffffff;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.04);
  }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }

  h3 {
    color: #1a1a2e;
    font-size: 1.125rem;
    margin: 0;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  .section-tag {
    color: #8e8ea0;
    font-size: 0.8125rem;
    font-weight: 500;
    background: #f0f0f5;
    padding: 4px 10px;
    border-radius: 8px;
  }

  .formulas {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .algo-item {
    border: 1.5px solid #f0f0f5;
    border-radius: 14px;
    overflow: hidden;
    transition: border-color 0.2s ease;
  }

  .algo-item.open {
    border-color: #e0e0ea;
  }

  .algo-header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    background: none;
    border: none;
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .algo-header:hover {
    background: #fafafa;
  }

  .algo-info {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .algo-badge {
    background: #1a1a2e;
    color: #ffffff;
    padding: 4px 12px;
    border-radius: 8px;
    font-size: 0.8125rem;
    font-weight: 700;
  }

  .algo-subtitle {
    color: #8e8ea0;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .chevron {
    color: #a0a0b0;
    transition: transform 0.2s ease;
    display: flex;
  }

  .chevron.open {
    transform: rotate(180deg);
  }

  .algo-body {
    padding: 0 20px 20px;
    animation: fadeIn 0.2s ease-out;
  }

  .algo-desc {
    color: #4a4a5a;
    font-size: 0.875rem;
    line-height: 1.6;
    margin: 0 0 16px 0;
  }

  .formula-box {
    background: #f5f5f7;
    padding: 16px 20px;
    border-radius: 10px;
    overflow-x: auto;
    margin: 0 0 16px 0;
    display: flex;
    justify-content: center;
  }

  .formula-box :global(.katex) {
    font-size: 1rem;
  }

  .vars-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
  }

  .var-item {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    background: #fafafa;
    border-radius: 8px;
    border: 1px solid #f0f0f5;
  }

  .var-item :global(.katex) {
    font-size: 0.875rem;
  }

  .var-desc {
    color: #6a6a7a;
    font-size: 0.75rem;
  }

  .algo-meta {
    display: flex;
    align-items: center;
  }

  .half-life {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #8e8ea0;
    font-size: 0.8125rem;
    font-weight: 500;
  }

  .links-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .link-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 20px;
    background: #ffffff;
    border-radius: 16px;
    text-decoration: none;
    transition: all 0.2s ease;
    border: 1px solid rgba(0, 0, 0, 0.04);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  }

  .link-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }

  .link-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .link-icon.github {
    background: #1a1a2e;
    color: #ffffff;
  }

  .link-icon.email {
    background: #f0f0f5;
    color: #1a1a2e;
  }

  .link-text {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .link-title {
    color: #1a1a2e;
    font-size: 0.9375rem;
    font-weight: 700;
  }

  .link-sub {
    color: #8e8ea0;
    font-size: 0.75rem;
  }

  .link-arrow {
    color: #a0a0b0;
    flex-shrink: 0;
  }

  .disclaimer-card {
    background: #fafafa;
    border-radius: 20px;
    padding: 24px;
    border: 1.5px solid #f0f0f5;
  }

  .disclaimer-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    color: #8e8ea0;
    font-size: 0.875rem;
    font-weight: 600;
  }

  .disclaimer-card p {
    color: #6a6a7a;
    font-size: 0.8125rem;
    line-height: 1.7;
    margin: 0;
  }

  @media (max-width: 640px) {
    .hero-card,
    .card,
    .disclaimer-card {
      padding: 20px;
      border-radius: 16px;
    }

    .hero-icon {
      width: 44px;
      height: 44px;
      border-radius: 12px;
    }

    .hero-icon svg {
      width: 24px;
      height: 24px;
    }

    h2 {
      font-size: 1.25rem;
    }

    .desc {
      font-size: 0.8125rem;
    }

    .intro {
      font-size: 0.875rem;
    }

    .stats-row {
      flex-direction: column;
    }

    .stat-item {
      padding: 10px;
    }

    .stat-num {
      font-size: 1.125rem;
    }

    h3 {
      font-size: 1rem;
    }

    .algo-header {
      padding: 12px 16px;
    }

    .algo-badge {
      font-size: 0.75rem;
      padding: 3px 10px;
    }

    .algo-subtitle {
      font-size: 0.8125rem;
    }

    .algo-body {
      padding: 0 16px 16px;
    }

    .formula-box {
      padding: 12px;
    }

    .formula-box :global(.katex) {
      font-size: 0.875rem;
    }

    .links-row {
      grid-template-columns: 1fr;
    }

    .link-card {
      padding: 16px;
    }

    .link-icon {
      width: 40px;
      height: 40px;
    }

    .link-title {
      font-size: 0.875rem;
    }
  }
</style>
