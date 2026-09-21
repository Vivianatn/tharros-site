<script setup>
import { RouterLink } from 'vue-router'
defineProps({ game: { type: Object, required: true } })
</script>

<template>
  <article class="game-card surface-light">
    <RouterLink class="game-card__art" :to="{ name: 'game', params: { slug: game.slug } }" tabindex="-1" aria-hidden="true">
      <img v-if="game.cover_url" :src="game.cover_url" :alt="`Visuel de ${game.title}`" width="800" height="600" loading="lazy" decoding="async">
    </RouterLink>
    <div class="game-card__body">
      <span class="game-card__tag">{{ game.status }}<template v-if="game.builds?.length"> · Téléchargeable</template></span>
      <h3>{{ game.title }}</h3>
      <p>{{ game.tagline }}</p>
      <RouterLink class="link-arrow" :to="{ name: 'game', params: { slug: game.slug } }">Fiche du jeu</RouterLink>
    </div>
  </article>
</template>

<style scoped>
.game-card { display: grid; grid-template-rows: auto 1fr; clip-path: var(--chamfer); overflow: hidden; border: 1px solid var(--line); transition: transform .35s var(--ease); }
.game-card:hover { transform: translateY(-4px); }
.game-card__art { display: block; aspect-ratio: 16 / 10; background: var(--charbon); overflow: hidden; }
.game-card__art img { width: 100%; height: 100%; object-fit: cover; transition: transform .8s var(--ease-out); }
.game-card:hover .game-card__art img { transform: scale(1.04); }
.game-card__body { padding: 26px 26px 30px; }
.game-card__tag { font-size: 12px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; color: var(--kicker); }
h3 { margin: 8px 0 10px; font-size: 32px; }
p { font-size: 15px; color: var(--fg-soft); margin-bottom: 16px; }
</style>
