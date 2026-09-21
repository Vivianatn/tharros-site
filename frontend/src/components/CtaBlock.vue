<script setup>
import { RouterLink } from 'vue-router'
import { useContentStore } from '@/stores/content'
import { useForm } from '@/composables/useForm'
import IconArrow from './IconArrow.vue'

const content = useContentStore()
const { values, errors, status, sending, submit, touch } = useForm(
  '/api/subscribe',
  { email: '', consent: false },
  { email: { required: true, email: true, max: 160 }, consent: { required: true, checkbox: true } },
)
</script>

<template>
  <section id="rejoindre" class="section" aria-labelledby="cta-title">
    <div class="container">
      <div v-reveal class="cta-block surface-charbon">
        <span class="kicker">{{ content.cta.kicker }}</span>
        <h2 id="cta-title">{{ content.cta.title }}</h2>
        <p class="lede">{{ content.cta.text }}</p>
        <form class="form" novalidate @submit.prevent="submit">
          <div class="field" :class="{ 'is-invalid': errors.email }">
            <label for="nl-email">Adresse e-mail</label>
            <input id="nl-email" v-model="values.email" type="email" autocomplete="email" maxlength="160" placeholder="vous@exemple.fr" @blur="touch('email')">
            <span class="field__error" aria-live="polite">{{ errors.email }}</span>
          </div>
          <div class="field field--check" :class="{ 'is-invalid': errors.consent }">
            <input id="nl-consent" v-model="values.consent" type="checkbox" @change="touch('consent')">
            <div>
              <label for="nl-consent">J'accepte de recevoir les nouvelles de Tharros et j'ai lu la <RouterLink :to="{ name: 'legal', params: { slug: 'confidentialite' } }">politique de confidentialité</RouterLink>. Désinscription en un clic.</label>
              <span class="field__error" aria-live="polite">{{ errors.consent }}</span>
            </div>
          </div>
          <div class="hp" aria-hidden="true"><label for="nl-website">Ne pas remplir</label><input id="nl-website" v-model="values.website" type="text" tabindex="-1" autocomplete="off"></div>
          <div><button type="submit" class="btn btn--primary" :disabled="sending">{{ content.cta.button }} <IconArrow /></button></div>
          <p class="form__status" :class="status.type && `is-${status.type}`" role="status" aria-live="polite">{{ sending ? 'Envoi en cours…' : status.message }}</p>
        </form>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta-block { padding: clamp(40px, 6vw, 72px); clip-path: var(--chamfer); }
.cta-block h2 { font-size: clamp(40px, 6vw, 72px); line-height: .92; }
.form { max-width: 620px; }
</style>
