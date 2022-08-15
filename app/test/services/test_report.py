import pytest

""" Doen't work for the final .48754 numbers... """
def test_get_report_service_with_orders(client, report_url, create_orders):
    response = client.get(report_url)
    pytest.assume(response.status_code == 200)
    pytest.assume(response.json['customers'] != None)
    pytest.assume(response.json['ingredient'] != None)
    pytest.assume(response.json['month'] != None)


def test_get_report_service_without_orders(client, report_url):
    response = client.get(report_url)
    pytest.assume(response.status.startswith('200'))
