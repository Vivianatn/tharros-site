<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import CtaBlock from '@/components/CtaBlock.vue'
import IconArrow from '@/components/IconArrow.vue'
import PillarGrid from '@/components/PillarGrid.vue'
import SpecList from '@/components/SpecList.vue'
import StatCounter from '@/components/StatCounter.vue'
import PostCard from '@/components/PostCard.vue'

const content = useContentStore()
const home = computed(() => content.home)
const game = computed(() => content.featuredGame)
useHead('', computed(() => content.site.description))
</script>

<template>
  <section class="hero surface-dark" aria-labelledby="hero-title">
    <div class="hero__bg" aria-hidden="true"></div>
    <img class="hero__emblem" src="/brand/tharros-emblem-light.svg" alt="" width="760" height="760" aria-hidden="true">
    <div class="container hero__inner">
      <span class="kicker hero__item">{{ home.kicker }}</span>
      <h1 id="hero-title" class="hero__item">{{ home.title_line1 }}<br><span class="accent">{{ home.title_line2 }}</span></h1>
      <p class="lede hero__item">{{ home.lede }}</p>
      <div class="hero__actions hero__item">
        <RouterLink class="btn btn--primary" :to="{ hash: '#rejoindre' }">{{ content.cta.button }} <IconArrow /></RouterLink>
        <RouterLink v-if="game" class="link-arrow" :to="{ name: 'game', params: { slug: game.slug } }">Découvrir {{ game.title }}</RouterLink>
      </div>
      <div class="hero__meta hero__item"><span v-for="m in home.meta" :key="m">{{ m }}</span></div>
    </div>
  </section>
  <div class="frise" aria-hidden="true"></div>

  <section v-if="game" class="section surface-light" aria-labelledby="game-title">
    <div class="container feature">
      <div v-reveal class="feature__art">
        <img v-if="game.cover_url" :src="game.cover_url" :alt="`Visuel de ${game.title}`" width="800" height="600" loading="lazy" decoding="async">
      </div>
      <div v-reveal="120">
        <span class="status-badge">{{ game.status }}</span>
        <span class="kicker">Notre premier jeu</span>
        <h2 id="game-title" class="feature__title">{{ game.title }}</h2>
        <p class="lede">{{ game.tagline }}</p>
        <SpecList :items="game.specs.slice(0, 4)" />
        <RouterLink class="link-arrow" :to="{ name: 'game', params: { slug: game.slug } }">Voir la fiche complète</RouterLink>
      </div>
    </div>
  </section>

  <section class="section surface-dark" aria-labelledby="manifeste-title">
    <div class="container">
      <div class="section__head">
        <span class="kicker">Manifeste</span>
        <h2 id="manifeste-title">{{ home.manifesto_title }}</h2>
        <p>{{ home.manifesto_intro }}</p>
      </div>
      <PillarGrid :items="home.manifesto" />
    </div>
  </section>
  <div class="frise surface-dark" aria-hidden="true"></div>

  <section class="section surface-light" aria-label="Le studio en chiffres">
    <div class="container stats">
      <StatCounter v-for="s in home.stats" :key="s.label" :value="s.num" :label="s.label" />
    </div>
  </section>

  <section class="section surface-charbon" aria-labelledby="studio-title">
    <div class="container feature">
      <div v-reveal>
        <span class="kicker">Le studio</span>
        <h2 id="studio-title" class="studio__title">{{ home.studio_title }}</h2>
        <p class="lede">{{ home.studio_text }}</p>
        <RouterLink class="link-arrow" :to="{ name: 'studio' }">Découvrir le studio</RouterLink>
      </div>
      <div v-reveal="150" class="studio__emblem">
        <img src="/brand/tharros-emblem-light.svg" alt="Emblème Tharros : crinière de lion en pic anguleux, ailes d'aigle, œil grenat, cerclés d'un anneau" width="320" height="320" loading="lazy" decoding="async">
      </div>
    </div>
  </section>

  <section v-if="content.latestPosts.length" class="section surface-light" aria-labelledby="journal-title">
    <div class="container">
      <div class="section__head">
        <span class="kicker">Journal de développement</span>
        <h2 id="journal-title">Dernières nouvelles</h2>
      </div>
      <div v-reveal><PostCard :post="content.latestPosts[0]" /></div>
      <RouterLink class="link-arrow" :to="{ name: 'journal' }" style="margin-top: 24px">Tous les billets</RouterLink>
    </div>
  </section>

  <CtaBlock />
</template>

<style scoped>
.hero { position: relative; overflow: hidden; padding: clamp(80px, 12vw, 160px) 0 clamp(64px, 9vw, 120px); isolation: isolate; }
.hero__bg { position: absolute; inset: 0; z-index: -1; pointer-events: none; background: radial-gradient(60% 60% at 80% 20%, rgba(193, 31, 53, .28), transparent 70%), radial-gradient(40% 40% at 10% 90%, rgba(184, 103, 46, .22), transparent 70%); }
.hero__bg::after { content: ''; position: absolute; inset: 0; background: repeating-linear-gradient(90deg, rgba(246, 241, 233, .06) 0 1px, transparent 1px 48px); mask-image: linear-gradient(180deg, transparent, #000 40%, transparent); -webkit-mask-image: linear-gradient(180deg, transparent, #000 40%, transparent); }
.hero__emblem { position: absolute; right: -8%; top: 50%; width: clamp(360px, 48vw, 760px); z-index: -1; pointer-events: none; opacity: .09; transform: translateY(-50%); animation: emblem-in 1.4s var(--ease-out) both; }
.hero__inner { display: grid; gap: 28px; max-width: 900px; }
.hero h1 { margin-bottom: 8px; }
.hero__item { animation: hero-in .9s var(--ease-out) both; }
.hero__item:nth-child(2) { animation-delay: .1s; }
.hero__item:nth-child(3) { animation-delay: .25s; }
.hero__item:nth-child(4) { animation-delay: .4s; }
.hero__item:nth-child(5) { animation-delay: .5s; }
.hero__actions { display: flex; flex-wrap: wrap; gap: 20px; align-items: center; }
.hero__meta { display: flex; flex-wrap: wrap; gap: 10px 28px; margin-top: 8px; font-size: 13px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--fg-muted); }
.feature__title { font-size: clamp(44px, 7vw, 88px); line-height: .9; }
.studio__title { font-size: clamp(40px, 6vw, 72px); }
.studio__emblem { display: grid; place-items: center; }
.studio__emblem img { width: min(320px, 70%); animation: spin-slow 60s linear infinite; }
</style>
