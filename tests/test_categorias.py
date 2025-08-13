def auth_token(client):
    client.post("/auth/register", json={"username": "u1", "password": "p1"})
    res = client.post("/auth/login", json={"username": "u1", "password": "p1"})
    return res.json()["access_token"]

def test_crear_y_listar_categorias(client):
    token = auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # crear
    r = client.post("/categorias", json={"nombre": "Electrónica"}, headers=headers)
    assert r.status_code in (200, 201)
    cat = r.json()
    assert cat["id"] >= 1 and cat["nombre"] == "Electrónica"

    # listar
    r = client.get("/categorias", headers=headers)
    assert r.status_code == 200
    assert any(c["nombre"] == "Electrónica" for c in r.json())
