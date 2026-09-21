<script setup>
import { RouterView } from 'vue-router'
import { useContentStore } from '@/stores/content'
import SiteHeader from '@/components/SiteHeader.vue'
import SiteFooter from '@/components/SiteFooter.vue'
import CookieBanner from '@/components/CookieBanner.vue'

const content = useContentStore()
content.load()
</script>

<template>
  <a class="skip-link" href="#main">Aller au contenu</a>
  <SiteHeader />
  <main id="main">
    <div v-if="!content.loaded && !content.error" class="loading" aria-live="polite">
      <img src="/brand/tharros-emblem.svg" alt="" width="64" height="64" class="loading__emblem">
      <span class="visually-hidden">Chargement…</span>
    </div>
    <div v-else-if="content.error" class="container section">
      <h1 style="font-size:40px">Le site est momentanément indisponible</h1>
      <p class="lede">Impossible de joindre le serveur ({{ content.error }}). Réessayez dans un instant.</p>
    </div>
    <RouterView v-else v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <!-- Enveloppe à racine unique : les vues ont plusieurs nœuds racines, Transition en exige un seul -->
        <div :key="$route.path" class="page">
          <component :is="Component" />
        </div>
      </Transition>
    </RouterView>
  </main>
  <SiteFooter />
  <CookieBanner />
</template>

<style scoped>
.loading { min-height: 60vh; display: grid; place-items: center; }
.loading__emblem { animation: spin-slow 2.4s linear infinite; opacity: .5; }
</style>
