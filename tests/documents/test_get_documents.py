import io
import pytest

def test_get_documents_success(client, token_admin):
    """Test récupération de la liste des documents avec succès"""
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
        first = data[0]
        assert "id" in first
        assert (
            "filename" in first
            or "image_url" in first
            or "file_url" in first
        )


def test_get_documents_without_authentication(client):
    """Test récupération des documents sans token"""
    response = client.get("/api/v1/documents")
    assert response.status_code == 401
    json_data = response.get_json()
    assert "message" in json_data


def test_get_documents_invalid_token(client):
    """Test récupération avec token invalide"""
    response = client.get(
        "/api/v1/documents",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )
    assert response.status_code in [401, 403]
    json_data = response.get_json()
    assert "message" in json_data


def test_get_documents_with_user_token(client, token_user):
    """Test récupération des documents avec un token utilisateur"""
    response = client.get(
        "/api/v1/documents",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code in [200, 403]
    if response.status_code == 200:
        json_data = response.get_json()
        assert "data" in json_data
        assert isinstance(json_data["data"], list)


def test_get_documents_with_pagination(client, token_admin):
    """Test récupération des documents avec pagination"""
    response = client.get(
        "/api/v1/documents?page=1&limit=5",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "data" in json_data
    data = json_data["data"]
    assert isinstance(data, list)
    assert len(data) >= 0


def test_get_documents_filter_by_dossier(client, token_admin, dossier):
    """Test récupération des documents filtrés par dossier"""
    # Créer un document dans le dossier
    data = {
        "dossier_id": str(dossier["id"]),
        "type_document": "identity",
        "file": (
            io.BytesIO(b"fake pdf content"),
            "filter_test.pdf"
        )
    }

    create_response = client.post(
        "/api/v1/documents",
        data=data,
        content_type="multipart/form-data",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )
    assert create_response.status_code in [200, 201]

    # Récupérer les documents du dossier
    response = client.get(
        f"/api/v1/documents?dossier_id={dossier['id']}",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "data" in json_data
    data = json_data["data"]
    assert isinstance(data, list)
    # Vérifier que la réponse a le bon format
    for doc in data:
        assert "id" in doc
        assert "dossier_id" in doc
        assert "type_document" in doc


def test_get_documents_filter_by_type(client, token_admin, dossier):
    """Test récupération des documents filtrés par type"""
    # Créer un document de type "identity"
    data = {
        "dossier_id": str(dossier["id"]),
        "type_document": "identity",
        "file": (
            io.BytesIO(b"fake pdf content"),
            "identity_test.pdf"
        )
    }

    create_response = client.post(
        "/api/v1/documents",
        data=data,
        content_type="multipart/form-data",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )
    assert create_response.status_code in [200, 201]

    # Récupérer les documents de type "identity"
    response = client.get(
        "/api/v1/documents?type_document=identity",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "data" in json_data
    data = json_data["data"]
    assert isinstance(data, list)
    # Vérifier que la réponse a le bon format
    for doc in data:
        assert "id" in doc
        assert "dossier_id" in doc
        assert "type_document" in doc


def test_get_documents_with_invalid_filter(client, token_admin):
    """Test récupération avec filtre invalide"""
    response = client.get(
        "/api/v1/documents?invalid_filter=test",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code in [200, 400]
    if response.status_code == 200:
        json_data = response.get_json()
        assert "data" in json_data


def test_get_documents_with_negative_page(client, token_admin):
    """Test récupération avec page négative"""
    response = client.get(
        "/api/v1/documents?page=-1",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code in [200, 400]


def test_get_documents_with_large_limit(client, token_admin):
    """Test récupération avec un grand limit"""
    response = client.get(
        "/api/v1/documents?limit=1000",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "data" in json_data
    assert isinstance(json_data["data"], list)


def test_get_documents_empty_list(client, token_admin):
    """Test récupération quand aucun document n'existe"""
    response = client.get(
        "/api/v1/documents?page=999",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "data" in json_data
    assert isinstance(json_data["data"], list)


def test_get_documents_with_ordering(client, token_admin):
    """Test récupération des documents avec ordre"""
    response = client.get(
        "/api/v1/documents?sort_by=created_at&order=desc",
        headers={
            "Authorization": f"Bearer {token_admin}"
        }
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "data" in json_data
    assert isinstance(json_data["data"], list)


def test_get_documents_response_structure(client, token_admin):
    """Test structure complète de la réponse"""
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
        doc = data[0]
        required_fields = ["id", "dossier_id", "type_document"]
        for field in required_fields:
            assert field in doc, f"Champ {field} manquant"
        assert isinstance(doc["id"], int)
        assert isinstance(doc["dossier_id"], int)
        assert isinstance(doc["type_document"], str)
        assert "filename" in doc or "image_url" in doc or "file_url" in doc