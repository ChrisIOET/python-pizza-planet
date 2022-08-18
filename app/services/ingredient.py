from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from app.controllers.base_service import BaseService

from ..controllers import IngredientController

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=GET)
def get_ingredients():
    controller = IngredientController.get_all()
    return BaseService.get_all(controller)

@ingredient.route('/', methods=POST)
def create_ingredient():
    controller = IngredientController.create(request.json)
    return BaseService.create(controller)

@ingredient.route('/', methods=PUT)
def update_ingredient():
    controller = IngredientController.update(request.json)
    return BaseService.update(controller)


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    controller = IngredientController.get_by_id(_id)
    return BaseService.get_id(controller)


