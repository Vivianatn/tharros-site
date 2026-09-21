/**
 * Client HTTP minimal pour l'API Tharros.
 * Aucun secret ici : le jeton d'administration est obtenu à la connexion et gardé en session.
 */
const TOKEN_KEY = 'tharros_admin_token'

export function getToken() {
  try { return sessionStorage.getItem(TOKEN_KEY) } catch { return null }
}

export function setToken(token) {
  try {
    if (token) sessionStorage.setItem(TOKEN_KEY, token)
    else sessionStorage.removeItem(TOKEN_KEY)
  } catch { /* stockage indisponible */ }
}

export class ApiError extends Error {
  constructor(status, message, detail) {
    super(message)
    this.status = status
    this.detail = detail
  }
}

function messageFromDetail(detail, status) {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) return detail.map((d) => String(d.msg || '').replace(/^Value error, /, '')).join(' ; ')
  return `Erreur ${status}`
}

async function request(method, url, { body, form, auth = false } = {}) {
  const headers = { Accept: 'application/json' }
  if (auth) {
    const token = getToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }
  let payload
  if (form) payload = form
  else if (body !== undefined) {
    headers['Content-Type'] = 'application/json'
    payload = JSON.stringify(body)
  }
  const res = await fetch(url, { method, headers, body: payload })
  const data = res.status === 204 ? null : await res.json().catch(() => null)
  if (!res.ok) throw new ApiError(res.status, messageFromDetail(data?.detail, res.status), data?.detail)
  return data
}

export const api = {
  get: (url, opts) => request('GET', url, opts),
  post: (url, body, opts) => request('POST', url, { body, ...opts }),
  put: (url, body, opts) => request('PUT', url, { body, ...opts }),
  patch: (url, body, opts) => request('PATCH', url, { body, ...opts }),
  delete: (url, opts) => request('DELETE', url, opts),
  upload: (url, form, opts) => request('POST', url, { form, ...opts }),
}
