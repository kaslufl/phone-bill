from datetime import datetime
from http import HTTPStatus
from test.factories import BillingFactory, CallFactory

from faker import Faker

faker = Faker()


def test_start_call_record_should_return_ok(client):
    phone = faker.numerify("##########")
    response = client.post(
        "/call",
        json={
            "id": 1,
            "type": "start",
            "timestamp": "2024-11-22T14:29:39.268Z",
            "call_id": 100,
            "source": phone,
            "destination": "74264176798",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 100,
        "start_timestamp": "2024-11-22T14:29:39.268000",
        "end_timestamp": None,
        "source": phone,
        "destination": "74264176798",
        "price": None,
    }


def test_end_call_record_should_return_ok(client):
    response = client.post(
        "/call",
        json={
            "id": 1,
            "type": "end",
            "timestamp": "2024-11-22T15:29:39.268Z",
            "call_id": 100,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 100,
        "start_timestamp": None,
        "end_timestamp": "2024-11-22T15:29:39.268000",
        "source": None,
        "destination": None,
        "price": None,
    }


def test_finish_call_data_with_end_call_record_should_return_ok(session, client):
    client_phone = faker.numerify("##########")

    call = CallFactory(
        id=100,
        source=client_phone,
        start_timestamp=datetime(2024, 11, 21, 20),
        end_timestamp=None,
        price=None,
    )
    session.add(call)

    billing_period = BillingFactory()
    session.add(billing_period)

    session.commit()

    response = client.post(
        "/call",
        json={
            "id": 1,
            "type": "end",
            "timestamp": datetime(2024, 11, 21, 21).isoformat(),
            "call_id": 100,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 100,
        "start_timestamp": datetime(2024, 11, 21, 20).isoformat(),
        "end_timestamp": datetime(2024, 11, 21, 21).isoformat(),
        "source": client_phone,
        "destination": call.destination,
        "price": 70,
    }


def test_finish_call_data_with_start_call_record_should_return_ok(session, client):
    client_phone = faker.numerify("##########")

    call = CallFactory(
        id=100,
        source=client_phone,
        start_timestamp=None,
        end_timestamp=datetime(2024, 11, 21, 21),
        price=None,
    )
    session.add(call)

    billing_period = BillingFactory()
    session.add(billing_period)

    session.commit()

    response = client.post(
        "/call",
        json={
            "id": 1,
            "type": "start",
            "timestamp": datetime(2024, 11, 21, 20).isoformat(),
            "call_id": 100,
            "source": client_phone,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 100,
        "start_timestamp": datetime(2024, 11, 21, 20).isoformat(),
        "end_timestamp": datetime(2024, 11, 21, 21).isoformat(),
        "source": client_phone,
        "destination": call.destination,
        "price": 70,
    }


def test_bad_request_start_call_record_should_return_ok(client):
    response = client.post(
        "/call",
        json={"id": 1, "type": "start"},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_bad_request_end_call_record_should_return_ok(client):
    response = client.post(
        "/call",
        json={"id": 1, "type": "end"},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
