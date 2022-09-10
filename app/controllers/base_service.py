from flask import jsonify


class BaseService:
    @staticmethod
    def get_all(controller: list):
        controller, error = controller
        response = controller if not error else {'error': error}
        status_code = 200 if controller else 404 if not error else 400
        return jsonify(response), status_code

    @staticmethod
    def create(controller):
        controller, error = controller
        response = controller if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    @staticmethod
    def update(controller):
        controller, error = controller
        response = controller if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    @staticmethod
    def get_id(controller):
        controller, error = controller
        response = controller if not error else {'error': error}
        status_code = 200 if controller else 404 if not error else 400
        return jsonify(response), status_code
