from numbers import Number
from flask import jsonify


class BaseService:
    @classmethod
    def get_all(cls, controller: list) -> tuple[str, Number]:
        controller, error = controller
        response = controller if not error else {'error': error}
        status_code = 200 if controller else 404 if not error else 400
        return jsonify(response), status_code

    @classmethod
    def create(cls, controller) -> tuple[str, Number]:
        controller, error = controller
        response = controller if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    @classmethod
    def update(cls, controller) -> tuple[str, Number]:
        controller, error = controller
        response = controller if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    @classmethod
    def get_id(cls, controller) -> tuple[str, Number]:
        controller, error = controller
        response = controller if not error else {'error': error}
        status_code = 200 if controller else 404 if not error else 400
        return jsonify(response), status_code
