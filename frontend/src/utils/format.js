const fmt = new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
const fmtShort = new Intl.DateTimeFormat('fr-FR', { month: 'short', year: 'numeric' })

export function formatDate(iso) { return iso ? fmt.format(new Date(iso)) : '' }
export function formatMonth(iso) { return iso ? fmtShort.format(new Date(iso)) : '' }

export function slugify(text = '') {
  return text
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

/** Date ISO → valeur pour <input type="datetime-local"> (heure locale). */
export function toLocalInput(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

export function fromLocalInput(value) {
  return value ? new Date(value).toISOString() : null
}
