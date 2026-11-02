<script lang="ts">
  import {
    openIconModal,
    selectedIcon,
    latestVersion,
    getIconSvgUrl,
    getIconFallbackSvgUrl,
    getIconAllVariants,
    isDarkLogo,
  } from "$lib/stores/iconStore";
  import type { IIcon, IconVersions } from "$lib/types/types";

  export let icon: IIcon;

  $: totalCount = getIconAllVariants(icon).length;
  $: defaultSvgVersion = (
    icon.versions?.svg?.includes("original" as IconVersions)
      ? "original"
      : icon.versions?.svg?.[0] ?? "plain"
  ) as IconVersions;
  $: isSelected = $selectedIcon?.name === icon.name;
  $: isDark = isDarkLogo(icon);

  function handleImageError(e: Event, version: IconVersions | string) {
    const target = e.currentTarget as HTMLImageElement | null;
    if (target) {
      const fallback = getIconFallbackSvgUrl(icon, version);
      if (target.src !== fallback) {
        target.src = fallback;
      }
    }
  }
</script>

<button
  type="button"
  class="group relative h-[148px] sm:h-[156px] min-h-[148px] flex flex-col justify-between rounded-xl border bg-white p-3 sm:p-3.5 text-left transition-transform duration-150 hover:-translate-y-0.5 dark:bg-[#11131a] cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-[#09090b] {isSelected
    ? 'ring-1 ring-emerald-500 border-emerald-500 dark:border-emerald-500'
    : 'border-slate-200/90 hover:border-slate-300 dark:border-white/[0.06] dark:hover:border-white/[0.18]'}"
  on:click={() => openIconModal(icon)}
  aria-label={`View ${icon.name} details and code integration`}
>
  <!-- Natural Tile Backing -->
  <div
    class="flex h-20 sm:h-22 w-full items-center justify-center rounded-lg bg-slate-50 border border-slate-100 dark:bg-white/[0.025] dark:border-white/[0.04]"
  >
    <img
      src={getIconSvgUrl(icon, defaultSvgVersion, $latestVersion)}
      alt={`${icon.name} icon`}
      loading="lazy"
      width="44"
      height="44"
      on:error={(e) => handleImageError(e, defaultSvgVersion)}
      class="size-10 sm:size-11 object-contain transition-transform duration-150 group-hover:scale-105 {isDark
        ? 'dark:brightness-0 dark:invert'
        : ''}"
    />
  </div>

  <!-- Tech Name & Version Count -->
  <div class="mt-2 flex flex-col items-center gap-0.5 w-full">
    <h3
      class="w-full truncate text-center text-xs font-medium text-slate-700 dark:text-slate-300 transition-colors group-hover:text-slate-900 dark:group-hover:text-white"
    >
      {icon.name}
    </h3>

    <span class="text-[10px] font-mono text-slate-400 dark:text-slate-500">
      {totalCount}
      {totalCount === 1 ? "variant" : "variants"}
    </span>
  </div>
</button>
