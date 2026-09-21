<script setup>
import { onMounted, reactive, ref } from 'vue'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'

const toast = useToast()
const items = ref([])
const editing = ref(null) // id en cours d'édition, ou 'new'
const form = reactive({ question: '', answer_md: '', published: true })
useHead('FAQ — administration')

async function load() { items.value = await api.get('/api/admin/faq', { auth: true }) }
onMounted(load)

function startNew() { editing.value = 'new'; Object.assign(form, { question: '', answer_md: '', published: true }) }
function startEdit(it) { editing.value = it.id; Object.assign(form, { question: it.question, answer_md: it.answer_md, published: it.published }) }

async function save() {
  try {
    if (editing.value === 'new') await api.post('/api/admin/faq', { ...form, sort_order: items.value.length }, { auth: true })
    else {
      const it = items.value.find((i) => i.id === editing.value)
      await api.put(`/api/admin/faq/${it.id}`, { ...form, sort_order: it.sort_order }, { auth: true })
    }
    editing.value = null
    toast.success('Question enregistrée')
    await load()
  } catch (e) { toast.error(e.message) }
}

async function remove(it) {
  if (!confirm(`Supprimer « ${it.question} » ?`)) return
  await api.delete(`/api/admin/faq/${it.id}`, { auth: true })
  toast.success('Question supprimée')
  await load()
}

async function move(i, dir) {
  const j = i + dir
  if (j < 0 || j >= items.value.length) return
  const a = items.value[i]; const b = items.value[j]
  await Promise.all([
    api.put(`/api/admin/faq/${a.id}`, { ...a, sort_order: j }, { auth: true }),
    api.put(`/api/admin/faq/${b.id}`, { ...b, sort_order: i }, { auth: true }),
  ])
  await load()
}
</script>

<template>
  <div class="admin-head">
    <div><span class="kicker">Contenu</span><h1>FAQ</h1><p>Questions fréquentes, dans l'ordre d'affichage.</p></div>
    <div class="admin-actions"><button type="button" class="btn btn--primary" @click="startNew">Nouvelle question</button></div>
  </div>

  <form v-if="editing !== null" class="card" @submit.prevent="save">
    <h2>{{ editing === 'new' ? 'Nouvelle question' : 'Modifier la question' }}</h2>
    <div class="form">
      <div class="field"><label for="q">Question</label><input id="q" v-model="form.question" type="text" required maxlength="200"></div>
      <div class="field"><label for="a">Réponse (Markdown)</label><textarea id="a" v-model="form.answer_md" required rows="4"></textarea></div>
      <div class="field"><label class="switch"><input v-model="form.published" type="checkbox"> {{ form.published ? 'Visible' : 'Masquée' }}</label></div>
      <div class="admin-actions">
        <button type="submit" class="btn btn--primary">Enregistrer</button>
        <button type="button" class="btn btn--ghost btn--small" @click="editing = null">Annuler</button>
      </div>
    </div>
  </form>

  <div class="card card--flat table-wrap">
    <table class="table">
      <thead><tr><th style="width: 90px">Ordre</th><th>Question</th><th>État</th><th></th></tr></thead>
      <tbody>
        <tr v-if="!items.length"><td colspan="4" class="empty">Aucune question.</td></tr>
        <tr v-for="(it, i) in items" :key="it.id">
          <td><button type="button" class="btn btn--link" :disabled="i === 0" @click="move(i, -1)">↑</button><button type="button" class="btn btn--link" :disabled="i === items.length - 1" @click="move(i, 1)">↓</button></td>
          <td><strong>{{ it.question }}</strong><br><small class="muted">{{ it.answer_md.slice(0, 100) }}…</small></td>
          <td><span class="pill" :class="it.published ? 'pill--on' : 'pill--off'">{{ it.published ? 'Visible' : 'Masquée' }}</span></td>
          <td class="actions">
            <button type="button" class="btn btn--link" @click="startEdit(it)">Modifier</button>
            <button type="button" class="btn btn--link" style="color: var(--grenat-sombre)" @click="remove(it)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
