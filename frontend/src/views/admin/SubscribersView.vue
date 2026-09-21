<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'
import { formatDate } from '@/utils/format'

const toast = useToast()
const items = ref([])
useHead('Liste d’attente — administration')

async function load() { items.value = await api.get('/api/admin/subscribers', { auth: true }) }
onMounted(load)

async function remove(s) {
  if (!confirm(`Désinscrire ${s.email} ?`)) return
  await api.delete(`/api/admin/subscribers/${s.id}`, { auth: true })
  toast.success('Adresse retirée')
  await load()
}

function exportCsv() {
  const csv = ['email;date'].concat(items.value.map((s) => `${s.email};${s.consented_at}`)).join('\n')
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }))
  a.download = 'liste-attente.csv'
  a.click()
}
</script>

<template>
  <div class="admin-head">
    <div><span class="kicker">Boîte de réception</span><h1>Liste d'attente</h1><p>{{ items.length }} inscrit·e·s. Consentement horodaté pour chaque adresse (RGPD).</p></div>
    <div class="admin-actions"><button type="button" class="btn btn--secondary" :disabled="!items.length" @click="exportCsv">Exporter en CSV</button></div>
  </div>
  <div class="card card--flat table-wrap">
    <table class="table">
      <thead><tr><th>E-mail</th><th>Inscription</th><th></th></tr></thead>
      <tbody>
        <tr v-if="!items.length"><td colspan="3" class="empty">Personne pour le moment.</td></tr>
        <tr v-for="s in items" :key="s.id">
          <td>{{ s.email }}</td>
          <td>{{ formatDate(s.consented_at) }}</td>
          <td class="actions"><button type="button" class="btn btn--link" style="color: var(--grenat-sombre)" @click="remove(s)">Désinscrire</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
