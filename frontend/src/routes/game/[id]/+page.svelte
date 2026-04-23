<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { getSession } from '$lib/api';
    import type { Session } from '$lib/types'; // Import the type
    import Matchup from "$lib/components/Matchup.svelte";
    import SongRanking from "$lib/components/SongRanking.svelte";

    // Initialize as the Session type or null
    let session: Session | null = null; 
    let loading = true;

    $: sessionId = $page.params.id;

    onMount(async () => {
        if (sessionId) {
            try {
                // Cast the response to our Session type
                session = await getSession(sessionId) as Session;
            } catch (err) {
                console.error(err);
            } finally {
                loading = false;
            }
        }
    });
</script>

<main class="py-10 px-6">
    {#if loading}
        <div class="text-center font-black italic uppercase">Loading...</div>
    {:else if session} 
        {#if session.is_active}
            <Matchup bind:session={session} />
        {:else}
            <SongRanking {session} />
        {/if}
    {:else}
        <div class="text-center font-black text-red-500 uppercase">Session Not Found</div>
    {/if}
</main>