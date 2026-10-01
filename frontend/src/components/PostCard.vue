<script setup>
import { RouterLink } from 'vue-router'
import { formatMonth } from '@/utils/format'
defineProps({ post: { type: Object, required: true } })
</script>

<template>
  <article class="post">
    <time :datetime="post.published_at">{{ formatMonth(post.published_at || post.created_at) }}</time>
    <div>
      <span class="post__tag">{{ post.tag }}<template v-if="post.embed_url"> · <span class="post__anim">Animé</span></template></span>
      <h2><RouterLink :to="{ name: 'post', params: { slug: post.slug } }">{{ post.title }}</RouterLink></h2>
      <p>{{ post.excerpt }}</p>
      <RouterLink class="link-arrow" :to="{ name: 'post', params: { slug: post.slug } }">Lire le billet</RouterLink>
    </div>
  </article>
</template>

<style scoped>
.post { display: grid; grid-template-columns: 160px 1fr; gap: 24px; padding: 32px 0; border-top: 1px solid var(--line); }
@media (max-width: 640px) { .post { grid-template-columns: 1fr; gap: 8px; } }
time { font-family: var(--font-display); font-size: 26px; font-weight: 800; color: var(--kicker); line-height: 1.1; text-transform: capitalize; }
h2 { font-size: clamp(26px, 3vw, 34px); margin-bottom: 10px; }
h2 a { color: var(--heading); text-decoration: none; }
h2 a:hover { color: var(--link); }
p { color: var(--fg-soft); margin-bottom: .6em; }
.post__tag { font-size: 12px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; color: var(--fg-muted); }
.post__anim { color: var(--kicker); }
</style>
