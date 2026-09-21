<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import MediaUploader from './MediaUploader.vue'

const emit = defineEmits(['select', 'close'])
const toast = useToast()
const items = ref([])
const loading = ref(true)

async function load() {
  try { items.value = await api.get('/api/admin/media', { auth: true }) } catch (e) { toast.error(e.message) } finally { loading.value = false }
}
onMounted(load)

function onUploaded(media) {
  items.value.unshift(media)
  emit('select', media)
}
</script>

<template>
  <div class="modal-backdrop" @click.self="emit('close')">
    <div class="modal" role="dialog" aria-modal="true" aria-label="Choisir un média">
      <div class="modal__head">
        <h2 style="margin: 0">Médiathèque</h2>
        <button type="button" class="btn btn--ghost btn--small" @click="emit('close')">Fermer</button>
      </div>
      <MediaUploader @uploaded="onUploaded" />
      <p v-if="loading" class="empty">Chargement…</p>
      <p v-else-if="!items.length" class="empty">Aucun média pour le moment : téléversez une image ci-dessus.</p>
      <div v-else class="media-grid" style="margin-top: 16px">
        <button v-for="m in items" :key="m.id" type="button" class="media-item" @click="emit('select', m)">
          <div class="media-item__thumb"><img :src="m.url" :alt="m.alt" loading="lazy"></div>
          <span class="media-item__name">{{ m.filename }}</span>
        </button>
      </div>
    </div>
  </div>
</template>
