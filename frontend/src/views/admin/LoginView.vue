<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useHead } from '@/composables/useHead'
import BrandLogo from '@/components/BrandLogo.vue'
import '@/styles/admin.css'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const email = ref('')
const password = ref('')
const error = ref('')
const busy = ref(false)
useHead('Connexion à l’administration')

async function submit() {
  error.value = ''
  busy.value = true
  try {
    await auth.login(email.value.trim(), password.value)
    router.push(route.query.next || { name: 'admin.dashboard' })
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="login">
    <form class="login__card" @submit.prevent="submit">
      <div style="color: var(--encre); margin-bottom: 20px"><BrandLogo :height="40" variant="fonce" /></div>
      <span class="kicker">Administration</span>
      <h1>Connexion</h1>
      <div class="form">
        <div class="field">
          <label for="email">E-mail</label>
          <input id="email" v-model="email" type="email" autocomplete="username" required>
        </div>
        <div class="field">
          <label for="password">Mot de passe</label>
          <input id="password" v-model="password" type="password" autocomplete="current-password" required>
        </div>
        <p v-if="error" class="form__status is-error" role="alert">{{ error }}</p>
        <div><button type="submit" class="btn btn--primary" :disabled="busy">{{ busy ? 'Connexion…' : 'Se connecter' }}</button></div>
        <p class="hint" style="font-size: 13px; color: var(--pierre)"><a href="/">← Retour au site</a></p>
      </div>
    </form>
  </div>
</template>
