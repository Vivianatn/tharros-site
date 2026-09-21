<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useMemberStore } from '@/stores/member'
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import { formatDate } from '@/utils/format'
import PageHead from '@/components/PageHead.vue'
import AvatarPicker from '@/components/AvatarPicker.vue'
import { avatarUrl } from '@/utils/avatars'

const member = useMemberStore()
const content = useContentStore()
const router = useRouter()
const profile = reactive({ display_name: member.member?.display_name || '', avatar: member.member?.avatar || 'a01', newsletter: member.member?.newsletter || false })
const pwd = reactive({ current: '', next: '', confirm: '' })
const status = reactive({ profile: '', password: '' })
useHead('Mon compte')

async function saveProfile() {
  try { await member.update(profile); status.profile = 'Profil enregistré.' } catch (e) { status.profile = e.message }
}
async function changePassword() {
  if (pwd.next !== pwd.confirm) { status.password = 'Les deux mots de passe ne correspondent pas.'; return }
  try {
    await member.changePassword(pwd.current, pwd.next)
    status.password = 'Mot de passe modifié.'
    Object.assign(pwd, { current: '', next: '', confirm: '' })
  } catch (e) { status.password = e.message }
}
async function logout() { await member.logout(); router.push({ name: 'home' }) }
async function remove() {
  if (!confirm('Supprimer définitivement votre compte et vos données ? Cette action est irréversible.')) return
  await member.remove()
  router.push({ name: 'home' })
}
</script>

<template>
  <PageHead kicker="Compte" :title="`Bonjour, ${member.member?.display_name}`" narrow>
    <p class="muted account__identity"><img :src="avatarUrl(member.member?.avatar)" alt="" width="48" height="48" class="account__avatar"> {{ member.member?.email }} · membre depuis le {{ formatDate(member.member?.created_at) }}</p>
  </PageHead>
  <section class="section surface-light">
    <div class="container container--narrow account">
      <div v-reveal class="account__block">
        <h2>Vos jeux</h2>
        <p v-if="!content.games.some((g) => g.builds?.length)" class="muted">Aucun téléchargement disponible pour le moment. Vous serez prévenu·e dès l'ouverture des phases de test.</p>
        <ul v-else class="spec-list">
          <li v-for="g in content.games.filter((g) => g.builds?.length)" :key="g.id">
            <span class="k">{{ g.title }}</span>
            <span><RouterLink :to="{ name: 'game', params: { slug: g.slug }, hash: '#telecharger' }">Télécharger ({{ g.builds.map((b) => b.platform).join(', ') }})</RouterLink></span>
          </li>
        </ul>
      </div>

      <form v-reveal class="account__block form" @submit.prevent="saveProfile">
        <h2>Profil</h2>
        <div class="field"><label for="a-name">Pseudo</label><input id="a-name" v-model="profile.display_name" type="text" minlength="2" maxlength="60" required></div>
        <div class="field"><label>Image de profil</label><AvatarPicker v-model="profile.avatar" /></div>
        <div class="field field--check"><input id="a-news" v-model="profile.newsletter" type="checkbox"><label for="a-news">Recevoir les nouvelles du studio</label></div>
        <p class="form__status" :class="status.profile.includes('enregistré') ? 'is-success' : 'is-error'">{{ status.profile }}</p>
        <div><button type="submit" class="btn btn--primary btn--small">Enregistrer</button></div>
      </form>

      <form v-reveal class="account__block form" @submit.prevent="changePassword">
        <h2>Mot de passe</h2>
        <div class="field"><label for="p-cur">Actuel</label><input id="p-cur" v-model="pwd.current" type="password" autocomplete="current-password" required></div>
        <div class="form__row">
          <div class="field"><label for="p-new">Nouveau</label><input id="p-new" v-model="pwd.next" type="password" autocomplete="new-password" minlength="10" required></div>
          <div class="field"><label for="p-conf">Confirmer</label><input id="p-conf" v-model="pwd.confirm" type="password" autocomplete="new-password" required></div>
        </div>
        <p class="form__status" :class="status.password.includes('modifié') ? 'is-success' : 'is-error'">{{ status.password }}</p>
        <div><button type="submit" class="btn btn--primary btn--small">Modifier</button></div>
      </form>

      <div v-reveal class="account__block">
        <h2>Session et données</h2>
        <div style="display: flex; flex-wrap: wrap; gap: 12px">
          <button type="button" class="btn btn--ghost btn--small" @click="logout">Se déconnecter</button>
          <button type="button" class="btn btn--ghost btn--small danger" @click="remove">Supprimer mon compte</button>
        </div>
        <p class="muted" style="font-size: 14px; margin-top: 12px">La suppression efface votre compte et vos données (droit à l'effacement, RGPD).</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.account { display: grid; gap: 40px; }
.account__block h2 { font-size: clamp(26px, 3vw, 34px); }
.account__identity { display: flex; align-items: center; gap: 12px; }
.account__avatar { border-radius: 50%; }
.danger { color: var(--grenat); border-color: var(--grenat); }
.danger:hover { color: var(--marbre); background: var(--grenat); }
</style>
