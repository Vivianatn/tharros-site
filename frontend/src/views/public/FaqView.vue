<script setup>
import { RouterLink } from 'vue-router'
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import PageHead from '@/components/PageHead.vue'
import MarkdownBlock from '@/components/MarkdownBlock.vue'
import CtaBlock from '@/components/CtaBlock.vue'

const content = useContentStore()
useHead('Questions fréquentes', "Tout ce qu'on nous demande sur Muses et sur le studio Tharros : date de sortie, plateformes, prix, phase de test.")
</script>

<template>
  <PageHead kicker="FAQ" title="Questions fréquentes">
    <p class="lede">Les réponses courtes. Pour le reste, la <RouterLink :to="{ name: 'contact' }">page contact</RouterLink>.</p>
  </PageHead>
  <section class="section surface-light">
    <div class="container container--narrow">
      <details v-for="(f, i) in content.faq" :key="f.id" v-reveal="Math.min(i, 6) * 60" :open="i === 0">
        <summary>{{ f.question }}</summary>
        <MarkdownBlock :source="f.answer_md" />
      </details>
    </div>
  </section>
  <CtaBlock />
</template>

<style scoped>
details { border-top: 1px solid var(--line); padding: 20px 0; }
details:last-child { border-bottom: 1px solid var(--line); }
summary { cursor: pointer; font-family: var(--font-display); font-size: clamp(22px, 2.6vw, 28px); font-weight: 800; text-transform: uppercase; list-style: none; display: flex; justify-content: space-between; gap: 16px; color: var(--heading); }
summary::-webkit-details-marker { display: none; }
summary::after { content: '+'; color: var(--grenat); font-weight: 900; transition: transform .3s var(--ease); }
details[open] summary::after { transform: rotate(45deg); }
details :deep(.prose) { margin-top: 14px; color: var(--fg-soft); }
</style>
