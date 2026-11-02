<script lang="ts">
import SearchBar from "./SearchBar.svelte"
import TagsDropdown from "./TagsDropdown.svelte"
import SortDropdown from "./SortDropdown.svelte"
import VersionDropdown from "./VersionDropdown.svelte"
import CategoryChips from "./CategoryChips.svelte"
import {
  searchTerm,
  selectedTags,
  selectedCategory,
  selectedVersionFilter,
  clearFilters,
} from "$lib/stores/iconStore"

$: hasActiveFilters =
  $searchTerm !== "" ||
  $selectedTags.length > 0 ||
  $selectedCategory !== "all" ||
  $selectedVersionFilter !== "all"
</script>

<div
  id="icons"
  class="sticky top-14 z-20 -mx-4 sm:-mx-6 lg:-mx-8 px-4 sm:px-6 lg:px-8 bg-white/90 dark:bg-[#09090b]/90 backdrop-blur-md border-b border-slate-200/80 dark:border-white/[0.08] py-2.5 transition-colors"
>
  <div class="scroll-mt-24 flex flex-col gap-2.5">
    <!-- Top: Category Chips (Linear-style tabs) -->
    <CategoryChips />

    <!-- Bottom: Search and Select Controls -->
    <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
      <!-- Search Bar -->
      <div class="w-full sm:max-w-xs">
        <SearchBar />
      </div>

      <!-- Filters Controls Group -->
      <div class="flex flex-wrap items-center gap-2">
        <VersionDropdown />
        <div class="min-w-[110px]">
          <TagsDropdown />
        </div>
        <SortDropdown />

        <!-- Clear Filters Button -->
        {#if hasActiveFilters}
          <button
            type="button"
            on:click={clearFilters}
            class="cursor-pointer inline-flex items-center gap-1 rounded-lg border border-slate-200 bg-white px-2.5 py-1.5 text-xs font-medium text-slate-600 transition hover:bg-slate-50 hover:text-red-600 dark:border-white/[0.08] dark:bg-[#11131a] dark:text-slate-400 dark:hover:text-red-400"
            aria-label="Clear all active filters"
          >
            <svg class="size-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            <span>Reset</span>
          </button>
        {/if}
      </div>
    </div>
  </div>
</div>
