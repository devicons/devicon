<script lang="ts">
import HeaderSnippet from "./HeaderSnippet.svelte"
import { latestVersion } from "$lib/stores/iconStore"
import HeaderStats from "./HeaderStats.svelte"
import ContactLinks from "../widgets/contact/ContactLinks.svelte"
</script>

<header
  class="flex flex-col justify-center items-center py-8 px-4 bg-base-300 bg-white dark:bg-gray-800 dark:text-white"
>
  <div
    id="title"
    class="mb-2 text-center text-8xl sm:text-9xl font-damion text-green-500"
  >
    Devicon
    <span class="block text-5xl -mt-6 sm:text-6xl sm:inline sm:mt-auto">
      v{$latestVersion}
    </span>
  </div>
  <p class="mt-4 text-xl text-center sm:mt-auto dark:text-gray-400">
    Icons about programming languages, software development, and graphic design
    tools.
  </p>

  <ContactLinks />
  <HeaderStats />
  <HeaderSnippet />
</header>

<style>
  .font-damion {
    font-family: 'Damion', Times, serif;
  }
</style>
