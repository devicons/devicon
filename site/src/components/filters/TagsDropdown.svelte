<script lang="ts">
import {
  availableTags,
  selectedTags,
  setSelectedTags,
} from "$lib/stores/iconStore"

let isDropdownOpen = false

$: hasSelectedTags = $selectedTags.length > 0
$: label = hasSelectedTags
  ? `Tags (${$selectedTags.length})`
  : "All Tags"

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
    class="flex w-full cursor-pointer items-center justify-between rounded-lg border border-slate-200 bg-white py-1.5 px-2.5 text-xs font-medium text-slate-700 outline-none transition hover:border-slate-300 dark:border-white/[0.08] dark:bg-[#11131a] dark:text-slate-200 dark:hover:border-white/[0.15]"
    aria-expanded={isDropdownOpen}
    aria-haspopup="true"
  >
    <span class="truncate">{label}</span>

    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="ml-1 size-3.5 text-slate-400 dark:text-slate-500"
      aria-hidden="true"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d={isDropdownOpen ? 'm4.5 15.75 7.5-7.5 7.5 7.5' : 'm19.5 8.25-7.5 7.5-7.5-7.5'}
      />
    </svg>
  </button>

  {#if isDropdownOpen}
    <!-- overlay backdrop -->
    <button
      class="fixed inset-0 z-20 cursor-default bg-transparent"
      on:click={() => (isDropdownOpen = false)}
      aria-label="Close dropdown"
    ></button>

    <div
      class="absolute right-0 z-30 mt-1.5 flex max-h-80 w-60 flex-col rounded-xl border border-slate-200 bg-white shadow-xl backdrop-blur-md dark:border-white/[0.08] dark:bg-[#11131a]"
    >
      <!-- scrollable tag list -->
      <div class="flex-1 overflow-y-auto py-1 no-scrollbar">
        {#each $availableTags as tag}
          {@const isChecked = $selectedTags.includes(tag)}
          <button
            type="button"
            class="flex w-full cursor-pointer items-center px-3 py-1.5 text-left text-xs transition hover:bg-slate-100 dark:hover:bg-white/5"
            on:click={() => toggleTag(tag)}
          >
            <input
              type="checkbox"
              checked={isChecked}
              class="mr-2.5 size-3.5 rounded border-slate-300 text-emerald-500 focus:ring-0 dark:border-white/20 dark:bg-white/5"
              tabindex="-1"
            />
            <span class="flex-1 truncate text-slate-700 dark:text-slate-200 {isChecked ? 'font-semibold text-emerald-600 dark:text-emerald-400' : ''}">{tag}</span>
          </button>
        {/each}
      </div>

      <!-- footer reset button -->
      <div class="border-t border-slate-200 p-2 dark:border-white/[0.08]">
        <button
          type="button"
          class="w-full rounded-md px-2.5 py-1 text-xs font-medium transition
                 {hasSelectedTags
            ? 'cursor-pointer bg-emerald-500/10 text-emerald-600 hover:bg-emerald-500/20 dark:text-emerald-400'
            : 'bg-slate-100 text-slate-400 dark:bg-white/5 dark:text-slate-500 cursor-not-allowed'}"
          disabled={!hasSelectedTags}
          on:click={() => setSelectedTags([])}
        >
          Reset tags
        </button>
      </div>
    </div>
  {/if}
</div>
