from app.common.http_methods import GET, POST, PUT
from flask import Blueprint

from app.services.index import base_service
from app.controllers.index_controller import IndexController

size = Blueprint('size', __name__)

controller = IndexController.get_selected_controller('3')


@size.route('/', methods=POST)
def create_size():
    return base_service.create(controller)


@size.route('/', methods=PUT)
def update_size():
    return base_service.update(controller)


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    return base_service.get_by_id(controller, _id)


@size.route('/', methods=GET)
def get_sizes():
    return base_service.get_all(controller)
