<script setup>
/**
 * Téléchargements d'un jeu : un fichier par plateforme (Windows, macOS, Linux).
 * Envoi en XHR pour afficher la progression (les builds font souvent des centaines de Mo).
 */
import { reactive } from 'vue'
import { getToken } from '@/api/client'
import { useToast } from '@/composables/useToast'

const props = defineProps({ gameId: { type: Number, required: true }, builds: { type: Array, default: () => [] } })
const emit = defineEmits(['changed'])
const toast = useToast()

const PLATFORMS = [
  { key: 'windows', label: 'Windows', hint: '.zip, .exe ou .msi' },
  { key: 'macos', label: 'macOS', hint: '.dmg, .pkg ou .zip' },
  { key: 'linux', label: 'Linux', hint: '.AppImage, .tar.gz, .deb ou .zip' },
]
const state = reactive(Object.fromEntries(PLATFORMS.map((p) => [p.key, { version: '', progress: 0, busy: false }])))

function current(platform) { return props.builds.find((b) => b.platform === platform) }
function size(bytes) { return bytes > 1024 * 1024 ? `${(bytes / 1048576).toFixed(0)} Mo` : `${Math.round(bytes / 1024)} Ko` }

function upload(platform, file) {
  if (!file) return
  const st = state[platform]
  st.busy = true
  st.progress = 0
  const form = new FormData()
  form.append('file', file)
  form.append('platform', platform)
  form.append('version', st.version)
  const xhr = new XMLHttpRequest()
  xhr.open('POST', `/api/admin/games/${props.gameId}/builds`)
  xhr.setRequestHeader('Authorization', `Bearer ${getToken()}`)
  xhr.upload.onprogress = (e) => { if (e.lengthComputable) st.progress = Math.round((e.loaded / e.total) * 100) }
  xhr.onload = () => {
    st.busy = false
    if (xhr.status === 201) {
      toast.success(`Build ${platform} en ligne (${size(file.size)})`)
      st.version = ''
      emit('changed')
    } else {
      let msg = `Erreur ${xhr.status}`
      try { msg = JSON.parse(xhr.responseText).detail || msg } catch { /* réponse non JSON */ }
      toast.error(msg)
    }
  }
  xhr.onerror = () => { st.busy = false; toast.error('Téléversement interrompu') }
  xhr.send(form)
}

async function remove(build) {
  if (!confirm(`Supprimer le build ${build.platform} (${build.original_name}) ?`)) return
  const res = await fetch(`/api/admin/games/${props.gameId}/builds/${build.id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${getToken()}` } })
  if (res.ok) { toast.success('Build supprimé'); emit('changed') } else toast.error('Suppression impossible')
}
</script>

<template>
  <div class="builds">
    <div v-for="p in PLATFORMS" :key="p.key" class="build">
      <div class="build__head">
        <strong>{{ p.label }}</strong>
        <span class="hint">{{ p.hint }}</span>
      </div>
      <div v-if="current(p.key)" class="build__current">
        <span class="pill pill--on">En ligne</span>
        <span>{{ current(p.key).original_name }}<template v-if="current(p.key).version"> · v{{ current(p.key).version }}</template> · {{ size(current(p.key).size_bytes) }} · {{ current(p.key).downloads }} téléchargement{{ current(p.key).downloads > 1 ? 's' : '' }}</span>
        <a class="btn btn--link" :href="`/api/downloads/${current(p.key).id}`">Tester</a>
        <button type="button" class="btn btn--link" style="color: var(--grenat-sombre)" @click="remove(current(p.key))">Supprimer</button>
      </div>
      <p v-else class="hint">Aucun fichier pour cette plateforme : le bouton n'apparaîtra pas sur le site.</p>
      <div class="build__upload">
        <div class="field" style="max-width: 160px">
          <label :for="`v-${p.key}`">Version</label>
          <input :id="`v-${p.key}`" v-model="state[p.key].version" type="text" maxlength="40" placeholder="1.0.0">
        </div>
        <div class="field">
          <label :for="`f-${p.key}`">{{ current(p.key) ? 'Remplacer le fichier' : 'Fichier du jeu' }}</label>
          <input :id="`f-${p.key}`" type="file" :disabled="state[p.key].busy" @change="upload(p.key, $event.target.files[0]); $event.target.value = ''">
        </div>
      </div>
      <div v-if="state[p.key].busy" class="progress" role="progressbar" :aria-valuenow="state[p.key].progress" aria-valuemin="0" aria-valuemax="100">
        <div class="progress__bar" :style="{ width: state[p.key].progress + '%' }"></div>
        <span>{{ state[p.key].progress < 100 ? `Envoi… ${state[p.key].progress} %` : 'Enregistrement…' }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.builds { display: grid; gap: 16px; }
.build { border: 1px solid var(--pierre-claire); background: var(--marbre); padding: 16px 18px; display: grid; gap: 10px; }
.build__head { display: flex; align-items: baseline; gap: 12px; font-size: 16px; }
.build__current { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; font-size: 14px; }
.build__upload { display: flex; flex-wrap: wrap; gap: 14px; align-items: end; }
.build__upload input[type="file"] { padding: 8px; background: var(--blanc); }
.progress { position: relative; height: 26px; background: var(--pierre-claire); overflow: hidden; font-size: 12px; font-weight: 700; display: grid; place-items: center; }
.progress__bar { position: absolute; inset: 0 auto 0 0; background: var(--or); transition: width .2s; }
.progress span { position: relative; }
</style>
