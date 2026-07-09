import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    target: 'esnext',
    minify: 'esbuild',
    cssMinify: true,
    sourcemap: false, // Set to true only if debugging production builds
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (
            id.includes('node_modules/react') ||
            id.includes('node_modules/react-dom') ||
            id.includes('node_modules/react-router-dom')
          ) {
            return 'vendor-react';
          }

          if (id.includes('node_modules/framer-motion')) {
            return 'vendor-animation';
          }

          if (id.includes('node_modules/@tanstack/react-query')) {
            return 'vendor-query';
          }

          if (
            id.includes('node_modules/lucide-react') ||
            id.includes('node_modules/react-hook-form') ||
            id.includes('node_modules/zod')
          ) {
            return 'vendor-ui';
          }
        },
      },
    },
    // Raise warning limit slightly to accommodate AI dashboard chunk
    chunkSizeWarningLimit: 800,
  },
  server: {
    port: 3000,
    strictPort: true,
  },
});