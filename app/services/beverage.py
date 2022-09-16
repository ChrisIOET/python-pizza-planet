from app.common.http_methods import GET, POST, PUT
from flask import Blueprint

from app.services.index import base_service
from app.controllers.index_controller import IndexController

beverage = Blueprint('beverage', __name__)

controller = IndexController.get_selected_controller('1')


@beverage.route('/', methods=GET)
def get_beverages():
    return base_service.get_all(controller)


@beverage.route('/', methods=POST)
def create_beverage():
    return base_service.create(controller)


@beverage.route('/', methods=PUT)
def update_beverage():
    return base_service.update(controller)


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return base_service.get_by_id(controller, _id)
