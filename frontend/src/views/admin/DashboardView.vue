<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useHead } from '@/composables/useHead'

const auth = useAuthStore()
const stats = ref(null)
useHead('Tableau de bord')
onMounted(async () => { stats.value = await api.get('/api/admin/dashboard', { auth: true }) })
</script>

<template>
  <div class="admin-head">
    <div>
      <span class="kicker">Tableau de bord</span>
      <h1>Bonjour, {{ auth.user?.display_name || 'Admin' }}</h1>
      <p>Tout le contenu du site se gère ici. Les changements sont visibles immédiatement.</p>
    </div>
    <div class="admin-actions">
      <RouterLink class="btn btn--primary" :to="{ name: 'admin.post.new' }">Nouveau billet</RouterLink>
    </div>
  </div>

  <div v-if="stats" class="stat-tiles">
    <RouterLink class="stat-tile" :to="{ name: 'admin.posts' }"><div class="stat-tile__num">{{ stats.posts_published }}<small style="font-size: 20px; color: var(--pierre)">/{{ stats.posts }}</small></div><div class="stat-tile__label">Billets publiés</div></RouterLink>
    <RouterLink class="stat-tile" :to="{ name: 'admin.games' }"><div class="stat-tile__num">{{ stats.games }}</div><div class="stat-tile__label">Jeux</div></RouterLink>
    <RouterLink class="stat-tile" :to="{ name: 'admin.faq' }"><div class="stat-tile__num">{{ stats.faq }}</div><div class="stat-tile__label">Questions FAQ</div></RouterLink>
    <RouterLink class="stat-tile" :to="{ name: 'admin.subscribers' }"><div class="stat-tile__num">{{ stats.subscribers }}</div><div class="stat-tile__label">Inscrits liste d'attente</div></RouterLink>
    <RouterLink class="stat-tile" :to="{ name: 'admin.messages' }"><div class="stat-tile__num">{{ stats.messages_unread }}</div><div class="stat-tile__label">Messages non lus</div></RouterLink>
    <RouterLink class="stat-tile" :to="{ name: 'admin.members' }"><div class="stat-tile__num">{{ stats.members }}</div><div class="stat-tile__label">Comptes joueurs</div></RouterLink>
    <RouterLink class="stat-tile" :to="{ name: 'admin.media' }"><div class="stat-tile__num">{{ stats.media }}</div><div class="stat-tile__label">Médias</div></RouterLink>
  </div>

  <div class="card" style="margin-top: 24px">
    <h2>Par où commencer ?</h2>
    <ul style="line-height: 2">
      <li><RouterLink :to="{ name: 'admin.post.new' }">Écrire un devlog</RouterLink> — titre, texte en Markdown, image de couverture, publication immédiate ou programmée.</li>
      <li><RouterLink :to="{ name: 'admin.game.new' }">Ajouter la fiche d'un jeu</RouterLink> — titre, statut, pitch, visuels, puis les fichiers à télécharger pour Windows, macOS et Linux.</li>
      <li><RouterLink :to="{ name: 'admin.settings', params: { section: 'home' } }">Modifier les textes des pages</RouterLink> — accueil, studio, presse, pages légales, réseaux sociaux.</li>
      <li><RouterLink :to="{ name: 'admin.media' }">Téléverser des images</RouterLink> — elles sont redimensionnées et converties en WebP automatiquement.</li>
      <li><RouterLink :to="{ name: 'admin.account' }">Changer le mot de passe</RouterLink> — à faire dès la première connexion.</li>
    </ul>
  </div>
</template>
