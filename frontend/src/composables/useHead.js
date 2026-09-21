import { watchEffect, unref } from 'vue'

const SITE = 'Tharros'

function setMeta(selector, attr, value) {
  const el = document.querySelector(selector)
  if (el) el.setAttribute(attr, value)
}

/** Titre, description, Open Graph et canonical uniques par page, mis à jour à chaque navigation. */
export function useHead(title, description) {
  watchEffect(() => {
    const t = unref(title)
    const d = unref(description)
    document.title = t ? `${t} | ${SITE}` : `${SITE} — Studio de jeu vidéo indépendant`
    if (d) {
      setMeta('meta[name="description"]', 'content', d)
      setMeta('meta[property="og:description"]', 'content', d)
    }
    setMeta('meta[property="og:title"]', 'content', document.title)
    let canonical = document.querySelector('link[rel="canonical"]')
    if (!canonical) {
      canonical = document.createElement('link')
      canonical.rel = 'canonical'
      document.head.appendChild(canonical)
    }
    canonical.href = location.origin + location.pathname
  })
}
