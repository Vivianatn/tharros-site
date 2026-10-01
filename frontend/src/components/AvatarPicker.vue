<script setup>
/**
 * Choix de l'image de profil parmi les 100 avatars prédéfinis.
 * Grand aperçu à gauche, grille filtrable à droite.
 */
import { computed, ref } from 'vue'
import { AVATARS, avatarLabel, avatarUrl } from '@/utils/avatars'

const props = defineProps({
  modelValue: { type: String, default: '001' },
  preview: { type: Boolean, default: true },
})
const emit = defineEmits(['update:modelValue'])

const query = ref('')

/** Recherche insensible aux accents et à la casse. */
const normalize = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
const results = computed(() => {
  const q = normalize(query.value.trim())
  return q ? AVATARS.filter((a) => normalize(a.label).includes(q)) : AVATARS
})
const currentLabel = computed(() => avatarLabel(props.modelValue))

function pickRandom() {
  const pool = results.value.length ? results.value : AVATARS
  emit('update:modelValue', pool[Math.floor(Math.random() * pool.length)].id)
}
</script>

<template>
  <div class="picker" :class="{ 'picker--with-preview': preview }">
    <div v-if="preview" class="picker__preview">
      <img :src="avatarUrl(modelValue)" :alt="`Avatar sélectionné : ${currentLabel}`" width="256" height="256">
      <strong>{{ currentLabel }}</strong>
      <small class="muted">Avatar {{ modelValue }} sur {{ AVATARS.length }}</small>
    </div>

    <div class="picker__choose">
      <div class="picker__tools">
        <input v-model="query" type="search" :placeholder="`Rechercher parmi ${AVATARS.length} avatars…`" aria-label="Rechercher un avatar">
        <button type="button" class="picker__random" title="Choisir au hasard" @click="pickRandom">Au hasard</button>
      </div>
      <p v-if="!results.length" class="muted picker__empty">Aucun avatar ne correspond à « {{ query }} ».</p>
      <div v-else class="picker__grid" role="radiogroup" aria-label="Image de profil">
        <button
          v-for="a in results" :key="a.id" type="button" role="radio" class="picker__item"
          :class="{ 'is-selected': a.id === modelValue }" :aria-checked="a.id === modelValue" :title="a.label"
          @click="emit('update:modelValue', a.id)"
        >
          <img :src="`/avatars/${a.id}.svg`" :alt="a.label" width="64" height="64" loading="lazy" decoding="async">
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.picker { display: grid; gap: 20px; }
@media (min-width: 720px) {
  .picker--with-preview { grid-template-columns: 200px 1fr; align-items: start; }
}
.picker__preview { display: grid; justify-items: center; gap: 6px; text-align: center; }
.picker__preview img { width: min(200px, 60vw); height: auto; border-radius: 50%; border: 3px solid var(--or); background: var(--encre); }
.picker__preview strong { font-size: 17px; margin-top: 6px; }
.picker__preview small { font-size: 12px; letter-spacing: .1em; text-transform: uppercase; }
.picker__tools { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; }
.picker__tools input { flex: 1 1 200px; font: inherit; padding: 10px 14px; background: var(--input-bg); color: var(--input-fg); border: 2px solid var(--input-border); }
.picker__tools input:focus { border-color: var(--or); outline: none; }
.picker__random { background: none; border: 2px solid var(--input-border); color: var(--fg); padding: 10px 16px; cursor: pointer; font: inherit; font-weight: 700; font-size: 13px; letter-spacing: .06em; text-transform: uppercase; }
.picker__random:hover { border-color: var(--or); color: var(--or); }
.picker__grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(58px, 1fr)); gap: 8px;
  max-height: 340px; overflow-y: auto; padding: 4px; border: 1px solid var(--line);
}
.picker__item { padding: 0; background: none; border: 3px solid transparent; border-radius: 50%; cursor: pointer; transition: transform .18s var(--ease), border-color .18s; }
.picker__item img { width: 100%; height: auto; border-radius: 50%; display: block; }
.picker__item:hover { transform: scale(1.09); }
.picker__item.is-selected { border-color: var(--or); }
.picker__empty { padding: 20px 4px; }
</style>
