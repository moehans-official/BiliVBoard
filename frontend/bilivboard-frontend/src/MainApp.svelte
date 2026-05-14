<script>
	import Rankings from './Rankings.svelte';
	import Nominations from './Nominations.svelte';
	import About from './About.svelte';

	let activeTab = 'rankings';
	let prevTab = 'rankings';
	let contentKey = 0;

	function switchTab(tab) {
		if (tab === activeTab) return;
		prevTab = activeTab;
		activeTab = tab;
		contentKey++;
	}
</script>

<main>
	<header>
		<div class="logo-section">
			<div class="logo-wrapper">
				<img src="/logo.png" alt="BiliVBoard Logo" class="logo" />
			</div>
			<h1 class="brand">BiliVBoard</h1>
			<p class="tagline">B站术力口周榜</p>
		</div>
		<nav>
			<button 
				class:active={activeTab === 'rankings'} 
				on:click={() => switchTab('rankings')}
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
				排行榜
			</button>
			<button 
				class:active={activeTab === 'nominations'} 
				on:click={() => switchTab('nominations')}
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 8h.01"/><path d="M6 6h16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2Z"/><path d="M6 6V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2"/></svg>
				提名
			</button>
			<button 
				class:active={activeTab === 'about'} 
				on:click={() => switchTab('about')}
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
				关于
			</button>
		</nav>
	</header>

	<div class="content" key={contentKey}>
		{#if activeTab === 'rankings'}
			<Rankings />
		{:else if activeTab === 'nominations'}
			<Nominations />
		{:else if activeTab === 'about'}
			<About />
		{/if}
	</div>

	<footer>
		<div class="footer-content">
			<span class="copyright">© 2026 BiliVBoard</span>
			<span class="divider">·</span>
			<span class="credit">Powered by moehans</span>
		</div>
	</footer>
</main>

<style>
	main {
		min-height: 100vh;
		background: #fafafa;
		padding: 0 16px 32px;
	}

	header {
		text-align: center;
		padding: 56px 0 36px;
		animation: fadeIn 0.6s ease-out;
	}

	.logo-section {
		margin-bottom: 28px;
	}

	.logo-wrapper {
		display: inline-block;
		margin-bottom: 16px;
		position: relative;
	}

	.logo-wrapper::after {
		content: '';
		position: absolute;
		inset: -4px;
		border-radius: 20px;
		background: rgba(0, 0, 0, 0.04);
		transition: opacity 0.3s ease;
		opacity: 0;
	}

	.logo-wrapper:hover::after {
		opacity: 1;
	}

	.logo {
		width: 72px;
		height: 72px;
		object-fit: contain;
		border-radius: 16px;
		transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
		position: relative;
		z-index: 1;
	}

	.logo:hover {
		transform: scale(1.06) rotate(3deg);
	}

	.brand {
		font-size: 1.875rem;
		font-weight: 800;
		color: #1a1a2e;
		letter-spacing: -0.03em;
		margin: 0 0 4px;
	}

	.tagline {
		font-size: 0.875rem;
		color: #8e8ea0;
		font-weight: 500;
		letter-spacing: 1px;
	}

	nav {
		display: inline-flex;
		background: #ffffff;
		border-radius: 14px;
		padding: 4px;
		gap: 4px;
		box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06), 0 1px 3px rgba(0, 0, 0, 0.04);
		border: 1px solid rgba(0, 0, 0, 0.04);
	}

	nav button {
		padding: 10px 22px;
		background-color: transparent;
		color: #6b7280;
		border: none;
		border-radius: 10px;
		font-size: 0.875rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.25s ease;
		font-family: inherit;
		display: flex;
		align-items: center;
		gap: 6px;
	}

	nav button:hover {
		color: #374151;
		background-color: #f5f5f7;
	}

	nav button:active {
		transform: scale(0.97);
	}

	nav button svg {
		flex-shrink: 0;
	}

	nav button.active {
		background-color: #1a1a2e;
		color: #ffffff;
		box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
	}

	.content {
		max-width: 1080px;
		margin: 0 auto;
		animation: slideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1);
	}

	footer {
		text-align: center;
		padding: 56px 0 32px;
		animation: fadeIn 0.6s ease-out 0.3s backwards;
	}

	.footer-content {
		display: inline-flex;
		align-items: center;
		gap: 10px;
		color: #b0b0c0;
		font-size: 0.75rem;
	}

	.divider {
		opacity: 0.5;
	}

	@media (max-width: 640px) {
		main {
			padding: 0 12px 24px;
		}

		header {
			padding: 36px 0 24px;
		}

		.logo {
			width: 56px;
			height: 56px;
			border-radius: 14px;
		}

		.brand {
			font-size: 1.625rem;
		}

		.tagline {
			font-size: 0.8125rem;
			letter-spacing: 0.5px;
		}

		nav {
			width: 100%;
			max-width: 340px;
		}

		nav button {
			flex: 1;
			padding: 9px 10px;
			font-size: 0.8125rem;
			gap: 4px;
		}

		nav button svg {
			width: 14px;
			height: 14px;
		}

		.content {
			max-width: 100%;
		}
	}
</style>
