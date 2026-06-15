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

    # 🔥 FIX IMPORTANT : debug auth
    print(response.get_json())

    assert response.status_code in [200, 201]