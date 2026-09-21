<script setup>
defineProps({ items: { type: Array, default: () => [] }, columns: { type: Number, default: 3 } })
</script>

<template>
  <div class="grid" :class="columns === 2 ? 'grid--2' : 'grid--3'">
    <article v-for="(p, i) in items" :key="i" v-reveal="i * 90" class="pillar">
      <div class="pillar__num">{{ p.num }}</div>
      <h3>{{ p.title }}</h3>
      <p>{{ p.text }}</p>
    </article>
  </div>
</template>
