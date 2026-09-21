import { reactive, ref } from 'vue'
import { api } from '@/api/client'

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/

/**
 * Formulaire public : validation côté client, pot de miel et délai anti-robot.
 * rules : { champ: { required, email, min, max, checkbox } }
 */
export function useForm(endpoint, initial, rules) {
  const values = reactive({ ...initial, website: '' })
  const errors = reactive({})
  const status = ref({ type: '', message: '' })
  const sending = ref(false)
  const startedAt = Date.now()

  function validateField(name) {
    const rule = rules[name]
    const v = values[name]
    if (!rule) return ''
    if (rule.checkbox) return rule.required && !v ? 'Veuillez cocher cette case pour continuer.' : ''
    const s = String(v ?? '').trim()
    if (rule.required && !s) return 'Ce champ est obligatoire.'
    if (rule.email && s && !EMAIL_RE.test(s)) return 'Adresse e-mail invalide.'
    if (rule.min && s.length < rule.min) return `Minimum ${rule.min} caractères.`
    if (rule.max && s.length > rule.max) return `Maximum ${rule.max} caractères.`
    return ''
  }

  function validate() {
    let ok = true
    for (const name of Object.keys(rules)) {
      errors[name] = validateField(name)
      if (errors[name]) ok = false
    }
    return ok
  }

  function touch(name) { errors[name] = validateField(name) }

  async function submit() {
    status.value = { type: '', message: '' }
    if (!validate()) return
    sending.value = true
    try {
      const res = await api.post(endpoint, { ...values, elapsed: Date.now() - startedAt })
      status.value = { type: 'success', message: res.message }
      Object.assign(values, initial)
    } catch (e) {
      status.value = { type: 'error', message: `Envoi impossible : ${e.message}.` }
    } finally {
      sending.value = false
    }
  }

  return { values, errors, status, sending, submit, touch }
}
