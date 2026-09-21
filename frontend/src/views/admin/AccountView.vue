<script setup>
import { onMounted, reactive, ref } from 'vue'
import { api } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import { useHead } from '@/composables/useHead'

const auth = useAuthStore()
const toast = useToast()
const form = reactive({ current_password: '', new_password: '', confirm: '' })
const busy = ref(false)
const mail = ref(null)
const mailBusy = ref(false)
useHead('Compte — administration')
onMounted(async () => { mail.value = await api.get('/api/admin/mail/status', { auth: true }) })

async function testMail() {
  mailBusy.value = true
  try {
    const r = await api.post('/api/admin/mail/test', {}, { auth: true })
    toast.success(r.message)
  } catch (e) {
    toast.error(e.message)
  } finally {
    mailBusy.value = false
  }
}

async function submit() {
  if (form.new_password !== form.confirm) return toast.error('Les deux mots de passe ne correspondent pas')
  if (form.new_password.length < 10) return toast.error('Dix caractères minimum')
  busy.value = true
  try {
    await api.post('/api/auth/password', { current_password: form.current_password, new_password: form.new_password }, { auth: true })
    toast.success('Mot de passe modifié')
    Object.assign(form, { current_password: '', new_password: '', confirm: '' })
  } catch (e) {
    toast.error(e.message)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="admin-head"><div><span class="kicker">Compte</span><h1>Compte &amp; notifications</h1><p>Connecté·e en tant que {{ auth.user?.email }}.</p></div></div>

  <div v-if="mail" class="card" style="max-width: 720px">
    <h2>Notifications par e-mail</h2>
    <p>Les messages du formulaire de contact et les inscriptions à la liste d'attente sont envoyés à <strong>{{ mail.to }}</strong>. Ils restent aussi consultables ici, dans <em>Messages</em> et <em>Liste d'attente</em>.</p>
    <ul class="spec-list" style="margin: 12px 0 20px">
      <li><span class="k">Service</span><span><span class="pill" :class="mail.mode === 'log' ? 'pill--off' : 'pill--on'">{{ mail.mode === 'smtp' ? 'SMTP (Gmail)' : mail.mode === 'resend' ? 'Resend' : 'Non configuré' }}</span></span></li>
      <li v-if="mail.mode === 'smtp'"><span class="k">Serveur</span><span>{{ mail.smtp_host }} · compte {{ mail.smtp_user }}</span></li>
      <li><span class="k">Expéditeur</span><span>{{ mail.from }}</span></li>
    </ul>
    <p v-if="mail.mode === 'log'" class="hint" style="margin-bottom: 14px">Pour activer l'envoi : dans le fichier <code>.env</code> à la racine du projet, renseignez <code>SMTP_PASSWORD</code> avec un mot de passe d'application Google (myaccount.google.com/apppasswords), puis relancez le serveur.</p>
    <button type="button" class="btn btn--secondary btn--small" :disabled="mailBusy" @click="testMail">{{ mailBusy ? 'Envoi…' : 'Envoyer un e-mail de test' }}</button>
  </div>

  <h2 style="font-size: 22px; margin: 28px 0 12px">Mot de passe administrateur</h2>
  <form class="card" style="max-width: 520px" @submit.prevent="submit">
    <div class="form">
      <div class="field"><label for="cur">Mot de passe actuel</label><input id="cur" v-model="form.current_password" type="password" autocomplete="current-password" required></div>
      <div class="field"><label for="new">Nouveau mot de passe</label><input id="new" v-model="form.new_password" type="password" autocomplete="new-password" minlength="10" required><span class="hint">Dix caractères minimum. Une phrase de passe est idéale.</span></div>
      <div class="field"><label for="conf">Confirmer</label><input id="conf" v-model="form.confirm" type="password" autocomplete="new-password" required></div>
      <div><button type="submit" class="btn btn--primary" :disabled="busy">Modifier</button></div>
    </div>
  </form>
</template>
