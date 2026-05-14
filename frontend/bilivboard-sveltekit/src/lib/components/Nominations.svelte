<script>
  let bvid = $state('');
  let captchaInput = $state('');
  let submitted = $state(false);
  let submitting = $state(false);
  let errorMessage = $state('');
  let captchaCode = $state('');

  function generateCaptcha() {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789';
    let result = '';
    for (let i = 0; i < 4; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    captchaCode = result;
    drawCaptcha();
  }

  function drawCaptcha() {
    const canvas = document.getElementById('captcha-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#f0f0f5';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < 50; i++) {
      ctx.fillStyle = `rgba(${Math.random() * 200}, ${Math.random() * 200}, ${Math.random() * 200}, 0.3)`;
      ctx.beginPath();
      ctx.arc(Math.random() * canvas.width, Math.random() * canvas.height, 1, 0, 2 * Math.PI);
      ctx.fill();
    }

    for (let i = 0; i < 4; i++) {
      ctx.save();
      ctx.translate(25 + i * 25, 28);
      ctx.rotate((Math.random() - 0.5) * 0.4);
      ctx.font = `bold ${20 + Math.random() * 8}px Inter, sans-serif`;
      ctx.fillStyle = '#1a1a2e';
      ctx.fillText(captchaCode[i], 0, 0);
      ctx.restore();
    }

    for (let i = 0; i < 3; i++) {
      ctx.strokeStyle = `rgba(${Math.random() * 150}, ${Math.random() * 150}, ${Math.random() * 150}, 0.2)`;
      ctx.beginPath();
      ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height);
      ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height);
      ctx.stroke();
    }
  }

  function refreshCaptcha() {
    generateCaptcha();
    captchaInput = '';
  }

  import { onMount } from 'svelte';
  onMount(() => {
    generateCaptcha();
  });

  async function submit() {
    errorMessage = '';

    if (!bvid.trim()) {
      errorMessage = '请输入BV号';
      return;
    }
    if (!bvid.startsWith('BV') || bvid.length < 10) {
      errorMessage = '请输入有效的BV号';
      return;
    }
    if (captchaInput.toLowerCase() !== captchaCode.toLowerCase()) {
      errorMessage = '验证码错误';
      refreshCaptcha();
      return;
    }

    submitting = true;
    try {
      const res = await fetch('/api/nominations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bvid: bvid.trim() })
      });
      const data = await res.json();
      if (data.success) {
        submitted = true;
      } else {
        errorMessage = data.message || '提交失败';
      }
    } catch (e) {
      errorMessage = '网络错误，请重试';
    } finally {
      submitting = false;
    }
  }
</script>

<section class="nominations">
  <div class="card">
    <div class="header">
      <div class="header-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="m9 14 2 2 4-4"/></svg>
      </div>
      <div class="header-text">
        <h2>提名</h2>
        <p class="desc">提交B站视频BV号进行提名</p>
      </div>
    </div>

    {#if submitted}
      <div class="success">
        <div class="success-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 12 2 2 4-4"/></svg>
        </div>
        <span>提交成功</span>
      </div>
    {:else}
      <div class="form">
        <div class="form-group">
          <label class="form-label">视频BV号</label>
          <div class="input-wrapper">
            <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/></svg>
            <input
              type="text"
              class="bvid-input"
              placeholder="BV1xx411c7mD"
              bind:value={bvid}
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">验证码</label>
          <div class="captcha-row">
            <div class="input-wrapper captcha-input-wrapper">
              <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><circle cx="12" cy="16" r="1"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <input
                type="text"
                class="captcha-input"
                placeholder="输入验证码"
                bind:value={captchaInput}
              />
            </div>
            <canvas id="captcha-canvas" width="120" height="44" onclick={refreshCaptcha}></canvas>
            <button class="refresh-btn" onclick={refreshCaptcha}>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>
            </button>
          </div>
        </div>

        {#if errorMessage}
          <div class="error-message">{errorMessage}</div>
        {/if}

        <button class="submit-btn" onclick={submit} disabled={submitting}>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 8h.01"/><path d="M6 6h16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2Z"/><path d="M6 6V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2"/></svg>
          {submitting ? '提交中...' : '提交提名'}
        </button>
      </div>
    {/if}
  </div>
</section>

<style>
  .nominations {
    max-width: 520px;
    margin: 0 auto;
  }

  .card {
    background: #ffffff;
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
    animation: fadeIn 0.4s ease-out;
    border: 1px solid rgba(0, 0, 0, 0.04);
  }

  .header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 28px;
  }

  .header-icon {
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

  .header-text {
    flex: 1;
  }

  h2 {
    color: #1a1a2e;
    font-size: 1.25rem;
    margin: 0 0 4px 0;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  .desc {
    color: #8e8ea0;
    font-size: 0.875rem;
    margin: 0;
    font-weight: 500;
  }

  .success {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    padding: 48px 0;
    animation: fadeIn 0.3s ease-out;
  }

  .success-icon {
    width: 64px;
    height: 64px;
    background: #e8f5e9;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #2e7d32;
  }

  .success span {
    color: #1a1a2e;
    font-size: 1.125rem;
    font-weight: 600;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .form-label {
    color: #1a1a2e;
    font-size: 0.875rem;
    font-weight: 600;
  }

  .input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }

  .input-icon {
    position: absolute;
    left: 14px;
    color: #a0a0b0;
    pointer-events: none;
  }

  .bvid-input,
  .captcha-input {
    width: 100%;
    padding: 14px 14px 14px 44px;
    border: 1.5px solid #e5e5ea;
    border-radius: 12px;
    font-size: 0.9375rem;
    font-family: inherit;
    color: #1a1a2e;
    background: #fafafa;
    transition: all 0.2s ease;
  }

  .bvid-input:focus,
  .captcha-input:focus {
    outline: none;
    border-color: #1a1a2e;
    background: #ffffff;
    box-shadow: 0 0 0 3px rgba(26, 26, 46, 0.08);
  }

  .bvid-input::placeholder,
  .captcha-input::placeholder {
    color: #b0b0c0;
  }

  .captcha-row {
    display: flex;
    gap: 12px;
    align-items: center;
  }

  .captcha-input-wrapper {
    flex: 1;
  }

  #captcha-canvas {
    border-radius: 12px;
    cursor: pointer;
    flex-shrink: 0;
    border: 1.5px solid #e5e5ea;
  }

  .refresh-btn {
    width: 44px;
    height: 44px;
    border: 1.5px solid #e5e5ea;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #8e8ea0;
    background: #fafafa;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .refresh-btn:hover {
    border-color: #1a1a2e;
    color: #1a1a2e;
    background: #ffffff;
  }

  .error-message {
    color: #c62828;
    font-size: 0.8125rem;
    font-weight: 500;
    padding: 8px 12px;
    background: #ffebee;
    border-radius: 8px;
  }

  .submit-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 14px 24px;
    background: #1a1a2e;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    font-size: 0.9375rem;
    font-weight: 600;
    font-family: inherit;
    transition: all 0.2s ease;
    margin-top: 4px;
  }

  .submit-btn:hover:not(:disabled) {
    background: #2a2a3e;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(26, 26, 46, 0.2);
  }

  .submit-btn:active:not(:disabled) {
    transform: translateY(0);
  }

  .submit-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  @media (max-width: 640px) {
    .card {
      padding: 24px;
      border-radius: 16px;
    }

    .header-icon {
      width: 40px;
      height: 40px;
      border-radius: 12px;
    }

    .header-icon svg {
      width: 20px;
      height: 20px;
    }

    h2 {
      font-size: 1.125rem;
    }

    .desc {
      font-size: 0.8125rem;
    }

    .bvid-input,
    .captcha-input {
      padding: 12px 12px 12px 40px;
      font-size: 0.875rem;
    }

    .input-icon {
      left: 12px;
      width: 16px;
      height: 16px;
    }

    .captcha-row {
      gap: 8px;
    }

    #captcha-canvas {
      width: 100px;
      height: 38px;
    }

    .refresh-btn {
      width: 38px;
      height: 38px;
    }

    .submit-btn {
      padding: 12px 20px;
      font-size: 0.875rem;
    }
  }
</style>
