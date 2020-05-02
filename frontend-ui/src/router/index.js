import Vue from 'vue';
import VueRouter from 'vue-router';
import ListServers from '@/views/ListServers.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'main',
    component: ListServers,
  },
  {
    path: '/list',
    name: 'list',
    component: ListServers,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
