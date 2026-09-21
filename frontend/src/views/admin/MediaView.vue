<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'
import MediaUploader from '@/components/admin/MediaUploader.vue'

const toast = useToast()
const items = ref([])
const selected = ref(null)
useHead('Médias — administration')

async function load() { items.value = await api.get('/api/admin/media', { auth: true }) }
onMounted(load)

function onUploaded(m) { items.value.unshift(m); selected.value = m }

async function saveAlt() {
  try {
    await api.patch(`/api/admin/media/${selected.value.id}`, { alt: selected.value.alt }, { auth: true })
    toast.success('Texte alternatif enregistré')
  } catch (e) { toast.error(e.message) }
}

async function remove(m) {
  if (!confirm(`Supprimer ${m.filename} ? Les pages qui l'utilisent afficheront une image manquante.`)) return
  await api.delete(`/api/admin/media/${m.id}`, { auth: true })
  selected.value = null
  toast.success('Média supprimé')
  await load()
}

async function copy(url) {
  try { await navigator.clipboard.writeText(url); toast.success('Adresse copiée') } catch { toast.error('Copie impossible') }
}

function size(bytes) { return bytes > 1024 * 1024 ? `${(bytes / 1048576).toFixed(1)} Mo` : `${Math.round(bytes / 1024)} Ko` }
</script>

<template>
  <div class="admin-head">
    <div><span class="kicker">Contenu</span><h1>Médias</h1><p>Images du site. Chaque image reçoit un texte alternatif pour l'accessibilité et le référencement.</p></div>
  </div>
  <div class="card"><MediaUploader @uploaded="onUploaded" /></div>

  <div class="feature" style="align-items: start; margin-top: 20px; grid-template-columns: 1.4fr 1fr">
    <div class="card">
      <p v-if="!items.length" class="empty">Aucun média. Téléversez une première image.</p>
      <div v-else class="media-grid">
        <button v-for="m in items" :key="m.id" type="button" class="media-item" :class="{ 'is-selected': selected?.id === m.id }" @click="selected = m">
          <div class="media-item__thumb"><img :src="m.url" :alt="m.alt" loading="lazy"></div>
          <span class="media-item__name">{{ m.filename }}</span>
        </button>
      </div>
    </div>
    <div v-if="selected" class="card">
      <div class="media-item__thumb" style="margin-bottom: 14px"><img :src="selected.url" :alt="selected.alt"></div>
      <p class="muted" style="font-size: 13px">{{ selected.filename }} · {{ selected.width ? `${selected.width}×${selected.height}` : 'vectoriel' }} · {{ size(selected.size_bytes) }}</p>
      <div class="field">
        <label for="alt">Texte alternatif</label>
        <input id="alt" v-model="selected.alt" type="text" maxlength="300" placeholder="Décrivez l'image en une phrase">
      </div>
      <div class="admin-actions" style="margin-top: 14px">
        <button type="button" class="btn btn--primary btn--small" @click="saveAlt">Enregistrer</button>
        <button type="button" class="btn btn--secondary btn--small" @click="copy(selected.url)">Copier l'adresse</button>
        <button type="button" class="btn btn--danger btn--small" @click="remove(selected)">Supprimer</button>
      </div>
    </div>
  </div>
</template>
