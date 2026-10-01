<script setup>
import { ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useContentStore } from '@/stores/content'
import { useMemberStore } from '@/stores/member'
import BrandLogo from './BrandLogo.vue'
import IconArrow from './IconArrow.vue'
import { avatarUrl } from '@/utils/avatars'

const content = useContentStore()
const member = useMemberStore()
const route = useRoute()
member.restore()
const open = ref(false)

const links = [
  { to: { name: 'games' }, label: 'Jeux', match: 'games' },
  { to: { name: 'journal' }, label: 'Journal', match: 'journal' },
  { to: { name: 'studio' }, label: 'Studio', match: 'studio' },
  { to: { name: 'press' }, label: 'Presse', match: 'press' },
  { to: { name: 'contact' }, label: 'Contact', match: 'contact' },
]

function isActive(match) {
  return String(route.name || '').startsWith(match) || (match === 'games' && route.name === 'game') || (match === 'journal' && route.name === 'post')
}

watch(() => route.fullPath, () => { open.value = false })
watch(open, (v) => { document.body.style.overflow = v ? 'hidden' : '' })
</script>

<template>
  <header class="site-header surface-dark">
    <div class="container site-header__inner">
      <RouterLink class="brand" :to="{ name: 'home' }" aria-label="Tharros — retour à l'accueil"><BrandLogo /></RouterLink>
      <button class="nav-toggle" type="button" :aria-expanded="open" aria-controls="nav" :aria-label="open ? 'Fermer le menu' : 'Ouvrir le menu'" @click="open = !open">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path v-if="!open" d="M3 6h18M3 12h18M3 18h18" /><path v-else d="M5 5l14 14M19 5L5 19" />
        </svg>
      </button>
      <nav id="nav" class="nav" :class="{ 'is-open': open }" aria-label="Navigation principale">
        <ul class="nav__list">
          <li v-for="l in links" :key="l.label"><RouterLink :to="l.to" :aria-current="isActive(l.match) ? 'page' : null">{{ l.label }}</RouterLink></li>
        </ul>
        <RouterLink class="nav__account" :to="member.isLoggedIn ? { name: 'account' } : { name: 'account.login' }" :title="member.isLoggedIn ? 'Mon compte' : 'Connexion'">
          <img v-if="member.isLoggedIn" :src="avatarUrl(member.member.avatar)" alt="" width="28" height="28" class="nav__avatar">
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="8" r="4" /><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7" /></svg>
          <span>{{ member.isLoggedIn ? member.member.display_name : 'Connexion' }}</span>
        </RouterLink>
        <RouterLink class="btn btn--primary" :to="{ name: 'home', hash: '#rejoindre' }">{{ content.cta.button || 'Rejoindre la liste' }} <IconArrow /></RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.site-header { position: sticky; top: 0; z-index: 100; background: color-mix(in srgb, var(--encre) 92%, transparent); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-bottom: 1px solid rgba(246, 241, 233, .08); }
.site-header__inner { display: flex; align-items: center; justify-content: space-between; gap: 24px; min-height: var(--header-h); }
.brand { display: inline-flex; align-items: center; transition: transform .3s var(--ease); }
.brand:hover { transform: scale(1.03); }
.nav { display: flex; align-items: center; gap: 32px; }
.nav__list { display: flex; gap: 28px; list-style: none; margin: 0; padding: 0; }
.nav__list a { color: var(--pierre-claire); text-decoration: none; font-weight: 600; font-size: 15px; letter-spacing: .04em; padding: 6px 0; position: relative; }
.nav__list a::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 2px; background: var(--grenat); transform: scaleX(0); transform-origin: left; transition: transform .3s var(--ease); }
.nav__list a:hover, .nav__list a[aria-current="page"] { color: var(--marbre); }
.nav__list a:hover::after, .nav__list a[aria-current="page"]::after { transform: scaleX(1); }
.nav__account { display: inline-flex; align-items: center; gap: 8px; color: var(--pierre-claire); text-decoration: none; font-weight: 600; font-size: 14px; max-width: 160px; }
.nav__account span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.nav__account svg { width: 20px; height: 20px; flex-shrink: 0; }
.nav__avatar { width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0; border: 2px solid var(--or); }
.nav__account:hover { color: var(--or); }
.nav-toggle { display: none; background: none; border: 0; color: var(--marbre); padding: 8px; cursor: pointer; }
.nav-toggle svg { width: 28px; height: 28px; }
@media (max-width: 900px) {
  .nav-toggle { display: inline-flex; }
  .nav { position: fixed; inset: var(--header-h) 0 0 0; background: var(--encre); flex-direction: column; align-items: stretch; justify-content: flex-start; padding: 32px var(--gutter); gap: 32px; transform: translateX(100%); transition: transform .4s var(--ease-out); }
  .nav.is-open { transform: none; }
  .nav__list { flex-direction: column; gap: 8px; }
  .nav__list a { display: block; font-family: var(--font-display); font-size: 40px; text-transform: uppercase; font-weight: 800; letter-spacing: .02em; padding: 8px 0; }
  .nav__list a::after { display: none; }
  .nav .btn { align-self: flex-start; }
  .nav__account { font-size: 18px; max-width: none; }
}
</style>
