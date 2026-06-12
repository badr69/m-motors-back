def test_delete_dossier_success(client, token_user, dossier):

    response = client.delete(
        f"/api/v1/rental_dossiers/{dossier['id']}",
        headers={"Authorization": f"Bearer {token_user}"}
    )

    assert response.status_code == 200


# ======================
# NOT FOUND
# ======================
def test_delete_dossier_not_found(client, token_user):

    response = client.delete(
        "/api/v1/rental_dossiers/999999",
        headers={"Authorization": f"Bearer {token_user}"}
    )

    assert response.status_code == 403 or response.status_code == 404


# ======================
# ADMIN DELETE (OPTIONAL COVERAGE BOOST)
# ======================
def test_delete_dossier_admin(client, token_admin, dossier):

    response = client.delete(
        f"/api/v1/rental_dossiers/{dossier['id']}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.status_code == 200