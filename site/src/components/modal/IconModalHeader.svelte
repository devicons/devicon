<script lang="ts">
export let title: string | undefined = undefined
export let onClose: () => void
export let tags: string[] = []
</script>

<div class="mb-5 flex items-center justify-between border-b border-slate-100 pb-3.5 dark:border-white/[0.06]">
  <div class="flex items-center gap-3">
    <h2 id="modal-title" class="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white capitalize">
      {title}
    </h2>
    {#if tags && tags.length > 0}
      <div class="hidden sm:flex items-center gap-1.5 overflow-x-auto no-scrollbar">
        {#each tags.slice(0, 3) as tag}
          <span class="rounded bg-slate-100 px-2 py-0.5 text-[11px] font-mono text-slate-500 dark:bg-white/[0.04] dark:text-slate-400">
            #{tag}
          </span>
        {/each}
      </div>
    {/if}
  </div>

  <button
    type="button"
    class="flex size-8 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-white/5 dark:hover:text-white cursor-pointer"
    on:click={onClose}
    aria-label="Close modal"
  >
    <svg class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="18" y1="6" x2="6" y2="18"/>
      <line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  </button>
</div>
