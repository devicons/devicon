import { writable, derived, get, type Writable, type Readable } from "svelte/store"
import { CURRENT_VERSION, type IIcon, type IconVersions, type SortOption } from "$lib/types/types"

export const icons: Writable<IIcon[]> = writable([])
export const availableTags: Writable<string[]> = writable([])
export const searchTerm: Writable<string> = writable("")
export const selectedTags: Writable<string[]> = writable([])
export const isDarkMode: Writable<boolean> = writable(false)
export const selectedIcon: Writable<IIcon | null> = writable(null)
export const isModalOpen: Writable<boolean> = writable(false)
export const isLoading: Writable<boolean> = writable(false)
export const error: Writable<string | null> = writable(null)
export const latestVersion: Writable<string> = writable(CURRENT_VERSION)
export const sortOption: Writable<SortOption> = writable<SortOption>("name-asc")

export function setSortOption(option: SortOption): void {
  sortOption.set(option)
}

export function getIconSvgUrl(
  icon: IIcon,
  version: IconVersions,
  ver?: string,
): string {
  const v = ver || get(latestVersion) || CURRENT_VERSION
  return `https://cdn.jsdelivr.net/npm/devicon@${v}/icons/${icon.name}/${icon.name}-${version}.svg`
}

export function getIconFallbackSvgUrl(
  icon: IIcon,
  version: IconVersions,
): string {
  return `https://raw.githubusercontent.com/devicons/devicon/master/icons/${icon.name}/${icon.name}-${version}.svg`
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
    const isDark = storedDarkMode === null ? true : storedDarkMode === "true"

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

export const filteredIcons: Readable<IIcon[]> = derived(
  [icons, searchTerm, selectedTags, sortOption],
  ([$icons, $searchTerm, $selectedTags, $sortOption]) => {
    const filtered = $icons.filter((icon) => {
      const matchesSearch =
        $searchTerm === "" ||
        icon.name.toLowerCase().includes($searchTerm.toLowerCase()) ||
        icon.altnames.some((altname) =>
          altname.toLowerCase().includes($searchTerm.toLowerCase()),
        )

      const matchesTags =
        $selectedTags.length === 0 ||
        (icon.tags && $selectedTags.every((tag) => icon.tags?.includes(tag)))

      return matchesSearch && matchesTags
    })

    if ($sortOption === "name-asc") {
      return [...filtered].sort((a, b) => a.name.localeCompare(b.name))
    }
    if ($sortOption === "name-desc") {
      return [...filtered].sort((a, b) => b.name.localeCompare(a.name))
    }
    if ($sortOption === "newest") {
      return [...filtered].reverse()
    }

    return filtered
  },
)

export const totalVersions: Readable<number> = derived([icons], ([$icons]) =>
  $icons.reduce(
    (acc, icon) =>
      acc +
      (icon?.versions?.font?.length ?? 0) +
      (icon?.versions?.svg?.length ?? 0),
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
}

export function toggleDarkMode(): void {
  isDarkMode.update((current) => {
    const newValue = !current

    if (typeof window !== "undefined") {
      localStorage.setItem("darkMode", newValue.toString())

      if (newValue) {
        document.documentElement.classList.add("dark")
      } else {
        document.documentElement.classList.remove("dark")
      }
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
