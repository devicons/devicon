<script lang="ts">
import { openIconModal } from "$lib/stores/iconStore"
import type { IIcon } from "$lib/types/types"

export let icons: IIcon[] = []

const isWhite = (color: string): boolean => {
  if (!color) return false

  let hex = color.trim().toLowerCase()

  if (hex.startsWith("#")) {
    hex = hex.slice(1)
  }

  if (hex.length === 3) {
    hex = hex
      .split("")
      .map((c) => c + c)
      .join("")
  }

  return hex === "ffffff"
}
</script>

<section class="flex flex-col gap-4 py-8">
  <p>
    <span class="font-bold">{icons.length}</span> Icons Found
  </p>

  <div class="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-6 lg:grid-cols-8">
    {#each icons as icon}
      <button
        type="button"
        class={'w-full cursor-pointer rounded-lg border border-gray-200 bg-white p-4 text-left transition hover:bg-gray-100 hover:text-gray-800 hover:shadow-md dark:border-gray-600 dark:bg-gray-800'}
        on:click={() => openIconModal(icon)}
        aria-label={`View ${icon.name} details`}
      >
        <div class="mb-2 flex h-24 items-center justify-center">
          <i
            class="text-4xl sm:h-12 sm:w-12 sm:text-6xl devicon-{icon.name}-{icon.versions
              .font?.[0] ?? 'plain'}"
            style={`color: ${isWhite(icon.color) ? '#000000' : icon.color};`}
          ></i>
        </div>

        <h3 class="truncate text-center text-sm font-medium">{icon.name}</h3>
      </button>
    {/each}
  </div>
</section>
