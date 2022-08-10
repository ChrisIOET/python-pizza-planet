import pytest
from app.controllers import (
    ItemController, OrderController,SizeController)
from app.controllers.base import BaseController
from app.test.utils.functions import get_random_choice, shuffle_list


def __order(items: list, size: dict, client_data: dict):
    items = [item.get('_id') for item in items]
    size_id = size.get('_id')
    return {
        **client_data,
        'items': items,
        'size_id': size_id
    }


def __create_items(items: list, controller: BaseController):
    created_items = []
    for item in items:
        created_item, _ = controller.create(item)
        created_items.append(created_item)
    return created_items


def __create_sizes_and_items(items: list, sizes: list):
    created_items = __create_items(items, ItemController)
    created_sizes = __create_items(sizes, SizeController)
    return created_sizes if len(created_sizes) > 1 else created_sizes.pop(), created_items


def test_create(app, items, size, client_data):
    created_size, created_items = __create_sizes_and_items(items, [
                                                                       size])
    order = __order(created_items, created_size, client_data)
    created_order, error = OrderController.create(order)
    size_id = order.pop('size_id', None)
    item_ids = order.pop('items', [])
    pytest.assume(error is None)
    for param, value in order.items():
        pytest.assume(param in created_order)
        pytest.assume(value == created_order[param])
        pytest.assume(created_order['_id'])
        pytest.assume(size_id == created_order['size']['_id'])

        items_in_detail = set(
            item['item']['_id'] for item in created_order['detail'])
        pytest.assume(not items_in_detail.difference(item_ids))


def test_calculate_order_price(app, items, size, client_data):
    created_size, created_items = __create_sizes_and_items(items, [
                                                                       size])
    order = __order(created_items, created_size, client_data)
    created_order, _ = OrderController.create(order)
    pytest.assume(created_order['total_price'] == round(
        created_size['price'] + sum(item['price'] for item in created_items), 2))


def test_get_by_id(app, items, size, client_data):
    created_size, created_items = __create_sizes_and_items(items, [
                                                                       size])
    order = __order(created_items, created_size, client_data)
    created_order, _ = OrderController.create(order)
    order_from_db, error = OrderController.get_by_id(created_order['_id'])
    size_id = order.pop('size_id', None)
    item_ids = order.pop('items', [])
    pytest.assume(error is None)
    for param, value in created_order.items():
        pytest.assume(order_from_db[param] == value)
        pytest.assume(size_id == created_order['size']['_id'])

        items_in_detail = set(
            item['item']['_id'] for item in created_order['detail'])
        pytest.assume(not items_in_detail.difference(item_ids))


def test_get_all(app, items, sizes, client_data):
    created_sizes, created_items = __create_sizes_and_items(
        items, sizes)
    created_orders = []
    for _ in range(5):
        order = __order(shuffle_list(created_items)[
                        :3], get_random_choice(created_sizes), client_data)
        created_order, _ = OrderController.create(order)
        created_orders.append(created_order)

    orders_from_db, error = OrderController.get_all()
    searchable_orders = {db_order['_id']
        : db_order for db_order in orders_from_db}
    pytest.assume(error is None)
    for created_order in created_orders:
        current_id = created_order['_id']
        assert current_id in searchable_orders
        for param, value in created_order.items():
            pytest.assume(searchable_orders[current_id][param] == value)
