import io
import pytest


def test_create_document_success(client, token_user, dossier):
    """Test création d'un document avec succès"""
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

    assert response.status_code in [200, 201]
    json_data = response.get_json()
    assert "data" in json_data
    data = json_data["data"]
    assert "id" in data
    assert "filename" in data
    assert data["filename"].endswith(".pdf")


def test_create_document_without_authentication(client):
    """Test création sans token d'authentification"""
    data = {
        "dossier_id": "1",
        "type_document": "identity",
        "file": (
            io.BytesIO(b"fake pdf content"),
            "test.pdf"
        )
    }

    response = client.post(
        "/api/v1/documents",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert "message" in json_data


def test_create_document_with_invalid_token(client):
    """Test création avec token invalide"""
    data = {
        "dossier_id": "1",
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
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code in [401, 403]
    json_data = response.get_json()
    assert "message" in json_data


def test_create_document_missing_file(client, token_user, dossier):
    """Test création sans fichier"""
    data = {
        "dossier_id": str(dossier["id"]),
        "type_document": "identity"
    }

    response = client.post(
        "/api/v1/documents",
        data=data,
        content_type="multipart/form-data",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code in [400, 422]
    json_data = response.get_json()
    assert "error" in json_data or "message" in json_data


def test_create_document_missing_type(client, token_user, dossier):
    """Test création sans type de document"""
    data = {
        "dossier_id": str(dossier["id"]),
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

    assert response.status_code < 500
    if response.status_code != 201:
        json_data = response.get_json()
        assert "error" in json_data or "message" in json_data


def test_create_document_missing_dossier_id(client, token_user):
    """Test création sans dossier_id"""
    data = {
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

    assert response.status_code in [400, 422]
    json_data = response.get_json()
    assert "error" in json_data or "message" in json_data


def test_create_document_dossier_not_found(client, token_user):
    """Test création avec dossier inexistant"""
    data = {
        "dossier_id": "99999",
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

    assert response.status_code < 500
    json_data = response.get_json()
    if response.status_code == 201:
        assert "data" in json_data
    else:
        assert "error" in json_data or "message" in json_data


def test_create_document_with_different_file_types(client, token_user, dossier):
    """Test création avec différents types de fichiers"""
    file_contents = [
        (b"fake pdf content", "document.pdf", True),
        (b"fake jpg content", "image.jpg", False),
        (b"fake png content", "image.png", False),
        (b"fake docx content", "document.docx", False),
    ]

    for content, filename, should_succeed in file_contents:
        data = {
            "dossier_id": str(dossier["id"]),
            "type_document": "identity",
            "file": (
                io.BytesIO(content),
                filename
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

        if should_succeed:
            assert response.status_code in [200, 201], f"{filename} devrait fonctionner"
            json_data = response.get_json()
            assert "data" in json_data
            assert "filename" in json_data["data"]
            assert json_data["data"]["filename"].endswith(filename.split(".")[-1])
        else:
            assert response.status_code < 500, f"{filename} ne devrait pas causer d'erreur 500"


def test_create_document_with_different_types(client, token_user, dossier):
    """Test création avec différents types de documents"""
    types = ["identity", "license", "registration", "insurance", "other"]

    for doc_type in types:
        data = {
            "dossier_id": str(dossier["id"]),
            "type_document": doc_type,
            "file": (
                io.BytesIO(b"fake pdf content"),
                f"test_{doc_type}.pdf"
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

        assert response.status_code in [200, 201]
        json_data = response.get_json()
        assert "data" in json_data
        assert json_data["data"]["type_document"] == doc_type


def test_create_document_with_large_file(client, token_user, dossier):
    """Test création avec un gros fichier (1MB)"""
    large_content = b"0" * 1024 * 1024  # 1MB

    data = {
        "dossier_id": str(dossier["id"]),
        "type_document": "identity",
        "file": (
            io.BytesIO(large_content),
            "large_file.pdf"
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

    assert response.status_code < 500


def test_create_document_empty_file(client, token_user, dossier):
    """Test création avec un fichier vide"""
    data = {
        "dossier_id": str(dossier["id"]),
        "type_document": "identity",
        "file": (
            io.BytesIO(b""),
            "empty.pdf"
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

    assert response.status_code < 500


def test_create_document_without_content_type(client, token_user, dossier):
    """Test création sans content-type multipart"""
    data = {
        "dossier_id": str(dossier["id"]),
        "type_document": "identity",
        "file": "not_a_file"
    }

    response = client.post(
        "/api/v1/documents",
        json=data,
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code in [400, 415, 422]
    json_data = response.get_json()
    assert "error" in json_data or "message" in json_data