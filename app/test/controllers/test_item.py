import pytest
from app.controllers import ItemController


def test_create(app, item: dict):
    created_item, error = ItemController.create(item)
    pytest.assume(error is None)
    for param, value in item.items():
        pytest.assume(param in created_item)
        pytest.assume(value == created_item[param])
        pytest.assume(created_item['_id'])


def test_update(app, item: dict):
    created_item, _ = ItemController.create(item)
    updated_fields = {
        'name': 'updated',
        'price': 10
    }
    updated_item, error = ItemController.update({
        '_id': created_item['_id'],
        **updated_fields
    })
    pytest.assume(error is None)
    item_from_database, error = ItemController.get_by_id(created_item['_id'])
    pytest.assume(error is None)
    for param, value in updated_fields.items():
        pytest.assume(updated_item[param] == value)
        pytest.assume(item_from_database[param] == value)


def test_get_by_id(app, item: dict):
    created_item, _ = ItemController.create(item)
    item_from_db, error = ItemController.get_by_id(created_item['_id'])
    pytest.assume(error is None)
    for param, value in created_item.items():
        pytest.assume(item_from_db[param] == value)


def test_get_all(app, items: list):
    created_items = []
    for item in items:
        created_item, _ = ItemController.create(item)
        created_items.append(created_item)

    items_from_db, error = ItemController.get_all()
    searchable_items = {db_item['_id']: db_item for db_item in items_from_db}
    pytest.assume(error is None)
    for created_item in created_items:
        current_id = created_item['_id']
        assert current_id in searchable_items
        for param, value in created_item.items():
            pytest.assume(searchable_item[current_id][param] == value)
