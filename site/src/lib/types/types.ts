export const CURRENT_VERSION = "2.17.0"

export type SortOption = "name-asc" | "name-desc" | "newest"

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
