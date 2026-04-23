<script lang="ts">
    import {createSession} from '$lib/api';
    import { goto } from '$app/navigation';

    let userId = "";
    let status = "";

    async function handleSubmit() {
        try {
            const data = await createSession(userId)
            status = "Session created, Redirecting...";
            console.log(data);

            if (data && data.id) {
                // Navigate to the game route
                goto(`/game/${data.id}`);
            }
            
        } catch (e: any) {
            status = e.message;
        }
    }
</script>

<div class="max-w-md mx-auto mt-10 p-8 bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] rounded-xl">
    <h3 class="text-3xl font-black text-black mb-6 tracking-tight uppercase">
        Start a new game
    </h3>

    <form on:submit|preventDefault={handleSubmit} class="flex flex-col space-y-5">
        <div>
            <label for="username" class="block text-sm font-black text-black uppercase mb-2">
                Player Username
            </label>
            <input
                id="username"
                bind:value={userId}
                type="text"
                placeholder="e.g dizzy_dev"
                class="w-full px-4 py-3 rounded-lg bg-white text-black border-2 border-black 
                focus:bg-yellow-50 outline-none transition-all placeholder:text-gray-400 font-bold"
            />
        </div>
        
        <button 
            type="submit"
            class="w-full py-4 bg-[#bef264] hover:bg-[#a3e635] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none
            text-black font-black uppercase rounded-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all">
            Create Session
        </button>
    </form>

    {#if status}
        <div class="fixed bottom-5 right-5 p-4 border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] bg-[#bef264] text-black font-black uppercase">
            {status}
        </div>
    {/if}
</div>
