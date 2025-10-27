import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../static/frontend',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/generate': 'http://localhost:5000',
      '/download': 'http://localhost:5000',
      '/viewer': 'http://localhost:5000',
    }
  }
})
