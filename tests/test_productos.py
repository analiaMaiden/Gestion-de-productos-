def auth_headers(client):
    client.post("/auth/register", json={"username": "u2", "password": "p2"})
    res = client.post("/auth/login", json={"username": "u2", "password": "p2"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def crear_categoria(client, headers):
    r = client.post("/categorias", json={"nombre": "Ropa"}, headers=headers)
    return r.json()["id"]

def test_crud_productos(client, fake_image_png):
    headers = auth_headers(client)
    cat_id = crear_categoria(client, headers)

    # CREATE (multipart con imagen)
    files = {"imagen": fake_image_png}
    data = {
        "nombre": "Camiseta",
        "descripcion": "Algodón",
        "precio": "19.99",
        "categoria_id": str(cat_id),
    }
    r = client.post("/productos", headers=headers, data=data, files=files)
    assert r.status_code in (200, 201)
    prod = r.json()
    pid = prod["id"]
    assert prod["nombre"] == "Camiseta"

    # READ
    r = client.get("/productos", headers=headers)
    assert r.status_code == 200
    assert any(p["id"] == pid for p in r.json())

    # UPDATE
    data["nombre"] = "Camiseta Premium"
    r = client.put(f"/productos/{pid}", headers=headers, data=data)
    assert r.status_code == 200
    assert r.json()["nombre"] == "Camiseta Premium"

    # DELETE
    r = client.delete(f"/productos/{pid}", headers=headers)
    assert r.status_code in (200, 204)

    # Verifica que ya no existe
    r = client.get("/productos", headers=headers)
    ids = [p["id"] for p in r.json()]
    assert pid not in ids
