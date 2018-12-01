import Vue from 'vue';
import Router from 'vue-router';
import Base from '@/components/Base';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Base,
      children: [
        {
          path: ':participant?/:session?',
          name: 'Thread',
          props: route => ({
            participant: route.params.participant,
            session: parseInt(route.params.session, 10),
          }),
        },
      ],
    },
  ],
});
