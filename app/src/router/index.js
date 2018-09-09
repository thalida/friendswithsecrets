import Vue from 'vue';
import Router from 'vue-router';
import Base from '@/components/Base';
// import Home from '@/components/Home';
import Thread from '@/components/Thread';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      // path: '/:participant?/:session?',
      // name: 'Base',
      // alias: [
      //   '/akilah/:session?',
      //   '/robyn/:session?',
      //   '/timothy/:session?',
      // ],
      component: Base,
      // props: route => ({
      //   participant: route.params.participant,
      //   session: parseInt(route.params.session, 10),
      // }),
      children: [
        // {
        //   path: '',
        //   name: 'Home',
        //   component: Home,
        // },
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
