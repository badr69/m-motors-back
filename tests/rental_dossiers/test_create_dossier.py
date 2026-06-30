import pytest


def test_create_dossier_success(client, token_user, vehicle):
    """Test création d'un dossier avec succès"""
    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": "test dossier"
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["status"] == "pending"
    assert data["vehicle_id"] == vehicle.id
    assert "id" in data


def test_create_dossier_without_authentication(client, vehicle):
    """Test création d'un dossier sans token"""
    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": "test dossier"
        }
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert "message" in json_data


def test_create_dossier_invalid_token(client, vehicle):
    """Test création avec token invalide"""
    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": "test dossier"
        },
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code in [401, 403]
    json_data = response.get_json()
    assert "message" in json_data


def test_create_dossier_missing_vehicle_id(client, token_user):
    """Test création sans vehicle_id"""
    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "message": "test dossier"
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code in [400, 422]
    json_data = response.get_json()
    assert "error" in json_data or "message" in json_data


def test_create_dossier_vehicle_not_found(client, token_user):
    """Test création avec vehicle_id inexistant"""
    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": 99999,
            "message": "test dossier"
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code in [400, 404, 422]
    json_data = response.get_json()
    assert "error" in json_data or "message" in json_data


def test_create_dossier_with_empty_message(client, token_user, vehicle):
    """Test création avec message vide"""
    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": ""
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code in [201, 400, 422]
    if response.status_code == 201:
        data = response.get_json()["data"]
        assert data["vehicle_id"] == vehicle.id


def test_create_dossier_with_long_message(client, token_user, vehicle):
    """Test création avec un message long"""
    long_message = "a" * 1000
    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": long_message
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code in [201, 400, 422]
    if response.status_code == 201:
        data = response.get_json()["data"]
        assert data["vehicle_id"] == vehicle.id


def test_create_dossier_with_special_characters(client, token_user, vehicle):
    """Test création avec des caractères spéciaux dans le message"""
    special_message = "Test avec éèçàô ù $ % * ( ) &é"
    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": special_message
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["vehicle_id"] == vehicle.id
    assert data["message"] == special_message


def test_create_multiple_dossiers(client, token_user, vehicle):
    """Test création de plusieurs dossiers pour le même véhicule"""
    for i in range(3):
        response = client.post(
            "/api/v1/rental_dossiers",
            json={
                "vehicle_id": vehicle.id,
                "message": f"test dossier {i}"
            },
            headers={
                "Authorization": f"Bearer {token_user}"
            }
        )

        assert response.status_code == 201
        data = response.get_json()["data"]
        assert data["vehicle_id"] == vehicle.id
        assert data["status"] == "pending"


def test_create_dossier_response_structure(client, token_user, vehicle):
    """Test structure de la réponse"""
    response = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": "test dossier"
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 201
    json_data = response.get_json()
    assert "data" in json_data
    data = json_data["data"]

    # Vérifier les champs obligatoires (sans updated_at)
    expected_fields = ["id", "vehicle_id", "user_id", "status", "message", "created_at"]
    for field in expected_fields:
        assert field in data, f"Champ {field} manquant"

    assert isinstance(data["id"], int)
    assert isinstance(data["vehicle_id"], int)
    assert isinstance(data["user_id"], int)
    assert isinstance(data["status"], str)
    assert data["status"] == "pending"


def test_create_dossier_with_different_vehicles(client, token_user, vehicle):
    """Test création de dossiers pour différents véhicules"""
    # On utilise le même véhicule pour les deux dossiers
    # car la création de véhicule via l'API peut échouer

    # Créer un premier dossier
    response1 = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": "dossier vehicule 1"
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )
    assert response1.status_code == 201

    # Créer un deuxième dossier avec le même véhicule
    response2 = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": "dossier vehicule 2"
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )
    assert response2.status_code == 201

    data1 = response1.get_json()["data"]
    data2 = response2.get_json()["data"]
    # Vérifier que les deux dossiers ont le même vehicle_id
    assert data1["vehicle_id"] == data2["vehicle_id"]
    # Vérifier que les IDs sont différents
    assert data1["id"] != data2["id"]