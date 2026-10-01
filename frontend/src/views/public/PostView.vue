<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { api } from '@/api/client'
import { useHead } from '@/composables/useHead'
import { formatDate } from '@/utils/format'
import MarkdownBlock from '@/components/MarkdownBlock.vue'
import DevlogPlayer from '@/components/DevlogPlayer.vue'
import CtaBlock from '@/components/CtaBlock.vue'
import NotFoundView from './NotFoundView.vue'

const route = useRoute()
const post = ref(null)
const notFound = ref(false)

watch(() => route.params.slug, async (slug) => {
  if (!slug) return
  notFound.value = false
  post.value = null
  try {
    post.value = await api.get(`/api/posts/${slug}`)
  } catch {
    notFound.value = true
  }
}, { immediate: true })

useHead(computed(() => post.value?.title || ''), computed(() => post.value?.excerpt))
</script>

<template>
  <NotFoundView v-if="notFound" />
  <template v-else-if="post">
    <section class="page-head surface-light">
      <div class="container container--narrow">
        <span class="kicker">{{ post.tag }} · <time :datetime="post.published_at">{{ formatDate(post.published_at || post.created_at) }}</time></span>
        <h1 class="title">{{ post.title }}</h1>
        <p v-if="post.excerpt" class="lede">{{ post.excerpt }}</p>
      </div>
    </section>
    <div class="frise" aria-hidden="true"></div>
    <article class="section surface-light">
      <div class="container container--narrow">
        <DevlogPlayer v-if="post.embed_url" :src="post.embed_url" :title="post.title" />
        <img v-else-if="post.cover_url" v-reveal :src="post.cover_url" :alt="`Illustration : ${post.title}`" class="cover" loading="lazy" decoding="async">
        <MarkdownBlock :source="post.body_md" />
        <p style="margin-top: 48px"><RouterLink class="link-arrow" :to="{ name: 'journal' }">Tous les billets</RouterLink></p>
      </div>
    </article>
    <CtaBlock />
  </template>
</template>

<style scoped>
.title { font-size: clamp(40px, 6vw, 80px); animation: hero-in .8s var(--ease-out) both; }
.cover { clip-path: var(--chamfer); margin-bottom: 40px; width: 100%; }
</style>
