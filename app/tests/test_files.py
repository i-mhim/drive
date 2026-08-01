def test_upload_file(authorized_client):
    with open("app/tests/test.txt", "wb") as f:
        f.write(b"Hello World")

    with open("app/tests/test.txt", "rb") as f:
        res = authorized_client.post(
            "/files/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )

    assert res.status_code == 201

    body = res.json()

    assert body["filename"] == "test.txt"

def test_upload_unauthorized(client):
    with open("app/tests/test.txt", "wb") as f:
        f.write(b"Hello")

    with open("app/tests/test.txt", "rb") as f:
        res = client.post(
            "/files/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )

    assert res.status_code == 401

def test_get_all_files(authorized_client, test_file):
    res = authorized_client.get("/files/")

    assert res.status_code == 200
    assert len(res.json()) == 1

def test_get_file(authorized_client, test_file):
    res = authorized_client.get(f"/files/{test_file.id}")

    assert res.status_code == 200

    assert res.json()["id"] == test_file.id

def test_get_nonexistent_file(authorized_client):
    res = authorized_client.get("/files/999")

    assert res.status_code == 404

def test_delete_file(authorized_client, test_file):
    res = authorized_client.delete(f"/files/{test_file.id}")

    assert res.status_code == 204

def test_delete_other_users_file(
    authorized_client2,
    test_file
):
    res = authorized_client2.delete(
        f"/files/{test_file.id}"
    )

    assert res.status_code == 403

def test_update_file(
    authorized_client,
    test_file
):
    res = authorized_client.patch(
        f"/files/{test_file.id}",
        json={
            "filename": "newname.txt"
        }
    )

    assert res.status_code == 200
    assert res.json()["filename"] == "newname.txt"

def test_update_other_users_file(
    authorized_client2,
    test_file
):
    res = authorized_client2.patch(
        f"/files/{test_file.id}",
        json={
            "filename": "hack.txt"
        }
    )

    assert res.status_code == 403

def test_download_file(
    authorized_client,
    test_file
):
    res = authorized_client.get(
        f"/files/{test_file.id}/download"
    )

    assert res.status_code == 200

def test_download_other_users_file(
    authorized_client2,
    test_file
):
    res = authorized_client2.get(
        f"/files/{test_file.id}/download"
    )

    assert res.status_code == 403