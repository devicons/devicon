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

<div class="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar" role="tablist" aria-label="Icon categories">
  {#each categories as category}
    {@const isActive = $selectedCategory === category.id}
    {@const count = $categoryCounts?.[category.id] ?? 0}
    <button
      type="button"
      role="tab"
      aria-selected={isActive}
      on:click={() => setSelectedCategory(category.id)}
      class="cursor-pointer inline-flex items-center gap-1.5 whitespace-nowrap rounded-lg px-2.5 py-1.5 text-xs font-medium transition-all {isActive
        ? 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30 font-semibold shadow-2xs'
        : 'border border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-white/[0.04]'}"
    >
      <span>{category.label}</span>
      {#if count > 0}
        <span
          class="rounded-full px-1.5 py-0.5 text-[10px] font-mono leading-none transition-colors {isActive
            ? 'bg-emerald-500/20 text-emerald-800 dark:text-emerald-300'
            : 'bg-slate-100 text-slate-500 dark:bg-white/5 dark:text-slate-400'}"
        >
          {count}
        </span>
      {/if}
    </button>
  {/each}
</div>
