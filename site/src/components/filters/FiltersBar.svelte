<script lang="ts">
import SearchBar from "./SearchBar.svelte"
import TagsDropdown from "./TagsDropdown.svelte"
import SortDropdown from "./SortDropdown.svelte"
</script>

<div class="flex flex-col sm:flex-row justify-between gap-4 rounded-lg py-4">
  <div class="flex-1">
    <SearchBar />
  </div>
  <div class="flex gap-4 sm:w-auto">
    <div class="flex-1 sm:w-64">
      <TagsDropdown />
    </div>
    <div class="w-36">
      <SortDropdown />
    </div>
  </div>
</div>
