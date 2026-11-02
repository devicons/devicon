<script lang="ts">
import { latestVersion } from "$lib/stores/iconStore"
import SyntaxCodeBlock from "../widgets/code/SyntaxCodeBlock.svelte"
import { copyToClipboard } from "$lib/common/copyToClipboard"

type PkgManager = "npm" | "pnpm" | "yarn" | "bun"
let activePkg: PkgManager = "npm"

const pkgCommands: Record<PkgManager, string> = {
  npm: "npm i react-devicons",
  pnpm: "pnpm add react-devicons",
  yarn: "yarn add react-devicons",
  bun: "bun add react-devicons",
}

let copiedPkg = false
async function copyPkgCommand() {
  await copyToClipboard(pkgCommands[activePkg])
  copiedPkg = true
  setTimeout(() => {
    copiedPkg = false
  }, 2000)
}

$: cdnLink =
  '<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/devicon.min.css" />'
$: cdnVersionedLink = `<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/devicon@${$latestVersion}/devicon.min.css" />`
const htmlUsageSnippet = `<i class="devicon-react-original colored"></i>
<i class="devicon-typescript-plain"></i>`

const reactSnippet = `import { ReactOriginalIcon } from "react-devicons/react/original";
import { TypescriptPlainIcon } from "react-devicons/typescript/plain";

export function TechBadge() {
  return (
    <div className="flex items-center gap-2">
      <ReactOriginalIcon size={32} />
      <TypescriptPlainIcon size={32} />
    </div>
  );
}`

</script>

<section id="integrations" class="scroll-mt-16 py-14">
  <div class="base-container flex flex-col gap-10">
    <!-- Section Header -->
    <div class="flex flex-col gap-2">
      <h2 class="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
        Integrations
      </h2>
      <p class="max-w-2xl text-sm text-slate-600 dark:text-slate-400">
        Official React component package and global CDN distribution for Devicon.
      </p>
    </div>

    <!-- 1. React Documentation Block -->
    <div class="flex flex-col gap-3">
      <div class="flex items-center gap-2">
        <h3 class="text-base font-semibold text-slate-900 dark:text-white">
          React Components
        </h3>
        <span class="rounded bg-emerald-500/10 px-2 py-0.5 text-[10px] font-mono font-medium text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
          Official
        </span>
      </div>

      <div class="rounded-xl border border-slate-200/90 bg-white p-5 dark:border-white/[0.07] dark:bg-[#11131a]">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          <!-- Left: Instructions & Install -->
          <div class="lg:col-span-5 flex flex-col gap-3">
            <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              Type-safe React SVG components. Each icon is individually exported for zero runtime overhead and automatic tree-shaking.
            </p>

            <!-- Package Manager Selector -->
            <div class="flex flex-col gap-1.5 pt-1">
              <div class="flex items-center gap-1 text-xs">
                {#each (["npm", "pnpm", "yarn", "bun"] as const) as pkg}
                  <button
                    type="button"
                    on:click={() => (activePkg = pkg)}
                    class="rounded px-2 py-0.5 font-mono text-[10px] font-semibold transition cursor-pointer {activePkg === pkg
                      ? 'bg-slate-900 text-white dark:bg-white/15 dark:text-white'
                      : 'text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-white/5'}"
                  >
                    {pkg}
                  </button>
                {/each}
              </div>

              <div class="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 font-mono text-xs text-slate-800 dark:border-white/[0.08] dark:bg-[#181b24] dark:text-slate-200">
                <span class="select-all">{pkgCommands[activePkg]}</span>
                <button
                  type="button"
                  on:click={copyPkgCommand}
                  class="ml-2 flex items-center gap-1 text-[11px] font-sans text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white cursor-pointer"
                  aria-label="Copy install command"
                >
                  {#if copiedPkg}
                    <svg class="size-3 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    <span class="text-emerald-500">Copied</span>
                  {:else}
                    <svg class="size-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                    </svg>
                    <span>Copy</span>
                  {/if}
                </button>
              </div>
            </div>

            <!-- Links -->
            <div class="flex items-center gap-3 pt-1 text-xs">
              <a
                href="https://github.com/devicons/react-devicons"
                target="_blank"
                rel="noopener noreferrer"
                class="font-medium text-slate-700 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white inline-flex items-center gap-1 underline underline-offset-2"
              >
                <span>GitHub Repository</span>
                <span>→</span>
              </a>
              <a
                href="https://www.npmjs.com/package/react-devicons"
                target="_blank"
                rel="noopener noreferrer"
                class="font-medium text-slate-700 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white inline-flex items-center gap-1 underline underline-offset-2"
              >
                <span>npm Package</span>
                <span>→</span>
              </a>
            </div>
          </div>

          <!-- Right: Code snippet -->
          <div class="lg:col-span-7">
            <SyntaxCodeBlock
              title="Usage Example"
              language="tsx"
              code={reactSnippet}
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 2. CDN & Webfont Block -->
    <div id="cdn" class="scroll-mt-16 flex flex-col gap-3">
      <div class="flex items-center gap-2">
        <h3 class="text-base font-semibold text-slate-900 dark:text-white">
          CDN & Webfont Distribution
        </h3>
        <span class="rounded bg-slate-100 dark:bg-white/[0.04] px-2 py-0.5 text-[10px] font-mono text-slate-500 dark:text-slate-400">
          jsDelivr
        </span>
      </div>

      <div class="rounded-xl border border-slate-200/90 bg-white p-5 dark:border-white/[0.07] dark:bg-[#11131a]">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          <div class="lg:col-span-5 flex flex-col gap-3">
            <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              Include Devicon in any web application or static HTML file without build steps. Add the stylesheet to your <code class="font-mono text-slate-800 dark:text-slate-200">&lt;head&gt;</code> and use standard CSS icon classes.
            </p>
            <div class="rounded-lg bg-slate-50 p-3 text-xs text-slate-500 dark:bg-[#181b24] dark:text-slate-400 border border-slate-200/60 dark:border-white/[0.04]">
              Tip: Append <code class="font-mono text-slate-700 dark:text-slate-300">colored</code> to display original brand colors, or omit it to inherit the parent CSS text color.
            </div>
          </div>

          <div class="lg:col-span-7 flex flex-col gap-3">
            <SyntaxCodeBlock
              title="Latest Version Link"
              language="html"
              code={cdnLink}
            />
            <SyntaxCodeBlock
              title="HTML Element Usage"
              language="html"
              code={htmlUsageSnippet}
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
