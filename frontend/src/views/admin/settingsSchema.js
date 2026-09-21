/**
 * Décrit les blocs de contenu modifiables et leurs champs.
 * type : text | textarea | markdown | image | list (avec fields)
 */
const kv = [{ key: 'k', label: 'Libellé' }, { key: 'v', label: 'Valeur', wide: true }]
const pillar = [{ key: 'num', label: 'Numéro' }, { key: 'title', label: 'Titre' }, { key: 'text', label: 'Texte', type: 'textarea', wide: true }]

export const SECTIONS = [
  {
    key: 'home', label: 'Accueil',
    fields: [
      { key: 'kicker', label: 'Sur-titre du hero', type: 'text' },
      { key: 'title_line1', label: 'Titre — ligne 1', type: 'text' },
      { key: 'title_line2', label: 'Titre — ligne 2 (en or)', type: 'text' },
      { key: 'lede', label: 'Chapeau', type: 'textarea' },
      { key: 'meta', label: 'Mentions sous le hero', type: 'list', fields: [{ key: 'value', label: 'Texte', wide: true }], scalar: true },
      { key: 'manifesto_title', label: 'Titre du manifeste', type: 'text' },
      { key: 'manifesto_intro', label: 'Introduction du manifeste', type: 'textarea' },
      { key: 'manifesto', label: 'Serments (cartes)', type: 'list', fields: pillar },
      { key: 'stats', label: 'Chiffres clés', type: 'list', fields: [{ key: 'num', label: 'Chiffre' }, { key: 'label', label: 'Libellé', wide: true }] },
      { key: 'studio_title', label: 'Titre du bloc studio', type: 'text' },
      { key: 'studio_text', label: 'Texte du bloc studio', type: 'textarea' },
    ],
  },
  {
    key: 'cta', label: 'Liste d’attente',
    fields: [
      { key: 'kicker', label: 'Sur-titre', type: 'text' },
      { key: 'title', label: 'Titre', type: 'text' },
      { key: 'text', label: 'Texte', type: 'textarea' },
      { key: 'button', label: 'Texte du bouton (le seul appel à l’action du site)', type: 'text' },
    ],
  },
  {
    key: 'studio', label: 'Studio',
    fields: [
      { key: 'title', label: 'Titre de la page', type: 'text' },
      { key: 'lede', label: 'Chapeau', type: 'textarea' },
      { key: 'history_title', label: 'Titre — histoire', type: 'text' },
      { key: 'history_md', label: 'Histoire', type: 'markdown' },
      { key: 'timeline', label: 'Chronologie', type: 'list', fields: [{ key: 'date', label: 'Date' }, { key: 'text', label: 'Texte', type: 'textarea', wide: true }] },
      { key: 'values', label: 'Valeurs (cartes)', type: 'list', fields: pillar },
      { key: 'team_title', label: 'Titre — équipe', type: 'text' },
      { key: 'team_intro', label: 'Introduction — équipe', type: 'textarea' },
      { key: 'member_name', label: 'Nom', type: 'text' },
      { key: 'member_role', label: 'Rôle', type: 'text' },
      { key: 'member_initials', label: 'Initiales (si pas de photo)', type: 'text' },
      { key: 'member_photo', label: 'Photo', type: 'image' },
      { key: 'roles', label: 'Répartition des rôles', type: 'list', fields: kv },
      { key: 'collab_title', label: 'Titre — collaborations', type: 'text' },
      { key: 'collab_intro', label: 'Introduction — collaborations', type: 'textarea' },
      { key: 'collabs', label: 'Collaborations ouvertes', type: 'list', fields: kv },
    ],
  },
  {
    key: 'press', label: 'Presse',
    fields: [
      { key: 'title', label: 'Titre', type: 'text' },
      { key: 'lede', label: 'Chapeau', type: 'textarea' },
      { key: 'studio_facts', label: 'Fiche d’identité du studio', type: 'list', fields: kv },
      { key: 'assets', label: 'Fichiers téléchargeables', type: 'list', fields: [{ key: 'title', label: 'Titre' }, { key: 'desc', label: 'Description' }, { key: 'url', label: 'Fichier', type: 'image', wide: true }, { key: 'dark', label: 'Aperçu sur fond sombre', type: 'checkbox' }] },
      { key: 'contact_md', label: 'Contact presse', type: 'markdown' },
    ],
  },
  {
    key: 'site', label: 'Identité & contact',
    fields: [
      { key: 'name', label: 'Nom du studio', type: 'text' },
      { key: 'tagline', label: 'Devise', type: 'text' },
      { key: 'description', label: 'Description (pied de page, référencement)', type: 'textarea' },
      { key: 'contact_email', label: 'E-mail de contact', type: 'text' },
      { key: 'press_email', label: 'E-mail presse', type: 'text' },
      { key: 'privacy_email', label: 'E-mail données personnelles', type: 'text' },
      { key: 'address', label: 'Adresse postale', type: 'text' },
      { key: 'socials', label: 'Réseaux sociaux', type: 'list', fields: [{ key: 'name', label: 'Réseau' }, { key: 'url', label: 'Adresse', wide: true }] },
      { key: 'analytics_domain', label: 'Domaine Plausible (vide = pas de mesure d’audience)', type: 'text' },
    ],
  },
  {
    key: 'legal.confidentialite', label: 'Confidentialité',
    fields: [{ key: 'title', label: 'Titre', type: 'text' }, { key: 'lede', label: 'Chapeau', type: 'textarea' }, { key: 'body_md', label: 'Contenu', type: 'markdown' }],
  },
  {
    key: 'legal.cgu', label: 'CGU',
    fields: [{ key: 'title', label: 'Titre', type: 'text' }, { key: 'lede', label: 'Chapeau', type: 'textarea' }, { key: 'body_md', label: 'Contenu', type: 'markdown' }],
  },
  {
    key: 'legal.mentions-legales', label: 'Mentions légales',
    fields: [{ key: 'title', label: 'Titre', type: 'text' }, { key: 'lede', label: 'Chapeau', type: 'textarea' }, { key: 'body_md', label: 'Contenu', type: 'markdown' }],
  },
]
