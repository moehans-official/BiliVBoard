<script>
	import Rankings from './Rankings.svelte';
	import Nominations from './Nominations.svelte';
	import About from './About.svelte';

	let activeTab = 'rankings';
	let contentKey = 0;

	function switchTab(tab) {
		if (tab === activeTab) return;
		activeTab = tab;
		contentKey++;
	}
</script>

<main>
	<header>
		<div class="logo-section">
			<img src="/logo.png" alt="BiliVBoard Logo" class="logo" />
			<h1 class="brand">BiliVBoard</h1>
			<p class="tagline">B站术力口周榜</p>
		</div>
		<nav>
			<button 
				class:active={activeTab === 'rankings'} 
				on:click={() => switchTab('rankings')}
			>
				排行榜
			</button>
			<button 
				class:active={activeTab === 'nominations'} 
				on:click={() => switchTab('nominations')}
			>
				提名
			</button>
			<button 
				class:active={activeTab === 'about'} 
				on:click={() => switchTab('about')}
			>
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
		background: linear-gradient(180deg, #fafafa 0%, #f5f5f7 100%);
		padding: 0 16px 32px;
	}

	header {
		text-align: center;
		padding: 48px 0 40px;
		animation: fadeIn 0.6s ease-out;
	}

	.logo-section {
		margin-bottom: 32px;
	}

	.logo {
		width: 72px;
		height: 72px;
		object-fit: contain;
		margin-bottom: 16px;
		border-radius: 16px;
		transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.logo:hover {
		transform: scale(1.08) rotate(2deg);
	}

	.brand {
		font-size: 1.75rem;
		font-weight: 700;
		color: #1a1a2e;
		letter-spacing: -0.02em;
		margin: 0 0 4px;
	}

	.tagline {
		font-size: 0.8125rem;
		color: #8e8ea0;
		font-weight: 400;
		letter-spacing: 0.5px;
	}

	nav {
		display: inline-flex;
		background: #ffffff;
		border-radius: 12px;
		padding: 4px;
		gap: 4px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.06);
	}

	nav button {
		padding: 8px 20px;
		background-color: transparent;
		color: #6b7280;
		border: none;
		border-radius: 8px;
		font-size: 0.875rem;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s ease;
		font-family: inherit;
	}

	nav button:hover {
		color: #374151;
		background-color: #f9fafb;
	}

	nav button:active {
		transform: scale(0.98);
	}

	nav button.active {
		background-color: #1a1a2e;
		color: #ffffff;
		box-shadow: 0 2px 8px rgba(26, 26, 46, 0.24);
	}

	.content {
		max-width: 800px;
		margin: 0 auto;
		animation: slideUp 0.4s ease-out;
	}

	footer {
		text-align: center;
		padding: 48px 0 32px;
		animation: fadeIn 0.6s ease-out 0.3s backwards;
	}

	.footer-content {
		display: inline-flex;
		align-items: center;
		gap: 8px;
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
			padding: 32px 0 28px;
		}

		.logo {
			width: 56px;
			height: 56px;
			border-radius: 12px;
		}

		.brand {
			font-size: 1.5rem;
		}

		.tagline {
			font-size: 0.75rem;
		}

		nav {
			width: 100%;
			max-width: 320px;
		}

		nav button {
			flex: 1;
			padding: 8px 12px;
			font-size: 0.8125rem;
		}
	}
</style>
