<script lang="ts">
const { children } = $props()
import Header from "../components/header/Header.svelte"
import Footer from "../components/footer/Footer.svelte"
import "../app.css"
import "devicon/devicon.min.css"
import DarkModeToggle from "../components/darkMode/DarkModeToggle.svelte"
</script>

<Header />

{@render children()}
<DarkModeToggle />
<Footer />
