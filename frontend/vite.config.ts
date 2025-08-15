import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3008,
    host: true,
    open: false,
    hmr: {
      overlay: false
    },
    cors: true,
    proxy: {
      // Proxy API requests to backend
      '/api': {
        target: 'http://localhost:8008',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  preview: {
    port: 3008,
    host: true,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom'],
    force: true
  },
  clearScreen: false
})