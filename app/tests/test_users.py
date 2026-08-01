def test_get_all_users(
    authorized_client,
    test_user,
    test_user2
):
    response = authorized_client.get(
        "/users/"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    emails = [
        user["email"]
        for user in data
    ]

    assert test_user["user"].email in emails
    assert test_user2["user"].email in emails



def test_get_all_users_unauthorized(
    client
):
    response = client.get(
        "/users/"
    )

    assert response.status_code == 401



def test_get_current_user(
    authorized_client,
    test_user
):
    response = authorized_client.get(
        "/users/me"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == test_user["user"].id
    assert data["email"] == test_user["user"].email



def test_get_current_user_unauthorized(
    client
):
    response = client.get(
        "/users/me"
    )

    assert response.status_code == 401