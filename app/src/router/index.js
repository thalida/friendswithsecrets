import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home';
import Thread from '@/components/Thread';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/:person',
      name: 'Thread',
      component: Thread,
      props: true,
    },
  ],
});
