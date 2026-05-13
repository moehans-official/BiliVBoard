<script>
	import Rankings from './Rankings.svelte';
	import Nominations from './Nominations.svelte';
	import About from './About.svelte';

	let activeTab = 'rankings';

	function switchTab(tab) {
		activeTab = tab;
	}
</script>

<main>
	<header>
		<img src="/logo.png" alt="BiliVBoard Logo" class="logo" />
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

	{#if activeTab === 'rankings'}
		<Rankings />
	{:else if activeTab === 'nominations'}
		<Nominations />
	{:else if activeTab === 'about'}
		<About />
	{/if}

	<footer>
		<span>© 2026 BiliVBoard. All rights reserved.</span>
	</footer>
</main>

<style>
	main {
		min-height: 100vh;
		background-color: #ffffff;
		padding: 48px 16px;
	}

	header {
		text-align: center;
		margin-bottom: 48px;
	}

	.logo {
		width: 120px;
		height: 120px;
		object-fit: contain;
		margin-bottom: 24px;
	}

	nav {
		display: flex;
		justify-content: center;
		gap: 8px;
	}

	nav button {
		padding: 8px 24px;
		background-color: transparent;
		color: #666666;
		border: 1px solid #eeeeee;
		border-radius: 20px;
		font-size: 0.875rem;
		cursor: pointer;
		transition: all 0.2s;
	}

	nav button:hover {
		background-color: #f8f8f8;
	}

	nav button.active {
		background-color: #111111;
		color: #ffffff;
		border-color: #111111;
	}

	footer {
		text-align: center;
		padding: 48px 16px 32px;
		color: #999999;
		font-size: 0.75rem;
	}

	footer .dot {
		margin: 0 8px;
	}
</style>
