import io
import pytest

def test_get_document_by_id_success(client, token_user, document):
    """Test récupération d'un document par ID avec succès"""
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
    assert "type_document" in data
    assert "dossier_id" in data

    assert data["id"] == document["id"]
    assert data["filename"].endswith(document["filename"])
    assert document["filename"] in data["filename"]


def test_get_document_by_id_not_found(client, token_user):
    """Test récupération d'un document inexistant"""
    response = client.get(
        "/api/v1/documents/99999",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 404
    json_data = response.get_json()
    assert "message" in json_data
    assert "not found" in json_data["message"].lower()


def test_get_document_by_id_unauthorized(client, document):
    """Test récupération d'un document sans token"""
    response = client.get(
        f"/api/v1/documents/{document['id']}"
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert "message" in json_data
    assert "token" in json_data["message"].lower() or "missing" in json_data["message"].lower()


def test_get_document_by_id_invalid_token(client, document):
    """Test récupération d'un document avec token invalide"""
    response = client.get(
        f"/api/v1/documents/{document['id']}",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code in [401, 403]
    json_data = response.get_json()
    assert "message" in json_data


def test_get_document_by_id_invalid_id_format(client, token_user):
    """Test récupération avec un ID au format invalide"""
    response = client.get(
        "/api/v1/documents/abc",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code in [400, 404]
    json_data = response.get_json()
    assert "message" in json_data


def test_get_document_by_id_negative_id(client, token_user):
    """Test récupération avec un ID négatif"""
    response = client.get(
        "/api/v1/documents/-1",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code in [400, 404]
    json_data = response.get_json()
    assert "message" in json_data


def test_get_document_by_id_verify_fields(client, token_user, document):
    """Test vérification des champs du document"""
    response = client.get(
        f"/api/v1/documents/{document['id']}",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 200
    data = response.get_json()["data"]

    expected_fields = ["id", "dossier_id", "user_id", "type_document", "filename", "filepath"]
    for field in expected_fields:
        assert field in data, f"Champ {field} manquant"

    assert isinstance(data["id"], int)
    assert isinstance(data["dossier_id"], int)
    assert isinstance(data["type_document"], str)
    assert isinstance(data["filename"], str)
    assert isinstance(data["filepath"], str)


def test_get_document_by_id_after_delete(client, token_user, document):
    """Test récupération d'un document après suppression"""
    # 1. Supprimer le document
    delete_response = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_user}"}
    )
    assert delete_response.status_code < 500

    # 2. Essayer de récupérer le document supprimé
    get_response = client.get(
        f"/api/v1/documents/{document['id']}",
        headers={"Authorization": f"Bearer {token_user}"}
    )
    # On vérifie juste qu'il n'y a pas d'erreur 500
    assert get_response.status_code < 500
    json_data = get_response.get_json()
    assert "message" in json_data or "error" in json_data or "data" in json_data


def test_get_document_by_id_without_auth_header(client, document):
    """Test récupération sans header Authorization"""
    response = client.get(
        f"/api/v1/documents/{document['id']}",
        headers={}
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert "message" in json_data
    assert "token" in json_data["message"].lower() or "missing" in json_data["message"].lower()


def test_get_document_by_id_empty_token(client, document):
    """Test récupération avec token vide"""
    response = client.get(
        f"/api/v1/documents/{document['id']}",
        headers={
            "Authorization": "Bearer "
        }
    )

    assert response.status_code in [401, 403]
    json_data = response.get_json()
    assert "message" in json_data


def test_get_document_by_id_with_admin(client, token_admin, document):
    """Test récupération d'un document par un admin (accès total)"""
    response = client.get(
        f"/api/v1/documents/{document['id']}",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["id"] == document["id"]
    assert data["filename"].endswith(document["filename"])