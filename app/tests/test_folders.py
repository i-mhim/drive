def test_create_folder(authorized_client):
    res = authorized_client.post(
        "/folders/",
        json={
            "name": "Documents",
            "parent_folder_id": None
        }
    )

    assert res.status_code == 201
    assert res.json()["name"] == "Documents"

def test_create_folder_unauthorized(client):
    res = client.post(
        "/folders/",
        json={
            "name": "Documents",
            "parent_folder_id": None
        }
    )

    assert res.status_code == 401

def test_create_duplicate_folder(
    authorized_client,
    test_folder
):
    res = authorized_client.post(
        "/folders/",
        json={
            "name": "Documents",
            "parent_folder_id": None
        }
    )

    assert res.status_code == 409

def test_create_folder_invalid_parent(
    authorized_client
):
    res = authorized_client.post(
        "/folders/",
        json={
            "name": "Child",
            "parent_folder_id": 999
        }
    )

    assert res.status_code == 404

def test_get_all_folders(
    authorized_client,
    test_folder
):
    res = authorized_client.get("/folders/")

    assert res.status_code == 200
    assert len(res.json()) == 1

def test_get_folder(
    authorized_client,
    test_folder
):
    res = authorized_client.get(
        f"/folders/{test_folder.id}"
    )

    assert res.status_code == 200
    assert res.json()["id"] == test_folder.id

def test_get_nonexistent_folder(
    authorized_client
):
    res = authorized_client.get("/folders/999")

    assert res.status_code == 404

def test_delete_folder(
    authorized_client,
    test_folder
):
    res = authorized_client.delete(
        f"/folders/{test_folder.id}"
    )

    assert res.status_code == 204

def test_delete_other_users_folder(
    authorized_client2,
    test_folder
):
    res = authorized_client2.delete(
        f"/folders/{test_folder.id}"
    )

    assert res.status_code == 403

def test_update_folder(
    authorized_client,
    test_folder
):
    res = authorized_client.patch(
        f"/folders/{test_folder.id}",
        json={
            "name": "Pictures"
        }
    )

    assert res.status_code == 200
    assert res.json()["name"] == "Pictures"

def test_update_other_users_folder(
    authorized_client2,
    test_folder
):
    res = authorized_client2.patch(
        f"/folders/{test_folder.id}",
        json={
            "name": "Hack"
        }
    )

    assert res.status_code == 403