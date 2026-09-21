<script setup>
defineProps({ kicker: String, title: String, lede: String, narrow: Boolean })
</script>

<template>
  <section class="page-head">
    <div class="container" :class="{ 'container--narrow': narrow }">
      <span v-if="kicker" class="kicker">{{ kicker }}</span>
      <h1 class="page-head__title">{{ title }}</h1>
      <p v-if="lede" class="lede">{{ lede }}</p>
      <slot />
    </div>
  </section>
  <div class="frise" aria-hidden="true"></div>
</template>

<style scoped>
.page-head__title { animation: hero-in .8s var(--ease-out) both; }
.lede { animation: hero-in .8s .15s var(--ease-out) both; }
</style>
