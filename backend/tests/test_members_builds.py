import io


def test_member_register_login_and_profile(client):
    r = client.post("/api/account/register", json={"email": "joueur@exemple.fr", "password": "motdepasse-solide", "display_name": "Joueur", "consent": True, "elapsed": 5000})
    assert r.status_code == 201, r.text
    assert "tharros_member" in r.cookies
    assert client.get("/api/account/me").json()["email"] == "joueur@exemple.fr"
    # doublon refusé
    assert client.post("/api/account/register", json={"email": "joueur@exemple.fr", "password": "motdepasse-solide", "display_name": "Joueur", "consent": True, "elapsed": 5000}).status_code == 409
    # déconnexion puis reconnexion
    client.post("/api/account/logout")
    assert client.get("/api/account/me").json() is None
    assert client.post("/api/account/login", json={"email": "joueur@exemple.fr", "password": "faux"}).status_code == 401
    assert client.post("/api/account/login", json={"email": "joueur@exemple.fr", "password": "motdepasse-solide"}).status_code == 200
    attribue = client.get("/api/account/me").json()["avatar"]
    assert attribue.isdigit() and 1 <= int(attribue) <= 100  # avatar tiré au hasard parmi les 100
    for invalide in ("000", "101", "a17", "17"):
        assert client.put("/api/account/me", json={"display_name": "Nouveau nom", "avatar": invalide, "newsletter": True}).status_code == 422
    r = client.put("/api/account/me", json={"display_name": "Nouveau nom", "avatar": "017", "newsletter": True})
    assert r.json()["display_name"] == "Nouveau nom" and r.json()["avatar"] == "017"


def test_member_token_is_not_admin(client):
    client.post("/api/account/login", json={"email": "joueur@exemple.fr", "password": "motdepasse-solide"})
    token_cookie = client.cookies.get("tharros_member")
    assert client.get("/api/admin/posts", headers={"Authorization": f"Bearer {token_cookie}"}).status_code == 401


def test_build_upload_download_and_account_gate(client, auth):
    game = client.get("/api/admin/games", headers=auth).json()[0]
    r = client.post(f"/api/admin/games/{game['id']}/builds", headers=auth, data={"platform": "windows", "version": "0.1"}, files={"file": ("muses-win.zip", io.BytesIO(b"PK" + b"0" * 100), "application/zip")})
    assert r.status_code == 201, r.text
    build = r.json()
    assert build["platform"] == "windows" and build["size_bytes"] == 102
    assert client.post(f"/api/admin/games/{game['id']}/builds", headers=auth, data={"platform": "amiga"}, files={"file": ("x.zip", b"PK", "application/zip")}).status_code == 422
    assert client.post(f"/api/admin/games/{game['id']}/builds", headers=auth, data={"platform": "linux"}, files={"file": ("x.txt", b"hello", "text/plain")}).status_code == 422
    # visible côté public
    pub = client.get(f"/api/games/{game['slug']}").json()
    assert pub["builds"][0]["id"] == build["id"] and "filename" not in pub["builds"][0]
    # téléchargement libre
    client.post("/api/account/logout")
    r = client.get(f"/api/downloads/{build['id']}")
    assert r.status_code == 200 and r.headers["content-disposition"].endswith('"muses-win.zip"')
    # réservé aux membres
    client.put(f"/api/admin/games/{game['id']}", headers=auth, json={**game, "download_requires_account": True})
    assert client.get(f"/api/downloads/{build['id']}").status_code == 401
    client.post("/api/account/login", json={"email": "joueur@exemple.fr", "password": "motdepasse-solide"})
    assert client.get(f"/api/downloads/{build['id']}").status_code == 200
    # remplacement : un seul build par plateforme
    client.post(f"/api/admin/games/{game['id']}/builds", headers=auth, data={"platform": "windows", "version": "0.2"}, files={"file": ("muses-win2.zip", b"PK000", "application/zip")})
    builds = client.get(f"/api/games/{game['slug']}").json()["builds"]
    assert len(builds) == 1 and builds[0]["version"] == "0.2"
    assert client.delete(f"/api/admin/games/{game['id']}/builds/{builds[0]['id']}", headers=auth).status_code == 200
    members = client.get("/api/admin/members", headers=auth).json()
    assert any(m["email"] == "joueur@exemple.fr" for m in members)
