import { defineStore } from 'pinia'

const KEY = 'tharros_consent'

function read() {
  try { return localStorage.getItem(KEY) } catch { return null }
}

/** Consentement cookies : l'outil de mesure d'audience n'est chargé qu'après « Accepter ». */
export const useConsentStore = defineStore('consent', {
  state: () => ({ choice: read(), bannerOpen: read() === null }),
  actions: {
    choose(value, analyticsDomain) {
      this.choice = value
      this.bannerOpen = false
      try { localStorage.setItem(KEY, value) } catch { /* stockage indisponible */ }
      if (value === 'accepted') this.loadAnalytics(analyticsDomain)
    },
    open() { this.bannerOpen = true },
    loadAnalytics(domain) {
      if (!domain || document.querySelector('script[data-analytics]')) return
      const s = document.createElement('script')
      s.defer = true
      s.src = 'https://plausible.io/js/script.js'
      s.dataset.domain = domain
      s.dataset.analytics = '1'
      document.head.appendChild(s)
    },
  },
})
