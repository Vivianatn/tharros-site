/**
 * v-reveal — fait apparaître l'élément quand il entre dans la fenêtre.
 * v-reveal="120" ajoute un délai (ms), utile pour décaler les cartes d'une grille.
 */
const observer = typeof IntersectionObserver === 'undefined'
  ? null
  : new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.dataset.reveal = 'visible'
        observer.unobserve(entry.target)
      }
    }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 })

export const reveal = {
  mounted(el, binding) {
    if (!observer) { el.dataset.reveal = 'visible'; return }
    el.dataset.reveal = ''
    if (binding.value) el.style.setProperty('--reveal-delay', `${binding.value}ms`)
    observer.observe(el)
    // filet de sécurité : rien ne doit rester invisible
    setTimeout(() => { el.dataset.reveal = 'visible' }, 2500)
  },
  unmounted(el) { observer?.unobserve(el) },
}
