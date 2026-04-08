<script lang="ts">
    import SongRanking from "$lib/components/SongRanking.svelte";
    import CreateSession from "$lib/components/createSession.svelte";
</script>


<main class="min-h-screen bg-white p-10">
    <div class="max-w-4xl mx-auto">
        <header class="mb-12 text-center">
            <h1 class="text-5xl font-extrabold">
                DIZZY SESSIONS
            </h1>
        </header>
        <section>

            <CreateSession />
        </section>
    </div>
</main>

