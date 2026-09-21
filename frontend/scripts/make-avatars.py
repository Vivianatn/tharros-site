# -*- coding: utf-8 -*-
"""Génère les 40 avatars prédéfinis (8 motifs × 5 palettes) dans frontend/public/avatars/.
Usage : python frontend/scripts/make-avatars.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "public" / "avatars"
OUT.mkdir(parents=True, exist_ok=True)

# (fond, motif, accent) — chaque palette respecte le contraste du moodboard
PALETTES = [
    ("Encre", "#171310", "#F6F1E9", "#C11F35"),
    ("Grenat", "#C11F35", "#F6F1E9", "#171310"),
    ("Bronze", "#B8672E", "#171310", "#F6F1E9"),
    ("Or", "#E8B96B", "#171310", "#C11F35"),
    ("Marbre", "#F6F1E9", "#171310", "#B8672E"),
]

# Motifs géométriques (viewBox 0 0 100 100) : f = couleur du motif, a = accent
MOTIFS = {
    "lion": ("Lion", '<polygon points="50,14 22,58 78,58" fill="{f}"/><rect x="34" y="58" width="32" height="20" fill="{f}"/><rect x="44" y="64" width="12" height="12" fill="{a}" transform="rotate(45 50 70)"/>'),
    "aigle": ("Aigle", '<polygon points="50,22 42,44 58,44" fill="{f}"/><polygon points="44,40 8,46 44,64" fill="{f}"/><polygon points="56,40 92,46 56,64" fill="{f}"/><polygon points="50,60 42,80 58,80" fill="{f}"/><circle cx="50" cy="36" r="3.5" fill="{a}"/>'),
    "colonne": ("Colonne", '<rect x="26" y="18" width="48" height="8" fill="{f}"/><rect x="32" y="26" width="36" height="6" fill="{f}"/><rect x="36" y="32" width="8" height="40" fill="{f}"/><rect x="46" y="32" width="8" height="40" fill="{f}"/><rect x="56" y="32" width="8" height="40" fill="{f}"/><rect x="30" y="72" width="40" height="8" fill="{f}"/><rect x="24" y="80" width="52" height="6" fill="{a}"/>'),
    "bouclier": ("Bouclier", '<circle cx="50" cy="50" r="32" fill="{f}"/><circle cx="50" cy="50" r="24" fill="none" stroke="{a}" stroke-width="3"/><circle cx="50" cy="50" r="8" fill="{a}"/>'),
    "laurier": ("Laurier", '<path d="M50 80 C30 70 22 50 26 30 C40 36 48 52 50 80 Z" fill="{f}"/><path d="M50 80 C70 70 78 50 74 30 C60 36 52 52 50 80 Z" fill="{f}"/><rect x="46" y="76" width="8" height="8" fill="{a}" transform="rotate(45 50 80)"/>'),
    "lyre": ("Lyre", '<path d="M30 22 C22 40 26 62 40 72 L40 78 L60 78 L60 72 C74 62 78 40 70 22 L64 26 C70 42 66 58 56 66 L44 66 C34 58 30 42 36 26 Z" fill="{f}"/><rect x="42" y="36" width="3" height="30" fill="{a}"/><rect x="48.5" y="36" width="3" height="30" fill="{a}"/><rect x="55" y="36" width="3" height="30" fill="{a}"/>'),
    "casque": ("Casque", '<path d="M28 70 L28 46 C28 30 38 20 50 20 C62 20 72 30 72 46 L72 70 L60 70 L60 52 L40 52 L40 70 Z" fill="{f}"/><rect x="47" y="8" width="6" height="14" fill="{a}"/><rect x="44" y="52" width="12" height="18" fill="{a}"/>'),
    "soleil": ("Soleil", '<g fill="{f}"><polygon points="50,10 55,30 45,30"/><polygon points="50,90 55,70 45,70"/><polygon points="10,50 30,45 30,55"/><polygon points="90,50 70,45 70,55"/><polygon points="22,22 38,32 32,38"/><polygon points="78,22 68,32 62,38"/><polygon points="22,78 32,62 38,68"/><polygon points="78,78 62,68 68,62"/></g><circle cx="50" cy="50" r="14" fill="{a}"/>'),
}

manifest = []
n = 0
for key, (label, shape) in MOTIFS.items():
    for pname, bg, fg, accent in PALETTES:
        n += 1
        ident = f"a{n:02d}"
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100" role="img" aria-label="Avatar {label} {pname}">'
            f'<rect width="100" height="100" fill="{bg}"/>'
            f'<circle cx="50" cy="50" r="44" fill="none" stroke="{fg}" stroke-width="3" opacity=".9"/>'
            + shape.format(f=fg, a=accent) + "</svg>\n"
        )
        (OUT / f"{ident}.svg").write_text(svg, encoding="utf-8")
        manifest.append({"id": ident, "label": f"{label} — {pname}"})

(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{n} avatars écrits dans {OUT}")
