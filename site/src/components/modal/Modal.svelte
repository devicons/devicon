<script lang="ts">
export let isOpen = false
export let onClose: () => void
export let title: string | undefined = undefined
</script>

{#if isOpen}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-black/75 backdrop-blur-xs"
    role="presentation"
  >
    <!-- Background overlay click catcher -->
    <button
      type="button"
      class="fixed inset-0 size-full cursor-default border-0 bg-transparent p-0"
      on:click={onClose}
      aria-label="Close dialog"
      tabindex="-1"
    ></button>

    <!-- Modal Dialog Body -->
    <div
      class="relative z-10 my-auto w-full max-w-4xl rounded-2xl border border-slate-200/90 bg-white p-5 sm:p-6 text-left shadow-2xl transition-all dark:border-white/[0.08] dark:bg-[#09090b] max-h-[92vh] flex flex-col overflow-y-auto no-scrollbar"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <slot {title} {onClose} />
    </div>
  </div>
{/if}
