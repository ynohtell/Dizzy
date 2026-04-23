<script lang="ts">
    import { submitChoice } from '$lib/api';
	import type { Session } from '$lib/types';
    import { fade, fly } from 'svelte/transition';

    // We accept the session object from the parent (+page.svelte)
    // We use "any" here to keep TypeScript happy with your dynamic backend data
    export let session: Session;

    let loading = false;

    // Reactive declaration: This automatically updates whenever session.current_matchup_index changes
    $: currentMatch = session.matchups[session.current_matchup_index];

    async function handleVote(winnerId: string) {
        if (loading || !session.is_active) return;
        
        loading = true;
        try {
            // We call the API and overwrite the session with the updated data from Python
            const updatedSession = await submitChoice(session.id, winnerId);
            session = updatedSession;
        } catch (error) {
            console.error("Voting error:", error);
            alert("Connection lost! Could not save your vote.");
        } finally {
            loading = false;
        }
    }

    // Keyboard support: Press '1' for Left, '2' for Right
    function handleKeyDown(event: KeyboardEvent) {
        if (loading) return;
        if (event.key === '1') handleVote(currentMatch.song_a.id);
        if (event.key === '2') handleVote(currentMatch.song_b.id);
    }
</script>

<svelte:window on:keydown={handleKeyDown} />

<div class="max-w-5xl mx-auto">
    <div class="flex justify-between items-center mb-8">
        <h2 class="text-2xl font-black uppercase italic">Round {session.current_round}</h2>
        <div class="text-sm font-bold bg-black text-white px-3 py-1 uppercase">
            Match {session.current_matchup_index + 1} of {session.matchups.length}
        </div>
    </div>

    {#key session.current_matchup_index}
        <div 
            in:fly={{ y: 20, duration: 300, delay: 100 }} 
            out:fade={{ duration: 100 }}
            class="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-12 items-center relative"
        >
            <button 
                on:click={() => handleVote(currentMatch.song_a.id)}
                disabled={loading}
                class="group relative p-10 bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] 
                       hover:bg-[#bef264] hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] 
                       active:translate-x-[4px] active:translate-y-[4px] active:shadow-none
                       transition-all duration-150 text-center min-h-[250px] flex flex-col justify-center items-center
                       disabled:opacity-50 disabled:cursor-wait"
            >
                <span class="absolute top-4 left-4 text-xs font-black text-gray-400 uppercase">Option 1</span>
                <h3 class="text-3xl md:text-5xl font-black uppercase tracking-tighter leading-none">
                    {currentMatch.song_a.title}
                </h3>
            </button>

            <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 
                        bg-black text-white text-2xl font-black italic px-6 py-2 rounded-full 
                        border-4 border-[#bef264] z-10 hidden md:block">
                VS
            </div>

            <button 
                on:click={() => handleVote(currentMatch.song_b.id)}
                disabled={loading}
                class="group relative p-10 bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] 
                       hover:bg-[#22d3ee] hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] 
                       active:translate-x-[4px] active:translate-y-[4px] active:shadow-none
                       transition-all duration-150 text-center min-h-[250px] flex flex-col justify-center items-center
                       disabled:opacity-50 disabled:cursor-wait"
            >
                <span class="absolute top-4 left-4 text-xs font-black text-gray-400 uppercase">Option 2</span>
                <h3 class="text-3xl md:text-5xl font-black uppercase tracking-tighter leading-none">
                    {currentMatch.song_b.title}
                </h3>
            </button>
        </div>
    {/key}

    <div class="mt-16 relative">
        <div class="w-full bg-white border-4 border-black h-8 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <div 
                class="bg-[#bef264] h-full transition-all duration-500 border-r-4 border-black" 
                style="width: {(session.current_matchup_index / session.matchups.length) * 100}%"
            ></div>
        </div>
        <p class="text-right mt-2 font-black uppercase text-sm italic">
            Energy Levels: {Math.round((session.current_matchup_index / session.matchups.length) * 100)}%
        </p>
    </div>
</div>