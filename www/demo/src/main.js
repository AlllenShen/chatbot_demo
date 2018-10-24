import Vue from "vue";
import App from "./App.vue";
import iview from "iview"
import VueResource from 'vue-resource'
import 'iview/dist/styles/iview.css';
import bus from './eventBus'

Vue.use(iview)
Vue.use(VueResource)
Vue.config.productionTip = false;
Vue.prototype.bus = bus;


new Vue({
  render: h => h(App),
}).$mount("#app");
