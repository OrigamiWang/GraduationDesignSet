import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import router from './router/index.js'
import axios from 'axios'
import store from './store/index.js'
import App from './App.vue'
import 'element-plus/dist/index.css'
import './style.css'
import './style/style.vue'
import './assets/styles.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import JsonViewer from "vue3-json-viewer"
import 'element-plus/theme-chalk/dark/css-vars.css'


const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(ElementPlus)
app.use(router)
app.use(store)
app.use(JsonViewer)
app.config.globalProperties.$http = axios
app.mount('#app')
