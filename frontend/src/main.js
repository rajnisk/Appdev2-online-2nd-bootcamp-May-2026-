import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import Bootstrap styles
import 'bootstrap/dist/css/bootstrap.css'


const app = createApp(App)

app.use(router)

app.mount('#app')
