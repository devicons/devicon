<script lang="ts">
export let content: string
export let flashMessage: string | undefined
export let flashDuration = 2000

let show = false
let flash = false

$: tooltipText = flash ? (flashMessage ?? content) : content
$: isVisible = show || flash

function handleClick() {
  if (!flashMessage) return
  flash = true
  setTimeout(() => (flash = false), flashDuration)
}
</script>

<div
  class="relative inline-flex w-fit"
  role="presentation"
  on:mouseenter={() => (show = true)}
  on:mouseleave={() => (show = false)}
  on:click={handleClick}
>
  <slot />

  {#if isVisible}
    <div
      class="fade-in pointer-events-none absolute z-10 max-w-xs rounded bg-green-600 px-2 py-1 text-sm whitespace-nowrap text-white shadow-lg bottom-full left-1/2 -translate-x-1/2 mb-2"
      role="tooltip"
    >
      {tooltipText}
    </div>
  {/if}
</div>

<style>
  .fade-in {
    animation: fade-in 0.3s ease-in-out both;
  }

  @keyframes fade-in {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
</style>
