export function scrollToSection(id: string, e?: Event): void {
  if (e) {
    e.preventDefault()
  }

  if (typeof document !== "undefined") {
    const el = document.getElementById(id)
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }

  if (typeof window !== "undefined" && window.location.hash) {
    window.history.replaceState(null, "", window.location.pathname + window.location.search)
  }
}
