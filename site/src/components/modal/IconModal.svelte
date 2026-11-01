<script lang="ts">
import { onMount } from "svelte"
import {
  selectedIcon,
  closeIconModal,
  latestVersion,
  getIconSvgUrl,
  getIconFallbackSvgUrl,
} from "$lib/stores/iconStore"

import Modal from "./Modal.svelte"
import IconModalHeader from "./IconModalHeader.svelte"
import FontVersionSelector from "./IconSelector/FontVersionSelector.svelte"
import SvgVersionSelector from "./IconSelector/SVGVersionSelector.svelte"
import type { IconVersions, IIcon } from "$lib/types/types"

let svgVersions: IconVersions[] = []
let selectedSvgVersion: IconVersions
let isCheckerboard = false

$: if ($selectedIcon?.versions?.svg) {
  svgVersions = $selectedIcon.versions.svg
  selectedSvgVersion = svgVersions.includes("original")
    ? "original"
    : svgVersions[0]
}

function getIconUrl(icon: IIcon, version: IconVersions) {
  return getIconSvgUrl(icon, version, $latestVersion)
}

function getFallbackIconUrl(icon: IIcon, version: IconVersions) {
  return getIconFallbackSvgUrl(icon, version)
}

function toggleCheckerboard() {
  isCheckerboard = !isCheckerboard
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === "Escape") closeIconModal()
}

onMount(() => {
  document.addEventListener("keydown", handleKeydown)
  return () => document.removeEventListener("keydown", handleKeydown)
})
</script>

<Modal isOpen={!!$selectedIcon} onClose={closeIconModal} title={$selectedIcon?.name}>
  <IconModalHeader
    title={$selectedIcon?.name}
    onClose={closeIconModal}
    {isCheckerboard}
    onToggleCheckerboard={toggleCheckerboard}
  />

  {#if $selectedIcon}
    <FontVersionSelector
      title="Font versions"
      versions={$selectedIcon.versions.font || []}
      selectedIcon={$selectedIcon}
      {isCheckerboard}
    />

    <SvgVersionSelector
      title="SVG versions"
      versions={svgVersions}
      selectedIcon={$selectedIcon}
      {getIconUrl}
      {getFallbackIconUrl}
      {isCheckerboard}
    />
  {/if}
</Modal>
