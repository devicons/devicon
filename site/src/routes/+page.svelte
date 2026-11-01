<script lang="ts">
import { onMount } from "svelte"
import IconGrid from "../components/iconGrid/IconGrid.svelte"
import IconModal from "../components/modal/IconModal.svelte"
import {
  fetchIconsData,
  filteredIcons,
  isModalOpen,
  isLoading,
  error,
} from "$lib/stores/iconStore"
import FiltersBar from "../components/filters/FiltersBar.svelte"

onMount(() => {
  fetchIconsData()
})
</script>

<main class="min-h-screen dark:bg-gray-900 dark:text-white">
  <div class="base-container">
    {#if $isLoading}
      <div class="flex items-center justify-center py-8">
        <div class="text-lg">Loading icons...</div>
      </div>
    {:else if $error}
      <div class="rounded-lg bg-red-100 p-4 dark:bg-red-900">
        <p class="text-red-700 dark:text-red-300">Error: {$error}</p>
      </div>
    {:else}
      <FiltersBar />
      <IconGrid icons={$filteredIcons} />
    {/if}
    {#if $isModalOpen}
      <IconModal />
    {/if}
  </div>
</main>
