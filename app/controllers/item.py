from ..repositories.managers import ItemManager
from .base import BaseController


class ItemController(BaseController):
    manager = ItemManager
