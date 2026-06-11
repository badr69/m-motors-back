def test_get_my_dossiers(client, token_user):

    response = client.get(
        "/api/v1/rental_dossiers/my",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 200

    json_data = response.get_json()

    assert "data" in json_data
    assert isinstance(json_data["data"], list)