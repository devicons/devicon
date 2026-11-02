<script lang="ts">
import { searchTerm, setSearchTerm } from "$lib/stores/iconStore"

function handleSearch(e: Event) {
  const target = e.target as HTMLInputElement
  setSearchTerm(target.value)
}
</script>

<div class="relative w-full">
  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-2.5 text-slate-400 dark:text-slate-500">
    <svg class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="11" cy="11" r="8"/>
      <path d="m21 21-4.35-4.35"/>
    </svg>
  </div>

  <input
    type="text"
    id="search"
    value={$searchTerm}
    on:input={handleSearch}
    placeholder="Filter icons..."
    class="w-full rounded-lg border border-slate-200 bg-white py-1.5 pr-7 pl-8 text-xs text-slate-800 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-slate-400 dark:border-white/[0.08] dark:bg-[#11131a] dark:text-slate-100 dark:placeholder:text-slate-500 dark:hover:border-white/[0.15] dark:focus:border-white/25"
  />

  {#if $searchTerm}
    <button
      type="button"
      on:click={() => setSearchTerm("")}
      class="absolute inset-y-0 right-0 flex items-center pr-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 cursor-pointer"
      aria-label="Clear search"
    >
      <svg class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </button>
  {/if}
</div>
