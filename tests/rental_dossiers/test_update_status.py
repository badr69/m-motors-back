def test_update_status(client, token_admin, dossier):

    response = client.patch(
        f"/api/v1/rental_dossiers/{dossier['id']}/status",
        json={
            "status": "approved"
        },
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["status"] == "approved"


def test_update_status_invalid(client, token_admin, dossier):

    response = client.patch(
        f"/api/v1/rental_dossiers/{dossier['id']}/status",
        json={"status": "invalid_status"},
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.status_code == 400