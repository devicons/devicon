<script lang="ts">
const { children } = $props()
import Navbar from "../components/navigation/Navbar.svelte"
import Footer from "../components/footer/Footer.svelte"
import "../app.css"
import "devicon/devicon.min.css"
</script>

<div class="flex min-h-screen flex-col bg-white text-zinc-900 dark:bg-[#09090b] dark:text-zinc-100">
  <Navbar />
  <div class="flex-1">
    {@render children()}
  </div>
  <Footer />
</div>
