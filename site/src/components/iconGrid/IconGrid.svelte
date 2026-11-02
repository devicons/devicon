<script lang="ts">
import type { IIcon } from "$lib/types/types"
import { isLoading, clearFilters } from "$lib/stores/iconStore"
import IconCard from "./IconCard.svelte"

export let icons: IIcon[] = []
</script>

<section class="flex flex-col gap-3 py-3" aria-label="Icons Grid">
  <!-- Status bar with count -->
  <div class="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
    <div>
      {#if $isLoading}
        <span>Loading developer icons...</span>
      {:else}
        <span>Showing <strong class="font-mono font-medium text-slate-900 dark:text-white">{icons.length}</strong> icons</span>
      {/if}
    </div>
  </div>

  {#if $isLoading}
    <!-- Skeleton Loading State -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-2.5" aria-busy="true">
      {#each Array(24) as _, i (i)}
        <div class="flex flex-col items-center justify-between rounded-xl border border-slate-200/80 bg-white p-3 animate-pulse dark:border-white/[0.06] dark:bg-[#11131a] h-[148px]">
          <div class="size-12 rounded-lg bg-slate-100 dark:bg-white/5 my-auto"></div>
          <div class="h-3 w-16 rounded bg-slate-100 dark:bg-white/5"></div>
          <div class="h-2 w-10 rounded bg-slate-50 dark:bg-white/5 mt-1"></div>
        </div>
      {/each}
    </div>
  {:else if icons.length === 0}
    <!-- Empty State -->
    <div class="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-200 py-16 px-4 text-center dark:border-white/[0.08] dark:bg-[#11131a]/40">
      <div class="flex size-12 items-center justify-center rounded-xl bg-slate-100 text-slate-400 dark:bg-white/5 dark:text-slate-500 mb-3">
        <svg class="size-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
          <line x1="8" y1="11" x2="14" y2="11"/>
        </svg>
      </div>

      <h3 class="text-sm font-semibold text-slate-900 dark:text-white">
        No icons found matching your filters
      </h3>
      <p class="mt-1 max-w-sm text-xs text-slate-500 dark:text-slate-400">
        Try adjusting your search query, selecting a different category, or resetting all filters.
      </p>

      <button
        type="button"
        on:click={clearFilters}
        class="mt-4 inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-xs transition hover:bg-slate-50 dark:border-white/[0.08] dark:bg-[#181b24] dark:text-slate-200 dark:hover:bg-[#222634] cursor-pointer"
      >
        <svg class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
          <path d="M3 3v5h5"/>
        </svg>
        <span>Reset all filters</span>
      </button>
    </div>
  {:else}
    <!-- Populated Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-2.5">
      {#each icons as icon (icon.name)}
        <IconCard {icon} />
      {/each}
    </div>
  {/if}
</section>
