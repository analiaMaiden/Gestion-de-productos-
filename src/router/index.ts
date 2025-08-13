import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import LoginPage from '@/pages/LoginPage.vue';
import ProductsPage from '@/pages/ProductsPage.vue';

const routes = [
  { path: '/login', name: 'login', component: LoginPage },
  { path: '/productos', name: 'productos', component: ProductsPage, meta: { requiresAuth: true } },
  { path: '/', redirect: '/productos' },
  { path: '/:pathMatch(.*)*', redirect: '/productos' }
];

const router = createRouter({ history: createWebHistory(), routes });

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) return '/login';
  if (to.path === '/login' && auth.isAuthenticated) return '/productos';
});

export default router;
