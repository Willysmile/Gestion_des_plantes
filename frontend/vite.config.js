import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
    // Optimiser HMR
    hmr: {
      host: 'localhost',
      port: 5173,
      protocol: 'ws',
    },
  },
  build: {
    // Optimiser la build
    minify: 'terser',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom', 'axios'],
        },
      },
    },
  },
  optimizeDeps: {
    // Pré-bundle les dépendances courantes
    include: ['react', 'react-dom', 'react-router-dom', 'axios'],
  },
})
