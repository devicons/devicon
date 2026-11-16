<script lang="ts">
  import { isDarkMode, toggleDarkMode } from "$lib/stores/iconStore";
</script>

<button
  type="button"
  on:click={toggleDarkMode}
  class="flex size-8 items-center justify-center rounded-lg border border-slate-200/80 bg-white text-slate-600 hover:border-slate-300 hover:bg-slate-50 dark:border-white/[0.07] dark:bg-white/[0.03] dark:text-slate-300 dark:hover:border-white/15 dark:hover:bg-white/[0.06] dark:hover:text-white cursor-pointer active:scale-95 transition-transform duration-150"
  aria-label={$isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
>
  <div class="relative size-4 flex items-center justify-center">
    <!-- Sun icon (visible in dark mode) -->
    <svg
      class="theme-toggle-icon absolute size-3.5 text-zinc-300 transition-all duration-300 ease-out {$isDarkMode
        ? 'scale-100 rotate-0 opacity-100'
        : 'scale-0 -rotate-90 opacity-0'}"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      aria-hidden="true"
    >
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" />
      <line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" />
      <line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>

    <!-- Moon icon (visible in light mode) -->
    <svg
      class="theme-toggle-icon absolute size-3.5 text-slate-700 transition-all duration-300 ease-out {$isDarkMode
        ? 'scale-0 rotate-90 opacity-0'
        : 'scale-100 rotate-0 opacity-100'}"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      aria-hidden="true"
    >
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  </div>
</button>
