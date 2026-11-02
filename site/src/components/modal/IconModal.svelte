<script lang="ts">
import { onMount } from "svelte"
import {
  selectedIcon,
  closeIconModal,
  latestVersion,
  getIconSvgUrl,
  getIconFallbackSvgUrl,
  getIconAllVariants,
  resolveSvgVersion,
  isDarkLogo,
} from "$lib/stores/iconStore"
import Modal from "./Modal.svelte"
import IconModalHeader from "./IconModalHeader.svelte"
import SyntaxCodeBlock from "../widgets/code/SyntaxCodeBlock.svelte"
import { copyToClipboard } from "$lib/common/copyToClipboard"
import type { IIcon, IntegrationTab } from "$lib/types/types"

type BgMode = "dark" | "light" | "checkerboard" | "transparent"
type PkgManager = "npm" | "pnpm" | "yarn" | "bun"

const previewSizes = [24, 32, 48, 64, 128] as const
type PreviewSize = (typeof previewSizes)[number]

let activeTab: IntegrationTab = "react"
let bgMode: BgMode = "dark"
let isColored = true
let activePkg: PkgManager = "npm"
let previewSize: PreviewSize = 64

const pkgCommands: Record<PkgManager, string> = {
  npm: "npm i react-devicons",
  pnpm: "pnpm add react-devicons",
  yarn: "yarn add react-devicons",
  bun: "bun add react-devicons",
}

let availableVariants: string[] = []
let selectedVersion = "original"
let currentIconName = ""

let rawSvgText = ""
let isLoadingSvg = false
let svgFetchError = false
let fetchToken = 0

let copiedFeedback: string | null = null
let feedbackTimeout: ReturnType<typeof setTimeout> | null = null

function triggerFeedback(msg: string) {
  copiedFeedback = msg
  if (feedbackTimeout) clearTimeout(feedbackTimeout)
  feedbackTimeout = setTimeout(() => {
    copiedFeedback = null
  }, 2000)
}

$: if ($selectedIcon) {
  if ($selectedIcon.name !== currentIconName) {
    currentIconName = $selectedIcon.name
    availableVariants = getIconAllVariants($selectedIcon)
    selectedVersion = availableVariants.includes("original")
      ? "original"
      : (availableVariants[0] ?? "plain")
  }
} else {
  currentIconName = ""
}

$: isDark = $selectedIcon ? isDarkLogo($selectedIcon) : false

function getIconUrl(icon: IIcon, version: string) {
  return getIconSvgUrl(icon, version, $latestVersion)
}

function getFallbackIconUrl(icon: IIcon, version: string) {
  return getIconFallbackSvgUrl(icon, version)
}

function handleImageError(e: Event, version: string) {
  if (!$selectedIcon) return
  const target = e.currentTarget as HTMLImageElement | null
  if (target) {
    const fallback = getFallbackIconUrl($selectedIcon, version)
    if (target.src !== fallback) {
      target.src = fallback
    }
  }
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

async function fetchRawSvg(icon: IIcon, version: string) {
  if (typeof window === "undefined" || !icon || !version) return
  const currentToken = ++fetchToken
  isLoadingSvg = true
  svgFetchError = false
  rawSvgText = ""

  try {
    const primaryUrl = getIconUrl(icon, version)
    let res = await fetch(primaryUrl)
    if (!res.ok) {
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
  } catch {
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
      // ignore
    }
    if (currentToken === fetchToken) {
      svgFetchError = true
      isLoadingSvg = false
    }
  }
}

$: if ($selectedIcon && selectedVersion) {
  fetchRawSvg($selectedIcon, selectedVersion)
}

$: formattedSvgText = formatSvg(rawSvgText)
$: currentSvgUrl = $selectedIcon
  ? getIconUrl($selectedIcon, selectedVersion)
  : ""
$: imgSnippet = `<img src="${currentSvgUrl}" alt="${$selectedIcon?.name ?? "icon"}" width="32" height="32" />`

function toPascalCase(str: string): string {
  if (!str) return ""
  return str
    .replace(/[^a-zA-Z0-9]+(.)/g, (_, chr) => chr.toUpperCase())
    .replace(/^[a-z]/, (chr) => chr.toUpperCase())
}

$: pascalName = $selectedIcon ? toPascalCase($selectedIcon.name) : ""
$: pascalVariant = toPascalCase(selectedVersion)
$: reactComponentName = `${pascalName}${pascalVariant}`

$: reactSnippet = `import { ${reactComponentName} } from "react-devicons/${$selectedIcon?.name}/${selectedVersion}";

export function HeaderIcon() {
  return <${reactComponentName} size={32} />;
}`

$: jsxComponentSnippet = `<${reactComponentName} size={32} />`
$: coloredSuffix = isColored ? " colored" : ""
$: fontClassSnippet = `<i class="devicon-${$selectedIcon?.name}-${selectedVersion}${coloredSuffix}"></i>`
$: cdnSnippet =
  '<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/devicon.min.css" />'

function downloadSvg() {
  const content = formattedSvgText || rawSvgText
  if (!content || !$selectedIcon || typeof window === "undefined") return
  const blob = new Blob([content], { type: "image/svg+xml;charset=utf-8" })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = `${$selectedIcon.name}-${selectedVersion}.svg`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  triggerFeedback("Downloaded SVG")
}

async function copySvgContent() {
  const content = formattedSvgText || rawSvgText
  if (!content) return
  await copyToClipboard(content)
  triggerFeedback("Copied SVG Markup")
}

async function copyJsxTag() {
  if (!jsxComponentSnippet) return
  await copyToClipboard(jsxComponentSnippet)
  triggerFeedback("Copied JSX Tag")
}

async function copyFontClass() {
  await copyToClipboard(fontClassSnippet)
  triggerFeedback("Copied Font Class")
}

async function copyIconName() {
  if (!$selectedIcon) return
  await copyToClipboard($selectedIcon.name)
  triggerFeedback("Copied Name")
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === "Escape") {
    closeIconModal()
    return
  }

  if (availableVariants.length > 1) {
    if (e.key === "ArrowLeft") {
      e.preventDefault()
      const idx = availableVariants.indexOf(selectedVersion)
      if (idx > 0) {
        selectedVersion = availableVariants[idx - 1]
      } else {
        selectedVersion = availableVariants[availableVariants.length - 1]
      }
    } else if (e.key === "ArrowRight") {
      e.preventDefault()
      const idx = availableVariants.indexOf(selectedVersion)
      if (idx >= 0 && idx < availableVariants.length - 1) {
        selectedVersion = availableVariants[idx + 1]
      } else {
        selectedVersion = availableVariants[0]
      }
    }
  }
}

onMount(() => {
  document.addEventListener("keydown", handleKeydown)
  return () => document.removeEventListener("keydown", handleKeydown)
})
</script>

<Modal isOpen={!!$selectedIcon} onClose={closeIconModal} title={$selectedIcon?.name}>
  {#if $selectedIcon}
    <!-- Header -->
    <IconModalHeader
      title={$selectedIcon.name}
      tags={$selectedIcon.tags || []}
      onClose={closeIconModal}
    />

    <!-- 2-Column Responsive Desktop Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- LEFT COLUMN: Preview & Customization (5 cols) -->
      <div class="lg:col-span-5 flex flex-col gap-3.5">
        <!-- Main Preview Box with 4 Background Surfaces -->
        <div class="relative flex flex-col items-center justify-center rounded-xl p-6 transition-all min-h-[200px] overflow-hidden {
          bgMode === 'dark' ? 'bg-[#11131a] border border-white/[0.08]' :
          bgMode === 'light' ? 'bg-white border border-slate-200' :
          bgMode === 'checkerboard' ? 'checkerboard border border-slate-200 dark:border-white/[0.08]' :
          'bg-transparent border border-dashed border-slate-200 dark:border-white/[0.12]'
        }">
          <!-- Scalable Vector / Image Container -->
          <div
            class="relative flex items-center justify-center transition-all {isColored ? '' : 'grayscale'}"
            style="width: {previewSize}px; height: {previewSize}px; max-width: 100%; max-height: 100%;"
          >
            {#if rawSvgText && !isLoadingSvg}
              <!-- Real Inline Vector SVG rendering -->
              <div class="flex items-center justify-center size-full [&>svg]:size-full [&>svg]:max-h-full [&>svg]:max-w-full [&>svg]:object-contain {isDark && bgMode === 'dark' ? 'brightness-0 invert' : ''}">
                {@html rawSvgText}
              </div>
            {:else if currentSvgUrl}
              <img
                src={currentSvgUrl}
                alt={`${$selectedIcon.name} (${selectedVersion})`}
                on:error={(e) => handleImageError(e, selectedVersion)}
                class="size-full object-contain transition-transform {isDark && bgMode === 'dark' ? 'brightness-0 invert' : ''}"
              />
            {/if}
          </div>

          <!-- Toast Feedback inside preview -->
          {#if copiedFeedback}
            <div class="absolute bottom-3 rounded-md bg-zinc-900/90 dark:bg-zinc-800/95 border border-white/10 px-2.5 py-1 text-xs font-medium text-emerald-400 shadow-md backdrop-blur-xs flex items-center gap-1.5">
              <svg class="size-3 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <span>{copiedFeedback}</span>
            </div>
          {/if}
        </div>

        <!-- Controls: Background switch, Size switch & Color toggle -->
        <div class="flex flex-col gap-2 rounded-lg border border-slate-200/80 bg-slate-50 p-2.5 dark:border-white/[0.06] dark:bg-[#11131a]">
          <!-- Top Row: Background Surfaces & Monochrome Toggle -->
          <div class="flex items-center justify-between gap-2">
            <!-- 4 Background Surfaces -->
            <div class="flex items-center gap-1 text-xs font-medium">
              <span class="mr-1 text-[11px] text-slate-500 dark:text-slate-400">Surface:</span>
              <button
                type="button"
                on:click={() => (bgMode = "dark")}
                class="size-5 rounded bg-[#11131a] border transition cursor-pointer {bgMode === 'dark' ? 'border-emerald-500 ring-1 ring-emerald-500/50' : 'border-white/20'}"
                title="Dark surface"
                aria-label="Dark Surface"
              ></button>
              <button
                type="button"
                on:click={() => (bgMode = "light")}
                class="size-5 rounded bg-white border transition cursor-pointer {bgMode === 'light' ? 'border-emerald-500 ring-1 ring-emerald-500/50' : 'border-slate-300'}"
                title="Light surface"
                aria-label="Light Surface"
              ></button>
              <button
                type="button"
                on:click={() => (bgMode = "checkerboard")}
                class="size-5 rounded checkerboard border transition cursor-pointer {bgMode === 'checkerboard' ? 'border-emerald-500 ring-1 ring-emerald-500/50' : 'border-slate-300 dark:border-white/20'}"
                title="Checkerboard surface"
                aria-label="Checkerboard Surface"
              ></button>
              <button
                type="button"
                on:click={() => (bgMode = "transparent")}
                class="flex size-5 items-center justify-center rounded border border-dashed transition cursor-pointer text-[10px] {bgMode === 'transparent' ? 'border-emerald-500 text-emerald-500 ring-1 ring-emerald-500/50' : 'border-slate-300 text-slate-400 dark:border-white/20'}"
                title="Transparent surface"
                aria-label="Transparent Surface"
              >
                ∅
              </button>
            </div>

            <!-- Colored vs Monochrome toggle -->
            <label class="flex items-center gap-1.5 text-xs font-medium text-slate-600 dark:text-slate-300 cursor-pointer select-none">
              <input
                type="checkbox"
                bind:checked={isColored}
                class="size-3.5 rounded border-slate-300 text-emerald-500 focus:ring-0 cursor-pointer"
              />
              <span>Colored</span>
            </label>
          </div>

          <!-- Bottom Row: Interactive Size Preview Buttons -->
          <div class="flex items-center justify-between border-t border-slate-200/60 pt-2 dark:border-white/[0.06]">
            <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400">Scale:</span>
            <div class="flex items-center gap-1">
              {#each previewSizes as size}
                <button
                  type="button"
                  on:click={() => (previewSize = size)}
                  class="rounded px-1.5 py-0.5 font-mono text-[10px] font-semibold transition cursor-pointer {previewSize === size
                    ? 'bg-slate-900 text-white dark:bg-white/15 dark:text-white'
                    : 'text-slate-500 hover:bg-slate-200 dark:text-slate-400 dark:hover:bg-white/5'}"
                  aria-label={`Preview at ${size}px`}
                >
                  {size}px
                </button>
              {/each}
            </div>
          </div>
        </div>

        <!-- Available Versions Thumbnail Selector -->
        <div>
          <div class="mb-1.5 flex items-center justify-between">
            <span class="text-[11px] font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              Variants ({availableVariants.length})
            </span>
            <span class="text-[10px] text-slate-400 dark:text-slate-500">
              <kbd class="px-1 py-0.2 rounded bg-slate-100 dark:bg-white/5 font-mono text-[9px]">←</kbd>
              <kbd class="px-1 py-0.2 rounded bg-slate-100 dark:bg-white/5 font-mono text-[9px]">→</kbd> cycle
            </span>
          </div>

          <div class="flex flex-wrap gap-1.5">
            {#each availableVariants as version}
              {@const isSelected = selectedVersion === version}
              <button
                type="button"
                on:click={() => (selectedVersion = version)}
                class="flex items-center gap-1.5 rounded-lg border px-2.5 py-1.5 text-xs transition-colors cursor-pointer {isSelected
                  ? 'border-emerald-500/60 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-medium'
                  : 'border-slate-200 bg-white hover:border-slate-300 dark:border-white/[0.06] dark:bg-[#11131a] dark:text-slate-300 dark:hover:border-white/15'}"
                aria-label={`Select ${version} version`}
              >
                <img
                  src={getIconUrl($selectedIcon, version)}
                  alt={version}
                  on:error={(e) => handleImageError(e, version)}
                  class="size-4 object-contain {isDark ? 'dark:brightness-0 dark:invert' : ''}"
                />
                <span class="text-[11px]">{version}</span>
              </button>
            {/each}
          </div>
        </div>

        <!-- Action Toolbar -->
        <div class="flex flex-col gap-1.5 pt-1">
          <!-- Primary Actions -->
          <div class="grid grid-cols-3 gap-1.5">
            <button
              type="button"
              on:click={downloadSvg}
              disabled={isLoadingSvg || (!formattedSvgText && !rawSvgText)}
              class="flex items-center justify-center gap-1.5 rounded-lg border border-slate-200 bg-white py-2 px-2 text-xs font-medium text-slate-700 shadow-xs transition hover:bg-slate-50 hover:border-slate-300 dark:border-white/[0.08] dark:bg-[#11131a] dark:text-slate-200 dark:hover:bg-[#181b24] cursor-pointer disabled:opacity-50"
              title="Download SVG file"
            >
              <svg class="size-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              <span class="truncate">Download SVG</span>
            </button>

            <button
              type="button"
              on:click={copySvgContent}
              disabled={isLoadingSvg || (!formattedSvgText && !rawSvgText)}
              class="flex items-center justify-center gap-1.5 rounded-lg border border-slate-200 bg-white py-2 px-2 text-xs font-medium text-slate-700 shadow-xs transition hover:bg-slate-50 hover:border-slate-300 dark:border-white/[0.08] dark:bg-[#11131a] dark:text-slate-200 dark:hover:bg-[#181b24] cursor-pointer disabled:opacity-50"
              title="Copy SVG markup"
            >
              <svg class="size-3.5 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
              </svg>
              <span class="truncate">Copy SVG</span>
            </button>

            <button
              type="button"
              on:click={copyFontClass}
              class="flex items-center justify-center gap-1.5 rounded-lg border border-slate-200 bg-white py-2 px-2 text-xs font-medium text-slate-700 shadow-xs transition hover:bg-slate-50 hover:border-slate-300 dark:border-white/[0.08] dark:bg-[#11131a] dark:text-slate-200 dark:hover:bg-[#181b24] cursor-pointer"
              title="Copy HTML font icon tag"
            >
              <svg class="size-3.5 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="4 7 4 4 20 4 20 7"/>
                <line x1="9" y1="20" x2="15" y2="20"/>
                <line x1="12" y1="4" x2="12" y2="20"/>
              </svg>
              <span class="truncate">Copy Class</span>
            </button>
          </div>

          <!-- Secondary Quick Actions -->
          <div class="grid grid-cols-2 gap-1.5">
            <button
              type="button"
              on:click={copyJsxTag}
              class="flex items-center justify-center gap-1.5 rounded-lg border border-slate-200 bg-white py-1.5 px-2 text-xs font-medium text-slate-600 transition hover:bg-slate-50 dark:border-white/[0.06] dark:bg-white/[0.02] dark:text-slate-400 dark:hover:bg-white/5 cursor-pointer"
              title="Copy JSX Component tag"
            >
              <svg class="size-3 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="16 18 22 12 16 6"/>
                <polyline points="8 6 2 12 8 18"/>
              </svg>
              <span class="truncate">Copy JSX Tag</span>
            </button>

            <button
              type="button"
              on:click={copyIconName}
              class="flex items-center justify-center gap-1.5 rounded-lg border border-slate-200 bg-white py-1.5 px-2 text-xs font-medium text-slate-600 transition hover:bg-slate-50 dark:border-white/[0.06] dark:bg-white/[0.02] dark:text-slate-400 dark:hover:bg-white/5 cursor-pointer"
              title="Copy icon identifier name"
            >
              <svg class="size-3 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <span class="truncate">Copy Name</span>
            </button>
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN: Code Integration Panel (7 cols) -->
      <div class="lg:col-span-7 flex flex-col gap-3">
        <!-- Integration Tabs (Segmented Control) -->
        <div class="flex items-center gap-1 rounded-lg border border-slate-200/80 bg-slate-100 p-0.5 dark:border-white/[0.06] dark:bg-[#11131a]">
          <button
            type="button"
            on:click={() => (activeTab = "react")}
            class="flex-1 rounded-md py-1.5 text-center text-xs font-medium transition-colors cursor-pointer {activeTab === 'react'
              ? 'bg-white text-slate-900 shadow-xs dark:bg-white/10 dark:text-white'
              : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'}"
          >
            React
          </button>
          <button
            type="button"
            on:click={() => (activeTab = "html")}
            class="flex-1 rounded-md py-1.5 text-center text-xs font-medium transition-colors cursor-pointer {activeTab === 'html'
              ? 'bg-white text-slate-900 shadow-xs dark:bg-white/10 dark:text-white'
              : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'}"
          >
            HTML / Webfont
          </button>
          <button
            type="button"
            on:click={() => (activeTab = "svg")}
            class="flex-1 rounded-md py-1.5 text-center text-xs font-medium transition-colors cursor-pointer {activeTab === 'svg'
              ? 'bg-white text-slate-900 shadow-xs dark:bg-white/10 dark:text-white'
              : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'}"
          >
            Pure SVG
          </button>
        </div>

        <!-- TAB CONTENT -->
        {#if activeTab === "react"}
          <!-- React Panel -->
          <div class="flex flex-col gap-2.5">
            <!-- Package Manager Selector -->
            <div class="flex items-center justify-between text-xs">
              <span class="font-medium text-slate-500 dark:text-slate-400 text-[11px]">Install:</span>
              <div class="flex items-center gap-1">
                {#each (["npm", "pnpm", "yarn", "bun"] as const) as pkg}
                  <button
                    type="button"
                    on:click={() => (activePkg = pkg)}
                    class="rounded px-1.5 py-0.5 font-mono text-[10px] font-semibold transition cursor-pointer {activePkg === pkg
                      ? 'bg-slate-900 text-white dark:bg-white/15 dark:text-white'
                      : 'text-slate-500 hover:bg-slate-200 dark:text-slate-400 dark:hover:bg-white/5'}"
                  >
                    {pkg}
                  </button>
                {/each}
              </div>
            </div>

            <!-- Install snippet -->
            <SyntaxCodeBlock
              language="bash"
              code={pkgCommands[activePkg]}
            />

            <!-- Component Import & Usage snippet -->
            <SyntaxCodeBlock
              title={`<${reactComponentName} />`}
              language="tsx"
              code={reactSnippet}
            />

            <!-- Package Documentation Link -->
            <div class="flex items-center justify-between rounded-lg bg-slate-50 px-3 py-2 text-xs dark:bg-white/[0.02] border border-slate-200/60 dark:border-white/[0.06]">
              <span class="text-slate-600 dark:text-slate-400 text-[11px]">
                Official package: <strong class="text-slate-800 dark:text-slate-200 font-mono">react-devicons</strong>
              </span>
              <a
                href="https://github.com/devicons/react-devicons"
                target="_blank"
                rel="noopener noreferrer"
                class="font-medium text-emerald-600 dark:text-emerald-400 hover:underline inline-flex items-center gap-1 text-[11px]"
              >
                <span>Docs</span>
                <span>→</span>
              </a>
            </div>
          </div>
        {:else if activeTab === "html"}
          <!-- HTML / Webfont Panel -->
          <div class="flex flex-col gap-2.5">
            <SyntaxCodeBlock
              title="1. Add CDN link to HTML <head>"
              language="html"
              code={cdnSnippet}
            />

            <SyntaxCodeBlock
              title="2. Insert Font Icon element"
              language="html"
              code={fontClassSnippet}
            />

            <div class="rounded-lg bg-slate-50 p-2.5 text-[11px] text-slate-500 dark:bg-white/[0.02] dark:text-slate-400 border border-slate-200/60 dark:border-white/[0.06] leading-relaxed">
              The <code class="font-mono text-emerald-600 dark:text-emerald-400">colored</code> class displays original multi-color styling. Remove it for monochrome color matching your CSS text color.
            </div>
          </div>
        {:else}
          <!-- Pure SVG Panel -->
          <div class="flex flex-col gap-2.5">
            {#if isLoadingSvg}
              <div class="flex items-center justify-center py-12 text-slate-400">
                <span class="text-xs">Loading SVG markup...</span>
              </div>
            {:else if svgFetchError}
              <div class="rounded-lg bg-red-50 p-3 text-xs text-red-600 dark:bg-red-500/10 dark:text-red-400">
                Failed to load raw SVG markup. You can download the SVG file directly using the button on the left.
              </div>
            {:else}
              <SyntaxCodeBlock
                title="Formatted Inline SVG"
                language="svg"
                code={formattedSvgText}
              />

              <SyntaxCodeBlock
                title="HTML <img> Tag"
                language="html"
                code={imgSnippet}
              />
            {/if}
          </div>
        {/if}
      </div>
    </div>
  {/if}
</Modal>
