import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_beverage_service__returns_new_beverage(create_beverage):

    beverage = create_beverage.json

    pytest.assume(create_beverage.status.startswith("200"))
    pytest.assume(beverage["_id"])
    pytest.assume(beverage["name"])
    pytest.assume(beverage["price"])


def test_beverage_service__returns_updated_beverage__when_name_is_random_and_price_is_between_one_and_five(
    client, create_beverage, beverage_uri
):

    current_beverage = create_beverage.json
    update_data = {
        **current_beverage,
        "name": get_random_string(),
        "price": get_random_price(1, 5),
    }

    response = client.put(beverage_uri, json=update_data)
    updated_beverage = response.json

    pytest.assume(response.status.startswith("200"))
    for param, value in update_data.items():
        pytest.assume(updated_beverage[param] == value)


def test_beverage_service__return_beverage__when_id_is_called(
    client, create_beverage, beverage_uri
):

    current_beverage = create_beverage.json

    response = client.get(f'{beverage_uri}id/{current_beverage["_id"]}')
    returned_beverage = response.json

    pytest.assume(response.status.startswith("200"))
    for param, value in current_beverage.items():
        pytest.assume(returned_beverage[param] == value)


def test_beverage_service__returns_all_beverages(
    client, create_beverages, beverage_uri
):

    response = client.get(beverage_uri)

    pytest.assume(response.status.startswith("200"))
    returned_beverages = {
        beverage["_id"]: beverage for beverage in response.json
    }
    for beverage in create_beverages:
        pytest.assume(beverage["_id"] in returned_beverages)
