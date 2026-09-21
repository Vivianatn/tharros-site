<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'
import { formatDate } from '@/utils/format'

const emit = defineEmits(['unread-changed'])
const toast = useToast()
const items = ref([])
const open = ref(null)
useHead('Messages — administration')

async function load() { items.value = await api.get('/api/admin/messages', { auth: true }) }
onMounted(load)

async function show(m) {
  open.value = m
  if (!m.read) {
    await api.patch(`/api/admin/messages/${m.id}/read`, {}, { auth: true })
    m.read = true
    emit('unread-changed')
  }
}

async function remove(m) {
  if (!confirm('Supprimer ce message ?')) return
  await api.delete(`/api/admin/messages/${m.id}`, { auth: true })
  if (open.value?.id === m.id) open.value = null
  toast.success('Message supprimé')
  await load()
  emit('unread-changed')
}
</script>

<template>
  <div class="admin-head"><div><span class="kicker">Boîte de réception</span><h1>Messages</h1><p>Reçus via le formulaire de contact.</p></div></div>
  <div class="feature" style="align-items: start; grid-template-columns: 1fr 1.2fr">
    <div class="card card--flat table-wrap">
      <table class="table">
        <thead><tr><th>De</th><th>Objet</th><th>Date</th></tr></thead>
        <tbody>
          <tr v-if="!items.length"><td colspan="3" class="empty">Aucun message.</td></tr>
          <tr v-for="m in items" :key="m.id" style="cursor: pointer" @click="show(m)">
            <td><strong v-if="!m.read">{{ m.name }}</strong><span v-else>{{ m.name }}</span></td>
            <td>{{ m.subject }}</td>
            <td>{{ formatDate(m.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="open" class="card">
      <span class="kicker">{{ formatDate(open.created_at) }}</span>
      <h2>{{ open.subject }}</h2>
      <p class="muted">{{ open.name }} — <a :href="`mailto:${open.email}?subject=Re: ${encodeURIComponent(open.subject)}`">{{ open.email }}</a></p>
      <p style="white-space: pre-wrap">{{ open.body }}</p>
      <div class="admin-actions">
        <a class="btn btn--primary btn--small" :href="`mailto:${open.email}?subject=Re: ${encodeURIComponent(open.subject)}`">Répondre</a>
        <button type="button" class="btn btn--danger btn--small" @click="remove(open)">Supprimer</button>
      </div>
    </div>
  </div>
</template>
