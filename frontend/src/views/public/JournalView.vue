<script setup>
import { ref } from 'vue'
import { api } from '@/api/client'
import { useHead } from '@/composables/useHead'
import PageHead from '@/components/PageHead.vue'
import PostCard from '@/components/PostCard.vue'
import CtaBlock from '@/components/CtaBlock.vue'

const posts = ref([])
const error = ref('')
api.get('/api/posts').then((p) => { posts.value = p }).catch((e) => { error.value = e.message })
useHead('Journal de développement', "Le journal de développement de Muses, publié par Tharros : avancées, doutes, coulisses d'un studio d'une seule personne.")
</script>

<template>
  <PageHead kicker="Journal de développement" title="Carnet de bord" lede="Un billet par mois, y compris quand ça n'avance pas. C'est le serment de transparence du studio : vous voyez le jeu se construire en direct." />
  <section class="section surface-light">
    <div class="container container--narrow">
      <p v-if="error" class="form__status is-error">{{ error }}</p>
      <p v-else-if="!posts.length" class="muted">Aucun billet publié pour le moment.</p>
      <div v-for="(p, i) in posts" :key="p.id" v-reveal="Math.min(i, 5) * 80"><PostCard :post="p" /></div>
    </div>
  </section>
  <CtaBlock />
</template>
