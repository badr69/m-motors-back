def test_get_document_by_id(client, token_user, document):

    response = client.get(
        f"/api/v1/documents/{document['id']}",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 200

    json_data = response.get_json()

    assert "data" in json_data

    data = json_data["data"]

    assert "id" in data
    assert "filename" in data

    assert data["id"] == document["id"]
    assert data["filename"] == document["filename"]