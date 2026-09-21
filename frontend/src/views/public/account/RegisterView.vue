<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useMemberStore } from '@/stores/member'
import { useHead } from '@/composables/useHead'
import PageHead from '@/components/PageHead.vue'
import IconArrow from '@/components/IconArrow.vue'
import AvatarPicker from '@/components/AvatarPicker.vue'
import { AVATARS } from '@/utils/avatars'

const member = useMemberStore()
const router = useRouter()
const route = useRoute()
const form = reactive({ display_name: '', email: '', password: '', confirm: '', avatar: AVATARS[Math.floor(Math.random() * AVATARS.length)].id, newsletter: false, consent: false, website: '' })
const errors = reactive({})
const error = ref('')
const busy = ref(false)
const startedAt = Date.now()
useHead('Créer un compte', 'Créez votre compte Tharros pour télécharger les jeux et suivre le studio.')

function validate() {
  errors.display_name = form.display_name.trim().length < 2 ? 'Deux caractères minimum.' : ''
  errors.email = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.email) ? '' : 'Adresse e-mail invalide.'
  errors.password = form.password.length < 10 ? 'Dix caractères minimum.' : ''
  errors.confirm = form.confirm !== form.password ? 'Les deux mots de passe ne correspondent pas.' : ''
  errors.consent = form.consent ? '' : 'Vous devez accepter les conditions.'
  return !Object.values(errors).some(Boolean)
}

async function submit() {
  error.value = ''
  if (!validate()) return
  busy.value = true
  try {
    await member.register({ display_name: form.display_name, email: form.email, password: form.password, avatar: form.avatar, newsletter: form.newsletter, consent: form.consent, website: form.website, elapsed: Date.now() - startedAt })
    router.push(route.query.next || { name: 'account' })
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <PageHead kicker="Compte" title="Créer un compte" lede="Un compte pour télécharger les jeux, participer aux phases de test et suivre le studio." narrow />
  <section class="section surface-light">
    <div class="container container--narrow">
      <form v-reveal class="form account-form" novalidate @submit.prevent="submit">
        <div class="form__row">
          <div class="field" :class="{ 'is-invalid': errors.display_name }">
            <label for="r-name">Pseudo</label>
            <input id="r-name" v-model="form.display_name" type="text" autocomplete="nickname" maxlength="60">
            <span class="field__error">{{ errors.display_name }}</span>
          </div>
          <div class="field" :class="{ 'is-invalid': errors.email }">
            <label for="r-email">Adresse e-mail</label>
            <input id="r-email" v-model="form.email" type="email" autocomplete="email" maxlength="160">
            <span class="field__error">{{ errors.email }}</span>
          </div>
        </div>
        <div class="form__row">
          <div class="field" :class="{ 'is-invalid': errors.password }">
            <label for="r-password">Mot de passe</label>
            <input id="r-password" v-model="form.password" type="password" autocomplete="new-password" minlength="10">
            <span class="field__error">{{ errors.password || 'Dix caractères minimum.' }}</span>
          </div>
          <div class="field" :class="{ 'is-invalid': errors.confirm }">
            <label for="r-confirm">Confirmer</label>
            <input id="r-confirm" v-model="form.confirm" type="password" autocomplete="new-password">
            <span class="field__error">{{ errors.confirm }}</span>
          </div>
        </div>
        <div class="field">
          <label>Image de profil <span class="muted" style="text-transform: none; letter-spacing: 0; font-weight: 500">— modifiable plus tard</span></label>
          <AvatarPicker v-model="form.avatar" />
        </div>
        <div class="field field--check">
          <input id="r-news" v-model="form.newsletter" type="checkbox">
          <label for="r-news">Je souhaite recevoir les nouvelles du studio (un e-mail par mois, au plus).</label>
        </div>
        <div class="field field--check" :class="{ 'is-invalid': errors.consent }">
          <input id="r-consent" v-model="form.consent" type="checkbox">
          <div>
            <label for="r-consent">J'accepte les <RouterLink :to="{ name: 'legal', params: { slug: 'cgu' } }">conditions d'utilisation</RouterLink> et la <RouterLink :to="{ name: 'legal', params: { slug: 'confidentialite' } }">politique de confidentialité</RouterLink>.</label>
            <span class="field__error">{{ errors.consent }}</span>
          </div>
        </div>
        <div class="hp" aria-hidden="true"><label for="r-website">Ne pas remplir</label><input id="r-website" v-model="form.website" type="text" tabindex="-1" autocomplete="off"></div>
        <p v-if="error" class="form__status is-error" role="alert">{{ error }}</p>
        <div><button type="submit" class="btn btn--primary" :disabled="busy">{{ busy ? 'Création…' : 'Créer mon compte' }} <IconArrow /></button></div>
        <p class="muted">Déjà un compte ? <RouterLink :to="{ name: 'account.login', query: route.query }">Se connecter</RouterLink></p>
      </form>
    </div>
  </section>
</template>
