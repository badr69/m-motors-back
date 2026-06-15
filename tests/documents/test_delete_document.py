def test_delete_document(client, token_admin, document):

    response = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.status_code == 200

    json_data = response.get_json()

    # 🔥 FIX IMPORTANT
    assert "message" in json_data
    assert json_data["message"] == "Document deleted successfully"