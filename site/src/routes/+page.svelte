<script lang="ts">
import { onMount } from "svelte"
import Hero from "../components/hero/Hero.svelte"
import FiltersBar from "../components/filters/FiltersBar.svelte"
import IconGrid from "../components/iconGrid/IconGrid.svelte"
import IntegrationsSection from "../components/integrations/IntegrationsSection.svelte"
import IconModal from "../components/modal/IconModal.svelte"
import {
  fetchIconsData,
  filteredIcons,
  isModalOpen,
  error,
} from "$lib/stores/iconStore"

let showBackToTop = false

function handleScroll() {
  if (typeof window !== "undefined") {
    showBackToTop = window.scrollY > 500
  }
}

function scrollToTop() {
  if (typeof window !== "undefined") {
    window.scrollTo({ top: 0, behavior: "smooth" })
  }
}

onMount(() => {
  fetchIconsData()
  window.addEventListener("scroll", handleScroll, { passive: true })

  if (typeof window !== "undefined" && window.location.hash) {
    const targetId = window.location.hash.replace(/^#/, "")
    const targetEl = document.getElementById(targetId)
    if (targetEl) {
      targetEl.scrollIntoView({ behavior: "smooth", block: "start" })
    }
    window.history.replaceState(null, "", window.location.pathname + window.location.search)
  }

  return () => window.removeEventListener("scroll", handleScroll)
})
</script>

<svelte:head>
  <title>DEVICON | All programming languages and development tools related icons font</title>
  <meta
    name="description"
    content="Devicon is a set of icons representing programming languages, designing & development tools. Explore, search, copy SVGs and integrate with React or Webfont."
  />
</svelte:head>

<main class="w-full">
  <!-- Hero Section & Animated Marquee -->
  <Hero />

  <!-- Icon Explorer & Grid Container -->
  <div id="icons" class="base-container py-6 scroll-mt-14">
    {#if $error}
      <div class="my-6 rounded-xl border border-red-200 bg-red-50 p-4 dark:border-red-500/20 dark:bg-red-500/10">
        <div class="flex items-center justify-between">
          <p class="text-xs sm:text-sm font-medium text-red-700 dark:text-red-300">
            Failed to load icon library: {$error}
          </p>
          <button
            type="button"
            on:click={() => fetchIconsData()}
            class="rounded-lg bg-red-600 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-red-700 cursor-pointer"
          >
            Retry
          </button>
        </div>
      </div>
    {/if}

    <FiltersBar />
    <IconGrid icons={$filteredIcons} />
  </div>

  <!-- Framework Integrations Section & CDN -->
  <IntegrationsSection />

  <!-- Icon Details & Code Modal -->
  {#if $isModalOpen}
    <IconModal />
  {/if}

  <!-- Floating Back to Top Button -->
  {#if showBackToTop}
    <button
      type="button"
      on:click={scrollToTop}
      class="fixed bottom-6 right-6 z-30 flex size-10 items-center justify-center rounded-full border border-slate-200/80 bg-white text-slate-700 shadow-md transition-all duration-150 hover:border-slate-300 hover:bg-slate-50 dark:border-white/10 dark:bg-[#181b24] dark:text-slate-200 dark:hover:border-white/20 dark:hover:bg-[#222634] focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:ring-offset-2 dark:focus:ring-offset-[#09090b] cursor-pointer"
      aria-label="Scroll back to top"
      title="Scroll to top"
    >
      <svg class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="18 15 12 9 6 15"/>
      </svg>
    </button>
  {/if}
</main>
