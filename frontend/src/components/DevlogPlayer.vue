<script setup>
/**
 * Lecteur d'animation de devlog : page HTML autonome jouée dans un cadre isolé.
 *
 * L'animation garde sa scène en 16/9 et y ajoute son en-tête et sa barre de chapitres,
 * de hauteur fixe. On calcule donc la plus grande taille qui tient dans la place
 * disponible — en largeur comme en hauteur — pour ne jamais faire défiler dans le cadre.
 */
import { onBeforeUnmount, onMounted, ref } from 'vue'
import IconArrow from './IconArrow.vue'

defineProps({ src: { type: String, required: true }, title: { type: String, default: 'Animation du devlog' } })

const CHROME_HEIGHT = 250 // en-tête + commandes + chapitres de l'animation
const MIN_WIDTH = 280

const started = ref(false)
const isFullscreen = ref(false)
const box = ref(null)
const frame = ref(null)
const size = ref({ width: 0, height: 0 })
const reportedHeight = ref(0) // hauteur annoncée par l'animation (postMessage)

/** Plus grande taille 16/9 (+ bandeau fixe) tenant dans la largeur et la hauteur offertes. */
function fit(availableWidth, availableHeight) {
  const widthFromHeight = (availableHeight - CHROME_HEIGHT) * (16 / 9)
  const width = Math.max(MIN_WIDTH, Math.min(availableWidth, widthFromHeight))
  return { width: Math.round(width), height: Math.round(width * (9 / 16) + CHROME_HEIGHT) }
}

function resize() {
  const next = isFullscreen.value
    ? fit(window.innerWidth, window.innerHeight)
    : box.value ? fit(box.value.clientWidth, Math.max(420, window.innerHeight * 0.86)) : size.value
  // L'animation connaît sa hauteur exacte (barre de chapitres sur plusieurs lignes en étroit) :
  // on l'applique pour qu'elle ne défile jamais dans le cadre.
  if (reportedHeight.value && !isFullscreen.value) next.height = Math.max(next.height, reportedHeight.value)
  size.value = next
}

function onMessage(event) {
  const h = Number(event.data?.tharrosHeight)
  if (h > 0 && h < 4000 && h !== reportedHeight.value) {
    reportedHeight.value = h
    resize()
  }
}

function onFullscreenChange() {
  isFullscreen.value = document.fullscreenElement === frame.value
  resize()
}

async function toggleFullscreen() {
  if (isFullscreen.value) {
    await document.exitFullscreen?.()
    return
  }
  started.value = true
  await new Promise((r) => requestAnimationFrame(r))
  const el = frame.value
  try {
    await (el?.requestFullscreen?.() ?? el?.webkitRequestFullscreen?.())
  } catch { /* refusé par le navigateur : on reste en lecture normale */ }
}

let observer
onMounted(() => {
  resize()
  observer = new ResizeObserver(resize)
  if (box.value) observer.observe(box.value)
  window.addEventListener('resize', resize)
  window.addEventListener('message', onMessage)
  document.addEventListener('fullscreenchange', onFullscreenChange)
})
onBeforeUnmount(() => {
  observer?.disconnect()
  window.removeEventListener('resize', resize)
  window.removeEventListener('message', onMessage)
  document.removeEventListener('fullscreenchange', onFullscreenChange)
})
</script>

<template>
  <figure class="devlog">
    <div ref="box" class="devlog__slot">
      <div ref="frame" class="devlog__frame" :class="{ 'is-fullscreen': isFullscreen }">
        <div class="devlog__inner" :style="{ width: size.width + 'px', height: size.height + 'px' }">
          <iframe
            v-if="started" :src="src" :title="title" class="devlog__iframe"
            sandbox="allow-scripts" allow="fullscreen" allowfullscreen
          ></iframe>
          <button v-else type="button" class="devlog__poster" @click="started = true">
            <img src="/brand/tharros-embleme-clair.svg" alt="" width="104" height="104" aria-hidden="true">
            <span class="btn btn--primary">Lancer l'animation <IconArrow /></span>
            <small>{{ title }}</small>
          </button>
        </div>
        <button v-if="isFullscreen" type="button" class="devlog__fs" aria-label="Quitter le plein écran" @click.stop="toggleFullscreen">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /></svg>
          <span>Quitter</span>
        </button>
      </div>
    </div>
    <figcaption class="devlog__bar">
      <span class="muted">Animation interactive — les commandes de lecture sont dans le cadre.</span>
      <span class="devlog__actions">
        <button type="button" class="devlog__btn" @click="toggleFullscreen">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" /></svg>
          Plein écran
        </button>
        <a class="link-arrow" :href="src" target="_blank" rel="noopener">Ouvrir dans un onglet</a>
      </span>
    </figcaption>
  </figure>
</template>

<style scoped>
/* Le lecteur déborde de la colonne de texte pour gagner en largeur */
.devlog { margin: 0 0 44px; display: grid; justify-items: center; gap: 10px; width: min(1180px, calc(100vw - 2 * var(--gutter))); margin-inline: 50%; translate: -50% 0; }
.devlog__slot { width: 100%; }
.devlog__frame { position: relative; display: grid; place-items: center; background: var(--encre); clip-path: var(--chamfer); margin-inline: auto; width: fit-content; max-width: 100%; }
.devlog__frame.is-fullscreen { clip-path: none; width: 100%; height: 100%; }
.devlog__inner { position: relative; max-width: 100%; }
.devlog__iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; display: block; }
.devlog__poster { position: absolute; inset: 0; width: 100%; display: grid; place-content: center; justify-items: center; gap: 18px; padding: 24px; cursor: pointer; border: 0; background: radial-gradient(60% 70% at 50% 40%, rgba(193, 31, 53, .35), transparent 70%), var(--encre); }
.devlog__poster img { opacity: .9; transition: transform .4s var(--ease-out); }
.devlog__poster:hover img { transform: scale(1.06); }
.devlog__poster small { color: var(--pierre-douce); font-size: 13px; letter-spacing: .12em; text-transform: uppercase; }
.devlog__fs {
  /* en bas à droite : l'en-tête et les chapitres de l'animation restent lisibles */
  position: absolute; bottom: 16px; right: 18px; z-index: 2;
  display: inline-flex; align-items: center; gap: 7px; padding: 7px 12px;
  background: color-mix(in srgb, var(--encre) 78%, transparent); color: var(--marbre);
  border: 1px solid rgba(246, 241, 233, .28); cursor: pointer;
  font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  opacity: .6; transition: opacity .2s, border-color .2s;
}
.devlog__frame:hover .devlog__fs, .devlog__fs:focus-visible { opacity: 1; border-color: var(--or); }
.devlog__fs svg { width: 15px; height: 15px; }
.devlog__actions { display: flex; flex-wrap: wrap; align-items: center; gap: 20px; }
.devlog__btn { display: inline-flex; align-items: center; gap: 8px; padding: 0; background: none; border: 0; cursor: pointer; font: inherit; font-weight: 700; letter-spacing: .04em; color: var(--fg); }
.devlog__btn svg { width: 16px; height: 16px; }
.devlog__btn:hover { color: var(--link); }
.devlog__bar { display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; font-size: 14px; width: 100%; }
@media (max-width: 640px) { .devlog__fs span { display: none; } }
</style>
