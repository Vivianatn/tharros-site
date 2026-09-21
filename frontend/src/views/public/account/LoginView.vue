<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useMemberStore } from '@/stores/member'
import { useHead } from '@/composables/useHead'
import PageHead from '@/components/PageHead.vue'
import IconArrow from '@/components/IconArrow.vue'

const member = useMemberStore()
const router = useRouter()
const route = useRoute()
const form = reactive({ email: '', password: '' })
const error = ref('')
const busy = ref(false)
useHead('Connexion', 'Connectez-vous à votre compte Tharros.')

async function submit() {
  error.value = ''
  busy.value = true
  try {
    await member.login(form.email.trim(), form.password)
    router.push(route.query.next || { name: 'account' })
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <PageHead kicker="Compte" title="Connexion" narrow />
  <section class="section surface-light">
    <div class="container container--narrow">
      <form v-reveal class="form" style="max-width: 480px" novalidate @submit.prevent="submit">
        <div class="field">
          <label for="l-email">Adresse e-mail</label>
          <input id="l-email" v-model="form.email" type="email" autocomplete="username" required>
        </div>
        <div class="field">
          <label for="l-password">Mot de passe</label>
          <input id="l-password" v-model="form.password" type="password" autocomplete="current-password" required>
        </div>
        <p v-if="error" class="form__status is-error" role="alert">{{ error }}</p>
        <div><button type="submit" class="btn btn--primary" :disabled="busy">{{ busy ? 'Connexion…' : 'Se connecter' }} <IconArrow /></button></div>
        <p class="muted">Pas encore de compte ? <RouterLink :to="{ name: 'account.register', query: route.query }">Créer un compte</RouterLink></p>
      </form>
    </div>
  </section>
</template>
