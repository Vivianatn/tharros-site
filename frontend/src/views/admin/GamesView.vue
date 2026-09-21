<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'

const toast = useToast()
const games = ref([])
useHead('Jeux — administration')

async function load() { games.value = await api.get('/api/admin/games', { auth: true }) }
onMounted(load)

async function remove(g) {
  if (!confirm(`Supprimer définitivement « ${g.title} » ?`)) return
  try {
    await api.delete(`/api/admin/games/${g.id}`, { auth: true })
    toast.success('Jeu supprimé')
    await load()
  } catch (e) { toast.error(e.message) }
}
</script>

<template>
  <div class="admin-head">
    <div><span class="kicker">Contenu</span><h1>Jeux</h1><p>Le jeu mis en avant apparaît sur l'accueil et le kit presse.</p></div>
    <div class="admin-actions"><RouterLink class="btn btn--primary" :to="{ name: 'admin.game.new' }">Nouveau jeu</RouterLink></div>
  </div>
  <div class="card card--flat table-wrap">
    <table class="table">
      <thead><tr><th>Jeu</th><th>Statut</th><th>Mis en avant</th><th>Visible</th><th></th></tr></thead>
      <tbody>
        <tr v-if="!games.length"><td colspan="5" class="empty">Aucun jeu.</td></tr>
        <tr v-for="g in games" :key="g.id">
          <td><RouterLink :to="{ name: 'admin.game.edit', params: { id: g.id } }"><strong>{{ g.title }}</strong></RouterLink><br><small class="muted">/jeux/{{ g.slug }}</small></td>
          <td>{{ g.status }}</td>
          <td><span class="pill" :class="g.featured ? 'pill--on' : 'pill--off'">{{ g.featured ? 'Oui' : 'Non' }}</span></td>
          <td><span class="pill" :class="g.published ? 'pill--on' : 'pill--off'">{{ g.published ? 'Publié' : 'Masqué' }}</span></td>
          <td class="actions">
            <a class="btn btn--link" :href="`/jeux/${g.slug}`" target="_blank" rel="noopener">Voir</a>
            <button type="button" class="btn btn--link" style="color: var(--grenat-sombre)" @click="remove(g)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
