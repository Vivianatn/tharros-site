<script setup>
import { ref } from 'vue'
import MediaPicker from './MediaPicker.vue'

defineProps({ modelValue: { type: String, default: '' }, label: String, id: String, hint: String })
const emit = defineEmits(['update:modelValue'])
const picking = ref(false)
</script>

<template>
  <div class="field">
    <label :for="id">{{ label }}</label>
    <div style="display: flex; gap: 8px; align-items: center">
      <input :id="id" :value="modelValue" type="text" placeholder="/media/… ou /brand/…" @input="emit('update:modelValue', $event.target.value)">
      <button type="button" class="btn btn--secondary btn--small" @click="picking = true">Choisir</button>
      <button v-if="modelValue" type="button" class="btn btn--link" @click="emit('update:modelValue', '')">Retirer</button>
    </div>
    <img v-if="modelValue" :src="modelValue" alt="" style="max-height: 120px; width: auto; margin-top: 6px; border: 1px solid var(--pierre-claire)">
    <span v-if="hint" class="hint">{{ hint }}</span>
    <MediaPicker v-if="picking" @select="(m) => { emit('update:modelValue', m.url); picking = false }" @close="picking = false" />
  </div>
</template>
