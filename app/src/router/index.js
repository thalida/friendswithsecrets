import Vue from 'vue';
import Router from 'vue-router';
import Base from '@/components/Base';
import Home from '@/components/Home';
import Thread from '@/components/Thread';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      component: Base,
      children: [
        {
          path: '',
          name: 'Home',
          component: Home,
        },
        {
          path: ':participant/:viewSession?',
          name: 'Thread',
          component: Thread,
          props: (route) => {
            const viewSession = route.params.viewSession || 1;
            return {
              participant: route.params.participant,
              viewSession: parseInt(viewSession, 10),
            };
          },
        },
      ],
    },
  ],
});
