<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useContentStore } from '@/stores/content'
import { useHead } from '@/composables/useHead'
import PageHead from '@/components/PageHead.vue'
import MarkdownBlock from '@/components/MarkdownBlock.vue'
import NotFoundView from './NotFoundView.vue'

const route = useRoute()
const content = useContentStore()
const page = computed(() => content.legal(route.params.slug))
useHead(computed(() => page.value?.title || ''), computed(() => page.value?.lede))
</script>

<template>
  <NotFoundView v-if="!page" />
  <template v-else>
    <PageHead kicker="Légal" :title="page.title" :lede="page.lede" narrow />
    <section class="section surface-light">
      <div class="container container--narrow"><MarkdownBlock :source="page.body_md" /></div>
    </section>
  </template>
</template>
