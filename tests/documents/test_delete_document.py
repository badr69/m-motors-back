def test_delete_document(client, token_admin, document):

    response = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "message" in data
    assert data["message"] == "Document deleted successfully"