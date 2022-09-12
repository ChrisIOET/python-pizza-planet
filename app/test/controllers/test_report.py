import pytest
from app.controllers import ReportController


def test_get_report_with_orders(app, create_orders):
    report, error = ReportController.obtain_report()
    pytest.assume(error is None)
    pytest.assume(report['most_requested_ingredient'] is not None)
    pytest.assume(report['top_3_customers'] is not None)
    pytest.assume(report['top_3_customers_values'] is not None)
    pytest.assume(report['most_revenue_month'] is not None)
    pytest.assume(report['max_revenue'] is not None)
