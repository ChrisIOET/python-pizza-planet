from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from app.controllers.beverage import BeverageController
from app.services.base_service import BaseService

beverage = Blueprint('beverage', __name__)


@beverage.route('/', methods=GET)
def get_beverages():
     controller = BeverageController.get_all()
     return BaseService.get_all(controller)
     
@beverage.route('/', methods=POST)
def create_beverage():
     controller = BeverageController.create(request.json)
     return BaseService.create(controller)
     
@beverage.route('/', methods=PUT)
def update_beverage():
     beverage, error = BeverageController.update(request.json)
     response = beverage if not error else {'error': error}
     status_code = 200 if not error else 400
     return jsonify(response), status_code

@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
     controller = BeverageController.get_by_id(_id)
     return BaseService.get_id(controller)


