import { sveltekit } from "@sveltejs/kit/vite"
import { defineConfig, type Plugin, type Connect } from "vite"
import tailwindcss from "@tailwindcss/vite"
import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

function deviconLocalPlugin(): Plugin {
  const jsonPath = fileURLToPath(new URL("../devicon.json", import.meta.url))
  const iconsDir = fileURLToPath(new URL("../icons", import.meta.url))

  const middleware: Connect.NextHandleFunction = (req, res, next) => {
    if (!req.url) {
      return next()
    }
    const cleanUrl = req.url.split("?")[0]

    if (cleanUrl === "/devicon.json" || cleanUrl.endsWith("/devicon.json")) {
      if (fs.existsSync(jsonPath)) {
        res.setHeader("Content-Type", "application/json")
        res.setHeader("Cache-Control", "no-cache")
        fs.createReadStream(jsonPath).on("error", next).pipe(res)
        return
      }
    }

    const iconsPrefix = "/icons/"
    const iconsIndex = cleanUrl.indexOf(iconsPrefix)
    if (iconsIndex !== -1) {
      const relative = decodeURIComponent(cleanUrl.slice(iconsIndex + iconsPrefix.length))
      const filePath = path.resolve(iconsDir, relative)
      if (
        filePath.startsWith(iconsDir) &&
        fs.existsSync(filePath) &&
        fs.statSync(filePath).isFile()
      ) {
        let content = fs.readFileSync(filePath, "utf8")
        if (!content.includes("xmlns=")) {
          content = content.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"')
        }
        res.setHeader("Content-Type", "image/svg+xml")
        res.setHeader("Cache-Control", "no-cache")
        res.end(content)
        return
      }
    }

    next()
  }

  return {
    name: "devicon-local",
    configureServer(server) {
      server.middlewares.use(middleware)
    },
    configurePreviewServer(server) {
      server.middlewares.use(middleware)
    },
    buildStart() {
      const dest = fileURLToPath(new URL("static/devicon.json", import.meta.url))
      if (fs.existsSync(jsonPath)) {
        fs.copyFileSync(jsonPath, dest)
      }
    },
  }
}

export default defineConfig({
  plugins: [deviconLocalPlugin(), tailwindcss(), sveltekit()],
  server: {
    fs: {
      allow: [".."],
    },
  },
  preview: {
    fs: {
      allow: [".."],
    },
  } as unknown as Record<string, unknown>,
})
