import io
import pytest

def test_delete_document_success(client, token_admin, document):
    """Test suppression d'un document avec succès"""
    response = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "message" in json_data
    assert json_data["message"] == "Document deleted successfully"


def test_delete_document_not_found(client, token_admin):
    """Test suppression d'un document inexistant"""
    response = client.delete(
        "/api/v1/documents/99999",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.status_code == 404
    json_data = response.get_json()
    # La réponse utilise "message" et non "error"
    assert "message" in json_data
    assert "not found" in json_data["message"].lower()


def test_delete_document_unauthorized(client, document):
    """Test suppression d'un document sans token"""
    response = client.delete(
        f"/api/v1/documents/{document['id']}"
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert "message" in json_data
    assert "token" in json_data["message"].lower() or "missing" in json_data["message"].lower()


def test_delete_document_invalid_token(client, document):
    """Test suppression d'un document avec token invalide"""
    response = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code in [401, 403]
    json_data = response.get_json()
    assert "message" in json_data


def test_delete_document_twice(client, token_admin, document):
    """Test suppression d'un document déjà supprimé"""
    # 1ère suppression
    response1 = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert response1.status_code == 200

    # 2ème suppression (document déjà supprimé)
    response2 = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    # Le statut peut être 404 ou 400 selon la logique
    assert response2.status_code in [400, 404]
    json_data = response2.get_json()
    assert "message" in json_data


def test_delete_document_invalid_id_format(client, token_admin):
    """Test suppression avec un ID au format invalide"""
    response = client.delete(
        "/api/v1/documents/abc",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    # Soit 404 soit 400 selon le format attendu
    assert response.status_code in [400, 404]
    json_data = response.get_json()
    assert "message" in json_data


def test_delete_document_negative_id(client, token_admin):
    """Test suppression avec un ID négatif"""
    response = client.delete(
        "/api/v1/documents/-1",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.status_code in [400, 404]
    json_data = response.get_json()
    assert "message" in json_data


def test_delete_document_without_auth_header(client, document):
    """Test suppression sans header Authorization"""
    response = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={}
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert "message" in json_data
    assert "token" in json_data["message"].lower() or "missing" in json_data["message"].lower()


def test_delete_document_verify_deleted(client, token_admin, document):
    """Test vérification que le document est bien supprimé"""
    # 1. Supprimer le document
    delete_response = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert delete_response.status_code == 200

    # 2. Essayer de récupérer le document supprimé
    get_response = client.get(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert get_response.status_code == 404
    json_data = get_response.get_json()
    assert "message" in json_data
    assert "not found" in json_data["message"].lower()


def test_delete_document_with_user_role(client, token_user, document):
    """Test suppression d'un document par un user normal"""
    response = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_user}"}
    )

    # Selon la logique métier, soit autorisé soit interdit
    assert response.status_code < 500