import { marked } from 'marked'
import DOMPurify from 'dompurify'

marked.setOptions({ gfm: true, breaks: true })

/** Convertit du Markdown en HTML sûr (scripts et attributs dangereux retirés). */
export function renderMarkdown(md = '') {
  return DOMPurify.sanitize(marked.parse(md), { USE_PROFILES: { html: true } })
}
