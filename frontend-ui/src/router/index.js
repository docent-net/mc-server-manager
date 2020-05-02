import Vue from 'vue';
import VueRouter from 'vue-router';
import ListServersView from '@/views/ListServers.vue';
import APIHealthView from '@/views/APIHealth.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'main',
    component: ListServersView,
  },
  {
    path: '/list',
    name: 'list',
    component: ListServersView,
  },
  {
    path: '/api_health',
    name: 'health',
    component: APIHealthView,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
