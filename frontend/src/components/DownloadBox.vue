<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useMemberStore } from '@/stores/member'
import IconArrow from './IconArrow.vue'

const props = defineProps({ game: { type: Object, required: true } })
const member = useMemberStore()
const route = useRoute()

const LABELS = { windows: 'Windows', macos: 'macOS', linux: 'Linux' }
const builds = computed(() => props.game.builds || [])

function detectPlatform() {
  const ua = navigator.userAgent
  if (/Mac/i.test(ua)) return 'macos'
  if (/Linux/i.test(ua) && !/Android/i.test(ua)) return 'linux'
  return 'windows'
}
const selected = ref(builds.value.find((b) => b.platform === detectPlatform())?.platform || builds.value[0]?.platform)
const current = computed(() => builds.value.find((b) => b.platform === selected.value))
const locked = computed(() => props.game.download_requires_account && !member.isLoggedIn)

function size(bytes) { return bytes > 1024 * 1024 ? `${(bytes / 1048576).toFixed(0)} Mo` : `${Math.round(bytes / 1024)} Ko` }
</script>

<template>
  <div v-if="builds.length" id="telecharger" class="download surface-charbon">
    <span class="kicker">Télécharger {{ game.title }}</span>
    <div class="download__platforms" role="tablist" aria-label="Système d'exploitation">
      <button v-for="b in builds" :key="b.id" type="button" role="tab" class="download__tab" :class="{ 'is-active': b.platform === selected }" :aria-selected="b.platform === selected" @click="selected = b.platform">
        <svg v-if="b.platform === 'windows'" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3 5.5l7.5-1v7H3zm8.5-1.2L21 3v8.5h-9.5zM3 12.5h7.5v7L3 18.5zm8.5 0H21V21l-9.5-1.3z" /></svg>
        <svg v-else-if="b.platform === 'macos'" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.4 12.8c0-2.4 2-3.6 2.1-3.7-1.1-1.7-2.9-1.9-3.5-1.9-1.5-.2-2.9.9-3.7.9-.8 0-1.9-.9-3.2-.8-1.6 0-3.1 1-4 2.4-1.7 3-.4 7.3 1.2 9.7.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.2-.8s1.9.8 3.2.8 2.2-1.2 3-2.4c.9-1.4 1.3-2.7 1.3-2.8-.1 0-2.6-1-2.6-3.8zM14 5.6c.7-.8 1.1-2 1-3.1-1 0-2.2.7-2.9 1.5-.6.7-1.2 1.9-1 3 1.1.1 2.2-.6 2.9-1.4z" /></svg>
        <svg v-else viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2c-2.2 0-3.6 1.8-3.6 4.4 0 1.2.2 2 .1 2.7-.4 1.3-2.2 3-2.7 5.1-.3 1.2-.2 2.2.1 3-.5.3-1.2.6-1.5 1.2-.3.7 0 1.5.5 1.9.6.5 1.7.5 2.6.9.6.3 1.3.6 2 .6.8 0 1.4-.4 1.9-.9h1.2c.5.5 1.1.9 1.9.9.7 0 1.4-.3 2-.6.9-.4 2-.4 2.6-.9.5-.4.8-1.2.5-1.9-.3-.6-1-.9-1.5-1.2.3-.8.4-1.8.1-3-.5-2.1-2.3-3.8-2.7-5.1-.1-.7.1-1.5.1-2.7C15.6 3.8 14.2 2 12 2zm-1.6 4.6c.5 0 .8.6.8 1.3s-.3 1.3-.8 1.3-.8-.6-.8-1.3.3-1.3.8-1.3zm3.2 0c.5 0 .8.6.8 1.3s-.3 1.3-.8 1.3-.8-.6-.8-1.3.3-1.3.8-1.3zM12 9.6c1 0 2 .6 2 1.2s-1.2 1.4-2 1.4-2-.8-2-1.4 1-1.2 2-1.2z" /></svg>
        {{ LABELS[b.platform] }}
      </button>
    </div>
    <div v-if="current" class="download__action">
      <template v-if="locked">
        <RouterLink class="btn btn--primary" :to="{ name: 'account.login', query: { next: route.fullPath + '#telecharger' } }">Se connecter pour télécharger <IconArrow /></RouterLink>
        <p class="muted">Ce téléchargement est réservé aux membres. <RouterLink :to="{ name: 'account.register', query: { next: route.fullPath + '#telecharger' } }">Créer un compte</RouterLink> — c'est gratuit.</p>
      </template>
      <template v-else>
        <a class="btn btn--primary" :href="`/api/downloads/${current.id}`" download>Télécharger pour {{ LABELS[current.platform] }} <IconArrow /></a>
        <p class="muted">{{ current.original_name }}<template v-if="current.version"> · version {{ current.version }}</template> · {{ size(current.size_bytes) }}</p>
      </template>
    </div>
  </div>
</template>

<style scoped>
.download { padding: clamp(28px, 4vw, 44px); clip-path: var(--chamfer); display: grid; gap: 18px; }
.download__platforms { display: flex; flex-wrap: wrap; gap: 8px; }
.download__tab { display: inline-flex; align-items: center; gap: 8px; padding: 10px 16px; background: transparent; border: 2px solid var(--pierre); color: var(--fg-soft); font-weight: 700; cursor: pointer; transition: border-color .2s, color .2s, background .2s; }
.download__tab svg { width: 18px; height: 18px; }
.download__tab:hover { border-color: var(--or); color: var(--fg); }
.download__tab.is-active { background: var(--or); border-color: var(--or); color: var(--encre); }
.download__action { display: grid; gap: 10px; justify-items: start; }
.download__action p { margin: 0; font-size: 14px; }
.download__action a:not(.btn) { color: var(--link); }
</style>
