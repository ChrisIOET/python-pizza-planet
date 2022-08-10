import pytest

from ..utils.functions import (shuffle_list, get_random_sequence,
                               get_random_string)


def client_data_mock() -> dict:
    return {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence()
    }


@pytest.fixture
def order_uri():
    return '/order'


@pytest.fixture
def client_data():
    return client_data_mock()


@pytest.fixture
def order(create_items, create_size, client_data) -> dict:
    items = [item.get('_id') for item in create_items]
    size_id = create_size.get('_id')
    return {
        **client_data_mock(),
        'items': items,
        'size_id': size_id
    }


@pytest.fixture
def create_orders(client, order_uri, create_items, create_sizes) -> list:
    items = [item.get('_id') for item in create_items]
    sizes = [size.get('_id') for size in create_sizes]
    orders = []
    for _ in range(10):
        new_order = client.post(order_uri, json={
            **client_data_mock(),
            'items': shuffle_list(items)[:5],
            'size_id': shuffle_list(sizes)[0]
        })
        orders.append(new_order)
    return orders
