<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'
import { slugify, toLocalInput, fromLocalInput } from '@/utils/format'
import MarkdownEditor from '@/components/admin/MarkdownEditor.vue'
import ImageField from '@/components/admin/ImageField.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const id = computed(() => route.params.id)
const isNew = computed(() => !id.value)
const busy = ref(false)
const slugTouched = ref(false)

const form = reactive({ title: '', slug: '', tag: 'Devlog', excerpt: '', body_md: '', cover_url: '', published: false, published_at: '' })
useHead(computed(() => (isNew.value ? 'Nouveau billet' : `Modifier : ${form.title}`)))

onMounted(async () => {
  if (isNew.value) return
  const posts = await api.get('/api/admin/posts', { auth: true })
  const post = posts.find((p) => String(p.id) === String(id.value))
  if (!post) { toast.error('Billet introuvable'); return router.push({ name: 'admin.posts' }) }
  Object.assign(form, { ...post, cover_url: post.cover_url || '', published_at: toLocalInput(post.published_at) })
  slugTouched.value = true
})

watch(() => form.title, (t) => { if (!slugTouched.value) form.slug = slugify(t) })

async function save(publish = null) {
  busy.value = true
  try {
    const payload = { ...form, cover_url: form.cover_url || null, published_at: fromLocalInput(form.published_at) }
    if (publish !== null) payload.published = publish
    const saved = isNew.value
      ? await api.post('/api/admin/posts', payload, { auth: true })
      : await api.put(`/api/admin/posts/${id.value}`, payload, { auth: true })
    toast.success(saved.published ? 'Billet publié' : 'Brouillon enregistré')
    if (isNew.value) router.replace({ name: 'admin.post.edit', params: { id: saved.id } })
    else Object.assign(form, { ...saved, cover_url: saved.cover_url || '', published_at: toLocalInput(saved.published_at) })
  } catch (e) {
    toast.error(e.message)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <form @submit.prevent="save()">
    <div class="admin-head">
      <div><span class="kicker">Journal</span><h1>{{ isNew ? 'Nouveau billet' : 'Modifier le billet' }}</h1></div>
      <div class="admin-actions">
        <button type="button" class="btn btn--ghost btn--small" @click="router.push({ name: 'admin.posts' })">Retour</button>
        <button type="submit" class="btn btn--secondary" :disabled="busy">Enregistrer</button>
        <button v-if="!form.published" type="button" class="btn btn--primary" :disabled="busy" @click="save(true)">Publier</button>
        <a v-else class="btn btn--primary" :href="`/journal/${form.slug}`" target="_blank" rel="noopener">Voir en ligne</a>
      </div>
    </div>

    <div class="card">
      <div class="form-grid">
        <div class="field span-2">
          <label for="title">Titre</label>
          <input id="title" v-model="form.title" type="text" required maxlength="160">
        </div>
        <div class="field">
          <label for="slug">Adresse (slug)</label>
          <input id="slug" v-model="form.slug" type="text" maxlength="160" @input="slugTouched = true">
          <span class="hint">/journal/{{ form.slug || '…' }}</span>
        </div>
        <div class="field">
          <label for="tag">Étiquette</label>
          <input id="tag" v-model="form.tag" type="text" maxlength="40" placeholder="Devlog n° 7">
        </div>
        <div class="field span-2">
          <label for="excerpt">Résumé (affiché dans les listes et pour le référencement)</label>
          <textarea id="excerpt" v-model="form.excerpt" maxlength="400" rows="2"></textarea>
        </div>
        <div class="span-2"><ImageField id="cover" v-model="form.cover_url" label="Image de couverture" hint="Facultative. Affichée en tête du billet." /></div>
        <div class="field span-2">
          <label for="body">Contenu</label>
          <MarkdownEditor id="body" v-model="form.body_md" />
        </div>
        <div class="field">
          <label>Publication</label>
          <label class="switch"><input v-model="form.published" type="checkbox"> {{ form.published ? 'Publié' : 'Brouillon' }}</label>
        </div>
        <div class="field">
          <label for="date">Date de publication</label>
          <input id="date" v-model="form.published_at" type="datetime-local">
          <span class="hint">Vide = maintenant. Une date future programme la publication.</span>
        </div>
      </div>
    </div>
  </form>
</template>
