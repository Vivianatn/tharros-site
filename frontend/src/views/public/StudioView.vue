<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import PageHead from '@/components/PageHead.vue'
import MarkdownBlock from '@/components/MarkdownBlock.vue'
import PillarGrid from '@/components/PillarGrid.vue'
import SpecList from '@/components/SpecList.vue'
import CtaBlock from '@/components/CtaBlock.vue'

const content = useContentStore()
const s = computed(() => content.studio)
useHead('Le studio', computed(() => s.value.lede))
</script>

<template>
  <PageHead kicker="Le studio" :title="s.title" :lede="s.lede" />

  <section class="section surface-light" aria-labelledby="history-title">
    <div class="container feature">
      <div v-reveal>
        <span class="kicker">Histoire</span>
        <h2 id="history-title">{{ s.history_title }}</h2>
        <MarkdownBlock :source="s.history_md" />
      </div>
      <div v-reveal="150" class="emblem">
        <img src="/brand/tharros-embleme-fonce.svg" alt="Emblème Tharros : masque de lion rayonnant, cerclé d'une frise grecque" width="320" height="320" loading="lazy">
      </div>
    </div>
  </section>

  <section class="section surface-dark" aria-labelledby="timeline-title">
    <div class="container">
      <div class="section__head"><span class="kicker">Chronologie</span><h2 id="timeline-title">Une ascension, palier par palier</h2></div>
      <ol class="timeline" style="max-width: 720px">
        <li v-for="(t, i) in s.timeline" :key="i" v-reveal="i * 100"><time>{{ t.date }}</time><p>{{ t.text }}</p></li>
      </ol>
    </div>
  </section>
  <div class="frise surface-dark" aria-hidden="true"></div>

  <section class="section surface-light" aria-labelledby="values-title">
    <div class="container">
      <div class="section__head"><span class="kicker">Valeurs</span><h2 id="values-title">Ce qui tient debout</h2></div>
      <PillarGrid :items="s.values" :columns="2" />
    </div>
  </section>

  <section class="section surface-charbon" aria-labelledby="team-title">
    <div class="container">
      <div class="section__head"><span class="kicker">Équipe</span><h2 id="team-title">{{ s.team_title }}</h2><p>{{ s.team_intro }}</p></div>
      <div class="feature" style="align-items: start">
        <div v-reveal class="member">
          <div class="member__avatar">
            <img v-if="s.member_photo" :src="s.member_photo" :alt="s.member_name" width="320" height="320">
            <span v-else aria-hidden="true">{{ s.member_initials }}</span>
          </div>
          <h3>{{ s.member_name }}</h3>
          <span class="member__role">{{ s.member_role }}</span>
        </div>
        <div v-reveal="120"><SpecList :items="s.roles" /></div>
      </div>
    </div>
  </section>

  <section id="collaborations" class="section surface-light" aria-labelledby="collab-title">
    <div class="container container--narrow">
      <span class="kicker">Collaborations</span>
      <h2 id="collab-title">{{ s.collab_title }}</h2>
      <p class="lede">{{ s.collab_intro }}</p>
      <SpecList :items="s.collabs" />
      <p>Si l'un de ces sujets vous parle, écrivez via la <RouterLink :to="{ name: 'contact' }">page contact</RouterLink> en précisant le sujet en objet, avec un lien vers votre travail.</p>
    </div>
  </section>
  <CtaBlock />
</template>

<style scoped>
.emblem { display: grid; place-items: center; }
.emblem img { width: min(300px, 70%); }
.member { display: grid; gap: 12px; max-width: 320px; }
.member__avatar { aspect-ratio: 1; display: grid; place-items: center; background: var(--encre); color: var(--or); font-family: var(--font-display); font-weight: 900; font-size: 96px; clip-path: var(--chamfer); overflow: hidden; }
.member__avatar img { width: 100%; height: 100%; object-fit: cover; }
.member h3 { font-size: 24px; margin: 0; }
.member__role { font-size: 13px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--fg-muted); }
</style>
