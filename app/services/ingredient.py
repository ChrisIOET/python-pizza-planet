from app.common.http_methods import GET, POST, PUT
from flask import Blueprint

from app.services.index import base_service
from app.controllers.index_controller import IndexController

ingredient = Blueprint('ingredient', __name__)

controller = IndexController.get_selected_controller('2')


@ingredient.route('/', methods=GET)
def get_ingredients():
    return base_service.get_all(controller)


@ingredient.route('/', methods=POST)
def create_ingredient():
    return base_service.create(controller)


@ingredient.route('/', methods=PUT)
def update_ingredient():
    return base_service.update(controller)


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    return base_service.get_id(controller)
