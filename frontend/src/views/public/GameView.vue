<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { api } from '@/api/client'
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import CtaBlock from '@/components/CtaBlock.vue'
import IconArrow from '@/components/IconArrow.vue'
import MarkdownBlock from '@/components/MarkdownBlock.vue'
import PillarGrid from '@/components/PillarGrid.vue'
import SpecList from '@/components/SpecList.vue'
import DownloadBox from '@/components/DownloadBox.vue'
import NotFoundView from './NotFoundView.vue'

const route = useRoute()
const content = useContentStore()
const game = ref(null)
const notFound = ref(false)

async function load(slug) {
  notFound.value = false
  game.value = content.games.find((g) => g.slug === slug) || null
  if (!game.value) {
    try { game.value = await api.get(`/api/games/${slug}`) } catch { notFound.value = true }
  }
  // L'ancre (#telecharger) est demandée avant que le contenu existe : on y défile une fois rendu
  if (route.hash && game.value) {
    await nextTick()
    document.querySelector(route.hash)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
watch(() => route.params.slug, load, { immediate: true })

useHead(computed(() => game.value?.title || ''), computed(() => game.value?.tagline))
</script>

<template>
  <NotFoundView v-if="notFound" />
  <template v-else-if="game">
    <section class="hero surface-dark" aria-labelledby="game-title">
      <div class="container hero__inner">
        <span class="status-badge hero__item">{{ game.status }}</span>
        <span class="kicker hero__item">Un jeu Tharros</span>
        <h1 id="game-title" class="hero__item">{{ game.title }}</h1>
        <p class="lede hero__item">{{ game.tagline }}</p>
        <div class="hero__actions hero__item">
          <a v-if="game.builds?.length" class="btn btn--primary" href="#telecharger">Télécharger le jeu <IconArrow /></a>
          <RouterLink v-else class="btn btn--primary" :to="{ name: 'home', hash: '#rejoindre' }">{{ content.cta.button }} <IconArrow /></RouterLink>
          <RouterLink class="link-arrow" :to="{ name: 'journal' }">Suivre le développement</RouterLink>
        </div>
      </div>
    </section>
    <div class="frise" aria-hidden="true"></div>

    <section class="section surface-light">
      <div class="container">
        <div v-if="game.banner_url" v-reveal class="feature__art banner">
          <img :src="game.banner_url" :alt="`Bannière de ${game.title}`" width="1600" height="700" decoding="async">
        </div>
        <div class="feature">
          <div v-reveal>
            <span class="kicker">Le jeu</span>
            <MarkdownBlock :source="game.pitch_md" />
          </div>
          <div v-reveal="120"><SpecList :items="game.specs" /></div>
        </div>
      </div>
    </section>

    <section v-if="game.builds?.length" class="section surface-light" style="padding-top: 0" aria-label="Téléchargement">
      <div class="container"><div v-reveal><DownloadBox :game="game" /></div></div>
    </section>

    <section v-if="game.pillars.length" class="section surface-dark" aria-labelledby="pillars-title">
      <div class="container">
        <div class="section__head"><span class="kicker">Piliers de design</span><h2 id="pillars-title">Ce qui fait {{ game.title }}</h2></div>
        <PillarGrid :items="game.pillars" />
      </div>
    </section>
    <div class="frise surface-dark" aria-hidden="true"></div>

    <section v-if="game.progress.length" class="section surface-light" aria-labelledby="progress-title">
      <div class="container container--narrow">
        <span class="kicker">Où en est le jeu ?</span>
        <h2 id="progress-title">État d'avancement</h2>
        <SpecList :items="game.progress" />
        <p>Le détail, mois par mois, est dans le <RouterLink :to="{ name: 'journal' }">journal de développement</RouterLink>. Les questions fréquentes sont dans la <RouterLink :to="{ name: 'faq' }">FAQ</RouterLink>.</p>
      </div>
    </section>
    <CtaBlock />
  </template>
</template>

<style scoped>
.hero { position: relative; overflow: hidden; padding: clamp(56px, 8vw, 96px) 0 clamp(48px, 7vw, 88px); background-image: radial-gradient(60% 70% at 85% 20%, rgba(193, 31, 53, .3), transparent 70%); }
.hero__inner { display: grid; gap: 20px; max-width: 900px; justify-items: start; }
.hero__item { animation: hero-in .9s var(--ease-out) both; }
.hero__item:nth-child(2) { animation-delay: .1s; }
.hero__item:nth-child(3) { animation-delay: .2s; }
.hero__item:nth-child(4) { animation-delay: .3s; }
.hero__item:nth-child(5) { animation-delay: .4s; }
.hero__actions { display: flex; flex-wrap: wrap; gap: 20px; align-items: center; }
.banner { aspect-ratio: 16 / 7; margin-bottom: clamp(40px, 6vw, 72px); }
</style>
