import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import VueSetupExtend from 'vite-plugin-vue-setup-extend';
export default defineConfig({
	// base: './',
	plugins: [
		vue(),
		VueSetupExtend(),
	],
	optimizeDeps: {
		include: ['schart.js']
	},
	resolve: {
		alias: {
			'@': '/src',
			'~': '/src/assets'
		}
	},
	define: {
		__VUE_PROD_HYDRATION_MISMATCH_DETAILS__: "true",
	},
	server: {
		proxy: {
			'/api': {
				target: 'http://127.0.0.1:5000', // 后端地址
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, '') // 移除路径中的 /api 前缀
			}
		}
	},
});
