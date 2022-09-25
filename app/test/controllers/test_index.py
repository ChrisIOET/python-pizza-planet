import pytest
from app.controllers.index import IndexController


def test_get_index__returns_main_page__when_is_called(app):
    is_connected, _ = IndexController.test_connection()
    pytest.assume(is_connected is True)
