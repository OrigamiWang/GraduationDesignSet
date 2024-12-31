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

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.use(store)
app.config.globalProperties.$http = axios
app.mount('#app')
