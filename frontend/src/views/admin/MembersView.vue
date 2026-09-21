<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'
import { formatDate } from '@/utils/format'
import { avatarUrl } from '@/utils/avatars'

const toast = useToast()
const items = ref([])
useHead('Comptes joueurs — administration')

async function load() { items.value = await api.get('/api/admin/members', { auth: true }) }
onMounted(load)

async function remove(m) {
  if (!confirm(`Supprimer le compte de ${m.email} ?`)) return
  await api.delete(`/api/admin/members/${m.id}`, { auth: true })
  toast.success('Compte supprimé')
  await load()
}
</script>

<template>
  <div class="admin-head">
    <div><span class="kicker">Boîte de réception</span><h1>Comptes joueurs</h1><p>{{ items.length }} compte{{ items.length > 1 ? 's' : '' }} créé{{ items.length > 1 ? 's' : '' }} depuis le site. Les mots de passe sont hachés et ne sont jamais visibles.</p></div>
  </div>
  <div class="card card--flat table-wrap">
    <table class="table">
      <thead><tr><th>Pseudo</th><th>E-mail</th><th>Nouvelles</th><th>Inscription</th><th>Dernière connexion</th><th></th></tr></thead>
      <tbody>
        <tr v-if="!items.length"><td colspan="6" class="empty">Aucun compte pour le moment.</td></tr>
        <tr v-for="m in items" :key="m.id">
          <td style="display: flex; align-items: center; gap: 10px"><img :src="avatarUrl(m.avatar)" alt="" width="32" height="32" style="border-radius: 50%"><strong>{{ m.display_name }}</strong></td>
          <td>{{ m.email }}</td>
          <td><span class="pill" :class="m.newsletter ? 'pill--on' : 'pill--off'">{{ m.newsletter ? 'Oui' : 'Non' }}</span></td>
          <td>{{ formatDate(m.created_at) }}</td>
          <td>{{ formatDate(m.last_login_at) }}</td>
          <td class="actions"><button type="button" class="btn btn--link" style="color: var(--grenat-sombre)" @click="remove(m)">Supprimer</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
