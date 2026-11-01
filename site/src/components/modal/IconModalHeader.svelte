<script lang="ts">
export let title: string | undefined = undefined
export let onClose: () => void
export let isCheckerboard: boolean = false
export let onToggleCheckerboard: (() => void) | undefined = undefined
</script>

<div class="mb-4 flex items-center justify-between">
  <h2 id="modal-title" class="text-xl font-bold dark:text-white">
    {title}
  </h2>
  <div class="flex items-center gap-2">
    {#if onToggleCheckerboard}
      <button
        type="button"
        class="flex cursor-pointer items-center gap-1.5 rounded-md border border-gray-200 px-2 py-1 text-xs font-medium text-gray-700 transition hover:bg-gray-100 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
        on:click={onToggleCheckerboard}
        title="Toggle checkerboard background"
        aria-label="Toggle checkerboard background"
      >
        <svg class="h-3.5 w-3.5" viewBox="0 0 16 16" fill="currentColor">
          <rect x="0" y="0" width="8" height="8" fill="currentColor" opacity="0.3"/>
          <rect x="8" y="0" width="8" height="8" fill="currentColor" opacity="0.8"/>
          <rect x="0" y="8" width="8" height="8" fill="currentColor" opacity="0.8"/>
          <rect x="8" y="8" width="8" height="8" fill="currentColor" opacity="0.3"/>
        </svg>
        <span>{isCheckerboard ? "Solid BG" : "Checkerboard"}</span>
      </button>
    {/if}
    <button
      class="cursor-pointer text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
      on:click={onClose}
      aria-label="Close modal"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M6 18L18 6M6 6l12 12"
        />
      </svg>
    </button>
  </div>
</div>
