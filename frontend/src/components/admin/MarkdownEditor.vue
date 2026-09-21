<script setup>
import { computed, ref } from 'vue'
import { renderMarkdown } from '@/utils/markdown'
import MediaPicker from './MediaPicker.vue'

const props = defineProps({ modelValue: { type: String, default: '' }, id: String, rows: { type: Number, default: 14 } })
const emit = defineEmits(['update:modelValue'])

const preview = ref(false)
const picker = ref(false)
const textarea = ref(null)
const html = computed(() => renderMarkdown(props.modelValue))

/** Entoure la sélection (ou insère un modèle) dans le textarea. */
function wrap(before, after = '', placeholder = 'texte') {
  const el = textarea.value
  const start = el.selectionStart
  const end = el.selectionEnd
  const value = props.modelValue
  const selected = value.slice(start, end) || placeholder
  const next = value.slice(0, start) + before + selected + after + value.slice(end)
  emit('update:modelValue', next)
  requestAnimationFrame(() => {
    el.focus()
    el.setSelectionRange(start + before.length, start + before.length + selected.length)
  })
}

function insertImage(media) {
  picker.value = false
  wrap(`![${media.alt || 'description de l’image'}](${media.url})`, '', '')
}
</script>

<template>
  <div class="md-editor">
    <div class="md-editor__bar" role="toolbar" aria-label="Mise en forme">
      <button type="button" title="Titre" @click="wrap('## ', '', 'Titre')">H2</button>
      <button type="button" title="Sous-titre" @click="wrap('### ', '', 'Sous-titre')">H3</button>
      <button type="button" title="Gras" @click="wrap('**', '**')"><b>B</b></button>
      <button type="button" title="Italique" @click="wrap('*', '*')"><i>I</i></button>
      <button type="button" title="Lien" @click="wrap('[', '](https://)', 'texte du lien')">Lien</button>
      <button type="button" title="Liste" @click="wrap('- ', '', 'élément')">Liste</button>
      <button type="button" title="Citation" @click="wrap('> ', '', 'citation')">Citation</button>
      <button type="button" title="Image depuis la médiathèque" @click="picker = true">Image</button>
      <span style="flex: 1"></span>
      <button type="button" :class="{ 'is-active': !preview }" @click="preview = false">Éditer</button>
      <button type="button" :class="{ 'is-active': preview }" @click="preview = true">Aperçu</button>
    </div>
    <div v-if="preview" class="md-editor__preview prose" v-html="html"></div>
    <textarea v-else :id="id" ref="textarea" :value="modelValue" :rows="rows" spellcheck="true" @input="emit('update:modelValue', $event.target.value)"></textarea>
    <span class="hint">Markdown : **gras**, *italique*, ## titre, - liste, [lien](url), ![image](url).</span>
    <MediaPicker v-if="picker" @select="insertImage" @close="picker = false" />
  </div>
</template>
