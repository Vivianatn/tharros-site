import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useMemberStore } from '@/stores/member'

const publicRoutes = {
  path: '/',
  component: () => import('@/layouts/PublicLayout.vue'),
  children: [
    { path: '', name: 'home', component: () => import('@/views/public/HomeView.vue') },
    { path: 'jeux', name: 'games', component: () => import('@/views/public/GamesView.vue') },
    { path: 'jeux/:slug', name: 'game', component: () => import('@/views/public/GameView.vue') },
    { path: 'journal', name: 'journal', component: () => import('@/views/public/JournalView.vue') },
    { path: 'journal/:slug', name: 'post', component: () => import('@/views/public/PostView.vue') },
    { path: 'studio', name: 'studio', component: () => import('@/views/public/StudioView.vue') },
    { path: 'presse', name: 'press', component: () => import('@/views/public/PressView.vue') },
    { path: 'faq', name: 'faq', component: () => import('@/views/public/FaqView.vue') },
    { path: 'contact', name: 'contact', component: () => import('@/views/public/ContactView.vue') },
    { path: 'compte/inscription', name: 'account.register', component: () => import('@/views/public/account/RegisterView.vue'), meta: { guestOnly: true } },
    { path: 'compte/connexion', name: 'account.login', component: () => import('@/views/public/account/LoginView.vue'), meta: { guestOnly: true } },
    { path: 'compte', name: 'account', component: () => import('@/views/public/account/AccountView.vue'), meta: { requiresMember: true } },
    { path: ':slug(confidentialite|cgu|mentions-legales)', name: 'legal', component: () => import('@/views/public/LegalView.vue') },
    { path: ':pathMatch(.*)*', name: 'not-found', component: () => import('@/views/public/NotFoundView.vue') },
  ],
}

const adminRoutes = {
  path: '/admin',
  component: () => import('@/layouts/AdminLayout.vue'),
  meta: { requiresAuth: true },
  children: [
    { path: '', name: 'admin.dashboard', component: () => import('@/views/admin/DashboardView.vue') },
    { path: 'journal', name: 'admin.posts', component: () => import('@/views/admin/PostsView.vue') },
    { path: 'journal/nouveau', name: 'admin.post.new', component: () => import('@/views/admin/PostEditView.vue') },
    { path: 'journal/:id', name: 'admin.post.edit', component: () => import('@/views/admin/PostEditView.vue') },
    { path: 'jeux', name: 'admin.games', component: () => import('@/views/admin/GamesView.vue') },
    { path: 'jeux/nouveau', name: 'admin.game.new', component: () => import('@/views/admin/GameEditView.vue') },
    { path: 'jeux/:id', name: 'admin.game.edit', component: () => import('@/views/admin/GameEditView.vue') },
    { path: 'faq', name: 'admin.faq', component: () => import('@/views/admin/FaqView.vue') },
    { path: 'contenu/:section?', name: 'admin.settings', component: () => import('@/views/admin/SettingsView.vue') },
    { path: 'medias', name: 'admin.media', component: () => import('@/views/admin/MediaView.vue') },
    { path: 'messages', name: 'admin.messages', component: () => import('@/views/admin/MessagesView.vue') },
    { path: 'abonnes', name: 'admin.subscribers', component: () => import('@/views/admin/SubscribersView.vue') },
    { path: 'membres', name: 'admin.members', component: () => import('@/views/admin/MembersView.vue') },
    { path: 'compte', name: 'admin.account', component: () => import('@/views/admin/AccountView.vue') },
  ],
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/admin/connexion', name: 'admin.login', component: () => import('@/views/admin/LoginView.vue') },
    adminRoutes,
    publicRoutes,
  ],
  scrollBehavior(to, from, saved) {
    if (saved) return saved
    if (to.hash) return { el: to.hash, behavior: 'smooth', top: 90 }
    return { top: 0 }
  },
})

// En quittant l'administration, le contenu public est rechargé pour refléter les modifications.
router.afterEach(async (to, from) => {
  if (from.path.startsWith('/admin') && !to.path.startsWith('/admin')) {
    const { useContentStore } = await import('@/stores/content')
    useContentStore().load(true)
  }
})

router.beforeEach(async (to) => {
  if (to.meta.requiresMember || to.meta.guestOnly) {
    const member = useMemberStore()
    await member.restore()
    if (to.meta.requiresMember && !member.isLoggedIn) return { name: 'account.login', query: { next: to.fullPath } }
    if (to.meta.guestOnly && member.isLoggedIn) return { name: 'account' }
  }
  if (!to.meta.requiresAuth) return true
  const auth = useAuthStore()
  await auth.restore()
  if (!auth.isAuthenticated) return { name: 'admin.login', query: { next: to.fullPath } }
  return true
})

// Après une mise à jour du site, un navigateur peut demander un fichier d'une ancienne compilation :
// on recharge la page une fois pour récupérer la nouvelle version.
router.onError((error, to) => {
  if (/Failed to fetch dynamically imported module|Importing a module script failed/.test(error.message)) {
    const key = 'tharros_reload_' + to.fullPath
    if (!sessionStorage.getItem(key)) {
      sessionStorage.setItem(key, '1')
      location.assign(to.fullPath)
    }
  }
})

export default router
