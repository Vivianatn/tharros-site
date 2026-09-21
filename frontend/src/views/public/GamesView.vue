<script setup>
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import PageHead from '@/components/PageHead.vue'
import GameCard from '@/components/GameCard.vue'
import CtaBlock from '@/components/CtaBlock.vue'

const content = useContentStore()
useHead('Nos jeux', 'Les jeux du studio Tharros : Muses, aventure narrative en développement, et les projets à venir.')
</script>

<template>
  <PageHead kicker="Nos jeux" title="Des légendes à jouer" lede="Un seul jeu à la fois, fait jusqu'au bout. Voici où en est le catalogue." />
  <section class="section surface-light">
    <div class="container grid grid--2">
      <div v-for="(g, i) in content.games" :key="g.id" v-reveal="i * 100"><GameCard :game="g" /></div>
      <article v-reveal="content.games.length * 100" class="pillar next">
        <div class="pillar__num">{{ content.games.length + 1 }}</div>
        <h3>Le prochain</h3>
        <p>Il n'existe pas encore, et c'est voulu : Tharros ne commence pas un second jeu avant d'avoir terminé le premier. Les idées s'accumulent dans un carnet ; elles attendront.</p>
      </article>
    </div>
  </section>
  <CtaBlock />
</template>

<style scoped>
.next { display: grid; align-content: center; }
</style>
