import pytest


def test_get_index__returns_main_page__when_is_called(client, index_uri):

    response = client.get(index_uri)

    pytest.assume(response.json['error'] == '')
    pytest.assume(response.json['status'] == 'up')
    pytest.assume(response.json['version'] == '0.0.2')
    pytest.assume(len(response.json) == 3)


def test_get_index__returns_main_page__when_is_called_without_connection(
    index_uri, mocker, client
):
    def error_response():
        raise RuntimeError()

    mocker.patch(
        "app.repositories.managers.IndexManager.test_connection",
        side_effect=error_response,
    )

    response = client.get(index_uri)

    pytest.assume(response.json['error'] == '')
    pytest.assume(response.json['status'] == 'down')
    pytest.assume(response.json['version'] == '0.0.2')
    pytest.assume(len(response.json) == 3)
