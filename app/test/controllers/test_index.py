import pytest
from app.controllers.index import IndexController


def test_index_controller_test_connection(app):
    is_connected, _ = IndexController.test_connection()
    pytest.assume(is_connected is True)
