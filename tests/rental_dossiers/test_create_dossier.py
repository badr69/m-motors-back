def test_create_dossier(client, token_user, vehicle):

    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": "test dossier"
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 201

    data = response.get_json()["data"]

    assert data["status"] == "pending"
    assert data["vehicle_id"] == vehicle.id