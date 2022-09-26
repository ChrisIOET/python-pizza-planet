import pytest


def test_report_service__returns_report__with_orders(
    client, report_url, create_orders
):

    response = client.get(report_url)

    pytest.assume(response.status_code == 200)
    pytest.assume(response.json["max_revenue"] is not None)
    pytest.assume(response.json["most_requested_ingredient"] is not None)
    pytest.assume(response.json["most_revenue_month"] is not None)
    pytest.assume(response.json["top_3_customers"] is not None)
    pytest.assume(response.json["top_3_customers_values"] is not None)
    pytest.assume(len(response.json) == 5)
