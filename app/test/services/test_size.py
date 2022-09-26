import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_size_service__returns_new_size(create_size):

    size = create_size.json

    pytest.assume(create_size.status.startswith("200"))
    pytest.assume(size["_id"])
    pytest.assume(size["name"])
    pytest.assume(size["price"])


def test_size_service__returns_updated_size__when_current_size_name_is_random_and_price_between_one_and_five(
    client, create_size, size_uri
):

    current_size = create_size.json
    update_data = {
        **current_size,
        "name": get_random_string(),
        "price": get_random_price(1, 5),
    }

    response = client.put(size_uri, json=update_data)

    pytest.assume(response.status.startswith("200"))
    updated_size = response.json
    for param, value in update_data.items():
        pytest.assume(updated_size[param] == value)


def test_size_service__return_size__when_id_is_called(
    client, create_size, size_uri
):
    current_size = create_size.json
    response = client.get(f'{size_uri}id/{current_size["_id"]}')
    pytest.assume(response.status.startswith("200"))
    returned_size = response.json
    for param, value in current_size.items():
        pytest.assume(returned_size[param] == value)


def test_size_service__returns_new_sizes(client, create_sizes, size_uri):
    response = client.get(size_uri)

    returned_sizes = {size["_id"]: size for size in response.json}

    pytest.assume(response.status.startswith("200"))
    for size in create_sizes:
        pytest.assume(size["_id"] in returned_sizes)
