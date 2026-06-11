def test_get_dossier_by_id(client, token_user, dossier):

    response = client.get(
        f"/api/v1/rental_dossiers/{dossier['id']}",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "data" in data
    assert data["data"]["id"] == dossier["id"]
    assert data["data"]["status"] == "pending"