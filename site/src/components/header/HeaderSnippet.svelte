<script lang="ts">
import { copyToClipboard } from "$lib/common/copyToClipboard"
import Tooltip from "../widgets/tooltip/Tooltip.svelte"

const snippet = `<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/devicon.min.css" />`
</script>

<div class="flex flex-col gap-2">
  <p class="dark:text-gray-400 text-center">For CSS usage, paste the code in the &lt;head&gt; of your HTML</p>
  <div
    class="code-snippet relative w-auto rounded-md bg-gray-100 p-4 dark:bg-gray-900 dark:text-gray-400 flex align-center justify-between"
  >
    <code class="break-all">{snippet}</code>
    <Tooltip content="Copy to clipboard" flashMessage="Copied!">
      <button
        class="my-auto rounded-full text-xl hover:cursor-pointer"
        on:click={() => copyToClipboard(snippet)}
        aria-label="Copy link tag"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"
          />
        </svg>
      </button>
    </Tooltip>
  </div>
</div>
