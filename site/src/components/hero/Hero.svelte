<script lang="ts">
import { onMount } from "svelte"
import { icons, totalVersions, searchTerm, setSearchTerm } from "$lib/stores/iconStore"
import IconMarquee from "./IconMarquee.svelte"

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
      Icons for developers, developers, developers!
    </h1>

    <!-- Natural Project Statement with Store-derived Metrics -->
    <p class="mt-4 max-w-2xl text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed">
      Over {$icons.length > 0 ? $icons.length : 660}+ technology icons and {$totalVersions > 0 ? $totalVersions.toLocaleString() : "2,100"}+ SVG variants for modern software engineering. Free and open source under MIT.
    </p>

    <!-- Steve Ballmer Featured Window Frame -->
    <div class="mt-6 flex flex-col items-center">
      <div class="group relative w-72 sm:w-80 md:w-96 overflow-hidden rounded-xl border border-slate-200/80 bg-white shadow-lg transition-all duration-200 hover:border-slate-300 dark:border-white/10 dark:bg-[#11131a] dark:shadow-2xl dark:hover:border-white/20">
        <!-- Window Titlebar -->
        <div class="flex items-center justify-between border-b border-slate-200/80 px-3 py-1.5 bg-slate-50/80 dark:border-white/[0.06] dark:bg-white/[0.02]">
          <div class="flex items-center gap-1.5">
            <span class="size-2.5 rounded-full bg-red-400/80 dark:bg-red-500/70"></span>
            <span class="size-2.5 rounded-full bg-amber-400/80 dark:bg-amber-500/70"></span>
            <span class="size-2.5 rounded-full bg-emerald-400/80 dark:bg-emerald-500/70"></span>
          </div>
          <div class="flex items-center gap-1.5 text-[11px] font-mono text-slate-500 dark:text-slate-400">
            <span class="size-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>ballmer.gif</span>
          </div>
          <span class="text-[10px] font-mono text-slate-400 dark:text-slate-500">DEV DAYS</span>
        </div>

        <!-- Media Screen (Exact 4:3 aspect ratio matching 480x360 source) -->
        <div class="relative aspect-[4/3] w-full overflow-hidden bg-black">
          <img
            src="/steve.gif"
            alt="Steve Ballmer chanting developers, developers, developers"
            class="size-full object-cover transition-transform duration-300 group-hover:scale-[1.01]"
            width="480"
            height="360"
            loading="eager"
          />
          <!-- Subtle edge highlight -->
          <div class="pointer-events-none absolute inset-0 ring-1 ring-inset ring-black/5 dark:ring-white/5"></div>
        </div>
      </div>
    </div>

    <!-- Linear-style Search Bar -->
    <div class="mt-8 w-full max-w-2xl">
      <div class="relative group">
        <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4 text-slate-400 dark:text-slate-500">
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
          class="w-full rounded-xl border border-slate-200 bg-white py-3.5 pr-24 pl-11 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-slate-400 dark:border-white/10 dark:bg-white/[0.02] dark:text-white dark:placeholder:text-slate-500 dark:hover:border-white/20 dark:focus:border-white/30"
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
