<script setup>
import { onMounted, ref } from 'vue'

/** Chiffre clé animé : compte de 0 à la valeur quand il devient visible. */
const props = defineProps({ value: { type: String, required: true }, label: String })
const el = ref(null)
const shown = ref(props.value)

onMounted(() => {
  const match = props.value.match(/^(\d+)(.*)$/)
  if (!match || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return
  const target = Number(match[1]); const suffix = match[2]
  shown.value = '0' + suffix
  const io = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return
    io.disconnect()
    const start = performance.now(); const duration = 1200
    const tick = (now) => {
      const p = Math.min(1, (now - start) / duration)
      shown.value = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix
      if (p < 1) requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
  }, { threshold: 0.5 })
  io.observe(el.value)
})
</script>

<template>
  <div ref="el" v-reveal>
    <div class="stat__num">{{ shown }}</div>
    <div class="stat__label">{{ label }}</div>
  </div>
</template>
