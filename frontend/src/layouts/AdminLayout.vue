<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { api } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import BrandLogo from '@/components/BrandLogo.vue'
import '@/styles/admin.css'

const auth = useAuthStore()
const router = useRouter()
const toast = useToast()
const unread = ref(0)

async function refreshUnread() {
  try { unread.value = (await api.get('/api/admin/dashboard', { auth: true })).messages_unread } catch { /* ignoré */ }
}
onMounted(refreshUnread)
defineExpose({ refreshUnread })

function logout() {
  auth.logout()
  router.push({ name: 'admin.login' })
}
</script>

<template>
  <div class="admin">
    <aside class="admin-side">
      <RouterLink class="admin-side__brand" :to="{ name: 'admin.dashboard' }"><BrandLogo :height="34" /><small>Admin</small></RouterLink>
      <nav class="admin-nav" aria-label="Administration">
        <RouterLink :to="{ name: 'admin.dashboard' }" exact-active-class="router-link-active">Tableau de bord</RouterLink>
        <div class="admin-nav__group">Contenu</div>
        <RouterLink :to="{ name: 'admin.posts' }">Journal</RouterLink>
        <RouterLink :to="{ name: 'admin.games' }">Jeux</RouterLink>
        <RouterLink :to="{ name: 'admin.faq' }">FAQ</RouterLink>
        <RouterLink :to="{ name: 'admin.settings', params: { section: 'home' } }">Pages du site</RouterLink>
        <RouterLink :to="{ name: 'admin.media' }">Médias</RouterLink>
        <div class="admin-nav__group">Boîte de réception</div>
        <RouterLink :to="{ name: 'admin.messages' }">Messages <span v-if="unread" class="badge">{{ unread }}</span></RouterLink>
        <RouterLink :to="{ name: 'admin.subscribers' }">Liste d'attente</RouterLink>
        <RouterLink :to="{ name: 'admin.members' }">Comptes joueurs</RouterLink>
        <div class="admin-nav__group">Compte</div>
        <RouterLink :to="{ name: 'admin.account' }">Mot de passe &amp; e-mails</RouterLink>
      </nav>
      <div class="admin-side__foot">
        <span>{{ auth.user?.email }}</span>
        <a href="/" target="_blank" rel="noopener">Voir le site ↗</a>
        <button type="button" @click="logout">Se déconnecter</button>
      </div>
    </aside>
    <main class="admin-main">
      <RouterView @unread-changed="refreshUnread" />
    </main>
    <div class="toasts" aria-live="polite">
      <div v-for="t in toast.items" :key="t.id" class="toast" :class="`toast--${t.type}`">{{ t.message }}</div>
    </div>
  </div>
</template>
