import { globSync } from 'glob'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      input: globSync("src/entrypoints/**/*.ts"),
      output: {
        dir: "jtremesay/static/gen/",
        entryFileNames: "[name].js"
      }
    }
  }
})
