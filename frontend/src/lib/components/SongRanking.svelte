<script lang="ts">
    import type { Session, Song } from '$lib/types';

    // FIX 1: Open the door for the 'session' prop
    export let session: Session;

    // FIX 2: Instead of a hardcoded ID, use the ID from the prop
    // Or better yet, use the songs already inside the session object!
    let sortedSongs: Song[] = [];

    // Reactive statement: Sort songs by rating whenever the session updates
    $: if (session && session.songs) {
        sortedSongs = [...session.songs].sort((a, b) => b.rating - a.rating);
    }
</script>

<div class="max-w-2xl mx-auto mt-8">
    <h2 class="text-4xl font-black uppercase italic mb-8 tracking-tighter">
        Final Standings
    </h2>

    <div class="border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] bg-white overflow-hidden">
        <table class="w-full text-left border-collapse">
            <thead class="bg-black text-white uppercase text-sm">
                <tr>
                    <th class="p-4 border-b-4 border-black">Rank</th>
                    <th class="p-4 border-b-4 border-black">Song</th>
                    <th class="p-4 border-b-4 border-black text-right">ELO</th>
                </tr>
            </thead>
            <tbody>
                {#each sortedSongs as song, i}
                    <tr class="group hover:bg-[#bef264] transition-colors border-b-2 border-black last:border-0">
                        <td class="p-4 font-black italic text-2xl">#{i + 1}</td>
                        <td class="p-4">
                            <div class="font-black uppercase text-lg">{song.title}</div>
                            <div class="text-xs font-bold text-gray-500 uppercase">{song.artist}</div>
                        </td>
                        <td class="p-4 text-right">
                            <span class="bg-black text-[#bef264] px-3 py-1 font-black rounded-full text-sm">
                                {song.rating}
                            </span>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>

    <button 
        on:click={() => window.location.href = '/'}
        class="mt-12 w-full py-4 bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] 
               hover:bg-yellow-400 font-black uppercase transition-all active:shadow-none active:translate-x-[4px]">
        Start New Session
    </button>
</div>