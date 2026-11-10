<script lang="ts">
import {
  latestVersion,
  setSearchTerm,
  getIconSvgUrl,
  getIconFallbackSvgUrl,
  isDarkLogo,
  isWhiteLogo,
  icons,
} from "$lib/stores/iconStore"
import type { IIcon, IconVersions } from "$lib/types/types"

interface MosaicItem {
  name: string
  label: string
  version: IconVersions | string
  hiddenMobile?: boolean
  isCenter?: boolean
}

// 21 items in a 7x3 grid:
// Row 1 (7 items): indices 0 & 6 hidden on mobile -> 5 items
// Row 2 (7 items): indices 7 & 13 hidden on mobile -> 5 items (center is index 10, Devicon)
// Row 3 (7 items): indices 14 & 20 hidden on mobile -> 5 items
const mosaicItems: MosaicItem[] = [
  // Row 1
  { name: "python", label: "Python", version: "plain", hiddenMobile: true },
  { name: "typescript", label: "TypeScript", version: "plain" },
  { name: "react", label: "React", version: "original" },
  { name: "rust", label: "Rust", version: "original" },
  { name: "go", label: "Go", version: "original-wordmark" },
  { name: "docker", label: "Docker", version: "plain" },
  { name: "kubernetes", label: "Kubernetes", version: "plain", hiddenMobile: true },

  // Row 2
  { name: "svelte", label: "Svelte", version: "plain", hiddenMobile: true },
  { name: "vuejs", label: "Vue.js", version: "plain" },
  { name: "postgresql", label: "PostgreSQL", version: "plain" },
  { name: "devicon", label: "Devicon", version: "original", isCenter: true },
  { name: "mongodb", label: "MongoDB", version: "plain" },
  { name: "nodejs", label: "Node.js", version: "plain" },
  { name: "nextjs", label: "Next.js", version: "original-wordmark", hiddenMobile: true },

  // Row 3
  { name: "cplusplus", label: "C++", version: "plain", hiddenMobile: true },
  { name: "git", label: "Git", version: "plain" },
  { name: "linux", label: "Linux", version: "plain" },
  { name: "redis", label: "Redis", version: "plain" },
  { name: "tailwindcss", label: "Tailwind CSS", version: "original" },
  { name: "java", label: "Java", version: "plain" },
  { name: "amazonwebservices", label: "AWS", version: "plain-wordmark", hiddenMobile: true },
]

function getIcon(name: string, fallbackVersion: IconVersions | string): IIcon {
  const found = $icons.find((i) => i.name === name)
  if (found) return found
  return {
    name,
    versions: { svg: [fallbackVersion as IconVersions], font: [] },
  } as unknown as IIcon
}

function handleImageError(e: Event, icon: IIcon, version: IconVersions | string) {
  const target = e.currentTarget as HTMLImageElement | null
  if (target) {
    const fallback = getIconFallbackSvgUrl(icon, version, target.src)
    if (target.src !== fallback && !target.src.endsWith(fallback)) {
      target.src = fallback
    }
  }
}

function handleTechClick(techName: string) {
  if (techName === "devicon") {
    setSearchTerm("")
  } else {
    setSearchTerm(techName)
  }
  const iconsSection = document.getElementById("icons")
  if (iconsSection) {
    iconsSection.scrollIntoView({ behavior: "smooth" })
  }
}
</script>

<div class="relative w-full max-w-2xl sm:max-w-3xl overflow-hidden rounded-2xl border border-slate-200/80 bg-white/50 p-3 sm:p-5 shadow-xs backdrop-blur-xs dark:border-white/[0.08] dark:bg-[#11131a]/60 dark:shadow-2xl">
  <!-- Top emerald accent line -->
  <div class="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-emerald-500/40 to-transparent"></div>
  <!-- Header Bar -->
  <div class="mb-3 flex items-center justify-between border-b border-slate-200/60 pb-2.5 text-[11px] font-mono text-slate-500 dark:border-white/[0.05] dark:text-slate-400">
    <div class="flex items-center gap-1.5">
      <span class="size-2 rounded-full bg-emerald-500"></span>
      <span class="font-semibold tracking-wider text-slate-700 uppercase dark:text-slate-300">Technology Mosaic</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-emerald-600 dark:text-emerald-400">v{$latestVersion}</span>
      <span>•</span>
      <span>{$icons.length > 0 ? $icons.length.toLocaleString() : "660"} ICONS</span>
    </div>
  </div>

  <!-- Mosaic Grid (5 cols mobile, 7 cols desktop) -->
  <div class="grid grid-cols-5 gap-2 sm:grid-cols-7 sm:gap-2.5">
    {#each mosaicItems as item (item.name)}
      {#if item.isCenter}
        <!-- Devicon Centerpiece Shield Mark -->
        <button
          type="button"
          on:click={() => handleTechClick("devicon")}
          class="group relative flex aspect-square flex-col items-center justify-center rounded-xl border-2 border-emerald-500/50 bg-gradient-to-br from-emerald-500/20 via-emerald-500/10 to-transparent p-2 shadow-md shadow-emerald-500/10 transition-transform duration-150 hover:scale-105 hover:border-emerald-500 hover:shadow-emerald-500/25 cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 sm:rounded-2xl sm:p-2.5"
          title="Devicon - Click to view all icons"
          aria-label="Devicon library centerpiece"
        >
          <div class="pointer-events-none absolute inset-0 bg-radial from-emerald-500/20 via-transparent to-transparent opacity-80"></div>
          <svg
            class="size-8 object-contain drop-shadow-xs transition-transform duration-200 group-hover:scale-110 sm:size-9 md:size-10"
            viewBox="0 0 128 128"
            aria-hidden="true"
          >
            <path fill="#558d6c" d="M4.92 8l10.17 87.05L64 119.95V8H4.92z"/>
            <path fill="#5aa579" d="M64 8v111.95l.05.05 48.93-24.91L123.08 8H64z"/>
            <path fill="#60be86" d="M18.84 22.11l6.49 65.18L64 105.97V22.11H18.84z"/>
            <path fill="#65d693" d="M64 22.11v83.86l.05.05 38.69-18.76 6.42-65.15H64z"/>
            <path fill="#5aa579" d="M105.72 54.9L73.14 39.42l-1.83-.9-1.12 2.28L64 53.41V68.3l9.15-18.08 21.5 9.57-23.09 10.37-.87.47v10.88L73 80.38l32.78-15.69a2 2 0 00.92-2v-5.78a2 2 0 00-.98-2.01z"/>
            <path fill="#558d6c" d="M56 69.39l-21.79-9.6 23.3-10.37 1.76-.7V37.76l-3.4 1.44-33.93 15.69a2.26 2.26 0 00-1.28 2v5.77a2.22 2.22 0 001.24 2l33.44 15.52 2 .9 1.21-2.26L64 68.3V53.41z"/>
          </svg>
          <span class="mt-1 text-[9px] font-mono font-bold tracking-wider text-emerald-600 uppercase dark:text-emerald-400 sm:text-[10px]">
            DEVICON
          </span>
        </button>
      {:else}
        {@const iconObj = getIcon(item.name, item.version)}
        {@const isDark = isDarkLogo(iconObj)}
        {@const isWhite = isWhiteLogo(iconObj)}
        <button
          type="button"
          on:click={() => handleTechClick(item.name)}
          class="{item.hiddenMobile ? 'hidden sm:flex' : 'flex'} group relative aspect-square flex-col items-center justify-center rounded-xl border border-slate-200/80 bg-white/70 p-2 shadow-2xs transition-all duration-150 hover:-translate-y-0.5 hover:border-emerald-500/40 hover:bg-emerald-500/5 hover:shadow-xs dark:border-white/[0.06] dark:bg-white/[0.025] dark:hover:border-emerald-500/40 dark:hover:bg-emerald-500/10 cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/50 sm:rounded-2xl sm:p-2.5"
          title={`Filter icons for ${item.label}`}
          aria-label={`Search for ${item.label} icons`}
        >
          <img
            src={getIconSvgUrl(iconObj, item.version, $latestVersion)}
            alt={`${item.label} icon`}
            loading="eager"
            width="32"
            height="32"
            on:error={(e) => handleImageError(e, iconObj, item.version)}
            class="size-6 object-contain transition-transform duration-150 group-hover:scale-110 sm:size-7 md:size-8 {isDark ? 'dark:invert' : ''} {isWhite ? 'invert dark:filter-none' : ''}"
          />
          <span class="mt-1 max-w-full truncate text-[10px] font-medium text-slate-500 group-hover:text-slate-900 dark:text-slate-400 dark:group-hover:text-white">
            {item.label}
          </span>
        </button>
      {/if}
    {/each}
  </div>
</div>
