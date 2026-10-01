<script setup>
/**
 * Logo horizontal Tharros (identité « sceau du lion »).
 * `variant` : 'clair' pour les fonds sombres (en-tête, pied de page), 'fonce' pour les fonds clairs.
 */
defineProps({
  height: { type: Number, default: 44 },
  variant: { type: String, default: 'clair' },
})
</script>

<template>
  <img
    :src="`/brand/tharros-logo-horizontal-${variant}.svg`"
    alt="Tharros" :style="{ height: height + 'px', width: 'auto' }"
    width="822" height="220" decoding="async"
  >
</template>
