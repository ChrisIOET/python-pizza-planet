from ..repositories.managers import IngredientManager
from .base import BaseController


class ItemController(BaseController):
    manager = IngredientManager
