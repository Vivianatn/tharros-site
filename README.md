# Tharros — site du studio

Site vitrine + administration complète pour le studio de jeu vidéo Tharros (identité « lion & aigle », Grèce antique, géométrie moderne).

- **Front** : Vue 3 + Vite + Vue Router + Pinia (site public animé et back-office)
- **Back** : FastAPI + SQLModel (SQLite) — API JSON, authentification JWT, envoi d'e-mails, optimisation d'images
- **Tout le contenu est modifiable depuis `/admin`** : devlogs, jeux (avec fichiers téléchargeables par plateforme), FAQ, textes de chaque page, médias, messages reçus, liste d'attente, comptes joueurs.
- **Comptes joueurs** : inscription / connexion / espace « Mon compte » (`/compte`), cookie httpOnly, suppression de compte (RGPD), image de profil parmi **100 avatars** prédéfinis (`frontend/public/avatars/`, identifiants `001`…`100`, libellés dans `manifest.json`).

## Démarrer

| Objectif | Commande |
|---|---|
| Développer (rechargement à chaud) | double-cliquer **`dev.bat`** → http://localhost:5173 |
| Tester comme en production | double-cliquer **`start.bat`** → http://localhost:8000 |
| Tout arrêter | double-cliquer **`stop.bat`** (libère les ports 8000 et 5173, tue les processus orphelins) |

> Le port **5173** n'existe que pendant que la fenêtre de `dev.bat` est ouverte. En dehors du développement, utilisez toujours **`start.bat` → port 8000**.

Les deux scripts installent les dépendances au premier lancement (Python `backend/.venv`, Node dans `frontend/node_modules`). Node est fourni en version portable dans `.tools/node` (aucune installation système).

**Administration** : http://localhost:8000/admin (ou http://localhost:5173/admin en mode dev) — identifiants définis dans `.env` (`ADMIN_EMAIL` / `ADMIN_PASSWORD`, utilisés à la création de la base). Changez le mot de passe dès la première connexion (menu *Compte*).

## Architecture

```
backend/
  app/main.py            Application FastAPI : API, en-têtes de sécurité, service du front compilé, repli SPA / 404
  app/config.py          Configuration (variables d'environnement, fichier .env)
  app/models.py          Tables : User, Post, Game, FaqItem, Setting (blocs JSON), Media, Subscriber, Message
  app/schemas.py         Validation des entrées / sorties (Pydantic)
  app/security.py        bcrypt + JWT, dépendance `get_current_user`
  app/routers/auth.py    /api/auth : connexion, profil, changement de mot de passe
  app/routers/public.py  /api : contenu public, billets, jeux, formulaires (contact, liste d'attente), sitemap.xml
  app/routers/admin.py   /api/admin : CRUD complet (protégé par jeton), téléversement des builds, comptes joueurs
  app/routers/members.py /api/account : inscription, connexion (cookie httpOnly), profil, suppression
  app/routers/downloads.py /api/downloads/{id} : téléchargement d'un build (réservé aux membres si activé)
  app/services/          mail (Resend), antispam (pot de miel, délai, limitation par IP), images (WebP)
  app/seed.py            Contenu initial (créé une fois, si la base est vide)
  tests/                 Tests d'intégration pytest
frontend/
  src/styles/tokens.css  Palette, typographie et SURFACES (voir « Lisibilité »)
  src/styles/base.css    Base, composants transverses, animations
  src/styles/admin.css   Interface d'administration
  src/router/            Routes publiques (/, /jeux/:slug, /journal/:slug, /studio, /presse, /faq, /contact, légales, 404)
                         et d'administration (/admin/…, protégées par un garde de navigation)
  src/stores/            Pinia : content (contenu public), auth (session admin), consent (cookies)
  src/composables/       useHead (SEO par page), useForm (validation + anti-spam), useToast
  src/directives/reveal  v-reveal : apparition au défilement (avec délai pour décaler les grilles)
  src/components/        En-tête, pied de page, bannière cookies, bloc CTA, cartes, éditeur Markdown, médiathèque…
  src/views/public/      Pages du site
  src/views/admin/       Pages du back-office (settingsSchema.js décrit les champs de chaque page éditable)
  public/                Favicons, polices auto-hébergées, logos, image de partage, robots.txt, manifest
```

## Lisibilité garantie (clair/sombre)

Chaque fond est une **surface** (`.surface-light`, `.surface-dark`, `.surface-charbon`) qui redéfinit les variables
`--fg`, `--fg-muted`, `--heading`, `--kicker`, `--link`, `--line`, `--card`… Les composants n'utilisent **jamais** une couleur
de texte en dur : ils lisent ces variables. Une carte claire posée sur une section sombre (page presse) porte simplement
`surface-light` et retrouve ses couleurs encre. Tous les couples respectent WCAG AA (≥ 4,5:1).

## Checklist de lancement (les 20 points)

| # | Exigence | Où |
|---|---|---|
| 1 | Page RGPD | `/confidentialite` (contenu éditable dans l'admin) |
| 2 | Page CGU | `/cgu` + `/mentions-legales` |
| 3 | API hors front-end | `backend/` — clés d'e-mail et secret JWT uniquement côté serveur (`.env`) |
| 4 | Force le HTTPS | HSTS en production (`main.py`) ; la redirection HTTP→HTTPS se fait au reverse-proxy (voir Déploiement) |
| 5 | Bannière cookies | `CookieBanner.vue` ; analytics chargé uniquement après accord ; « Gérer les cookies » en pied de page |
| 6 | Meta title | `useHead` : titre, description, OG et canonical par page |
| 7 | Image réseaux | `public/og-image.jpg` (1200×630) |
| 8 | Favicon | SVG + PNG + apple-touch-icon + manifest |
| 9 | Sitemap + robots.txt | `/api/sitemap.xml` (dynamique : jeux et billets publiés), `public/robots.txt` |
| 10 | Textes images | `alt` sur chaque image ; champ « texte alternatif » dans la médiathèque |
| 11 | Compresse images | Téléversements redimensionnés (≤ 2000 px) et convertis en WebP ; visuels SVG |
| 12 | Vitesse pages | Polices auto-hébergées préchargées, code découpé par page, une requête `/api/content` pour tout le contenu |
| 13 | Contraste | Système de surfaces (ci-dessus) |
| 14 | Site responsive | Grilles fluides, menu mobile |
| 15 | Page 404 custom | `NotFoundView.vue` + code HTTP 404 réel renvoyé par le serveur |
| 16 | Liens cassés | Routes nommées (`RouterLink :to="{ name }"`) : impossible de pointer vers une route inexistante |
| 17 | Valid formulaires | Client (`useForm`) **et** serveur (Pydantic) |
| 18 | Anti-spam | Pot de miel, délai minimal 3 s, limitation par IP, limites de longueur |
| 19 | Outil d'analytics | Plausible : renseignez le domaine dans Admin → Pages du site → Identité |
| 20 | Un seul CTA | « Rejoindre la liste » — texte modifiable dans Admin → Liste d'attente |

## Fiches de jeux et téléchargements

Admin → **Jeux → Nouveau jeu** : titre, statut, accroche, pitch, visuels, fiche technique, piliers, avancement.
Une fois la fiche enregistrée, la section **Téléchargements** permet de déposer un fichier par système
(Windows : .zip/.exe/.msi — macOS : .dmg/.pkg/.zip — Linux : .AppImage/.tar.gz/.deb/.zip), avec numéro de
version et barre de progression. Sur la fiche publique, un bouton « Télécharger » propose automatiquement
le système du visiteur, avec les autres au choix. L'interrupteur **Réservé aux joueurs connectés** exige un compte.

Les fichiers sont stockés dans `backend/media/builds/` (à sauvegarder). Taille maximale : `MAX_BUILD_MB` (4000 par
défaut). Derrière Nginx, augmentez `client_max_body_size` en conséquence.

## Notifications par e-mail (Gmail)

Les messages du formulaire de contact et les inscriptions à la liste d'attente sont envoyés à `MAIL_TO`
(`tharrs.studio@gmail.com`). Pour que Gmail accepte l'envoi :

1. Sur le compte Google du studio, activez la validation en deux étapes.
2. Créez un **mot de passe d'application** : https://myaccount.google.com/apppasswords (16 caractères).
3. Collez-le dans `.env` → `SMTP_PASSWORD=…`, puis relancez `start.bat`.
4. Admin → *Mot de passe & e-mails* → **Envoyer un e-mail de test**.

Sans mot de passe, rien n'est perdu : les messages restent visibles dans Admin → *Messages* / *Liste d'attente*.

## Tests

```
backend\.venv\Scripts\python -m pytest backend
```

## Déploiement sur un serveur (Docker)

Dépôt : https://github.com/Vivianatn/tharros-site

```bash
git clone https://github.com/Vivianatn/tharros-site.git && cd tharros-site
cp .env.example .env        # puis éditez : SECRET_KEY aléatoire, ENVIRONMENT=production,
                            # SITE_URL=https://votre-domaine, ADMIN_*, SMTP_* (voir plus haut)
docker compose up -d --build
```

Le site écoute sur `127.0.0.1:8000`. Placez un reverse-proxy avec HTTPS devant, par exemple Caddy
(`/etc/caddy/Caddyfile`) — il obtient et renouvelle le certificat tout seul et force le HTTPS :

```
votre-domaine.fr {
    reverse_proxy 127.0.0.1:8000
    request_body { max_size 4GB }   # builds de jeux volumineux
}
```

Mise à jour : `git pull && docker compose up -d --build`. Données à sauvegarder : les volumes Docker
`tharros-data` (base SQLite) et `tharros-media` (images et builds).

Sans Docker : `cd frontend && npm run build`, puis dans `backend/` : `pip install -r requirements.txt` et
`uvicorn app.main:app --host 127.0.0.1 --port 8000` (via systemd).

## À personnaliser (depuis l'admin)

- **Identité & contact** : nom, e-mails, adresse, réseaux sociaux (les liens pointent encore vers les plateformes), domaine Plausible.
- **Mentions légales / confidentialité** : remplacer les crochets `[…]` (forme juridique, SIREN, hébergeur, nom).
- **Studio** : nom de la personne, photo, rôles. **Muses** : pitch, spécifications, visuels — le contenu fourni est un exemple cohérent.
