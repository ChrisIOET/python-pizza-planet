from numbers import Number
from flask import jsonify, request


class BaseService:

    @classmethod
    def get_all(cls, controller) -> tuple[str, Number]:
        controller, error = controller.get_all()
        response = controller if not error else {'error': error}
        status_code = 200 if controller else 404 if not error else 400
        return jsonify(response), status_code

    @classmethod
    def create(cls, controller) -> tuple[str, Number]:
        controller, error = controller.create(request.json)
        response = controller if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    @classmethod
    def update(cls, controller) -> tuple[str, Number]:
        controller, error = controller.update(request.json)
        response = controller if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    @classmethod
    def get_by_id(cls, _id, controller) -> tuple[str, Number]:
        controller, error = controller.get_by_id(_id)
        response = controller if not error else {'error': error}
        status_code = 200 if controller else 404 if not error else 400
        return jsonify(response), status_code
