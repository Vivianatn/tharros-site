<script setup>
import { RouterLink } from 'vue-router'
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import { useForm } from '@/composables/useForm'
import PageHead from '@/components/PageHead.vue'
import IconArrow from '@/components/IconArrow.vue'

const content = useContentStore()
const { values, errors, status, sending, submit, touch } = useForm(
  '/api/contact',
  { name: '', email: '', subject: '', message: '', consent: false },
  {
    name: { required: true, min: 2, max: 80 },
    email: { required: true, email: true, max: 160 },
    subject: { required: true, max: 120 },
    message: { required: true, min: 20, max: 4000 },
    consent: { required: true, checkbox: true },
  },
)
useHead('Contact', 'Contactez le studio Tharros : presse, collaborations, questions sur Muses. Réponse sous cinq jours ouvrés.')
</script>

<template>
  <PageHead kicker="Contact" title="Écrivez-nous" lede="Presse, collaborations, questions ou simple message : une seule porte, et une réponse sous cinq jours ouvrés." />
  <section class="section surface-light">
    <div class="container feature" style="align-items: start">
      <form v-reveal class="form" novalidate aria-label="Formulaire de contact" @submit.prevent="submit">
        <div class="form__row">
          <div class="field" :class="{ 'is-invalid': errors.name }">
            <label for="c-name">Nom</label>
            <input id="c-name" v-model="values.name" type="text" autocomplete="name" maxlength="80" @blur="touch('name')">
            <span class="field__error">{{ errors.name }}</span>
          </div>
          <div class="field" :class="{ 'is-invalid': errors.email }">
            <label for="c-email">Adresse e-mail</label>
            <input id="c-email" v-model="values.email" type="email" autocomplete="email" maxlength="160" @blur="touch('email')">
            <span class="field__error">{{ errors.email }}</span>
          </div>
        </div>
        <div class="field" :class="{ 'is-invalid': errors.subject }">
          <label for="c-subject">Objet</label>
          <input id="c-subject" v-model="values.subject" type="text" maxlength="120" placeholder="Presse, collaboration, question…" @blur="touch('subject')">
          <span class="field__error">{{ errors.subject }}</span>
        </div>
        <div class="field" :class="{ 'is-invalid': errors.message }">
          <label for="c-message">Message</label>
          <textarea id="c-message" v-model="values.message" maxlength="4000" @blur="touch('message')"></textarea>
          <span class="field__error">{{ errors.message }}</span>
        </div>
        <div class="field field--check" :class="{ 'is-invalid': errors.consent }">
          <input id="c-consent" v-model="values.consent" type="checkbox" @change="touch('consent')">
          <div>
            <label for="c-consent">J'accepte que mes données soient utilisées pour traiter ma demande, conformément à la <RouterLink :to="{ name: 'legal', params: { slug: 'confidentialite' } }">politique de confidentialité</RouterLink>.</label>
            <span class="field__error">{{ errors.consent }}</span>
          </div>
        </div>
        <div class="hp" aria-hidden="true"><label for="c-website">Ne pas remplir</label><input id="c-website" v-model="values.website" type="text" tabindex="-1" autocomplete="off"></div>
        <div><button type="submit" class="btn btn--primary" :disabled="sending">Envoyer le message <IconArrow /></button></div>
        <p class="form__status" :class="status.type && `is-${status.type}`" role="status" aria-live="polite">{{ sending ? 'Envoi en cours…' : status.message }}</p>
      </form>

      <aside v-reveal="120">
        <h2 class="h-small">Ou directement</h2>
        <ul class="spec-list">
          <li><span class="k">Presse</span><span><a :href="`mailto:${content.site.press_email}`">{{ content.site.press_email }}</a><br><small>Kit média sur la <RouterLink :to="{ name: 'press' }">page presse</RouterLink>.</small></span></li>
          <li><span class="k">Général</span><span><a :href="`mailto:${content.site.contact_email}`">{{ content.site.contact_email }}</a></span></li>
          <li><span class="k">Adresse</span><span>{{ content.site.name }} Studio<br>{{ content.site.address }}</span></li>
        </ul>
        <p class="muted" style="font-size: 14px">Le studio étant une seule personne, merci de votre patience. Avant d'écrire, la <RouterLink :to="{ name: 'faq' }">FAQ</RouterLink> répond peut-être déjà.</p>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.h-small { font-size: clamp(28px, 3.4vw, 40px); }
</style>
