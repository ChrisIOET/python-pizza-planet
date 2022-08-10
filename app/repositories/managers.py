from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column

from .models import Item, Order, OrderDetail, Size, db
from .serializers import (ItemSerializer, OrderSerializer,
                          SizeSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


# class BeverageManager(BaseManager):
#     model = Beverage
#     serializer = BeverageSerializer

#     @classmethod
#     def get_by_id_list(cls, ids: Sequence):
#         return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class ItemManager(BaseManager):
    model = Item
    serializer = ItemSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []

    @classmethod
    def get_by_type_list(cls, type: str):
        return cls.session.query(cls.model).filter(cls.model.type == type).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    itemsList = List[Item]
    # print(itemsList, 'itemslist', 'Beverage')
    # beverages: List[Beverage]

    @classmethod
    def create(cls, order_data: dict, items: List[Item]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((
            OrderDetail(order_id=new_order._id,
                            item_id=item._id,
                            item_price=item.price,
                            # # beverage_price=item.price,
                            # # beverage_id=item._id,

                            )  # aca hay que añadir la bebida y el precio
            for item in items))

        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()
