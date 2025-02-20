import pytest
from app.controllers import BeverageController

from app.test.utils.functions import get_random_string, get_random_price


def test_beverage_controller__returns_new_beverage(app, beverage: dict):
    created_beverage, error = BeverageController.create(beverage)
    pytest.assume(error is None)
    for param, value in beverage.items():
        pytest.assume(param in created_beverage)
        pytest.assume(value == created_beverage[param])
        pytest.assume(created_beverage["_id"])


def test_beverage_controller__returns_updated_beverage__when_name_is_random_and_price_is_between_ten_and_twenty(
    app, beverage: dict
):
    created_beverage, _ = BeverageController.create(beverage)
    updated_fields = {
        "name": get_random_string(),
        "price": get_random_price(10, 20),
    }
    updated_beverage, error = BeverageController.update(
        {"_id": created_beverage["_id"], **updated_fields}
    )
    pytest.assume(error is None)
    beverage_from_database, error = BeverageController.get_by_id(
        created_beverage["_id"]
    )
    for param, value in updated_fields.items():
        pytest.assume(updated_beverage[param] == value)
        pytest.assume(beverage_from_database[param] == value)


def test_beverage_controller__return_beverage__when_id_is_called(
    app, beverage: dict
):
    created_beverage, _ = BeverageController.create(beverage)
    beverage_from_db, error = BeverageController.get_by_id(
        created_beverage["_id"]
    )
    pytest.assume(error is None)
    for param, value in created_beverage.items():
        pytest.assume(beverage_from_db[param] == value)


def test_beverage_controller__returns_all_beverages(app, beverages: list):
    created_beverages = []
    for beverage in beverages:
        created_beverage, _ = BeverageController.create(beverage)
        created_beverages.append(created_beverage)

    beverages_from_db, error = BeverageController.get_all()
    searchable_beverages = {
        beverage["_id"]: beverage for beverage in beverages_from_db
    }
    pytest.assume(error is None)
    for beverage in created_beverages:
        pytest.assume(beverage["_id"] in searchable_beverages)
        for param, value in beverage.items():
            pytest.assume(
                searchable_beverages[beverage["_id"]][param] == value
            )
