<script lang="ts">
import { latestVersion } from "$lib/stores/iconStore"
import { scrollToSection } from "$lib/common/navigation"
import ThemeToggle from "./ThemeToggle.svelte"

let isMobileMenuOpen = false

function toggleMobileMenu() {
  isMobileMenuOpen = !isMobileMenuOpen
}

function closeMobileMenu() {
  isMobileMenuOpen = false
}
</script>

<header class="sticky top-0 z-40 w-full border-b border-slate-200/80 bg-white/80 backdrop-blur-md transition-colors dark:border-white/[0.07] dark:bg-[#09090b]/80">
  <div class="base-container flex h-14 items-center justify-between">
    <!-- Brand / Logo -->
    <a
      href="/"
      class="group flex items-center gap-2.5 transition focus:outline-none"
      aria-label="Devicon Home"
    >
      <div class="flex size-7 items-center justify-center rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 transition group-hover:bg-emerald-500/20">
        <i class="devicon-devicon-plain colored text-base"></i>
      </div>
      <div class="flex items-baseline gap-2">
        <span class="text-slate-900 dark:text-white font-semibold tracking-tight text-lg">
          Devicon
        </span>
        <span class="text-slate-500 font-mono text-xs">
          v{$latestVersion}
        </span>
      </div>
    </a>

    <!-- Desktop Navigation Links -->
    <nav class="hidden md:flex items-center gap-1 font-medium text-xs sm:text-sm text-slate-600 dark:text-slate-400" aria-label="Main Navigation">
      <a
        href="#icons"
        on:click={(e) => scrollToSection("icons", e)}
        class="rounded-md px-3 py-1.5 transition hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 cursor-pointer"
      >
        Icons
      </a>
      <a
        href="#integrations"
        on:click={(e) => scrollToSection("integrations", e)}
        class="rounded-md px-3 py-1.5 transition hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 cursor-pointer"
      >
        Integrations
      </a>
      <a
        href="#cdn"
        on:click={(e) => scrollToSection("cdn", e)}
        class="rounded-md px-3 py-1.5 transition hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/5 cursor-pointer"
      >
        CDN
      </a>
    </nav>

    <!-- Desktop Actions -->
    <div class="hidden md:flex items-center gap-2">
      <!-- GitHub Link -->
      <a
        href="https://github.com/devicons/devicon"
        target="_blank"
        rel="noopener noreferrer"
        class="flex items-center gap-1.5 rounded-lg border border-slate-200/80 bg-white px-2.5 py-1.5 text-xs font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50 dark:border-white/[0.07] dark:bg-white/[0.03] dark:text-slate-300 dark:hover:border-white/15 dark:hover:bg-white/[0.06] dark:hover:text-white"
        aria-label="Devicon on GitHub"
      >
        <svg class="size-3.5" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
          <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
        </svg>
        <span>GitHub</span>
      </a>

      <!-- Discord Link -->
      <a
        href="https://discord.com/invite/hScy8KWACQ"
        target="_blank"
        rel="noopener noreferrer"
        class="flex items-center gap-1.5 rounded-lg border border-slate-200/80 bg-white px-2.5 py-1.5 text-xs font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50 dark:border-white/[0.07] dark:bg-white/[0.03] dark:text-slate-300 dark:hover:border-white/15 dark:hover:bg-white/[0.06] dark:hover:text-white"
        aria-label="Join Devicon Discord Community"
      >
        <svg class="size-3.5" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
          <path d="M13.545 2.907a13.2 13.2 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.2 12.2 0 0 0-3.658 0 8 8 0 0 0-.412-.833.05.05 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.04.04 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032q.003.022.021.037a13.3 13.3 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019q.463-.63.818-1.329a.05.05 0 0 0-.01-.059l-.018-.011a9 9 0 0 1-1.248-.595.05.05 0 0 1-.02-.066l.015-.019q.127-.095.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.05.05 0 0 1 .053.007q.121.1.248.195a.05.05 0 0 1-.004.085 8 8 0 0 1-1.249.594.05.05 0 0 0-.03.03.05.05 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.2 13.2 0 0 0 4.001-2.02.05.05 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.03.03 0 0 0-.02-.019m-8.198 7.307c-.789 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612m5.316 0c-.788 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612"/>
        </svg>
        <span>Discord</span>
      </a>

      <!-- Theme Toggle -->
      <ThemeToggle />
    </div>

    <!-- Mobile Actions (Theme + Hamburger) -->
    <div class="flex items-center gap-1.5 md:hidden">
      <ThemeToggle />

      <button
        type="button"
        on:click={toggleMobileMenu}
        class="flex size-8 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-700 transition dark:border-white/[0.07] dark:bg-white/[0.03] dark:text-slate-300 cursor-pointer"
        aria-label="Toggle navigation menu"
        aria-expanded={isMobileMenuOpen}
      >
        {#if isMobileMenuOpen}
          <svg class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        {:else}
          <svg class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        {/if}
      </button>
    </div>
  </div>

  <!-- Mobile Drawer / Dropdown -->
  {#if isMobileMenuOpen}
    <div class="border-b border-slate-200 bg-white/95 px-4 py-4 backdrop-blur-lg dark:border-white/[0.07] dark:bg-[#09090b]/95 md:hidden">
      <nav class="flex flex-col gap-1 font-medium text-sm text-slate-700 dark:text-slate-200">
        <a
          href="#icons"
          on:click={(e) => {
            closeMobileMenu()
            scrollToSection("icons", e)
          }}
          class="rounded-lg px-3 py-2 transition hover:bg-slate-100 dark:hover:bg-white/5 cursor-pointer"
        >
          Icons
        </a>
        <a
          href="#integrations"
          on:click={(e) => {
            closeMobileMenu()
            scrollToSection("integrations", e)
          }}
          class="rounded-lg px-3 py-2 transition hover:bg-slate-100 dark:hover:bg-white/5 cursor-pointer"
        >
          Integrations
        </a>
        <a
          href="#cdn"
          on:click={(e) => {
            closeMobileMenu()
            scrollToSection("cdn", e)
          }}
          class="rounded-lg px-3 py-2 transition hover:bg-slate-100 dark:hover:bg-white/5 cursor-pointer"
        >
          CDN
        </a>
        <div class="my-2 border-t border-slate-200 dark:border-white/[0.07]"></div>
        <div class="flex flex-col gap-1">
          <a
            href="https://github.com/devicons/devicon"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-white/5"
          >
            <svg class="size-4" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            <span>GitHub Repository</span>
          </a>
          <a
            href="https://discord.com/invite/hScy8KWACQ"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-white/5"
          >
            <svg class="size-4" viewBox="0 0 16 16" fill="currentColor">
              <path d="M13.545 2.907a13.2 13.2 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.2 12.2 0 0 0-3.658 0 8 8 0 0 0-.412-.833.05.05 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.04.04 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032q.003.022.021.037a13.3 13.3 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019q.463-.63.818-1.329a.05.05 0 0 0-.01-.059l-.018-.011a9 9 0 0 1-1.248-.595.05.05 0 0 1-.02-.066l.015-.019q.127-.095.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.05.05 0 0 1 .053.007q.121.1.248.195a.05.05 0 0 1-.004.085 8 8 0 0 1-1.249.594.05.05 0 0 0-.03.03.05.05 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.2 13.2 0 0 0 4.001-2.02.05.05 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.03.03 0 0 0-.02-.019m-8.198 7.307c-.789 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612m5.316 0c-.788 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612"/>
            </svg>
            <span>Discord Community</span>
          </a>
        </div>
      </nav>
    </div>
  {/if}
</header>
