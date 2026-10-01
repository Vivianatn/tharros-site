<script setup>
import { computed, reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useMemberStore } from '@/stores/member'
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import { formatDate } from '@/utils/format'
import { avatarLabel, avatarUrl } from '@/utils/avatars'
import AvatarPicker from '@/components/AvatarPicker.vue'
import IconArrow from '@/components/IconArrow.vue'

const member = useMemberStore()
const content = useContentStore()
const router = useRouter()

const profile = reactive({
  display_name: member.member?.display_name || '',
  avatar: member.member?.avatar || '001',
  newsletter: member.member?.newsletter || false,
})
const pwd = reactive({ current: '', next: '', confirm: '' })
const status = reactive({ profile: '', password: '' })
const editingAvatar = ref(false)

const gamesWithBuilds = computed(() => content.games.filter((g) => g.builds?.length))
const dirty = computed(() => profile.display_name !== member.member?.display_name
  || profile.avatar !== member.member?.avatar
  || profile.newsletter !== member.member?.newsletter)

useHead('Mon compte')

async function saveProfile() {
  try {
    await member.update(profile)
    status.profile = 'Profil enregistré.'
    editingAvatar.value = false
  } catch (e) {
    status.profile = e.message
  }
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
  <section class="hero surface-dark" aria-labelledby="account-title">
    <div class="hero__bg" aria-hidden="true"></div>
    <div class="container card">
      <img class="card__avatar" :src="avatarUrl(member.member?.avatar)" :alt="`Votre avatar : ${avatarLabel(member.member?.avatar)}`" width="256" height="256">
      <div class="card__identity">
        <span class="kicker">Mon compte</span>
        <h1 id="account-title">{{ member.member?.display_name }}</h1>
        <p class="card__meta">
          <span>{{ member.member?.email }}</span>
          <span>Membre depuis le {{ formatDate(member.member?.created_at) }}</span>
          <span>Avatar : {{ avatarLabel(member.member?.avatar) }}</span>
        </p>
        <button type="button" class="btn btn--primary" @click="editingAvatar = !editingAvatar">
          {{ editingAvatar ? 'Masquer les avatars' : "Changer d'avatar" }} <IconArrow />
        </button>
      </div>
    </div>
  </section>
  <div class="frise" aria-hidden="true"></div>

  <section class="section surface-light">
    <div class="container account">
      <form class="account__block form" @submit.prevent="saveProfile">
        <h2>Profil</h2>
        <div class="field" style="max-width: 420px">
          <label for="a-name">Pseudo</label>
          <input id="a-name" v-model="profile.display_name" type="text" minlength="2" maxlength="60" required>
        </div>
        <div class="field">
          <label>Image de profil</label>
          <AvatarPicker v-if="editingAvatar" v-model="profile.avatar" />
          <div v-else class="account__current">
            <img :src="avatarUrl(profile.avatar)" :alt="avatarLabel(profile.avatar)" width="256" height="256">
            <div>
              <strong>{{ avatarLabel(profile.avatar) }}</strong>
              <p class="muted">Choisissez parmi 100 avatars inspirés de la Grèce antique.</p>
              <button type="button" class="link-arrow" @click="editingAvatar = true">Parcourir les avatars</button>
            </div>
          </div>
        </div>
        <div class="field field--check">
          <input id="a-news" v-model="profile.newsletter" type="checkbox">
          <label for="a-news">Recevoir les nouvelles du studio</label>
        </div>
        <p class="form__status" :class="status.profile.includes('enregistré') ? 'is-success' : 'is-error'">{{ status.profile }}</p>
        <div><button type="submit" class="btn btn--primary" :disabled="!dirty">Enregistrer</button></div>
      </form>

      <div class="account__block">
        <h2>Vos jeux</h2>
        <p v-if="!gamesWithBuilds.length" class="muted">Aucun téléchargement disponible pour le moment. Vous serez prévenu·e dès l'ouverture des phases de test.</p>
        <ul v-else class="spec-list">
          <li v-for="g in gamesWithBuilds" :key="g.id">
            <span class="k">{{ g.title }}</span>
            <span><RouterLink :to="{ name: 'game', params: { slug: g.slug }, hash: '#telecharger' }">Télécharger ({{ g.builds.map((b) => b.platform).join(', ') }})</RouterLink></span>
          </li>
        </ul>
      </div>

      <form class="account__block form" @submit.prevent="changePassword">
        <h2>Mot de passe</h2>
        <div class="field" style="max-width: 420px"><label for="p-cur">Actuel</label><input id="p-cur" v-model="pwd.current" type="password" autocomplete="current-password" required></div>
        <div class="form__row" style="max-width: 640px">
          <div class="field"><label for="p-new">Nouveau</label><input id="p-new" v-model="pwd.next" type="password" autocomplete="new-password" minlength="10" required></div>
          <div class="field"><label for="p-conf">Confirmer</label><input id="p-conf" v-model="pwd.confirm" type="password" autocomplete="new-password" required></div>
        </div>
        <p class="form__status" :class="status.password.includes('modifié') ? 'is-success' : 'is-error'">{{ status.password }}</p>
        <div><button type="submit" class="btn btn--primary">Modifier</button></div>
      </form>

      <div class="account__block">
        <h2>Session et données</h2>
        <div class="account__actions">
          <button type="button" class="btn btn--ghost btn--small" @click="logout">Se déconnecter</button>
          <button type="button" class="btn btn--ghost btn--small danger" @click="remove">Supprimer mon compte</button>
        </div>
        <p class="muted" style="font-size: 14px; margin-top: 12px">La suppression efface votre compte et vos données (droit à l'effacement, RGPD).</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero { position: relative; overflow: hidden; padding: clamp(40px, 6vw, 72px) 0; }
.hero__bg { position: absolute; inset: 0; background: radial-gradient(55% 70% at 18% 40%, rgba(193, 31, 53, .3), transparent 70%); }
.card { position: relative; display: flex; flex-wrap: wrap; align-items: center; gap: clamp(24px, 4vw, 48px); }
.card__avatar { width: clamp(140px, 22vw, 220px); height: auto; border-radius: 50%; border: 4px solid var(--or); background: var(--encre); flex-shrink: 0; animation: hero-in .8s var(--ease-out) both; }
.card__identity { display: grid; justify-items: start; gap: 6px; animation: hero-in .8s .12s var(--ease-out) both; }
.card__identity h1 { font-size: clamp(40px, 7vw, 76px); margin: 0 0 10px; }
.card__meta { display: flex; flex-wrap: wrap; gap: 6px 22px; margin: 0 0 18px; color: var(--fg-muted); font-size: 15px; }
.account { display: grid; gap: 48px; }
.account__block h2 { font-size: clamp(26px, 3vw, 34px); }
.account__current { display: flex; flex-wrap: wrap; align-items: center; gap: 22px; }
.account__current img { width: 128px; height: 128px; border-radius: 50%; border: 3px solid var(--line); background: var(--encre); }
.account__current strong { font-size: 18px; }
.account__current p { margin: 4px 0 10px; font-size: 15px; }
.account__current button { background: none; border: 0; padding: 0; cursor: pointer; font: inherit; font-weight: 700; color: var(--fg); }
.account__actions { display: flex; flex-wrap: wrap; gap: 12px; }
.danger { color: var(--grenat); border-color: var(--grenat); }
.danger:hover { color: var(--marbre); background: var(--grenat); }
</style>
