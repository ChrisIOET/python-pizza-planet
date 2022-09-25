import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_ingredient_service__returns_new_ingredient(create_ingredient):

    ingredient = create_ingredient.json

    pytest.assume(create_ingredient.status.startswith("200"))
    pytest.assume(ingredient["_id"])
    pytest.assume(ingredient["name"])
    pytest.assume(ingredient["price"])


def test_ingredient_service__returns_updated_ingredient__when_name_is_random_and_price_is_between_one_and_five(
    client, create_ingredient, ingredient_uri
):

    current_ingredient = create_ingredient.json
    update_data = {
        **current_ingredient,
        "name": get_random_string(),
        "price": get_random_price(1, 5),
    }

    response = client.put(ingredient_uri, json=update_data)
    updated_ingredient = response.json

    pytest.assume(response.status.startswith("200"))
    for param, value in update_data.items():
        pytest.assume(updated_ingredient[param] == value)


def test_ingredient_service__return_ingredient__when_id_is_called(
    client, create_ingredient, ingredient_uri
):
    current_ingredient = create_ingredient.json

    response = client.get(f'{ingredient_uri}id/{current_ingredient["_id"]}')
    returned_ingredient = response.json

    pytest.assume(response.status.startswith("200"))
    for param, value in current_ingredient.items():
        pytest.assume(returned_ingredient[param] == value)


def test_ingredients_service__returns_all_ingredients(
    client, create_ingredients, ingredient_uri
):

    response = client.get(ingredient_uri)
    returned_ingredients = {
        ingredient["_id"]: ingredient for ingredient in response.json
    }

    pytest.assume(response.status.startswith("200"))
    for ingredient in create_ingredients:
        pytest.assume(ingredient["_id"] in returned_ingredients)
