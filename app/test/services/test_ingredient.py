import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_item_service(create_item):
    item = create_item.json
    pytest.assume(create_item.status.startswith('200'))
    pytest.assume(item['_id'])
    pytest.assume(item['name'])
    pytest.assume(item['price'])


def test_update_item_service(client, create_item, item_uri):
    current_item = create_item.json
    update_data = {**current_item, 'name': get_random_string(),
                   'price': get_random_price(1, 5)}
    response = client.put(item_uri, json=update_data)
    pytest.assume(response.status.startswith('200'))
    updated_item = response.json
    for param, value in update_data.items():
        pytest.assume(updated_item[param] == value)


def test_get_item_by_id_service(client, create_item, item_uri):
    current_item = create_item.json
    response = client.get(f'{item_uri}id/{current_item["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_item = response.json
    for param, value in current_item.items():
        pytest.assume(returned_item[param] == value)


def test_get_items_service(client, create_items, item_uri):
    response = client.get(item_uri)
    pytest.assume(response.status.startswith('200'))
    returned_items = {item['_id']: item for item in response.json}
    for item in create_items:
        pytest.assume(item['_id'] in returned_items)
