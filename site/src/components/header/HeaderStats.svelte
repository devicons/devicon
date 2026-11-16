<script lang="ts">
import { icons, totalVersions } from "$lib/stores/iconStore"
</script>
  <div class="stats mt-2 mb-8 flex rounded-2xl bg-gray-200 dark:bg-gray-700">
    <div
      class="stat place-items-center p-4 border-r border-gray-50 dark:border-gray-600"
    >
      <div class="stat-title dark:text-gray-400">Total Icons</div>
      <div class="stat-value text-4xl font-bold text-green-500">
        {$icons.length}
      </div>
    </div>
    <div class="stat place-items-center p-4">
      <div class="stat-title dark:text-gray-400">Total Versions</div>
      <div class="stat-value text-4xl font-bold text-green-500">
        {$totalVersions}
      </div>
    </div>
  </div>