from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify
from app.controllers.report import ReportController
from app.services.base_service import BaseService

report = Blueprint('report', __name__)

@report.route('/', methods=GET)
def get_report():
    controller = ReportController.obtain_report()
    return BaseService.get_all(controller)
