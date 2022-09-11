import pytest


def test_create_order(create_orders):
    for order in create_orders:
        pytest.assume(order.status.startswith('200'))
        pytest.assume(order.json['_id'])
        pytest.assume(order.json['client_address'])
        pytest.assume(order.json['client_name'])
        pytest.assume(order.json['client_phone'])
        pytest.assume(order.json['date'])
        pytest.assume(order.json['detail'])
        pytest.assume(order.json['size'])
        pytest.assume(order.json['total_price'])


def test_get_orders_service(client, create_orders, order_uri):
    get_client = client.get(order_uri)
    pytest.assume(get_client.status.startswith('200'))
    orders_returned = {
        get_client['_id']: get_client for get_client in get_client.json
    }
    for order in create_orders:
        pytest.assume(len(orders_returned) == len(create_orders))
        pytest.assume(order.json['_id'] in orders_returned)


def test_get_order_by_id_service(client, create_orders, order_uri):
    orders = []
    for order in create_orders:
        orders.append(order.json)
    current_order = orders[0]
    response = client.get(f'{order_uri}id/{current_order["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_order = response.json
    for param, value in current_order.items():
        pytest.assume(returned_order[param] == value)
