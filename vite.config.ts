import { defineConfig } from 'vite'
import { djangoVitePlugin } from 'django-vite-plugin'
import { globSync } from 'glob'

export default defineConfig({
    plugins: [
        djangoVitePlugin({
            input: [
                ...globSync('front/main/*.ts'),
            ]
        })
    ],
});
