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

    # ======================
    # SAFE CHECK
    # ======================
    if len(data) > 0:

        first = data[0]

        assert "id" in first

        # backend peut renvoyer filename OU image_url selon implémentation
        assert (
            "filename" in first
            or "image_url" in first
            or "file_url" in first
        )