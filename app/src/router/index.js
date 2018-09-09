import Vue from 'vue';
import Router from 'vue-router';
import Base from '@/components/Base';
import Thread from '@/components/Thread';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      component: Base,
      children: [
        {
          path: ':participant?/:session?',
          name: 'Thread',
          component: Thread,
          props: route => ({
            participant: route.params.participant,
            session: parseInt(route.params.session, 10),
          }),
        },
      ],
    },
  ],
});
