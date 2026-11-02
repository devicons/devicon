<script lang="ts">
import {
  selectedCategory,
  setSelectedCategory,
  categoryCounts,
} from "$lib/stores/iconStore"
import type { CategoryOption } from "$lib/types/types"

const categories: { id: CategoryOption; label: string }[] = [
  { id: "all", label: "All" },
  { id: "language", label: "Languages" },
  { id: "framework", label: "Frameworks" },
  { id: "database", label: "Databases" },
  { id: "library", label: "Libraries" },
  { id: "cloud", label: "Cloud & DevOps" },
  { id: "tool", label: "Tools" },
]
</script>

<div class="flex items-center gap-1 overflow-x-auto pb-1 no-scrollbar" role="tablist" aria-label="Icon categories">
  {#each categories as category}
    {@const isActive = $selectedCategory === category.id}
    {@const count = $categoryCounts?.[category.id] ?? 0}
    <button
      type="button"
      role="tab"
      aria-selected={isActive}
      on:click={() => setSelectedCategory(category.id)}
      class="cursor-pointer inline-flex items-center gap-1.5 whitespace-nowrap rounded-md px-2.5 py-1.5 text-xs font-medium transition-colors {isActive
        ? 'bg-slate-200/90 text-slate-900 dark:bg-white/10 dark:text-white font-semibold'
        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/[0.04]'}"
    >
      <span>{category.label}</span>
      {#if count > 0}
        <span class="text-[11px] font-mono text-slate-400 dark:text-slate-500">
          {count}
        </span>
      {/if}
    </button>
  {/each}
</div>
