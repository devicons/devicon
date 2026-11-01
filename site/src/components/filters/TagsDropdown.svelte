<script lang="ts">
import {
  availableTags,
  selectedTags,
  setSelectedTags,
} from "$lib/stores/iconStore"

let isDropdownOpen = false

// derived values
$: hasSelectedTags = $selectedTags.length > 0
$: label = hasSelectedTags
  ? `Select Tags (${$selectedTags.length}/${$availableTags.length})`
  : "Select Tags"

function toggleTag(tag: string) {
  setSelectedTags(
    $selectedTags.includes(tag)
      ? $selectedTags.filter((t) => t !== tag)
      : [...$selectedTags, tag],
  )
}
</script>

<div class="relative w-full">
  <button
    id="tag-dropdown"
    type="button"
    on:click={() => (isDropdownOpen = !isDropdownOpen)}
    class="flex w-full cursor-pointer items-center justify-between rounded-md border border-gray-200 p-2 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
    aria-expanded={isDropdownOpen}
    aria-haspopup="true"
  >
    <span>{label}</span>

    <!-- icon -->
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="h-5 w-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d={isDropdownOpen ? 'm4.5 15.75 7.5-7.5 7.5 7.5' : 'm19.5 8.25-7.5 7.5-7.5-7.5'}
      />
    </svg>
  </button>

  {#if isDropdownOpen}
    <!-- overlay -->
    <button
      class="fixed inset-0 z-10"
      on:click={() => (isDropdownOpen = false)}
      aria-label="Close dropdown"
    ></button>

    <div
      class="absolute z-20 mt-1 flex max-h-96 w-full flex-col rounded-md border border-gray-200 bg-white shadow-lg dark:border-gray-600 dark:bg-gray-800"
    >
      <!-- scrollable tag list -->
      <div class="flex-1 overflow-y-auto py-1">
        {#each $availableTags as tag}
          <button
            type="button"
            class="flex w-full cursor-pointer items-center px-3 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700"
            on:click={() => toggleTag(tag)}
          >
            <input
              type="checkbox"
              checked={$selectedTags.includes(tag)}
              class="mr-2"
              tabindex="-1"
            />
            <span class="flex-1 dark:text-gray-100">{tag}</span>
          </button>
        {/each}
      </div>

      <!-- footer reset button -->
      <div class="border-t border-gray-200 p-2 dark:border-gray-600">
        <button
          type="button"
          class="w-full rounded-md px-3 py-2 text-sm font-medium
                 {hasSelectedTags
            ? 'cursor-pointer bg-gray-100 text-gray-800 hover:bg-gray-100 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'
            : 'bg-gray-100 text-gray-400 dark:bg-gray-700 dark:text-gray-500'}"
          disabled={!hasSelectedTags}
          on:click={() => setSelectedTags([])}
        >
          Reset filters
        </button>
      </div>
    </div>
  {/if}
</div>
