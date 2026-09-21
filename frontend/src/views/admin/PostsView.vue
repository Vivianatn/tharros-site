<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'
import { formatDate } from '@/utils/format'

const toast = useToast()
const posts = ref([])
useHead('Journal — administration')

async function load() { posts.value = await api.get('/api/admin/posts', { auth: true }) }
onMounted(load)

async function remove(post) {
  if (!confirm(`Supprimer définitivement « ${post.title} » ?`)) return
  try {
    await api.delete(`/api/admin/posts/${post.id}`, { auth: true })
    toast.success('Billet supprimé')
    await load()
  } catch (e) { toast.error(e.message) }
}

async function togglePublished(post) {
  try {
    await api.put(`/api/admin/posts/${post.id}`, { ...post, published: !post.published }, { auth: true })
    toast.success(post.published ? 'Billet dépublié' : 'Billet publié')
    await load()
  } catch (e) { toast.error(e.message) }
}
</script>

<template>
  <div class="admin-head">
    <div><span class="kicker">Contenu</span><h1>Journal</h1><p>Les devlogs, du brouillon à la publication.</p></div>
    <div class="admin-actions"><RouterLink class="btn btn--primary" :to="{ name: 'admin.post.new' }">Nouveau billet</RouterLink></div>
  </div>
  <div class="card card--flat table-wrap">
    <table class="table">
      <thead><tr><th>Titre</th><th>Étiquette</th><th>Date</th><th>État</th><th></th></tr></thead>
      <tbody>
        <tr v-if="!posts.length"><td colspan="5" class="empty">Aucun billet. Écrivez le premier !</td></tr>
        <tr v-for="p in posts" :key="p.id">
          <td><RouterLink :to="{ name: 'admin.post.edit', params: { id: p.id } }"><strong>{{ p.title }}</strong></RouterLink><br><small class="muted">/journal/{{ p.slug }}</small></td>
          <td>{{ p.tag }}</td>
          <td>{{ formatDate(p.published_at || p.created_at) }}</td>
          <td><span class="pill" :class="p.published ? 'pill--on' : 'pill--off'">{{ p.published ? 'Publié' : 'Brouillon' }}</span></td>
          <td class="actions">
            <button type="button" class="btn btn--link" @click="togglePublished(p)">{{ p.published ? 'Dépublier' : 'Publier' }}</button>
            <a v-if="p.published" class="btn btn--link" :href="`/journal/${p.slug}`" target="_blank" rel="noopener">Voir</a>
            <button type="button" class="btn btn--link" style="color: var(--grenat-sombre)" @click="remove(p)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
