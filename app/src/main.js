import Vue from 'vue';
// import Vue2TouchEvents from 'vue2-touch-events';

import App from './App';
import router from './router';
import store from './store';

Vue.config.productionTip = false;

// Vue.use(Vue2TouchEvents);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App),
});
