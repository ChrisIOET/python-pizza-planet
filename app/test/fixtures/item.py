import pytest

from ..utils.functions import get_random_price, get_random_string


def item_mock() -> dict:
    return {
        'name': get_random_string(),
        'price': get_random_price(10, 20)
    }


@pytest.fixture
def item_uri():
    return '/item/'


@pytest.fixture
def item():
    return item_mock()


@pytest.fixture
def items():
    return [item_mock() for _ in range(5)]


@pytest.fixture
def create_item(client, item_uri) -> dict:
    response = client.post(item_uri, json=item_mock())
    return response


@pytest.fixture
def create_items(client, item_uri) -> list:
    items = []
    for _ in range(10):
        new_item = client.post(item_uri, json=item_mock())
        items.append(new_item.json)
    return items
