from app.common.http_methods import GET, POST
from flask import Blueprint

from app.services.index import base_service
from app.controllers.index_controller import IndexController

order = Blueprint('order', __name__)

controller = IndexController.get_selected_controller('4')


@order.route('/', methods=POST)
def create_order():
    return base_service.create(controller)


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    return base_service.get_id(controller)


@order.route('/', methods=GET)
def get_orders():
    return base_service.get_all(controller)
