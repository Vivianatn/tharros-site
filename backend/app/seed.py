"""Contenu initial : créé une seule fois, si la base est vide. Tout est ensuite modifiable depuis l'administration."""
from datetime import datetime, timezone

from sqlmodel import Session, select

from .config import get_settings
from .models import FaqItem, Game, Post, Setting, User
from .security import hash_password

SETTINGS: dict[str, dict] = {
    "site": {
        "name": "Tharros",
        "tagline": "Le courage du lion. Le regard de l'aigle.",
        "description": "Studio de jeu vidéo indépendant d'une seule personne. Muses, notre premier jeu, est en développement.",
        "contact_email": "tharrs.studio@gmail.com",
        "press_email": "tharrs.studio@gmail.com",
        "privacy_email": "tharrs.studio@gmail.com",
        "address": "[Adresse du siège social], France",
        "socials": [
            {"name": "Bluesky", "url": "https://bsky.app/"},
            {"name": "Discord", "url": "https://discord.com/"},
            {"name": "YouTube", "url": "https://www.youtube.com/"},
            {"name": "Steam", "url": "https://store.steampowered.com/"},
        ],
        "analytics_domain": "",
    },
    "home": {
        "kicker": "Studio de jeu vidéo indépendant · France",
        "title_line1": "Le courage du lion.",
        "title_line2": "Le regard de l'aigle.",
        "lede": "Tharros forge des jeux taillés dans la Grèce des mythes : une direction artistique de bronze et de marbre, une seule personne aux commandes, et le refus de toute concession.",
        "meta": ["Fondé en 2024", "Premier jeu : Muses", "En développement"],
        "manifesto_title": "Un blason, trois serments",
        "manifesto_intro": "Tharros signifie « courage » en grec ancien. C'est devenu un nom, puis une méthode.",
        "manifesto": [
            {"num": "I", "title": "Courage", "text": "Des jeux exigeants qui respectent le temps et l'intelligence de celles et ceux qui y jouent. Pas de microtransactions, pas de contenu coupé pour être revendu."},
            {"num": "II", "title": "Ascension", "text": "Chaque projet doit faire grimper le studio d'un cran : en technique, en écriture, en direction artistique. Un studio qui n'apprend plus est un studio qui redescend."},
            {"num": "III", "title": "Territoire", "text": "Un univers cohérent, la Grèce des mythes, creusé titre après titre plutôt que de courir après la tendance du moment."},
        ],
        "stats": [
            {"num": "1", "label": "Personne au studio"},
            {"num": "1", "label": "Jeu en développement"},
            {"num": "100 %", "label": "Indépendant, autofinancé"},
            {"num": "0", "label": "Microtransaction"},
        ],
        "studio_title": "Une personne, une créature de légende",
        "studio_text": "Tharros, c'est un studio d'une seule personne : code, art, écriture et son sortent du même bureau. C'est lent, c'est exigeant, et c'est exactement ce qui permet de ne rien lâcher sur la vision.",
    },
    "cta": {
        "kicker": "Liste d'attente",
        "title": "Rejoignez la légion",
        "text": "Soyez prévenu·e en premier des annonces, des phases de test et de la sortie de Muses. Un e-mail par mois, au plus. Pas de spam, jamais de revente.",
        "button": "Rejoindre la liste",
    },
    "studio": {
        "title": "Taillé dans le marbre, forgé dans le bronze",
        "lede": "Tharros est un studio indépendant d'une seule personne, fondé en 2024. Un jeu à la fois, fait jusqu'au bout.",
        "history_title": "Une personne, un serment",
        "history_md": "Tharros naît en 2024 d'une décision simple : après des années à contribuer aux jeux des autres, en faire un qui soit entièrement le sien — de la première ligne de code à la dernière note de musique. Le pacte fondateur tient en une phrase : ne jamais livrer quelque chose dont on a honte.\n\nLe nom vient du grec ancien θάρρος, « courage ». Le blason associe le lion, souverain de la terre, et l'aigle, souverain du ciel : une seule créature de légende, dessinée par des lignes droites plutôt que par le trait organique du bestiaire classique.\n\nDepuis 2025, tout le temps du studio va à [Muses](/jeux/muses), son premier jeu.",
        "timeline": [
            {"date": "2024", "text": "Fondation du studio. Identité visuelle : le blason lion-aigle, la palette marbre, bronze et grenat."},
            {"date": "2025", "text": "Le concept de Muses est retenu parmi une dizaine d'idées. Prototype de navigation et premiers tests de la « vue de l'aigle ». Passage à plein temps."},
            {"date": "2026", "text": "Production de Muses : construction des lieux, écriture des neuf Muses, système de dialogue. Ouverture du journal de développement mensuel et de ce site."},
            {"date": "Ensuite", "text": "Phase de test fermée, page Steam, puis sortie — quand le jeu sera prêt, pas avant."},
        ],
        "values": [
            {"num": "I", "title": "Discipline", "text": "Des semaines régulières, pas de nuits blanches. Un studio d'une personne ne survit pas au crunch : la cadence se choisit, elle ne se subit pas."},
            {"num": "II", "title": "Légende", "text": "Chaque décision de design doit servir le mythe qu'on raconte. Si une mécanique n'a pas de sens dans le monde, elle n'entre pas dans le jeu."},
            {"num": "III", "title": "Transparence", "text": "Un journal de développement public tous les mois, y compris quand ça va mal. La communauté voit le jeu se faire."},
            {"num": "IV", "title": "Accessibilité", "text": "Sous-titres, remappage complet, options de lisibilité et de rythme dès la conception, pas en patch de sortie."},
        ],
        "team_title": "Une personne, tous les rôles",
        "team_intro": "Pas d'organigramme : la même personne conçoit, code, dessine, écrit et compose.",
        "member_name": "[Prénom Nom]",
        "member_role": "Fondateur·rice · tout le reste",
        "member_initials": "T",
        "member_photo": "",
        "roles": [
            {"k": "Design", "v": "Concept, systèmes, niveaux, énigmes"},
            {"k": "Code", "v": "Gameplay, outils, interface"},
            {"k": "Art", "v": "Direction artistique, modélisation, interface"},
            {"k": "Écriture", "v": "Univers, dialogues, les neuf Muses"},
            {"k": "Son", "v": "Musique et design sonore"},
            {"k": "Le reste", "v": "Site, journal, communauté, comptabilité"},
        ],
        "collab_title": "Rejoindre la phalange",
        "collab_intro": "Le studio ne recrute pas de salarié·e pour le moment. En revanche, certaines briques de Muses seront confiées à des indépendant·es :",
        "collabs": [
            {"k": "Localisation", "v": "Traduction du texte vers l'anglais (puis d'autres langues après la sortie)."},
            {"k": "Voix", "v": "À l'étude — narration et quelques répliques clés."},
            {"k": "Tests", "v": "Une phase de test fermée aura lieu avant la sortie : la liste d'attente est la porte d'entrée."},
        ],
    },
    "press": {
        "title": "Kit média",
        "lede": "Tout ce qu'il faut pour parler de Tharros et de Muses : les faits, les logos, les visuels. Utilisation libre dans un cadre éditorial.",
        "studio_facts": [
            {"k": "Nom", "v": "Tharros Studio"},
            {"k": "Fondation", "v": "2024, France"},
            {"k": "Taille", "v": "Une personne"},
            {"k": "Financement", "v": "Autofinancé, indépendant"},
            {"k": "Étymologie", "v": "Du grec ancien θάρρος, « courage »"},
        ],
        "assets": [
            {"title": "Logo horizontal — encre", "desc": "Pour fonds clairs.", "url": "/brand/tharros-logo.svg", "dark": False},
            {"title": "Logo horizontal — marbre", "desc": "Pour fonds sombres.", "url": "/brand/tharros-logo-light.svg", "dark": True},
            {"title": "Emblème seul", "desc": "Icône, avatar, favicon.", "url": "/brand/tharros-emblem.svg", "dark": False},
            {"title": "Muses — visuel clé", "desc": "Format 4:3.", "url": "/brand/muses.svg", "dark": True},
            {"title": "Muses — bannière", "desc": "Format large 16:7.", "url": "/brand/muses-wide.svg", "dark": True},
            {"title": "Image de partage", "desc": "1200 × 630, JPEG.", "url": "/og-image.jpg", "dark": True},
        ],
        "contact_md": "Écrivez à tharrs.studio@gmail.com avec « Presse » en objet. Les clés de test seront distribuées à l'ouverture de la phase de test fermée.",
    },
    "legal.confidentialite": {
        "title": "Politique de confidentialité",
        "lede": "Ce que nous collectons, pourquoi, combien de temps, et comment exercer vos droits.",
        "body_md": (
            "## 1. Responsable du traitement\n\nTharros Studio, [forme juridique], [Adresse du siège social], France — tharrs.studio@gmail.com.\n\n"
            "## 2. Données collectées\n\n| Traitement | Données | Base légale | Durée |\n|---|---|---|---|\n"
            "| Formulaire de contact | Nom, e-mail, objet, message, IP | Intérêt légitime | 12 mois |\n"
            "| Liste d'attente | E-mail, preuve de consentement, IP | Consentement | Jusqu'à désinscription |\n"
            "| Mesure d'audience | Données agrégées, sans identifiant | Consentement | 24 mois |\n"
            "| Journaux de l'hébergeur | IP, URL, horodatage | Intérêt légitime | 30 jours |\n\n"
            "## 3. Sous-traitants\n\n- Hébergement : [hébergeur]\n- E-mails transactionnels : Resend, Inc.\n- Mesure d'audience : Plausible Analytics (UE), chargé uniquement après votre accord.\n\n"
            "## 4. Cookies\n\nLe site fonctionne sans cookie. Votre choix sur la bannière est mémorisé dans le stockage local de votre navigateur (`tharros_consent`). Vous pouvez le modifier via « Gérer les cookies » en pied de page.\n\n"
            "## 5. Vos droits\n\nAccès, rectification, effacement, limitation, opposition, portabilité et retrait du consentement : tharrs.studio@gmail.com. Réponse sous un mois. Réclamation possible auprès de la [CNIL](https://www.cnil.fr/).\n\n"
            "## 6. Sécurité\n\nSite servi en HTTPS. Les formulaires sont traités par une API côté serveur ; aucune clé n'est présente dans le navigateur.\n\n"
            "## 7. Mineurs\n\nLa liste d'attente est réservée aux personnes de 15 ans et plus."
        ),
    },
    "legal.cgu": {
        "title": "Conditions générales d'utilisation",
        "lede": "Les règles du jeu pour utiliser ce site.",
        "body_md": (
            "## Article 1 — Objet\n\nLes présentes CGU encadrent l'accès et l'utilisation du site tharros-studio.fr, édité par Tharros Studio. En accédant au site, vous les acceptez sans réserve.\n\n"
            "## Article 2 — Accès\n\nLe site est accessible gratuitement. Tharros peut l'interrompre pour maintenance sans préavis.\n\n"
            "## Article 3 — Propriété intellectuelle\n\nTextes, marques, logos, blason, illustrations, code et les noms « Tharros » et « Muses » sont protégés. Toute reproduction sans autorisation écrite est interdite, hors citation courte et usage du kit presse dans un cadre éditorial.\n\n"
            "## Article 4 — Contenus créés par les joueurs et joueuses\n\nCaptures, vidéos et fan art sont encouragés, y compris avec monétisation raisonnable, à condition d'apporter une contribution créative et de ne pas nuire à l'image du studio.\n\n"
            "## Article 5 — Formulaires\n\nVous vous engagez à fournir des informations exactes et à ne pas envoyer de contenus illicites, injurieux ou automatisés.\n\n"
            "## Article 6 — Responsabilité\n\nLes informations (dates, plateformes, fonctionnalités) sont indicatives et peuvent évoluer.\n\n"
            "## Article 7 — Droit applicable\n\nDroit français. Tribunaux du ressort du siège de Tharros, sous réserve des règles applicables aux consommateurs."
        ),
    },
    "legal.mentions-legales": {
        "title": "Mentions légales",
        "lede": "Informations obligatoires au titre de la loi pour la confiance dans l'économie numérique.",
        "body_md": (
            "## Éditeur\n\nTharros Studio — [forme juridique]\n[Prénom Nom], [Adresse du siège social], France\nSIREN : [numéro] — TVA : [numéro ou « non applicable, art. 293 B du CGI »]\nE-mail : tharrs.studio@gmail.com\n\nDirecteur·rice de la publication : [Prénom Nom].\n\n"
            "## Hébergement\n\n[Nom de l'hébergeur], [adresse].\n\n"
            "## Crédits\n\nIdentité visuelle, blason et site : Tharros Studio. Polices : Big Shoulders Display et Manrope (SIL Open Font License), auto-hébergées."
        ),
    },
}

GAME = dict(
    slug="muses",
    title="Muses",
    status="En développement",
    tagline="Les neuf Muses se sont tues, et avec elles la mémoire du monde. Partez les retrouver, une à une, dans une Grèce de marbre et de bronze.",
    pitch_md=(
        "Muses est un jeu d'aventure narrative à la troisième personne. Vous parcourez une Grèce figée — temples vides, théâtres muets, bibliothèques aux pages blanches — à la recherche des neuf Muses. Chacune garde un art oublié : la poésie, l'histoire, la musique, la danse, l'astronomie… Retrouver une Muse, c'est rendre cet art au monde, et voir le monde changer autour de vous.\n\n"
        "Pas de combat. Ce qui avance, ce sont vos conversations, vos observations et les liens que vous tissez entre les lieux. Le jeu retient ce que vous dites : les Muses s'en souviennent, et le finale dépend de qui vous avez ramené — et comment."
    ),
    cover_url="/brand/muses.svg",
    banner_url="/brand/muses-wide.svg",
    specs=[
        {"k": "Genre", "v": "Aventure narrative, exploration, énigmes"},
        {"k": "Vue", "v": "Troisième personne"},
        {"k": "Joueurs", "v": "Solo"},
        {"k": "Plateforme", "v": "PC (Steam) — consoles à l'étude"},
        {"k": "Langues", "v": "Français et anglais (texte)"},
        {"k": "Sortie", "v": "À annoncer"},
    ],
    pillars=[
        {"num": "01", "title": "Le monde se souvient", "text": "Chaque Muse retrouvée transforme les lieux déjà visités : une place vide se remplit de musique, une fresque effacée réapparaît."},
        {"num": "02", "title": "Parler, pas frapper", "text": "Aucun combat. Les Muses ne se gagnent pas, elles se convainquent. Vos choix de dialogue ont des conséquences durables."},
        {"num": "03", "title": "Le regard de l'aigle", "text": "À tout moment, prenez de la hauteur : une vue d'ensemble pour lire les lieux, relier les indices et repérer ce qui a changé."},
    ],
    progress=[
        {"k": "Terminé", "v": "Concept, direction artistique, prototype de navigation, système de dialogue"},
        {"k": "En cours", "v": "Construction des neuf lieux, écriture des Muses, musique"},
        {"k": "À venir", "v": "Phase de test fermée, localisation, page Steam"},
    ],
    featured=True,
    published=True,
)

POSTS = [
    dict(slug="pourquoi-muses", title="Pourquoi Muses", tag="Devlog n° 1", published_at=datetime(2025, 11, 15, tzinfo=timezone.utc),
         excerpt="Un jeu sans combat sur des déesses qu'on a oubliées, par un studio d'une personne.",
         body_md="Ce premier billet raconte d'où vient l'idée, et pourquoi c'est celle-là qu'il fallait faire en premier.\n\n## L'oubli comme mécanique\n\nQue se passe-t-il quand plus personne ne se souvient de la musique ? C'est la question de départ de Muses.\n\n## Un studio d'une personne\n\nFaire petit, faire net, faire jusqu'au bout."),
    dict(slug="direction-artistique-verrouillee", title="Direction artistique verrouillée", tag="Devlog n° 2", published_at=datetime(2026, 1, 20, tzinfo=timezone.utc),
         excerpt="Marbre, bronze, grenat. Géométrie plutôt que trait organique.",
         body_md="Le moodboard du studio devient la bible visuelle du jeu — les mêmes lignes droites, les mêmes frises. Chaque lieu de Muses est construit à partir de trois formes : le triangle, le cercle, la colonne."),
    dict(slug="le-systeme-de-dialogue-tient-debout", title="Le système de dialogue tient debout", tag="Devlog n° 3", published_at=datetime(2026, 9, 10, tzinfo=timezone.utc),
         excerpt="Premier prototype jouable des conversations avec les Muses : choix, conséquences, et surtout mémoire.",
         body_md="Une Muse se souvient de ce que vous lui avez dit trois lieux plus tôt. Le code est laid, mais ça marche.\n\nLe mois prochain : le nettoyer, et écrire Calliope."),
]

FAQ = [
    ("Quand sort Muses ?", "Quand il sera prêt. Aucune date n'est annoncée ; elle le sera d'abord aux personnes inscrites sur la liste d'attente."),
    ("Sur quelles plateformes ?", "PC via Steam au lancement. Les consoles sont à l'étude pour après la sortie."),
    ("Combien coûtera le jeu ?", "Le prix n'est pas fixé. Ce qui est fixé : un achat unique, pas de microtransactions."),
    ("Y a-t-il des combats ?", "Non. Muses avance par la conversation, l'observation et l'exploration."),
    ("Comment participer à la phase de test ?", "Inscrivez-vous à la liste d'attente : les invitations partiront de là, par e-mail."),
    ("Le studio, c'est vraiment une seule personne ?", "Oui : design, code, art, écriture et son. Certaines briques (localisation, voix) seront confiées à des indépendant·es."),
    ("Puis-je streamer ou faire des vidéos sur Muses ?", "Oui, y compris monétisées, dans les conditions des [CGU](/cgu)."),
    ("Où obtenir les logos et visuels ?", "Sur la page [presse](/presse), librement utilisables dans un cadre éditorial."),
]


def seed(session: Session) -> None:
    settings = get_settings()
    if session.exec(select(User)).first() is None:
        session.add(User(email=settings.admin_email.lower(), password_hash=hash_password(settings.admin_password)))
    for key, value in SETTINGS.items():
        if session.get(Setting, key) is None:
            session.add(Setting(key=key, value=value))
    if session.exec(select(Game)).first() is None:
        session.add(Game(**GAME))
    if session.exec(select(Post)).first() is None:
        for p in POSTS:
            session.add(Post(published=True, **p))
    if session.exec(select(FaqItem)).first() is None:
        for i, (q, a) in enumerate(FAQ):
            session.add(FaqItem(question=q, answer_md=a, sort_order=i))
    session.commit()
