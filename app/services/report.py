from app.common.http_methods import GET
from flask import Blueprint
from app.controllers.report import ReportController


report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    return ReportController.obtain_report()
