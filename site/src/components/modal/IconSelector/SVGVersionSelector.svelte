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

type FormatTab = "svg" | "img"
let activeTab: FormatTab = "svg"

let selectedVersion: IconVersions = versions.includes("original")
  ? "original"
  : versions[0]

let currentIconName = ""
let rawSvgText = ""
let isLoadingSvg = false
let svgFetchError = false
let fetchToken = 0

$: if (selectedIcon && selectedIcon.name !== currentIconName) {
  currentIconName = selectedIcon.name
  selectedVersion = versions.includes("original") ? "original" : versions[0]
}

$: if (versions.length > 0 && !versions.includes(selectedVersion)) {
  selectedVersion = versions.includes("original") ? "original" : versions[0]
}

function formatSvg(raw: string): string {
  if (!raw) return ""

  const viewBoxMatch = raw.match(/viewBox=["']([^"']+)["']/i)
  const viewBox = viewBoxMatch ? viewBoxMatch[1] : "0 0 128 128"

  const match = raw.match(/<svg[^>]*>([\s\S]*?)<\/svg>/i)
  const inner = match ? match[1].trim() : raw.trim()

  const tokens = inner.replace(/>\s*</g, ">\n<").split("\n")
  let indent = 2
  const formattedLines: string[] = []

  for (let token of tokens) {
    token = token.trim()
    if (!token) continue
    if (token.startsWith("</")) {
      indent = Math.max(2, indent - 2)
    }
    formattedLines.push(" ".repeat(indent) + token)
    if (
      token.startsWith("<") &&
      !token.startsWith("</") &&
      !token.endsWith("/>") &&
      !token.startsWith("<!--")
    ) {
      indent += 2
    }
  }

  return `<svg viewBox="${viewBox}">\n${formattedLines.join("\n")}\n</svg>`
}

$: formattedSvgText = formatSvg(rawSvgText)
$: imgSnippet = `<img src="${getIconUrl(selectedIcon, selectedVersion)}" />`

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

async function fetchRawSvg(icon: IIcon, version: IconVersions) {
  if (typeof window === "undefined" || !icon || !version) return
  const currentToken = ++fetchToken
  isLoadingSvg = true
  svgFetchError = false
  rawSvgText = ""

  try {
    const primaryUrl = getIconUrl(icon, version)
    let res = await fetch(primaryUrl)
    if (!res.ok && getFallbackIconUrl) {
      res = await fetch(getFallbackIconUrl(icon, version))
    }
    if (currentToken !== fetchToken) return

    if (res.ok) {
      const text = await res.text()
      if (currentToken === fetchToken) {
        rawSvgText = text.trim()
        isLoadingSvg = false
      }
    } else {
      if (currentToken === fetchToken) {
        svgFetchError = true
        isLoadingSvg = false
      }
    }
  } catch (err) {
    if (getFallbackIconUrl) {
      try {
        const fallbackRes = await fetch(getFallbackIconUrl(icon, version))
        if (currentToken !== fetchToken) return
        if (fallbackRes.ok) {
          const text = await fallbackRes.text()
          if (currentToken === fetchToken) {
            rawSvgText = text.trim()
            isLoadingSvg = false
            return
          }
        }
      } catch {
        // ignore fallback errors
      }
    }
    if (currentToken === fetchToken) {
      svgFetchError = true
      isLoadingSvg = false
    }
  }
}

$: if (selectedIcon && selectedVersion) {
  fetchRawSvg(selectedIcon, selectedVersion)
}

function downloadSvg() {
  const contentToDownload = formattedSvgText || rawSvgText
  if (!contentToDownload || typeof window === "undefined") return
  const blob = new Blob([contentToDownload], { type: "image/svg+xml;charset=utf-8" })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = `${selectedIcon.name}-${selectedVersion}.svg`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
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

  <div class="mt-4 flex flex-wrap items-center justify-between gap-2">
    <div class="flex items-center rounded-lg bg-gray-200 p-1 dark:bg-gray-800">
      <button
        type="button"
        class="cursor-pointer rounded-md px-3 py-1 text-xs font-semibold transition-all {activeTab === 'svg'
          ? 'bg-white text-gray-900 shadow-sm dark:bg-gray-700 dark:text-white'
          : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white'}"
        on:click={() => (activeTab = "svg")}
        aria-label="Pure SVG format"
      >
        Pure SVG
      </button>
      <button
        type="button"
        class="cursor-pointer rounded-md px-3 py-1 text-xs font-semibold transition-all {activeTab === 'img'
          ? 'bg-white text-gray-900 shadow-sm dark:bg-gray-700 dark:text-white'
          : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white'}"
        on:click={() => (activeTab = "img")}
        aria-label="&lt;img&gt; Element format"
      >
        &lt;img&gt; Element
      </button>
    </div>

    <div class="flex items-center gap-2">
      {#if activeTab === "svg"}
        <button
          type="button"
          class="flex cursor-pointer items-center gap-1.5 rounded-md border border-gray-300 px-3 py-1.5 text-xs font-semibold text-gray-700 transition hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
          on:click={downloadSvg}
          disabled={isLoadingSvg || !formattedSvgText}
          aria-label="Download SVG"
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
              d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"
            />
          </svg>
          <span>Download SVG</span>
        </button>

        <Tooltip content="Copy raw SVG text" flashMessage="Copied SVG!">
          <button
            type="button"
            class="flex cursor-pointer items-center gap-1.5 rounded-md bg-green-500 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-green-600 disabled:cursor-not-allowed disabled:opacity-50"
            on:click={() => copyToClipboard(formattedSvgText)}
            disabled={isLoadingSvg || !formattedSvgText}
            aria-label="Copy Pure SVG"
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
                d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"
              />
            </svg>
            <span>Copy Pure SVG</span>
          </button>
        </Tooltip>
      {:else}
        <Tooltip content="Copy <img> tag" flashMessage="Copied <img>!">
          <button
            type="button"
            class="flex cursor-pointer items-center gap-1.5 rounded-md bg-green-500 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-green-600"
            on:click={() => copyToClipboard(imgSnippet)}
            aria-label="Copy <img> Tag"
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
                d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"
              />
            </svg>
            <span>Copy &lt;img&gt; Tag</span>
          </button>
        </Tooltip>
      {/if}
    </div>
  </div>

  <div
    class="code-snippet relative mt-2 max-h-48 w-full overflow-x-auto overflow-y-auto rounded-md bg-gray-100 p-4 font-mono text-xs text-left no-scrollbar dark:bg-gray-900 dark:text-gray-400"
  >
    {#if activeTab === "svg"}
      {#if isLoadingSvg}
        <span class="text-gray-500 italic">Loading SVG content...</span>
      {:else if svgFetchError}
        <span class="text-red-500">Failed to load SVG markup.</span>
      {:else}
        <pre class="font-mono text-xs whitespace-pre text-left no-scrollbar"><code>{formattedSvgText}</code></pre>
      {/if}
    {:else}
      <pre class="font-mono text-xs whitespace-pre-wrap break-all text-left no-scrollbar"><code>{imgSnippet}</code></pre>
    {/if}
  </div>
{:else}
  <p class="text-gray-500 dark:text-gray-400">No SVG versions available</p>
{/if}
