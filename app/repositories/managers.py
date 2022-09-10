import datetime
from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column
from sqlalchemy import func

from app.common.utils import format_currency_with_double_decimals

from .models import Beverage, Ingredient, Order, OrderDetail, Size, db
from .serializers import (
    BeverageSerializer,
    IngredientSerializer,
    OrderDetailSerializer,
    OrderSerializer,
    SizeSerializer,
    ma,
)


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


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        )


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        )


def get_ingredients(new_order, ingredients: List[Ingredient]):
    items: List[OrderDetail] = []
    for ingredient in ingredients:
        order_detail = OrderDetail(
            order_id=new_order._id,
            ingredient_id=ingredient._id,
            ingredient_price=ingredient.price,
        )
        items.append(order_detail)
    return items


def get_beverages(new_order, beverages: List[Beverage]):
    items: List[OrderDetail] = []
    for beverage in beverages:
        order_detail = OrderDetail(
            order_id=new_order._id,
            beverage_id=beverage._id,
            beverage_price=beverage.price,
        )
        items.append(order_detail)
    return items


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(
        cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]
    ):
        new_order = cls.model(**order_data)

        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)

        ingredients = get_ingredients(new_order, ingredients)
        beverages = get_beverages(new_order, beverages)

        cls.session.add_all(ingredients)
        cls.session.add_all(beverages)

        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def get_all_orders(cls):
        return cls.session.query(cls.model).all() or []

    @classmethod
    def update(cls):
        raise NotImplementedError(f"Method not suported for {cls.__name__}")


class OrderDetailManager(BaseManager):
    model = OrderDetail
    serializer = OrderDetailSerializer

    @classmethod
    def get_all_orders_details(cls):
        return cls.session.query(cls.model).all() or []

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        )


class IndexManager(BaseManager):
    @classmethod
    def test_connection(cls):
        cls.session.query(column("1")).from_statement(text("SELECT 1")).all()


class ReportManager(BaseManager):

    session = db.session

    @classmethod
    def get_most_requested_ingredient(cls):
        most_request_ingredient = (
            cls.session.query(Ingredient, func.count(OrderDetail.ingredient_id))
            .join(OrderDetail)
            .group_by(Ingredient)
            .order_by(func.count(OrderDetail.ingredient_id).desc())
            .first()
        )
        return f"{most_request_ingredient[0].name}, {most_request_ingredient[1]} times"

    @classmethod
    def get_most_revenue_month(cls):
        max_month_revenue = (
            cls.session.query(Order.date)
            .group_by(Order.date)
            .order_by(func.sum(Order.total_price).desc())
            .first()
        )
        month = max_month_revenue[0].month
        return f"{month}"

    @classmethod
    def get_max_revenue(cls):
        max_revenue = (
            cls.session.query(func.sum(Order.total_price))
            .group_by(Order.date)
            .order_by(func.sum(Order.total_price).desc())
            .first()
        )
        return max_revenue[0]

    @classmethod
    def get_top3_customers_data(cls):
        def get_customer_dict(customer):
            return f" dni: {customer[0]}, name: {customer[1]}"

        all_customers = (
            cls.session.query(Order.client_dni, Order.client_name)
            .group_by(Order.client_dni)
            .order_by(func.sum(Order.total_price).desc())
            .limit(3)
            .all()
        )

        return [get_customer_dict(customer) for customer in all_customers]

    @classmethod
    def get_top3_customers_values(cls):
        top_3_customers_value = (
            cls.session.query(func.sum(Order.total_price))
            .group_by(Order.client_dni)
            .order_by(func.sum(Order.total_price).desc())
            .limit(3)
            .all()
        )

        return [f"${customer[0]:.2f}" for customer in top_3_customers_value]

    @classmethod
    def obtain_all_data_from_customers(cls):
        return {
            "most_requested_ingredient": cls.get_most_requested_ingredient(),
            "most_revenue_month": cls.get_most_revenue_month()[0],
            "max_revenue": cls.get_max_revenue(),
            "top_3_customers": cls.get_top3_customers_data(),
            "top_3_customers_values": cls.get_top3_customers_values(),
        }
