<script lang="ts">
const { children } = $props()
import Navbar from "../components/navigation/Navbar.svelte"
import Footer from "../components/footer/Footer.svelte"
import "../app.css"
import "devicon/devicon.min.css"
</script>

<div class="relative flex min-h-screen flex-col bg-white text-zinc-900 dark:bg-[#09090b] dark:text-zinc-100 overflow-x-hidden">
  <!-- Top Background Engineering Grid Pattern -->
  <div 
    class="pointer-events-none absolute inset-x-0 top-0 h-[640px] bg-devicon-grid [mask-image:radial-gradient(ellipse_70%_60%_at_50%_0%,#000_40%,transparent_100%)]"
    aria-hidden="true"
  ></div>

  <!-- Left Side Engineering Stripe Rail (Visible on wide screens) -->
  <div 
    class="pointer-events-none fixed top-14 bottom-0 left-0 hidden w-6 sm:w-8 xl:w-12 border-r border-emerald-500/10 dark:border-emerald-500/15 bg-devicon-stripes [mask-image:linear-gradient(to_bottom,black_20%,transparent_90%)] 2xl:block"
    aria-hidden="true"
  ></div>

  <!-- Right Side Engineering Stripe Rail (Visible on wide screens) -->
  <div 
    class="pointer-events-none fixed top-14 bottom-0 right-0 hidden w-6 sm:w-8 xl:w-12 border-l border-emerald-500/10 dark:border-emerald-500/15 bg-devicon-stripes [mask-image:linear-gradient(to_bottom,black_20%,transparent_90%)] 2xl:block"
    aria-hidden="true"
  ></div>

  <Navbar />
  <div class="flex-1 relative z-10">
    {@render children()}
  </div>
  <Footer />
</div>
