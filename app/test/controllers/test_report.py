import pytest
from app.controllers import ReportController

"""  unconverted data remains: .434218 seconds """


def test_get_report_with_orders(app, create_orders):
    report, error = ReportController.obtain_report()
    pytest.assume(error is None)
    pytest.assume(report['ingredient'] is not None)
    pytest.assume(report['customers'] is not None)
    pytest.assume(report['month'] is not None)


def test_get_report_without_orders(app):
    report, error = ReportController.obtain_report()
    pytest.assume(error is None)
