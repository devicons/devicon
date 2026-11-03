<script lang="ts">
import { latestVersion } from "$lib/stores/iconStore"
import { scrollToSection } from "$lib/common/navigation"
</script>

<footer class="relative border-t border-slate-200/80 bg-white py-14 text-slate-600 transition-colors dark:border-white/[0.07] dark:bg-[#09090b] dark:text-slate-400">
  <!-- Subtle emerald top accent line -->
  <div class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-emerald-500/40 to-transparent"></div>

  <div class="base-container flex flex-col gap-10">
    <!-- Main 3-column Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-8">
      <!-- Col 1: Brand & Info (4 cols) -->
      <div class="lg:col-span-4 flex flex-col gap-3">
        <div class="flex items-center gap-2.5">
          <div class="flex size-7.5 items-center justify-center rounded-lg bg-emerald-500/10 border border-emerald-500/20 p-1">
            <svg class="size-full" viewBox="0 0 128 128" aria-hidden="true">
              <path fill="#558d6c" d="M4.92 8l10.17 87.05L64 119.95V8H4.92z"/>
              <path fill="#5aa579" d="M64 8v111.95l.05.05 48.93-24.91L123.08 8H64z"/>
              <path fill="#60be86" d="M18.84 22.11l6.49 65.18L64 105.97V22.11H18.84z"/>
              <path fill="#65d693" d="M64 22.11v83.86l.05.05 38.69-18.76 6.42-65.15H64z"/>
              <path fill="#5aa579" d="M105.72 54.9L73.14 39.42l-1.83-.9-1.12 2.28L64 53.41V68.3l9.15-18.08 21.5 9.57-23.09 10.37-.87.47v10.88L73 80.38l32.78-15.69a2 2 0 00.92-2v-5.78a2 2 0 00-.98-2.01z"/>
              <path fill="#558d6c" d="M56 69.39l-21.79-9.6 23.3-10.37 1.76-.7V37.76l-3.4 1.44-33.93 15.69a2.26 2.26 0 00-1.28 2v5.77a2.22 2.22 0 001.24 2l33.44 15.52 2 .9 1.21-2.26L64 68.3V53.41z"/>
            </svg>
          </div>
          <span class="text-slate-900 dark:text-white font-semibold tracking-tight text-lg">
            Devicon
          </span>
          <span class="inline-flex items-center rounded-full bg-emerald-500/10 px-2 py-0.5 text-[11px] font-mono font-medium text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
            v{$latestVersion}
          </span>
        </div>

        <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed max-w-sm">
          An open-source collection of developer icons for programming languages, frameworks, cloud services, and software tools.
        </p>

        <!-- Community Badges -->
        <div class="flex flex-wrap items-center gap-2 pt-2">
          <a
            href="https://github.com/devicons/devicon"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200/80 bg-slate-50/60 px-2.5 py-1 text-xs font-medium text-slate-700 transition hover:border-emerald-500/40 hover:bg-emerald-500/5 hover:text-emerald-600 dark:border-white/[0.08] dark:bg-white/[0.03] dark:text-slate-300 dark:hover:border-emerald-500/40 dark:hover:bg-emerald-500/10 dark:hover:text-emerald-400"
            aria-label="GitHub Repository"
          >
            <svg class="size-3.5" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            <span>GitHub</span>
          </a>
          <a
            href="https://discord.com/invite/hScy8KWACQ"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200/80 bg-slate-50/60 px-2.5 py-1 text-xs font-medium text-slate-700 transition hover:border-emerald-500/40 hover:bg-emerald-500/5 hover:text-emerald-600 dark:border-white/[0.08] dark:bg-white/[0.03] dark:text-slate-300 dark:hover:border-emerald-500/40 dark:hover:bg-emerald-500/10 dark:hover:text-emerald-400"
            aria-label="Discord Community"
          >
            <svg class="size-3.5" viewBox="0 0 16 16" fill="currentColor">
              <path d="M13.545 2.907a13.2 13.2 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.2 12.2 0 0 0-3.658 0 8 8 0 0 0-.412-.833.05.05 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.04.04 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032q.003.022.021.037a13.3 13.3 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019q.463-.63.818-1.329a.05.05 0 0 0-.01-.059l-.018-.011a9 9 0 0 1-1.248-.595.05.05 0 0 1-.02-.066l.015-.019q.127-.095.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.05.05 0 0 1 .053.007q.121.1.248.195a.05.05 0 0 1-.004.085 8 8 0 0 1-1.249.594.05.05 0 0 0-.03.03.05.05 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.2 13.2 0 0 0 4.001-2.02.05.05 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.03.03 0 0 0-.02-.019m-8.198 7.307c-.789 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612m5.316 0c-.788 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612"/>
            </svg>
            <span>Discord</span>
          </a>
        </div>
      </div>

      <!-- Col 2: Navigation & Links (3 cols) -->
      <div class="lg:col-span-3 flex flex-col gap-2.5">
        <h4 class="text-xs font-semibold uppercase tracking-wider text-slate-900 dark:text-white">
          Resources
        </h4>
        <ul class="flex flex-col gap-1.5 text-xs">
          <li>
            <a
              href="#icons"
              on:click={(e) => scrollToSection("icons", e)}
              class="transition hover:text-emerald-600 dark:hover:text-emerald-400 cursor-pointer"
            >
              Icon Catalog
            </a>
          </li>
          <li>
            <a
              href="#integrations"
              on:click={(e) => scrollToSection("integrations", e)}
              class="transition hover:text-emerald-600 dark:hover:text-emerald-400 cursor-pointer"
            >
              React Library
            </a>
          </li>
          <li>
            <a
              href="#cdn"
              on:click={(e) => scrollToSection("cdn", e)}
              class="transition hover:text-emerald-600 dark:hover:text-emerald-400 cursor-pointer"
            >
              CDN & Webfont
            </a>
          </li>
          <li>
            <a href="https://github.com/devicons/devicon" target="_blank" rel="noopener noreferrer" class="transition hover:text-emerald-600 dark:hover:text-emerald-400">GitHub Project</a>
          </li>
          <li>
            <a href="https://discord.com/invite/hScy8KWACQ" target="_blank" rel="noopener noreferrer" class="transition hover:text-emerald-600 dark:hover:text-emerald-400">Discord Community</a>
          </li>
        </ul>
      </div>

      <!-- Col 3: Contributors (5 cols) -->
      <div class="lg:col-span-5 flex flex-col gap-2.5">
        <h4 class="text-xs font-semibold uppercase tracking-wider text-slate-900 dark:text-white">
          Contributors
        </h4>
        <p class="text-xs text-slate-500 dark:text-slate-400">
          Devicon is built and maintained by hundreds of open-source contributors across the globe.
        </p>
        <a
          href="https://github.com/devicons/devicon/graphs/contributors"
          target="_blank"
          rel="noopener noreferrer"
          class="transition opacity-85 hover:opacity-100"
        >
          <img
            src="https://contrib.rocks/image?repo=devicons/devicon"
            alt="Devicon Contributors"
            loading="lazy"
            class="max-w-full h-auto rounded"
          />
        </a>
        <p class="text-[11px] text-slate-400 dark:text-slate-500">
          Contributor graph via <a href="https://contrib.rocks" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600 dark:hover:text-slate-300">contrib.rocks</a>.
        </p>
      </div>
    </div>

    <!-- Legal, Credits, & Attributions Section -->
    <div class="border-t border-slate-200/60 pt-6 dark:border-white/[0.06] flex flex-col gap-3 text-xs leading-relaxed text-slate-500 dark:text-slate-400">
      <p>
        All product names, logos, and brands are property of their respective owners. All company,
        product and service names used in this website are for identification purposes only. Usage of
        these names, logos, and brands does not imply endorsement of Devicon or its members. All
        icons/SVGs in this project are not monetized in any way. It is up to the user to use the logo
        properly according to the company/group's brand policy.
      </p>

      <div class="flex flex-wrap items-center justify-between gap-2 pt-2 text-[11px] text-slate-400 dark:text-slate-500">
        <p>
          Originally created by <a href="https://github.com/konpa" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600 dark:hover:text-slate-300">Konpa</a> (MIT License). Webfont compiled with <a href="https://icomoon.io/" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600 dark:hover:text-slate-300">Icomoon</a>.
        </p>
        <p>
          Released under the <a href="https://github.com/devicons/devicon/blob/master/LICENSE" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600 dark:hover:text-slate-300">MIT License</a>.
        </p>
      </div>
    </div>
  </div>
</footer>
