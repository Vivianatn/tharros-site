<script setup>
import { ref } from 'vue'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'

const emit = defineEmits(['uploaded'])
const toast = useToast()
const over = ref(false)
const busy = ref(false)
const input = ref(null)

async function upload(files) {
  for (const file of files) {
    busy.value = true
    try {
      const form = new FormData()
      form.append('file', file)
      const media = await api.upload('/api/admin/media', form, { auth: true })
      emit('uploaded', media)
      toast.success(`${file.name} téléversé (optimisé en ${media.filename.split('.').pop().toUpperCase()})`)
    } catch (e) {
      toast.error(`${file.name} : ${e.message}`)
    } finally {
      busy.value = false
    }
  }
}

function onDrop(e) {
  over.value = false
  upload(e.dataTransfer.files)
}
</script>

<template>
  <div class="dropzone" :class="{ 'is-over': over }" @dragover.prevent="over = true" @dragleave="over = false" @drop.prevent="onDrop" @click="input.click()">
    <input ref="input" type="file" accept="image/png,image/jpeg,image/webp,image/gif,image/svg+xml" multiple hidden @change="upload($event.target.files); $event.target.value = ''">
    <strong>{{ busy ? 'Téléversement…' : 'Glissez des images ici ou cliquez' }}</strong>
    <br><small>PNG, JPEG, WebP, GIF ou SVG · 10 Mo max · redimensionnées et converties en WebP automatiquement</small>
  </div>
</template>
