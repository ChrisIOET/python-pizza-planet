from app.common.http_methods import GET, POST
from flask import Blueprint, jsonify, request

from app.controllers.base_service import BaseService

from ..controllers import OrderController

order = Blueprint('order', __name__)

@order.route('/', methods=POST)
def create_order():
    controller = OrderController.create(request.json)
    return BaseService.create(controller)


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    controller = OrderController.get_by_id(_id)
    return BaseService.get_id(controller)


@order.route('/', methods=GET)
def get_orders():
    controller = OrderController.get_all()
    return BaseService.get_all(controller)
