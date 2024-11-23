from datetime import datetime
from http import HTTPStatus

from test.factories import CallFactory

from faker import Faker

faker = Faker()


def test_get_report_with_data(session, client):
    sub = faker.numerify("##########")
    des = faker.numerify("##########")
    call = CallFactory(source=sub, destination=des,start_timestamp = datetime(2024, 10, 22, 21), end_timestamp = datetime(2024, 10, 22, 23))
    
    session.add(call)
    session.commit()
    
    response = client.get(
        "/call/report",
        params={
            "subscriber": sub,
            "billing_period": '10/2024'
        },
    )
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "subscriber": sub,
        "billing_period": '10/2024',
        "calls": [
            {
                "destination": des,
                "start_date": "10/2024",
                "start_hour": "21:00:00",
                "duration": "02h00m00s",
                "price": "R$ 1,00",
            }
        ],
    }

def test_get_report_with_no_data_should_return_not_found(client):
    sub = faker.numerify("##########")
    
    response = client.get(
        "/call/report",
        params={
            "subscriber": sub,
            "billing_period": '10/2024'
        },
    )
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": "No data was found."
    }