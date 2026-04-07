<script lang="ts">
    import {createSession} from '$lib/api';

    let userId = "";
    let status = "";

    async function handleSubmit() {
        try {
            const data = await createSession(userId)
            status = "Sesion created";
            console.log(data);
        } catch (e: any) {
            status = e.message;
        }
    }
</script>

<div class="max-w-md mx-auto mt-10 p-8 bg-gray-900 rounded-2xl border border-gray-800 shadow-2xl">
    <h3 class="text-2xl font-black text-white mb-6 tracking-tight">
        Start a new game
    </h3>

    <form on:submit|preventDefault={handleSubmit} class="flex flex-col space-y-4">
        <div>
            <label for="username" class="block text-xs font-bold text-gray-400 uppercase mb-1 ml-1">
                Player Username
            </label>
            <input
                id="username"
                bind:value={userId}
                type="text"
                placeholder="e.g dizzy_dev"
                class="w-full px-4 py-3 rounded-lg bg-gray-800 text-white border border-gray-700
                focus:ring-1.3 focus:ring-emerald-500 focus:border-transparent outline-none
                transition-all duration-200 placeholder:text-gray-600
                "
            />
        </div>
        
        <button 
            type="submit"
            class="w-full py-3 bg-emerald-600 hover:bg-emerald-500 active:scale-95
            text-white font-bold rounded-lg shadow-lg shadow-emerald-900/20 transition-all duration-150
            ">
            Create Session
        </button>
    </form>

    {#if status}
        <p class="mt-4 text-center text-sm font-medium {status.includes('Error') ? 'text-red-400' : 'text-emerald-400'}">
            {status}
        </p>
    {/if}
</div>
