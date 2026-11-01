<script lang="ts">
export let isOpen = false
export let onClose
export let title
</script>

{#if isOpen}
  <button
    class="bg-black-950 bg-opacity-50 fixed inset-0 z-50 flex items-center justify-center p-4"
    on:click|self={onClose}
  >
    <div
      class="max-h-[100vh] w-full max-w-xl rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <slot {title} {onClose} />
    </div>
  </button>
{/if}
