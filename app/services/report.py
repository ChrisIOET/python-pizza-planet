from app.common.http_methods import GET
from flask import Blueprint
from app.controllers.report import ReportController
from app.controllers.base_service import BaseService

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    controller = ReportController.obtain_report()
    return BaseService.get_all(controller)
