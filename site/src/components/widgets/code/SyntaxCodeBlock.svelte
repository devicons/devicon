<script lang="ts">
import { copyToClipboard } from "$lib/common/copyToClipboard"

export let code: string = ""
export let language: string = ""
export let title: string = ""

let copied = false
let timeoutId: ReturnType<typeof setTimeout> | null = null

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
}

function highlightCode(rawCode: string, _lang: string): string {
  if (!rawCode) return ""

  const lines = rawCode.split("\n")
  const highlightedLines = lines.map((line) => {
    // Tokenizer regex:
    // 1. Comments: //... or <!--...-->
    // 2. Strings: "..." or '...' or `...`
    // 3. Tags: </?[A-Za-z0-9_.-]+ or /?>
    // 4. Attributes: attr=
    // 5. Keywords: import, from, export, etc.
    // 6. Numbers: \b\d+\b
    const tokenRegex =
      /(\/\/.*|<!--[\s\S]*?-->)|("([^"\\]*(\\.[^"\\]*)*)"|'([^'\\]*(\\.[^'\\]*)*)'|`([^`\\]*(\\.[^`\\]*)*)`)|(<\/?[A-Za-z0-9_.-]+|\/?>)|(\b[a-zA-Z0-9_-]+(?==))|(\b(?:import|from|export|default|function|return|const|let|var|type|interface|npm|pnpm|yarn|bun|add|i|install)\b)|(\b\d+\b)/g

    let result = ""
    let lastIndex = 0
    let match: RegExpExecArray | null = null

    // biome-ignore lint/suspicious/noAssignInExpressions: regex exec loop pattern
    while ((match = tokenRegex.exec(line)) !== null) {
      if (match.index > lastIndex) {
        result += escapeHtml(line.slice(lastIndex, match.index))
      }

      const [full, comment, str, , , , , , , tag, attr, kw, num] = match

      if (comment) {
        result += `<span class="text-slate-500 italic">${escapeHtml(comment)}</span>`
      } else if (str) {
        result += `<span class="text-emerald-400">${escapeHtml(str)}</span>`
      } else if (tag) {
        result += `<span class="text-cyan-400">${escapeHtml(tag)}</span>`
      } else if (attr) {
        result += `<span class="text-amber-300">${escapeHtml(attr)}</span>`
      } else if (kw) {
        result += `<span class="text-purple-400 font-semibold">${escapeHtml(kw)}</span>`
      } else if (num) {
        result += `<span class="text-orange-300">${escapeHtml(num)}</span>`
      } else {
        result += escapeHtml(full)
      }

      lastIndex = tokenRegex.lastIndex
    }

    if (lastIndex < line.length) {
      result += escapeHtml(line.slice(lastIndex))
    }

    return result
  })

  return highlightedLines.join("\n")
}

$: highlightedHtml = highlightCode(code, language)

async function handleCopy() {
  if (!code) return
  await copyToClipboard(code)
  copied = true
  if (timeoutId) clearTimeout(timeoutId)
  timeoutId = setTimeout(() => {
    copied = false
  }, 2000)
}
</script>

<div class="group relative overflow-hidden rounded-xl border border-slate-200/90 bg-slate-900 text-slate-100 shadow-xs dark:border-white/[0.08] dark:bg-[#11131a]">
  <!-- Header bar -->
  <div class="flex items-center justify-between border-b border-slate-800 bg-slate-950/70 px-3.5 py-1.5 text-xs dark:border-white/[0.06] dark:bg-[#09090b]/80">
    <div class="flex items-center gap-2">
      {#if title}
        <span class="font-medium text-slate-300 dark:text-slate-200">{title}</span>
      {/if}
      {#if language}
        <span class="rounded bg-white/10 px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-slate-400">
          {language}
        </span>
      {/if}
    </div>

    <button
      type="button"
      on:click={handleCopy}
      class="flex items-center gap-1.5 rounded px-2 py-0.5 text-[11px] font-medium transition cursor-pointer {copied
        ? 'bg-emerald-500/20 text-emerald-400'
        : 'text-slate-400 hover:bg-white/10 hover:text-slate-200'}"
      aria-label="Copy code to clipboard"
    >
      {#if copied}
        <svg class="size-3.5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        <span>Copied!</span>
      {:else}
        <svg class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
        </svg>
        <span>Copy</span>
      {/if}
    </button>
  </div>

  <!-- Code area -->
  <div class="code-snippet max-h-72 overflow-x-auto overflow-y-auto p-3 text-left no-scrollbar">
    <pre class="font-mono text-xs leading-relaxed text-slate-200 select-all cursor-default text-left"><code>{@html highlightedHtml}</code></pre>
  </div>
</div>
