<script setup>
/**
 * Lecteur d'animation de devlog : page HTML autonome jouée dans un cadre isolé.
 * Le cadre est en bac à sable (sans accès au site) et ne se charge qu'à la demande,
 * pour ne pas peser sur l'ouverture du billet.
 */
import { ref } from 'vue'
import IconArrow from './IconArrow.vue'

defineProps({ src: { type: String, required: true }, title: { type: String, default: 'Animation du devlog' } })
const started = ref(false)
const frame = ref(null)

function fullscreen() {
  const el = frame.value
  ;(el?.requestFullscreen || el?.webkitRequestFullscreen)?.call(el)
}
</script>

<template>
  <figure class="devlog">
    <div class="devlog__frame">
      <iframe
        v-if="started" ref="frame" :src="src" :title="title" class="devlog__iframe"
        sandbox="allow-scripts" allow="fullscreen" allowfullscreen loading="lazy"
      ></iframe>
      <button v-else type="button" class="devlog__poster" @click="started = true">
        <img src="/brand/tharros-embleme-clair.svg" alt="" width="96" height="96" aria-hidden="true">
        <span class="btn btn--primary">Lancer l'animation <IconArrow /></span>
        <small>{{ title }}</small>
      </button>
    </div>
    <figcaption class="devlog__bar">
      <span class="muted">Animation interactive — commandes de lecture dans le cadre.</span>
      <span class="devlog__actions">
        <button v-if="started" type="button" class="link-arrow" @click="fullscreen">Plein écran</button>
        <a class="link-arrow" :href="src" target="_blank" rel="noopener">Ouvrir dans un onglet</a>
      </span>
    </figcaption>
  </figure>
</template>

<style scoped>
.devlog { margin: 0 0 40px; display: grid; gap: 10px; }
.devlog__frame { position: relative; aspect-ratio: 16 / 9; background: var(--encre); clip-path: var(--chamfer); overflow: hidden; }
.devlog__iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; display: block; }
.devlog__poster { position: absolute; inset: 0; width: 100%; display: grid; place-content: center; justify-items: center; gap: 16px; padding: 24px; cursor: pointer; border: 0; background: radial-gradient(60% 70% at 50% 40%, rgba(193, 31, 53, .35), transparent 70%), var(--encre); }
.devlog__poster img { opacity: .9; transition: transform .4s var(--ease-out); }
.devlog__poster:hover img { transform: scale(1.06); }
.devlog__poster small { color: var(--pierre-douce); font-size: 13px; letter-spacing: .12em; text-transform: uppercase; }
.devlog__bar { display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; font-size: 14px; }
.devlog__actions { display: flex; gap: 20px; }
.devlog__actions button { background: none; border: 0; cursor: pointer; padding: 0; font: inherit; font-weight: 700; color: var(--fg); }
.devlog__actions button:hover { color: var(--link); }
</style>
