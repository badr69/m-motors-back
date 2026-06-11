import io

def test_create_document(client, token_user, dossier):

    data = {
        "dossier_id": str(dossier["id"]),
        "type_document": "identity",
        "file": (
            io.BytesIO(b"fake pdf content"),
            "test.pdf"
        )
    }

    response = client.post(
        "/api/v1/documents",
        data=data,
        content_type="multipart/form-data",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 201

    response_data = response.get_json()["data"]

    assert response_data["filename"] == "test.pdf"