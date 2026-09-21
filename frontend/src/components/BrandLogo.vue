<script setup>
/** Logo horizontal Tharros — emblème lion-aigle + wordmark. Couleur héritée (currentColor). */
defineProps({ height: { type: Number, default: 44 } })
</script>

<template>
  <svg viewBox="0 0 690 180" :style="{ height: height + 'px', width: 'auto' }" aria-hidden="true" focusable="false">
    <circle cx="90" cy="90" r="87" fill="none" stroke="currentColor" stroke-width="5" />
    <polygon points="90,15.8 59,77.8 121,77.8" fill="currentColor" />
    <g transform="rotate(-20 54 99)"><polygon points="78.5,81 29.5,99 78.5,117" fill="currentColor" /></g>
    <g transform="rotate(20 126 99)"><polygon points="101.5,81 150.5,99 101.5,117" fill="currentColor" /></g>
    <rect x="83" y="131.6" width="14" height="14" fill="#C11F35" transform="rotate(45 90 138.6)" />
    <text x="212" y="134" font-family="'Big Shoulders Display', Impact, sans-serif" font-weight="800" font-size="122" letter-spacing="2" fill="currentColor">THARROS</text>
  </svg>
</template>
