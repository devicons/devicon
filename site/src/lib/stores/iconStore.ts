import { writable, derived, get, type Writable, type Readable } from "svelte/store"
import {
  CURRENT_VERSION,
  type IIcon,
  type IconVersions,
  type SortOption,
  type CategoryOption,
} from "$lib/types/types"

export const icons: Writable<IIcon[]> = writable([])
export const availableTags: Writable<string[]> = writable([])
export const searchTerm: Writable<string> = writable("")
export const selectedTags: Writable<string[]> = writable([])
export const selectedCategory: Writable<CategoryOption> = writable<CategoryOption>("all")
export const selectedVersionFilter: Writable<string> = writable("all")
export const isDarkMode: Writable<boolean> = writable(true)
export const selectedIcon: Writable<IIcon | null> = writable(null)
export const isModalOpen: Writable<boolean> = writable(false)
export const isLoading: Writable<boolean> = writable(false)
export const error: Writable<string | null> = writable(null)
export const latestVersion: Writable<string> = writable(CURRENT_VERSION)
export const sortOption: Writable<SortOption> = writable<SortOption>("name-asc")

export function setSortOption(option: SortOption): void {
  sortOption.set(option)
}

export function setSelectedCategory(category: CategoryOption): void {
  selectedCategory.set(category)
}

export function setSelectedVersionFilter(version: string): void {
  selectedVersionFilter.set(version)
}

const CANONICAL_ORDER = [
  "original",
  "original-wordmark",
  "plain",
  "plain-wordmark",
  "line",
  "line-wordmark",
]

export function getIconAllVariants(icon: IIcon): string[] {
  if (!icon) return []
  const variants = new Set<string>([
    ...(icon.versions?.svg || []),
    ...(icon.versions?.font || []),
  ])

  for (const aliasObj of icon.aliases || []) {
    if (aliasObj?.alias) {
      variants.add(aliasObj.alias)
    }
    if (aliasObj?.base === "original" && aliasObj?.alias === "plain") {
      if (variants.has("original-wordmark")) {
        variants.add("plain-wordmark")
      }
    }
    if (aliasObj?.base === "plain" && aliasObj?.alias === "original") {
      if (variants.has("plain-wordmark")) {
        variants.add("original-wordmark")
      }
    }
  }

  // Second pass in case wordmark was added during alias processing
  for (const aliasObj of icon.aliases || []) {
    if (aliasObj?.base === "original" && aliasObj?.alias === "plain") {
      if (variants.has("original-wordmark")) {
        variants.add("plain-wordmark")
      }
    }
    if (aliasObj?.base === "plain" && aliasObj?.alias === "original") {
      if (variants.has("plain-wordmark")) {
        variants.add("original-wordmark")
      }
    }
  }

  return Array.from(variants).sort((a, b) => {
    const idxA = CANONICAL_ORDER.indexOf(a)
    const idxB = CANONICAL_ORDER.indexOf(b)
    if (idxA !== -1 && idxB !== -1) return idxA - idxB
    if (idxA !== -1) return -1
    if (idxB !== -1) return 1
    return a.localeCompare(b)
  })
}

export function resolveSvgVersion(icon: IIcon, variant: string): string {
  if (!icon) return "original"

  if (icon.versions?.svg?.includes(variant as IconVersions)) {
    return variant
  }

  for (const alias of icon.aliases || []) {
    if (
      alias.alias === variant &&
      icon.versions?.svg?.includes(alias.base as IconVersions)
    ) {
      return alias.base
    }
  }

  if (variant.endsWith("-wordmark")) {
    const root = variant.replace(/-wordmark$/, "")
    for (const alias of icon.aliases || []) {
      if (alias.alias === root) {
        const baseWordmark = `${alias.base}-wordmark` as IconVersions
        if (icon.versions?.svg?.includes(baseWordmark)) {
          return baseWordmark
        }
      }
    }
  }

  return icon.versions?.svg?.[0] || "original"
}

export function isDarkLogo(icon: IIcon): boolean {
  if (!icon) return false
  const explicitDark = [
    "github",
    "apple",
    "nextjs",
    "express",
    "socketio",
    "vercel",
    "bash",
  ]
  if (explicitDark.includes(icon.name?.toLowerCase())) return true

  if (!icon.color) return false
  let hex = icon.color.trim().toLowerCase()
  if (hex.startsWith("#")) hex = hex.slice(1)
  if (hex.length === 3) {
    hex = hex
      .split("")
      .map((c) => c + c)
      .join("")
  }
  if (hex.length !== 6) return false
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const saturation = max === 0 ? 0 : (max - min) / max
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
  return saturation < 0.35 && luminance < 0.35
}

export function getIconSvgUrl(
  icon: IIcon,
  version: IconVersions | string,
  ver?: string,
): string {
  const resolved = resolveSvgVersion(icon, version)
  const v = ver || get(latestVersion) || CURRENT_VERSION
  return `https://cdn.jsdelivr.net/npm/devicon@${v}/icons/${icon.name}/${icon.name}-${resolved}.svg`
}

export function getIconFallbackSvgUrl(
  icon: IIcon,
  version: IconVersions | string,
): string {
  const resolved = resolveSvgVersion(icon, version)
  return `https://raw.githubusercontent.com/devicons/devicon/master/icons/${icon.name}/${icon.name}-${resolved}.svg`
}

async function fetchLatestVersion(): Promise<string> {
  try {
    const response = await fetch(
      "https://api.github.com/repos/devicons/devicon/releases/latest",
    )
    if (response.ok) {
      const data = await response.json()
      if (data?.tag_name) {
        return data.tag_name.replace(/^v/, "")
      }
    }
  } catch {
    // try npm fallback
  }

  try {
    const npmResponse = await fetch("https://registry.npmjs.org/devicon/latest")
    if (npmResponse.ok) {
      const npmData = await npmResponse.json()
      if (npmData?.version) {
        return npmData.version
      }
    }
  } catch {
    // ignore
  }

  return CURRENT_VERSION
}

export async function fetchIconsData(): Promise<void> {
  isLoading.set(true)
  error.set(null)

  try {
    const version = await fetchLatestVersion()
    latestVersion.set(version)

    let response: Response | null = null
    try {
      response = await fetch(
        `https://cdn.jsdelivr.net/npm/devicon@${version}/devicon.json`,
      )
      if (!response.ok) {
        response = null
      }
    } catch {
      response = null
    }

    if (!response) {
      response = await fetch(
        "https://raw.githubusercontent.com/devicons/devicon/master/devicon.json",
      )
    }

    if (!response.ok) {
      throw new Error(`Failed to fetch icons: ${response.statusText}`)
    }

    const iconsData: IIcon[] = await response.json()

    const availableTagsSet = new Set<string>()
    iconsData.forEach((icon) => {
      if (icon.tags && Array.isArray(icon.tags)) {
        for (const tag of icon.tags) {
          availableTagsSet.add(tag)
        }
      }
    })

    const sortedTags = Array.from(availableTagsSet).sort()

    icons.set(iconsData)
    availableTags.set(sortedTags)

    initializeDarkMode()
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err)
    console.error("Error fetching icons:", err)
    error.set(message)
    icons.set([])
    availableTags.set([])
  } finally {
    isLoading.set(false)
  }
}

function initializeDarkMode(): void {
  if (typeof window !== "undefined") {
    const storedDarkMode = localStorage.getItem("darkMode")
    const isDark = storedDarkMode !== "false"

    isDarkMode.set(isDark)

    if (isDark) {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }
}

export function initializeStore(
  initialIcons: IIcon[],
  initialTags: string[],
): void {
  icons.set(initialIcons)
  availableTags.set(initialTags)
  initializeDarkMode()
}

const CATEGORY_TAG_MAP: Record<CategoryOption, string[]> = {
  all: [],
  language: ["language", "programming"],
  framework: ["framework"],
  database: ["database", "nosql", "sql"],
  library: ["library"],
  cloud: ["cloud", "devops", "hosting", "server", "cloud-computing"],
  tool: [
    "tool",
    "editor",
    "ide",
    "automation",
    "build",
    "vcs",
    "version-control",
    "design",
  ],
}

export const categoryCounts: Readable<Record<CategoryOption, number>> = derived(
  [icons],
  ([$icons]) => {
    const counts: Record<CategoryOption, number> = {
      all: $icons.length,
      language: 0,
      framework: 0,
      database: 0,
      library: 0,
      cloud: 0,
      tool: 0,
    }

    for (const icon of $icons) {
      const lowerTags = (icon.tags || []).map((t) => t.toLowerCase())

      for (const cat of [
        "language",
        "framework",
        "database",
        "library",
        "cloud",
        "tool",
      ] as const) {
        const mapped = CATEGORY_TAG_MAP[cat]
        const matches = lowerTags.some(
          (tag) => tag === cat || mapped?.includes(tag),
        )
        if (matches) {
          counts[cat]++
        }
      }
    }

    return counts
  },
)

export const filteredIcons: Readable<IIcon[]> = derived(
  [icons, searchTerm, selectedTags, selectedCategory, selectedVersionFilter, sortOption],
  ([
    $icons,
    $searchTerm,
    $selectedTags,
    $selectedCategory,
    $selectedVersionFilter,
    $sortOption,
  ]) => {
    const query = $searchTerm.trim().toLowerCase()

    const filtered = $icons.filter((icon) => {
      const matchesSearch =
        query === "" ||
        icon.name.toLowerCase().includes(query) ||
        Boolean(icon.altnames?.some((alt) => alt.toLowerCase().includes(query)))

      const matchesTags =
        $selectedTags.length === 0 ||
        Boolean(icon.tags && $selectedTags.every((tag) => icon.tags.includes(tag)))

      const matchesCategory =
        $selectedCategory === "all" ||
        Boolean(
          icon.tags?.some((tag) => {
            const lowerTag = tag.toLowerCase()
            if (lowerTag === $selectedCategory) return true
            const mapped = CATEGORY_TAG_MAP[$selectedCategory]
            return mapped?.includes(lowerTag)
          }),
        )

      const allVariants = getIconAllVariants(icon)
      const matchesVersion =
        $selectedVersionFilter === "all" ||
        Boolean(
          allVariants.some((v) =>
            $selectedVersionFilter === "wordmark"
              ? v.includes("wordmark")
              : v.startsWith($selectedVersionFilter),
          ),
        )

      return matchesSearch && matchesTags && matchesCategory && matchesVersion
    })

    if ($sortOption === "name-asc") {
      return [...filtered].sort((a, b) => a.name.localeCompare(b.name))
    }
    if ($sortOption === "name-desc") {
      return [...filtered].sort((a, b) => b.name.localeCompare(a.name))
    }
    if ($sortOption === "most-versions") {
      return [...filtered].sort((a, b) => {
        return getIconAllVariants(b).length - getIconAllVariants(a).length
      })
    }
    if ($sortOption === "newest") {
      return [...filtered].reverse()
    }

    return filtered
  },
)

export const totalVersions: Readable<number> = derived([icons], ([$icons]) =>
  $icons.reduce(
    (acc, icon) => acc + getIconAllVariants(icon).length,
    0,
  ),
)

export function setSearchTerm(term: string): void {
  searchTerm.set(term)
}

export function setSelectedTags(tags: string[]): void {
  selectedTags.set(tags)
}

export function clearFilters(): void {
  searchTerm.set("")
  selectedTags.set([])
  selectedCategory.set("all")
  selectedVersionFilter.set("all")
}

export function toggleDarkMode(): void {
  if (typeof window !== "undefined") {
    document.documentElement.classList.add("disable-transitions")
  }

  isDarkMode.update((current) => {
    const newValue = !current

    if (typeof window !== "undefined") {
      localStorage.setItem("darkMode", newValue.toString())

      if (newValue) {
        document.documentElement.classList.add("dark")
      } else {
        document.documentElement.classList.remove("dark")
      }

      // Flush computed style reflow so theme changes instantly without intermediate transitions
      window.getComputedStyle(document.documentElement).opacity

      requestAnimationFrame(() => {
        document.documentElement.classList.remove("disable-transitions")
      })
    }

    return newValue
  })
}

export function openIconModal(icon: IIcon): void {
  selectedIcon.set(icon)
  isModalOpen.set(true)
}

export function closeIconModal(): void {
  selectedIcon.set(null)
  isModalOpen.set(false)
}
