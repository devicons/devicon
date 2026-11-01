<script lang="ts">
import { sortOption, setSortOption } from "$lib/stores/iconStore"
import type { SortOption } from "$lib/types/types"

const sortOptions: { value: SortOption; label: string }[] = [
  { value: "name-asc", label: "Name (A-Z)" },
  { value: "name-desc", label: "Name (Z-A)" },
  { value: "newest", label: "Newest" },
]

function handleSortChange(e: Event) {
  const target = e.target as HTMLSelectElement
  setSortOption(target.value as SortOption)
}
</script>

<div class="relative min-w-[140px]">
  <select
    id="sort-select"
    value={$sortOption}
    on:change={handleSortChange}
    class="w-full cursor-pointer appearance-none rounded-md border border-gray-200 bg-white p-2 pr-8 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
    aria-label="Sort icons"
  >
    {#each sortOptions as opt}
      <option value={opt.value}>{opt.label}</option>
    {/each}
  </select>

  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width="1.5"
    stroke="currentColor"
    class="pointer-events-none absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500 dark:text-gray-300"
  >
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      d="m19.5 8.25-7.5 7.5-7.5-7.5"
    />
  </svg>
</div>
