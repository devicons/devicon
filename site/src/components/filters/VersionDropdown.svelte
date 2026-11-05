<script lang="ts">
import {
  selectedVersionFilter,
  setSelectedVersionFilter,
} from "$lib/stores/iconStore"

const versionOptions: { value: string; label: string }[] = [
  { value: "all", label: "All Variants" },
  { value: "original", label: "Original" },
  { value: "plain", label: "Plain" },
  { value: "line", label: "Line" },
  { value: "wordmark", label: "Wordmark" },
]

function handleChange(e: Event) {
  const target = e.target as HTMLSelectElement
  setSelectedVersionFilter(target.value)
}
</script>

<div class="relative min-w-[110px]">
  <select
    id="version-filter-select"
    value={$selectedVersionFilter}
    on:change={handleChange}
    class="w-full cursor-pointer appearance-none rounded-lg border border-slate-200 bg-white py-1.5 pl-2.5 pr-7 text-xs font-medium text-slate-700 outline-none transition hover:border-slate-300 focus:border-slate-400 dark:border-white/[0.08] dark:bg-[#11131a] dark:text-slate-200 dark:hover:border-white/[0.15] dark:focus:border-white/25"
    aria-label="Filter by icon version"
  >
    {#each versionOptions as opt}
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
