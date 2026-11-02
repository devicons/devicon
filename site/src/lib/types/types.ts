export const CURRENT_VERSION = "2.18.0"

export type SortOption = "name-asc" | "name-desc" | "most-versions" | "newest"

export type CategoryOption =
  | "all"
  | "language"
  | "framework"
  | "database"
  | "library"
  | "cloud"
  | "tool"

export type IntegrationTab = "react" | "html" | "svg"

export type IconVersions =
  | "plain"
  | "line"
  | "original"
  | "plain-wordmark"
  | "line-wordmark"
  | "original-wordmark"

export type IconType = "svg" | "font"

export interface IIcon {
  name: string
  altnames: string[]
  tags: string[]
  versions: {
    svg: IconVersions[]
    font: IconVersions[]
  }
  color: string
  aliases: {
    base: IconVersions
    alias: IconVersions
  }[]
}
