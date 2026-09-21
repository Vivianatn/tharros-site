import { defineStore } from 'pinia'
import { api } from '@/api/client'

/** Contenu public du site, chargé une fois puis partagé par toutes les pages. */
export const useContentStore = defineStore('content', {
  state: () => ({
    settings: {},
    games: [],
    latestPosts: [],
    faq: [],
    loaded: false,
    error: null,
  }),
  getters: {
    site: (s) => s.settings.site || {},
    home: (s) => s.settings.home || {},
    cta: (s) => s.settings.cta || {},
    studio: (s) => s.settings.studio || {},
    press: (s) => s.settings.press || {},
    featuredGame: (s) => s.games.find((g) => g.featured) || s.games[0] || null,
    legal: (s) => (slug) => s.settings[`legal.${slug}`] || null,
  },
  actions: {
    async load(force = false) {
      if (this.loaded && !force) return
      try {
        const data = await api.get('/api/content')
        this.settings = data.settings
        this.games = data.games
        this.latestPosts = data.latest_posts
        this.faq = data.faq
        this.loaded = true
        this.error = null
      } catch (e) {
        this.error = e.message
      }
    },
  },
})
