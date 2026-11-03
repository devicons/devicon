<script lang="ts">
import { onMount } from "svelte"
import { icons, totalVersions, searchTerm, setSearchTerm } from "$lib/stores/iconStore"
import IconMarquee from "./IconMarquee.svelte"
import HeroMosaic from "./HeroMosaic.svelte"

let searchInputEl: HTMLInputElement | null = null

function handleGlobalKeyDown(e: KeyboardEvent) {
  if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
    return
  }
  if (e.key === "/" || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k")) {
    e.preventDefault()
    focusAndScrollSearch()
  }
}

function focusAndScrollSearch() {
  if (searchInputEl) {
    searchInputEl.focus()
  }
  const iconsSection = document.getElementById("icons")
  if (iconsSection) {
    iconsSection.scrollIntoView({ behavior: "smooth" })
  }
}

function handleInput(e: Event) {
  const val = (e.target as HTMLInputElement).value
  setSearchTerm(val)
  const iconsSection = document.getElementById("icons")
  if (iconsSection && window.scrollY < iconsSection.offsetTop - 250) {
    iconsSection.scrollIntoView({ behavior: "smooth" })
  }
}

onMount(() => {
  window.addEventListener("keydown", handleGlobalKeyDown)
  return () => window.removeEventListener("keydown", handleGlobalKeyDown)
})
</script>

<section class="relative pt-12 pb-6 md:pt-20 md:pb-8">
  <div class="base-container flex flex-col items-center text-center">
    <!-- Headline -->
    <h1 class="max-w-4xl text-4xl sm:text-6xl md:text-7xl font-bold tracking-[-0.045em] leading-[1.08] text-slate-900 dark:text-white">
      Icons for <span class="text-emerald-500 dark:text-emerald-400">developers</span>, developers, developers!
    </h1>

    <!-- Natural Project Statement with Store-derived Metrics -->
    <p class="mt-4 max-w-2xl text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed">
      {$icons.length > 0 ? $icons.length.toLocaleString() : "660"} technology icons and {$totalVersions > 0 ? $totalVersions.toLocaleString() : "2,100"} SVG variants for modern software engineering. Free and open source under MIT.
    </p>

    <!-- Devicon Technology Mosaic -->
    <div class="mt-6 sm:mt-8 w-full flex justify-center">
      <HeroMosaic />
    </div>

    <!-- Linear-style Search Bar with Emerald Focus -->
    <div class="mt-8 w-full max-w-2xl">
      <div class="relative group">
        <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4 text-slate-400 transition-colors group-focus-within:text-emerald-500 dark:text-slate-500">
          <svg class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
          </svg>
        </div>

        <input
          bind:this={searchInputEl}
          type="text"
          value={$searchTerm}
          on:input={handleInput}
          placeholder="Search languages, frameworks, databases, tools..."
          class="w-full rounded-xl border border-slate-200 bg-white py-3.5 pr-24 pl-11 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 dark:border-white/10 dark:bg-white/[0.02] dark:text-white dark:placeholder:text-slate-500 dark:hover:border-white/20 dark:focus:border-emerald-500/60 dark:focus:ring-emerald-500/20"
        />

        <div class="absolute inset-y-0 right-0 flex items-center pr-3 gap-1.5">
          <button
            type="button"
            on:click={focusAndScrollSearch}
            class="hidden sm:inline-flex items-center rounded border border-slate-200/80 bg-slate-100 px-1.5 py-0.5 text-[10px] font-mono font-medium text-slate-500 transition hover:bg-slate-200 hover:text-slate-700 dark:border-white/10 dark:bg-white/5 dark:text-slate-400 dark:hover:bg-white/10 cursor-pointer"
            title="Press ⌘K or click to focus"
          >
            ⌘K
          </button>
          <button
            type="button"
            on:click={focusAndScrollSearch}
            class="inline-flex items-center rounded border border-slate-200/80 bg-slate-100 px-1.5 py-0.5 text-[10px] font-mono font-medium text-slate-500 transition hover:bg-slate-200 hover:text-slate-700 dark:border-white/10 dark:bg-white/5 dark:text-slate-400 dark:hover:bg-white/10 cursor-pointer"
            title="Press / or click to focus"
          >
            /
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Unobtrusive Technology Ribbon -->
  <div class="mt-10">
    <IconMarquee />
  </div>
</section>
