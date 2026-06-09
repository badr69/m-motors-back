def test_get_my_dossiers(client, token_user):

    response = client.get(
        "/api/v1/rental_dossiers/my",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert isinstance(data, list)