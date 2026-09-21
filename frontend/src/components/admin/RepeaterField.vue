<script setup>
/**
 * Liste répétable d'objets (spécifications, piliers, chronologie…).
 * fields : [{ key, label, type: 'text' | 'textarea' | 'checkbox' | 'image', wide: bool }]
 */
import { ref } from 'vue'
import MediaPicker from './MediaPicker.vue'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  fields: { type: Array, required: true },
  label: String,
  addLabel: { type: String, default: 'Ajouter un élément' },
})
const emit = defineEmits(['update:modelValue'])
const pickingFor = ref(null)

function update(list) { emit('update:modelValue', list) }
function set(i, key, value) {
  const list = props.modelValue.map((it, idx) => (idx === i ? { ...it, [key]: value } : it))
  update(list)
}
function add() {
  const blank = Object.fromEntries(props.fields.map((f) => [f.key, f.type === 'checkbox' ? false : '']))
  update([...props.modelValue, blank])
}
function remove(i) { update(props.modelValue.filter((_, idx) => idx !== i)) }
function move(i, dir) {
  const j = i + dir
  if (j < 0 || j >= props.modelValue.length) return
  const list = [...props.modelValue]
  ;[list[i], list[j]] = [list[j], list[i]]
  update(list)
}
function pick(media) {
  set(pickingFor.value.index, pickingFor.value.key, media.url)
  pickingFor.value = null
}
</script>

<template>
  <div class="field">
    <label v-if="label">{{ label }}</label>
    <div class="repeater">
      <div v-for="(item, i) in modelValue" :key="i" class="repeater__item">
        <div class="repeater__fields">
          <div v-for="f in fields" :key="f.key" class="field" :class="{ wide: f.wide }">
            <label :for="`rep-${label}-${i}-${f.key}`" style="font-size: 11px">{{ f.label }}</label>
            <textarea v-if="f.type === 'textarea'" :id="`rep-${label}-${i}-${f.key}`" :value="item[f.key]" rows="3" @input="set(i, f.key, $event.target.value)"></textarea>
            <label v-else-if="f.type === 'checkbox'" class="switch"><input type="checkbox" :checked="item[f.key]" @change="set(i, f.key, $event.target.checked)"> {{ item[f.key] ? 'Oui' : 'Non' }}</label>
            <div v-else-if="f.type === 'image'" style="display: flex; gap: 8px">
              <input :id="`rep-${label}-${i}-${f.key}`" :value="item[f.key]" type="text" placeholder="/media/…" @input="set(i, f.key, $event.target.value)">
              <button type="button" class="btn btn--secondary btn--small" @click="pickingFor = { index: i, key: f.key }">Choisir</button>
            </div>
            <input v-else :id="`rep-${label}-${i}-${f.key}`" :value="item[f.key]" type="text" @input="set(i, f.key, $event.target.value)">
          </div>
        </div>
        <div class="repeater__tools">
          <button type="button" title="Monter" :disabled="i === 0" @click="move(i, -1)">↑</button>
          <button type="button" title="Descendre" :disabled="i === modelValue.length - 1" @click="move(i, 1)">↓</button>
          <button type="button" title="Supprimer" @click="remove(i)">✕</button>
        </div>
      </div>
      <div><button type="button" class="btn btn--secondary btn--small" @click="add">+ {{ addLabel }}</button></div>
    </div>
    <MediaPicker v-if="pickingFor" @select="pick" @close="pickingFor = null" />
  </div>
</template>
