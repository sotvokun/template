import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'

import routes from 'virtual:generated-pages'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import 'virtual:uno.css'

import App from './App.vue'

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

createApp(App)
  .use(router)
  .use(pinia)
  .mount('#app')
