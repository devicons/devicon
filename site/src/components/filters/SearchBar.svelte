<script lang="ts">
import { searchTerm, setSearchTerm } from "$lib/stores/iconStore"

function handleSearch(e: Event) {
  const target = e.target as HTMLInputElement
  setSearchTerm(target.value)
}
</script>

<div class="relative w-full">
  <input
    type="text"
    id="search"
    bind:value={$searchTerm}
    on:input={handleSearch}
    placeholder="Search Icons..."
    class="w-full rounded-md border border-gray-200 p-2 pl-9 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
  />

  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width="1.5"
    stroke="currentColor"
    class="absolute top-1/2 left-2 h-5 w-5 -translate-y-1/2 text-gray-500 dark:text-gray-300"
  >
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
    />
  </svg>
</div>
