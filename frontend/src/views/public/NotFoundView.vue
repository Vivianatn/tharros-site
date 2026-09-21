<script setup>
import { RouterLink } from 'vue-router'
import { useHead } from '@/composables/useHead'
import IconArrow from '@/components/IconArrow.vue'

useHead('Page introuvable', "La page que vous cherchez n'existe pas ou a été déplacée.")
</script>

<template>
  <section class="err surface-light">
    <div class="container">
      <div class="err__code" aria-hidden="true">404</div>
      <h1 class="err__title">Cette page a été oubliée</h1>
      <p class="lede" style="margin-inline: auto">Comme les Muses. Mais contrairement à elles, celle-ci ne reviendra pas : rentrez plutôt à l'accueil.</p>
      <div class="err__actions">
        <RouterLink class="btn btn--primary" :to="{ name: 'home' }">Retour à l'accueil <IconArrow /></RouterLink>
        <RouterLink class="link-arrow" :to="{ name: 'games' }">Voir nos jeux</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.err { min-height: 70vh; display: grid; place-items: center; text-align: center; padding: 64px 0; }
.err__code { font-family: var(--font-display); font-weight: 900; font-size: clamp(120px, 28vw, 320px); line-height: .8; color: var(--grenat); animation: hero-in .8s var(--ease-out) both; }
.err__title { font-size: clamp(32px, 5vw, 56px); }
.err__actions { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-top: 24px; }
</style>
