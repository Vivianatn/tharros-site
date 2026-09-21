def test_public_content_is_seeded(client):
    r = client.get("/api/content")
    assert r.status_code == 200
    data = r.json()
    assert data["games"][0]["slug"] == "muses"
    assert "home" in data["settings"]
    assert len(data["faq"]) > 0


def test_admin_requires_token(client):
    assert client.get("/api/admin/posts").status_code == 401


def test_login_rejects_bad_password(client):
    r = client.post("/api/auth/login", json={"email": "admin@tharros-studio.fr", "password": "nope"})
    assert r.status_code == 401


def test_post_lifecycle(client, auth):
    r = client.post("/api/admin/posts", json={"title": "Brouillon test", "body_md": "corps", "published": False}, headers=auth)
    assert r.status_code == 201
    post = r.json()
    assert post["slug"] == "brouillon-test"
    # non publié : invisible côté public
    assert client.get(f"/api/posts/{post['slug']}").status_code == 404
    r = client.put(f"/api/admin/posts/{post['id']}", json={**post, "published": True}, headers=auth)
    assert r.status_code == 200 and r.json()["published_at"] is not None
    assert client.get(f"/api/posts/{post['slug']}").status_code == 200
    assert client.delete(f"/api/admin/posts/{post['id']}", headers=auth).status_code == 200


def test_slug_uniqueness(client, auth):
    a = client.post("/api/admin/posts", json={"title": "Même titre"}, headers=auth).json()
    b = client.post("/api/admin/posts", json={"title": "Même titre"}, headers=auth).json()
    assert a["slug"] == "meme-titre" and b["slug"] == "meme-titre-2"


def test_contact_validation_and_honeypot(client):
    bad = client.post("/api/contact", json={"name": "A", "email": "x", "subject": "", "message": "court", "consent": True, "elapsed": 5000})
    assert bad.status_code == 422
    bot = client.post("/api/contact", json={"name": "Robot", "email": "bot@x.io", "subject": "spam", "message": "x" * 30, "consent": True, "elapsed": 5000, "website": "http://spam"})
    assert bot.status_code == 200
    ok = client.post("/api/contact", json={"name": "Alice", "email": "alice@exemple.fr", "subject": "Presse", "message": "Bonjour, je souhaite une interview.", "consent": True, "elapsed": 5000})
    assert ok.status_code == 200 and ok.json()["ok"]


def test_subscribe_and_list(client, auth):
    r = client.post("/api/subscribe", json={"email": "fan@exemple.fr", "consent": True, "elapsed": 5000})
    assert r.status_code == 200
    subs = client.get("/api/admin/subscribers", headers=auth).json()
    assert any(s["email"] == "fan@exemple.fr" for s in subs)


def test_settings_roundtrip(client, auth):
    r = client.put("/api/admin/settings/home", json={"kicker": "Nouveau kicker"}, headers=auth)
    assert r.status_code == 200
    assert client.get("/api/content").json()["settings"]["home"]["kicker"] == "Nouveau kicker"


def test_sitemap(client):
    r = client.get("/api/sitemap.xml")
    assert r.status_code == 200 and "/jeux/muses" in r.text
