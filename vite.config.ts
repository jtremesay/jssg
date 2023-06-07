import { globSync } from 'glob'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      input: globSync("front/main/**/*.ts"),
      output: {
        dir: "out/static/gen/",
        entryFileNames: "[name].js"
      }
    }
  }
})
