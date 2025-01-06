import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
// export default defineConfig({
//   base: "./",
//   plugins:
//     [
//       vue(),
//     ],
//   server: {
//     host: '127.0.0.1',
//     port: '5173',
//     cors: true,
//     logLevel: 'info',
//     logInfo: true,
//     logRequests: true,
//     proxy: {
//       '/api': {
//         target: 'http://localhost:4000',
//         changeOrigin: true,
//         rewrite: (path) => path.replace(/^\/api/, '')
//       }
//     }
//   },
// })

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // 后端地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '') // 移除路径中的 /api 前缀
      },
    }
  }
})