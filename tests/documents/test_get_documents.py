def test_get_documents(client, token_admin):

    response = client.get(
        "/api/v1/documents",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code == 200

    json_data = response.get_json()

    assert "data" in json_data

    data = json_data["data"]

    assert isinstance(data, list)

    if len(data) > 0:
        assert "id" in data[0]
        assert "filename" in data[0]