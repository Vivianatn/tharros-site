<script setup>
import { computed } from 'vue'
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import PageHead from '@/components/PageHead.vue'
import SpecList from '@/components/SpecList.vue'
import MarkdownBlock from '@/components/MarkdownBlock.vue'

const content = useContentStore()
const p = computed(() => content.press)
const game = computed(() => content.featuredGame)
const gameFacts = computed(() => (game.value
  ? [{ k: 'Titre', v: game.value.title }, { k: 'Statut', v: game.value.status }, ...game.value.specs.slice(0, 4)]
  : []))
useHead('Presse & kit média', computed(() => p.value.lede))
</script>

<template>
  <PageHead kicker="Presse" :title="p.title" :lede="p.lede" />

  <section class="section surface-light">
    <div class="container feature" style="align-items: start">
      <div v-reveal><span class="kicker">Fiche d'identité</span><h2 class="h-small">Le studio</h2><SpecList :items="p.studio_facts" /></div>
      <div v-if="game" v-reveal="120"><span class="kicker">Fiche d'identité</span><h2 class="h-small">{{ game.title }}</h2><SpecList :items="gameFacts" /></div>
    </div>
  </section>

  <section class="section surface-dark" aria-labelledby="assets-title">
    <div class="container">
      <div class="section__head">
        <span class="kicker">Ressources</span>
        <h2 id="assets-title">Logos et visuels</h2>
        <p>Fichiers vectoriels : ils s'agrandissent sans perte. Ne pas déformer, recolorer ni recadrer le blason.</p>
      </div>
      <div class="grid grid--3">
        <!-- Chaque carte est une surface claire : ses couleurs de texte sont redéfinies, jamais héritées du fond sombre -->
        <div v-for="(a, i) in p.assets" :key="a.url" v-reveal="i * 80" class="asset-card surface-light">
          <div class="asset-card__preview" :class="{ 'is-dark': a.dark }"><img :src="a.url" :alt="a.title" loading="lazy"></div>
          <h3>{{ a.title }}</h3>
          <p>{{ a.desc }}</p>
          <a class="link-arrow" :href="a.url" download>Télécharger</a>
        </div>
      </div>
    </div>
  </section>
  <div class="frise surface-dark" aria-hidden="true"></div>

  <section class="section surface-light">
    <div class="container container--narrow">
      <span class="kicker">Contact presse</span>
      <h2 class="h-small">Interviews, clés, captures</h2>
      <MarkdownBlock :source="p.contact_md" />
    </div>
  </section>
</template>

<style scoped>
.h-small { font-size: clamp(28px, 3.4vw, 40px); }
.asset-card { display: grid; gap: 12px; padding: 22px; background: var(--blanc); border: 1px solid var(--pierre-claire); align-content: start; }
.asset-card__preview { display: grid; place-items: center; aspect-ratio: 16 / 9; background: var(--marbre); padding: 20px; overflow: hidden; }
.asset-card__preview.is-dark { background: var(--encre); }
.asset-card__preview img { width: 100%; height: 100%; object-fit: contain; }
.asset-card h3 { font-size: 22px; margin: 0; }
.asset-card p { font-size: 14px; color: var(--fg-muted); margin: 0; }
</style>
