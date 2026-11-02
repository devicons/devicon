<script lang="ts">
import { sortOption, setSortOption } from "$lib/stores/iconStore"
import type { SortOption } from "$lib/types/types"

const sortOptions: { value: SortOption; label: string }[] = [
  { value: "name-asc", label: "Name (A-Z)" },
  { value: "name-desc", label: "Name (Z-A)" },
  { value: "most-versions", label: "Most Versions" },
  { value: "newest", label: "Newest" },
]

function handleSortChange(e: Event) {
  const target = e.target as HTMLSelectElement
  setSortOption(target.value as SortOption)
}
</script>

<div class="relative min-w-[120px]">
  <select
    id="sort-select"
    value={$sortOption}
    on:change={handleSortChange}
    class="w-full cursor-pointer appearance-none rounded-lg border border-slate-200 bg-white py-1.5 pl-2.5 pr-7 text-xs font-medium text-slate-700 outline-none transition hover:border-slate-300 focus:border-slate-400 dark:border-white/[0.08] dark:bg-[#11131a] dark:text-slate-200 dark:hover:border-white/[0.15] dark:focus:border-white/25"
    aria-label="Sort icons"
  >
    {#each sortOptions as opt}
      <option value={opt.value} class="dark:bg-[#11131a]">{opt.label}</option>
    {/each}
  </select>

  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width="1.5"
    stroke="currentColor"
    class="pointer-events-none absolute right-2 top-1/2 size-3.5 -translate-y-1/2 text-slate-400 dark:text-slate-500"
    aria-hidden="true"
  >
    <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/>
  </svg>
</div>
