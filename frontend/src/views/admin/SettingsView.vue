<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'
import MarkdownEditor from '@/components/admin/MarkdownEditor.vue'
import ImageField from '@/components/admin/ImageField.vue'
import RepeaterField from '@/components/admin/RepeaterField.vue'
import { SECTIONS } from './settingsSchema'

const route = useRoute()
const toast = useToast()
const section = computed(() => SECTIONS.find((s) => s.key === (route.params.section || 'home')) || SECTIONS[0])
const value = ref({})
const busy = ref(false)
useHead(computed(() => `${section.value.label} — pages du site`))

/** Les listes scalaires (tableau de chaînes) sont éditées comme des objets { value } puis reconverties. */
function toEditable(raw, fields) {
  const out = { ...raw }
  for (const f of fields) {
    if (f.type === 'list' && f.scalar) out[f.key] = (raw[f.key] || []).map((v) => ({ value: v }))
    if (f.type === 'list' && !f.scalar) out[f.key] = raw[f.key] || []
  }
  return out
}
function fromEditable(edited, fields) {
  const out = { ...edited }
  for (const f of fields) if (f.type === 'list' && f.scalar) out[f.key] = (edited[f.key] || []).map((o) => o.value)
  return out
}

async function load() {
  const all = await api.get('/api/admin/settings', { auth: true })
  const found = all.find((s) => s.key === section.value.key)
  value.value = toEditable(found?.value || {}, section.value.fields)
}
watch(section, load, { immediate: true })

async function save() {
  busy.value = true
  try {
    await api.put(`/api/admin/settings/${section.value.key}`, fromEditable(value.value, section.value.fields), { auth: true })
    toast.success(`${section.value.label} enregistré`)
  } catch (e) {
    toast.error(e.message)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="admin-head">
    <div><span class="kicker">Contenu</span><h1>Pages du site</h1><p>Textes, listes et images de chaque page. Les modifications sont visibles immédiatement.</p></div>
    <div class="admin-actions"><button type="button" class="btn btn--primary" :disabled="busy" @click="save">Enregistrer</button></div>
  </div>

  <nav class="tabs" aria-label="Sections">
    <RouterLink v-for="s in SECTIONS" :key="s.key" :to="{ name: 'admin.settings', params: { section: s.key } }">{{ s.label }}</RouterLink>
  </nav>

  <form class="card" @submit.prevent="save">
    <div class="form">
      <template v-for="f in section.fields" :key="f.key">
        <div v-if="f.type === 'text'" class="field"><label :for="f.key">{{ f.label }}</label><input :id="f.key" v-model="value[f.key]" type="text"></div>
        <div v-else-if="f.type === 'textarea'" class="field"><label :for="f.key">{{ f.label }}</label><textarea :id="f.key" v-model="value[f.key]" rows="3"></textarea></div>
        <div v-else-if="f.type === 'markdown'" class="field"><label :for="f.key">{{ f.label }}</label><MarkdownEditor :id="f.key" v-model="value[f.key]" :rows="12" /></div>
        <ImageField v-else-if="f.type === 'image'" :id="f.key" v-model="value[f.key]" :label="f.label" />
        <RepeaterField v-else-if="f.type === 'list'" v-model="value[f.key]" :fields="f.fields" :label="f.label" />
      </template>
    </div>
    <div class="admin-actions" style="margin-top: 24px"><button type="submit" class="btn btn--primary" :disabled="busy">Enregistrer</button></div>
  </form>
</template>
