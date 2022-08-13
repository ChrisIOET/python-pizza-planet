from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from app.controllers.base_service import BaseService

from ..controllers import SizeController

size = Blueprint('size', __name__)


@size.route('/', methods=POST)
def create_size():
    controller = SizeController.create(request.json)
    return BaseService.create(controller)


@size.route('/', methods=PUT)
def update_size():
    controller = SizeController.update(request.json)
    return BaseService.update(controller)


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    controller = SizeController.get_by_id(_id)
    return BaseService.get_id(controller)

@size.route('/', methods=GET)
def get_sizes():
    controller = SizeController.get_all()
    return BaseService.get_all(controller)
