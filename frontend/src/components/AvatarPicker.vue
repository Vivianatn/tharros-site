<script setup>
/** Choix parmi les 40 avatars prédéfinis (frontend/public/avatars). */
import { AVATARS } from '@/utils/avatars'

defineProps({ modelValue: { type: String, default: 'a01' } })
const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="avatars" role="radiogroup" aria-label="Image de profil">
    <button
      v-for="a in AVATARS" :key="a.id" type="button" role="radio" class="avatars__item"
      :class="{ 'is-selected': a.id === modelValue }" :aria-checked="a.id === modelValue" :title="a.label"
      @click="emit('update:modelValue', a.id)"
    >
      <img :src="`/avatars/${a.id}.svg`" :alt="a.label" width="64" height="64" loading="lazy">
    </button>
  </div>
</template>

<style scoped>
.avatars { display: grid; grid-template-columns: repeat(auto-fill, minmax(56px, 1fr)); gap: 8px; }
.avatars__item { padding: 0; background: none; border: 3px solid transparent; border-radius: 50%; cursor: pointer; transition: transform .2s var(--ease), border-color .2s; }
.avatars__item img { width: 100%; height: auto; border-radius: 50%; }
.avatars__item:hover { transform: scale(1.08); }
.avatars__item.is-selected { border-color: var(--or); box-shadow: 0 0 0 2px var(--encre); }
</style>
