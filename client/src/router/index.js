import { createRouter, createWebHistory } from 'vue-router'
import ProjectPage from "@/pages/ProjectPage.vue";
import MainPage from "@/pages/MainPage.vue";
import LoginPage from "@/pages/LoginPage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: 'active',
  linkExactActiveClass: 'active-exact',
  routes: [
    {
      path: '/',
      component: MainPage
    },
    {
      path: '/login',
      component: LoginPage
    },
    {
      path: '/projects',
      component: ProjectPage
    }
  ],
})

export default router
