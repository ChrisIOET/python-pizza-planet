from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import ItemController

item = Blueprint('item', __name__)


@item.route('/', methods=GET)
def get_items():
    items, error = ItemController.get_all()
    response = items if not error else {'error': error}
    status_code = 200 if items else 404 if not error else 400
    return jsonify(response), status_code

@item.route('/', methods=POST)
def create_item():
    item, error = ItemController.create(request.json)
    response = item if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code

@item.route('/', methods=PUT)
def update_item():
    item, error = ItemController.update(request.json)
    response = item if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code


@item.route('/id/<_id>', methods=GET)
def get_item_by_id(_id: int):
    item, error = ItemController.get_by_id(_id)
    response = item if not error else {'error': error}
    status_code = 200 if item else 404 if not error else 400
    return jsonify(response), status_code



