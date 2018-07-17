import Vue from 'vue';
import VueSession from 'vue-session';

import App from './App';
import router from './router';

Vue.config.productionTip = false;
Vue.use(VueSession);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App),
});
