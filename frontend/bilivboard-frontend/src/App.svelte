<script>
	import LandingPage from './LandingPage.svelte';
	import MainApp from './MainApp.svelte';

	let isMaintenance = window.APP_CONFIG?.MAINTENANCE ?? true;
</script>

{#if isMaintenance}
	<LandingPage />
{:else}
	<MainApp />
{/if}
