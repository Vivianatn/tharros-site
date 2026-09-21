<script setup>
import { RouterLink } from 'vue-router'
import { useContentStore } from '@/stores/content'
import { useConsentStore } from '@/stores/consent'
import BrandLogo from './BrandLogo.vue'

const content = useContentStore()
const consent = useConsentStore()
const year = new Date().getFullYear()
</script>

<template>
  <footer class="site-footer surface-dark">
    <div class="container">
      <div class="site-footer__grid">
        <div>
          <RouterLink class="brand" :to="{ name: 'home' }" aria-label="Tharros — retour à l'accueil"><BrandLogo :height="44" /></RouterLink>
          <p class="site-footer__tagline">{{ content.site.description }}</p>
        </div>
        <div>
          <h3>Studio</h3>
          <ul>
            <li><RouterLink :to="{ name: 'games' }">Nos jeux</RouterLink></li>
            <li><RouterLink :to="{ name: 'journal' }">Journal de développement</RouterLink></li>
            <li><RouterLink :to="{ name: 'studio' }">Le studio</RouterLink></li>
            <li><RouterLink :to="{ name: 'faq' }">FAQ</RouterLink></li>
            <li><RouterLink :to="{ name: 'press' }">Presse</RouterLink></li>
            <li><RouterLink :to="{ name: 'contact' }">Contact</RouterLink></li>
          </ul>
        </div>
        <div>
          <h3>Légal</h3>
          <ul>
            <li><RouterLink :to="{ name: 'legal', params: { slug: 'mentions-legales' } }">Mentions légales</RouterLink></li>
            <li><RouterLink :to="{ name: 'legal', params: { slug: 'confidentialite' } }">Politique de confidentialité</RouterLink></li>
            <li><RouterLink :to="{ name: 'legal', params: { slug: 'cgu' } }">Conditions générales d'utilisation</RouterLink></li>
            <li><a href="#" @click.prevent="consent.open()">Gérer les cookies</a></li>
          </ul>
        </div>
        <div>
          <h3>Suivre</h3>
          <ul class="socials">
            <li v-for="s in content.site.socials" :key="s.name"><a :href="s.url" rel="noopener" target="_blank">{{ s.name }}</a></li>
          </ul>
          <ul style="margin-top: 18px"><li><a :href="`mailto:${content.site.contact_email}`">{{ content.site.contact_email }}</a></li></ul>
        </div>
      </div>
      <div class="site-footer__bottom">
        <span>© {{ year }} {{ content.site.name || 'Tharros' }} Studio — Tous droits réservés.</span>
        <span>Fait en France · Aucun cookie sans votre accord.</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.site-footer { padding: 64px 0 32px; }
.site-footer__grid { display: grid; grid-template-columns: 1.4fr 1fr 1fr 1fr; gap: 40px; }
@media (max-width: 860px) { .site-footer__grid { grid-template-columns: 1fr 1fr; } }
@media (max-width: 520px) { .site-footer__grid { grid-template-columns: 1fr; } }
.brand { display: inline-flex; color: var(--marbre); }
h3 { font-size: 16px; letter-spacing: .16em; color: var(--or); margin-bottom: 16px; }
ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }
a { color: var(--pierre-claire); text-decoration: none; }
a:hover { color: var(--marbre); text-decoration: underline; }
.site-footer__tagline { margin: 18px 0 0; max-width: 320px; font-size: 15px; color: var(--pierre-douce); }
.site-footer__bottom { margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--line); display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; font-size: 13px; color: var(--pierre-douce); }
</style>
