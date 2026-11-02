<script lang="ts">
import { setSearchTerm } from "$lib/stores/iconStore"

const marqueeIcons = [
  { name: "react", version: "original", label: "React" },
  { name: "typescript", version: "plain", label: "TypeScript" },
  { name: "python", version: "plain", label: "Python" },
  { name: "rust", version: "original", label: "Rust" },
  { name: "go", version: "original-wordmark", label: "Go" },
  { name: "docker", version: "plain", label: "Docker" },
  { name: "kubernetes", version: "plain", label: "Kubernetes" },
  { name: "nextjs", version: "original-wordmark", label: "Next.js" },
  { name: "vuejs", version: "plain", label: "Vue.js" },
  { name: "svelte", version: "plain", label: "Svelte" },
  { name: "tailwindcss", version: "original", label: "Tailwind CSS" },
  { name: "postgresql", version: "plain", label: "PostgreSQL" },
  { name: "nodejs", version: "plain", label: "Node.js" },
  { name: "graphql", version: "plain", label: "GraphQL" },
  { name: "linux", version: "plain", label: "Linux" },
  { name: "git", version: "plain", label: "Git" },
  { name: "cplusplus", version: "plain", label: "C++" },
  { name: "csharp", version: "plain", label: "C#" },
  { name: "java", version: "plain", label: "Java" },
  { name: "flutter", version: "plain", label: "Flutter" },
  { name: "swift", version: "plain", label: "Swift" },
  { name: "mongodb", version: "plain", label: "MongoDB" },
  { name: "redis", version: "plain", label: "Redis" },
  { name: "amazonwebservices", version: "plain", label: "AWS" },
]

function handleTechClick(techName: string) {
  setSearchTerm(techName)
  const iconsSection = document.getElementById("icons")
  if (iconsSection) {
    iconsSection.scrollIntoView({ behavior: "smooth" })
  }
}
</script>

<div
  class="relative w-full overflow-hidden py-3 [mask-image:linear-gradient(to_right,transparent,black_12%,black_88%,transparent)]"
  role="region"
  aria-label="Popular technologies marquee"
>
  <div class="animate-marquee flex items-center gap-6">
    {#each [...marqueeIcons, ...marqueeIcons] as item, idx (`${item.name}-${idx}`)}
      <button
        type="button"
        on:click={() => handleTechClick(item.name)}
        class="flex items-center gap-2 px-2.5 py-1.5 opacity-60 hover:opacity-100 transition-opacity cursor-pointer select-none focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-400 dark:focus-visible:ring-white/20 rounded-md"
        title={`Filter icons for ${item.label}`}
        aria-label={`Search for ${item.label} icons`}
      >
        <i class="devicon-{item.name}-{item.version} colored text-lg"></i>
        <span class="text-xs font-medium text-slate-500 dark:text-slate-400 whitespace-nowrap">
          {item.label}
        </span>
      </button>
    {/each}
  </div>
</div>
