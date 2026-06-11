def test_delete_dossier(client, token_user, dossier):

    response = client.delete(
        f"/api/v1/rental_dossiers/{dossier['id']}",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 200