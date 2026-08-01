from app import models


def create_permission_payload(test_file, test_user2):
    return {
        "file_id": test_file.id,
        "user_id": test_user2["user"].id,
        "role": "viewer"
    }


def test_create_permission(authorized_client, test_file, test_user2):
    response = authorized_client.post(
        "/permissions/",
        json=create_permission_payload(test_file, test_user2)
    )

    assert response.status_code == 201

    data = response.json()

    assert data["file_id"] == test_file.id
    assert data["user_id"] == test_user2["user"].id
    assert data["role"] == "viewer"



def test_create_permission_unauthorized(
    authorized_client2,
    test_file,
    test_user2
):
    response = authorized_client2.post(
        "/permissions/",
        json=create_permission_payload(test_file, test_user2)
    )

    assert response.status_code == 403



def test_cannot_share_with_self(
    authorized_client,
    test_file,
    test_user
):
    payload = {
        "file_id": test_file.id,
        "user_id": test_user["user"].id,
        "role": "viewer"
    }

    response = authorized_client.post(
        "/permissions/",
        json=payload
    )

    assert response.status_code == 400



def test_duplicate_permission(
    authorized_client,
    test_file,
    test_user2,
    session
):
    permission = models.Permission(
        file_id=test_file.id,
        user_id=test_user2["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()

    response = authorized_client.post(
        "/permissions/",
        json=create_permission_payload(test_file, test_user2)
    )

    assert response.status_code == 400



def test_get_permissions(
    authorized_client,
    test_file,
    test_user2,
    session
):
    permission = models.Permission(
        file_id=test_file.id,
        user_id=test_user2["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()

    response = authorized_client.get(
        f"/permissions/{test_file.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["user_id"] == test_user2["user"].id



def test_get_permissions_not_owner(
    authorized_client2,
    test_file
):
    response = authorized_client2.get(
        f"/permissions/{test_file.id}"
    )

    assert response.status_code == 403



def test_received_permissions(
    authorized_client2,
    test_file,
    test_user,
    session
):
    permission = models.Permission(
        file_id=test_file.id,
        user_id=test_user["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()


    response = authorized_client2.get(
        "/permissions/received"
    )

    assert response.status_code == 200



def test_given_permissions(
    authorized_client,
    authorized_client2,
    test_file,
    test_user2,
    session
):
    permission = models.Permission(
        file_id=test_file.id,
        user_id=test_user2["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()

    response = authorized_client.get(
        "/permissions/given"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1



def test_delete_permission(
    authorized_client,
    test_file,
    test_user2,
    session
):

    permission = models.Permission(
        file_id=test_file.id,
        user_id=test_user2["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()
    session.refresh(permission)

    response = authorized_client.delete(
        f"/permissions/{permission.id}"
    )

    assert response.status_code == 204



def test_delete_permission_unauthorized(
    authorized_client2,
    test_file,
    test_user2,
    session
):

    permission = models.Permission(
        file_id=test_file.id,
        user_id=test_user2["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()
    session.refresh(permission)

    response = authorized_client2.delete(
        f"/permissions/{permission.id}"
    )

    assert response.status_code == 403



def test_delete_nonexistent_permission(
    authorized_client
):
    response = authorized_client.delete(
        "/permissions/999"
    )

    assert response.status_code == 404



def test_update_permission(
    authorized_client,
    test_file,
    test_user2,
    session
):

    permission = models.Permission(
        file_id=test_file.id,
        user_id=test_user2["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()
    session.refresh(permission)


    response = authorized_client.patch(
        f"/permissions/{permission.id}",
        json={
            "role": "editor"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["role"] == "editor"



def test_update_permission_unauthorized(
    authorized_client2,
    test_file,
    test_user2,
    session
):

    permission = models.Permission(
        file_id=test_file.id,
        user_id=test_user2["user"].id,
        role="viewer"
    )

    session.add(permission)
    session.commit()
    session.refresh(permission)


    response = authorized_client2.patch(
        f"/permissions/{permission.id}",
        json={
            "role": "editor"
        }
    )

    assert response.status_code == 403