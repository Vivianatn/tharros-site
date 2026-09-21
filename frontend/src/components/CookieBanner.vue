<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useConsentStore } from '@/stores/consent'
import { useContentStore } from '@/stores/content'

const consent = useConsentStore()
const content = useContentStore()

onMounted(() => {
  if (consent.choice === 'accepted') consent.loadAnalytics(content.site.analytics_domain)
})
</script>

<template>
  <Transition name="banner">
    <div v-if="consent.bannerOpen" class="cookie-banner surface-dark" role="dialog" aria-live="polite" aria-label="Consentement aux cookies">
      <p><strong>Des cookies ? Seulement si vous le voulez.</strong> Un outil de mesure d'audience nous dit quelles pages vous intéressent. Il n'est chargé qu'après votre accord. <RouterLink :to="{ name: 'legal', params: { slug: 'confidentialite' } }">En savoir plus</RouterLink></p>
      <div class="actions">
        <button type="button" class="btn btn--primary btn--small" @click="consent.choose('accepted', content.site.analytics_domain)">Accepter</button>
        <button type="button" class="btn btn--ghost btn--small" @click="consent.choose('refused')">Refuser</button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.cookie-banner { position: fixed; left: 16px; bottom: 16px; z-index: 200; width: min(420px, calc(100vw - 32px)); padding: 18px 20px; clip-path: var(--chamfer); box-shadow: 0 20px 50px rgba(0, 0, 0, .35); }
.cookie-banner p { font-size: 13px; line-height: 1.5; margin: 0 0 12px; color: var(--fg-soft); }
.actions { display: flex; flex-wrap: wrap; gap: 10px; }
.banner-enter-active, .banner-leave-active { transition: opacity .4s var(--ease), transform .4s var(--ease); }
.banner-enter-from, .banner-leave-to { opacity: 0; transform: translateY(20px); }
</style>
