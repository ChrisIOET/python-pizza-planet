from .beverage import BeverageController
from .ingredient import IngredientController
from .size import SizeController
from .order import OrderController


class IndexController(object):

    @staticmethod
    def get_selected_controller(controller_type):

        if controller_type is None:
            raise ValueError("type controller is unknown or doesn't exist")
        if controller_type == "1":
            return BeverageController
        if controller_type == "2":
            return IngredientController
        if controller_type == "3":
            return SizeController
        if controller_type == "4":
            return OrderController
        else:
            return None
