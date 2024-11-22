from http import HTTPStatus


def test_app_should_return_ok_hello_world(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World!"}
