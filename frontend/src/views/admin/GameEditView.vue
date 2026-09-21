<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/api/client'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'
import { slugify } from '@/utils/format'
import MarkdownEditor from '@/components/admin/MarkdownEditor.vue'
import ImageField from '@/components/admin/ImageField.vue'
import RepeaterField from '@/components/admin/RepeaterField.vue'
import BuildManager from '@/components/admin/BuildManager.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const id = computed(() => route.params.id)
const isNew = computed(() => !id.value)
const busy = ref(false)
const slugTouched = ref(false)

const form = reactive({
  title: '', slug: '', status: 'En développement', tagline: '', pitch_md: '', cover_url: '', banner_url: '',
  specs: [], pillars: [], progress: [], featured: false, published: true, sort_order: 0, download_requires_account: false,
})
const builds = ref([])
useHead(computed(() => (isNew.value ? 'Nouveau jeu' : `Modifier : ${form.title}`)))

const kv = [{ key: 'k', label: 'Libellé' }, { key: 'v', label: 'Valeur', wide: true }]
const pillarFields = [{ key: 'num', label: 'Numéro' }, { key: 'title', label: 'Titre' }, { key: 'text', label: 'Texte', type: 'textarea', wide: true }]

onMounted(async () => {
  if (isNew.value) return
  const games = await api.get('/api/admin/games', { auth: true })
  const game = games.find((g) => String(g.id) === String(id.value))
  if (!game) { toast.error('Jeu introuvable'); return router.push({ name: 'admin.games' }) }
  const { builds: gameBuilds, ...rest } = game
  Object.assign(form, { ...rest, cover_url: game.cover_url || '', banner_url: game.banner_url || '' })
  builds.value = gameBuilds || []
  slugTouched.value = true
})

async function reloadBuilds() {
  const games = await api.get('/api/admin/games', { auth: true })
  builds.value = games.find((g) => String(g.id) === String(id.value))?.builds || []
}
watch(() => form.title, (t) => { if (!slugTouched.value) form.slug = slugify(t) })

async function save() {
  busy.value = true
  try {
    const { builds: _b, ...fields } = form
    const payload = { ...fields, cover_url: form.cover_url || null, banner_url: form.banner_url || null }
    const saved = isNew.value
      ? await api.post('/api/admin/games', payload, { auth: true })
      : await api.put(`/api/admin/games/${id.value}`, payload, { auth: true })
    toast.success('Jeu enregistré')
    if (isNew.value) router.replace({ name: 'admin.game.edit', params: { id: saved.id } })
  } catch (e) {
    toast.error(e.message)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <form @submit.prevent="save">
    <div class="admin-head">
      <div><span class="kicker">Jeux</span><h1>{{ isNew ? 'Nouveau jeu' : form.title }}</h1></div>
      <div class="admin-actions">
        <button type="button" class="btn btn--ghost btn--small" @click="router.push({ name: 'admin.games' })">Retour</button>
        <button type="submit" class="btn btn--primary" :disabled="busy">Enregistrer</button>
      </div>
    </div>

    <div class="card">
      <h2>Identité</h2>
      <div class="form-grid">
        <div class="field"><label for="title">Titre</label><input id="title" v-model="form.title" type="text" required maxlength="120"></div>
        <div class="field"><label for="slug">Adresse (slug)</label><input id="slug" v-model="form.slug" type="text" @input="slugTouched = true"><span class="hint">/jeux/{{ form.slug || '…' }}</span></div>
        <div class="field"><label for="status">Statut</label><input id="status" v-model="form.status" type="text" maxlength="60" placeholder="En développement, Sortie 2027, Disponible…"></div>
        <div class="field"><label for="order">Ordre d'affichage</label><input id="order" v-model.number="form.sort_order" type="number"></div>
        <div class="field span-2"><label for="tagline">Accroche</label><textarea id="tagline" v-model="form.tagline" rows="2" maxlength="300"></textarea></div>
        <div class="field"><label>Mis en avant (accueil, presse)</label><label class="switch"><input v-model="form.featured" type="checkbox"> {{ form.featured ? 'Oui' : 'Non' }}</label></div>
        <div class="field"><label>Visible sur le site</label><label class="switch"><input v-model="form.published" type="checkbox"> {{ form.published ? 'Publié' : 'Masqué' }}</label></div>
      </div>
    </div>

    <div class="card">
      <h2>Visuels</h2>
      <div class="form-grid">
        <ImageField id="cover" v-model="form.cover_url" label="Visuel clé (4:3)" />
        <ImageField id="banner" v-model="form.banner_url" label="Bannière large (16:7)" />
      </div>
    </div>

    <div class="card">
      <h2>Téléchargements</h2>
      <p class="hint" style="margin-top: -8px; margin-bottom: 16px">Déposez le fichier du jeu pour chaque système. Sur la fiche publique, un bouton « Télécharger » proposera automatiquement le bon système au visiteur.</p>
      <div class="field" style="margin-bottom: 16px"><label class="switch"><input v-model="form.download_requires_account" type="checkbox"> {{ form.download_requires_account ? 'Réservé aux joueurs connectés' : 'Téléchargement libre (sans compte)' }}</label><span class="hint">Pensez à enregistrer la fiche après avoir changé ce réglage.</span></div>
      <BuildManager v-if="!isNew" :game-id="Number(id)" :builds="builds" @changed="reloadBuilds" />
      <p v-else class="hint">Enregistrez d'abord la fiche pour pouvoir ajouter des fichiers.</p>
    </div>

    <div class="card">
      <h2>Présentation</h2>
      <div class="field"><label for="pitch">Pitch</label><MarkdownEditor id="pitch" v-model="form.pitch_md" :rows="10" /></div>
    </div>

    <div class="card">
      <h2>Fiche technique</h2>
      <RepeaterField v-model="form.specs" :fields="kv" label="Spécifications (genre, plateforme, sortie…)" add-label="Ajouter une ligne" />
    </div>
    <div class="card">
      <h2>Piliers de design</h2>
      <RepeaterField v-model="form.pillars" :fields="pillarFields" label="Trois piliers recommandés" add-label="Ajouter un pilier" />
    </div>
    <div class="card">
      <h2>État d'avancement</h2>
      <RepeaterField v-model="form.progress" :fields="kv" label="Terminé / En cours / À venir" add-label="Ajouter une ligne" />
    </div>
  </form>
</template>
