<script lang="ts">
import type { IconVersions, IIcon } from "$lib/types/types"
import { copyToClipboard } from "$lib/common/copyToClipboard"
import Tooltip from "../../widgets/tooltip/Tooltip.svelte"

export let title: string
export let versions: IconVersions[]
export let selectedIcon: IIcon
export let getIconUrl: (icon: IIcon, version: IconVersions) => string
export let getFallbackIconUrl:
  | ((icon: IIcon, version: IconVersions) => string)
  | undefined = undefined
export let isCheckerboard: boolean = false

let selectedVersion: IconVersions = versions.includes("original")
  ? "original"
  : versions[0]

let isCopyingSvg = false

$: codeSnippet = `<img src="${getIconUrl(selectedIcon, selectedVersion)}"/>`

const selectVersion = (version: IconVersions) => (selectedVersion = version)

function handleImageError(e: Event, version: IconVersions) {
  if (getFallbackIconUrl) {
    const target = e.currentTarget as HTMLImageElement | null
    if (target) {
      const fallback = getFallbackIconUrl(selectedIcon, version)
      if (target.src !== fallback) {
        target.src = fallback
      }
    }
  }
}

async function copyRawSvg() {
  if (isCopyingSvg) return
  isCopyingSvg = true
  try {
    const primaryUrl = getIconUrl(selectedIcon, selectedVersion)
    let res = await fetch(primaryUrl)
    if (!res.ok && getFallbackIconUrl) {
      res = await fetch(getFallbackIconUrl(selectedIcon, selectedVersion))
    }
    if (res.ok) {
      const svgText = await res.text()
      await copyToClipboard(svgText)
    }
  } catch (err) {
    if (getFallbackIconUrl) {
      try {
        const fallbackRes = await fetch(
          getFallbackIconUrl(selectedIcon, selectedVersion),
        )
        if (fallbackRes.ok) {
          const svgText = await fallbackRes.text()
          await copyToClipboard(svgText)
        }
      } catch (fallbackErr) {
        console.error("Failed to fetch fallback SVG:", fallbackErr)
      }
    }
  } finally {
    isCopyingSvg = false
  }
}
</script>

<h3 class="mb-2">{title}</h3>

{#if versions.length > 0}
  <div
    class="mb-4 flex w-full flex-wrap rounded-lg p-4 transition-colors {isCheckerboard
      ? 'checkerboard border border-gray-300 dark:border-gray-600'
      : 'bg-gray-100 dark:bg-gray-700'}"
  >
    {#each versions as version}
      <button
        type="button"
        class="h-24 cursor-pointer p-1 transition-all
          {selectedVersion === version
          ? 'rounded-lg bg-green-50 ring-2 ring-green-500 dark:bg-green-950/10'
          : 'hover:opacity-80'}"
        on:click={() => selectVersion(version)}
        aria-label={`Select ${version} version`}
      >
        <img
          src={getIconUrl(selectedIcon, version)}
          on:error={(e) => handleImageError(e, version)}
          alt={`${selectedIcon.name} (${version})`}
          class="h-full"
        />
      </button>
    {/each}
  </div>

  <div class="mt-4 flex items-center justify-between">
    <span class="text-sm font-medium text-gray-700 dark:text-gray-300">HTML & SVG Markup</span>
    <Tooltip content="Copy raw SVG text" flashMessage="Copied SVG!">
      <button
        type="button"
        class="flex cursor-pointer items-center gap-1.5 rounded-md bg-green-500 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-green-600"
        on:click={copyRawSvg}
        aria-label="Copy SVG Code"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="2"
          stroke="currentColor"
          class="size-4"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5"
          />
        </svg>
        <span>Copy SVG Code</span>
      </button>
    </Tooltip>
  </div>

  <div
    class="code-snippet relative mt-2 flex w-full items-center justify-between rounded-md bg-gray-100 p-4 dark:bg-gray-900 dark:text-gray-400"
  >
    <code class="break-all">{codeSnippet}</code>
    <Tooltip content="Copy to clipboard" flashMessage="Copied!">
      <button
        type="button"
        class="ml-2 flex-shrink-0 cursor-pointer rounded-full text-xl"
        on:click={() => copyToClipboard(codeSnippet)}
        aria-label="Copy code snippet"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"
          />
        </svg>
      </button>
    </Tooltip>
  </div>
{:else}
  <p class="text-gray-500 dark:text-gray-400">No SVG versions available</p>
{/if}
