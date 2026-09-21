<script setup>
defineProps({ items: { type: Array, default: () => [] } })
</script>

<template>
  <ul class="spec-list">
    <li v-for="(it, i) in items" :key="i"><span class="k">{{ it.k }}</span><span>{{ it.v }}</span></li>
  </ul>
</template>
