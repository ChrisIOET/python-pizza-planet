import datetime
from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column

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
            cls.session.query(cls.model)
            .filter(cls.model._id.in_(set(ids)))
            .all()
            or []
        )


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model)
            .filter(cls.model._id.in_(set(ids)))
            .all()
            or []
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
        cls,
        order_data: dict,
        ingredients: List[Ingredient],
        beverages: List[Beverage],
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
            cls.session.query(cls.model)
            .filter(cls.model._id.in_(set(ids)))
            .all()
            or []
        )


class IndexManager(BaseManager):
    @classmethod
    def test_connection(cls):
        cls.session.query(column("1")).from_statement(text("SELECT 1")).all()


class ReportManager(BaseManager):
    @classmethod
    def get_most_requested_ingredient(cls):
        order_details = OrderDetailManager.get_all()
        all_ingredients_list = [
            orderDetail["ingredient"]["_id"] for orderDetail in order_details
        ]
        most_request_ingredient = max(
            set(all_ingredients_list),
            key=all_ingredients_list.count,
            default=0,
        )

        return f"id:{most_request_ingredient}"

    def get_most_ingredient_name_requested():
        ingredient_name = IngredientManager.get_all()
        most_request_ingredient = ReportManager.get_most_requested_ingredient()
        most_request_ingredient_name = [
            ingredient["name"]
            for ingredient in ingredient_name
            if ingredient["_id"] == len(most_request_ingredient)
        ][0]
        return most_request_ingredient_name

    @classmethod
    def get_all_months_dict(cls):
        orders = OrderManager.get_all()
        all_months_dict = {}
        for order in orders:
            get_selected_month = datetime.datetime.strptime(
                order["date"], "%Y-%m-%dT%H:%M:%S"
            ).month
            all_months_dict[get_selected_month] = float(
                "{:.2f}".format(
                    round(
                        all_months_dict.get(get_selected_month, 0)
                        + order["total_price"],
                        2,
                    )
                )
            )
        return all_months_dict

    @classmethod
    def get_max_month_revenue_in_orders(cls):
        all_months_dict = cls.get_all_months_dict()
        max_month_revenue = max(
            all_months_dict, key=all_months_dict.get, default=0
        )

        return max_month_revenue

    @classmethod
    def get_max_revenue_in_orders(cls):
        all_months_dict = cls.get_all_months_dict()
        max_revenue = max(all_months_dict.values(), default=0)

        return "{:.2f}".format(max_revenue)

    @classmethod
    def get_all_customers_dict(cls):
        orders = OrderManager.get_all()
        all_customers_dict = {}
        for order in orders:
            all_customers_dict[
                f"id:{order['client_dni']} name:{order['client_name']}"
            ] = float(
                "{:.2f}".format(
                    round(
                        all_customers_dict.get(
                            (f"id:{order['client_dni']}"
                             f"name:{order['client_name']}"),
                            0,
                        )
                        + order["total_price"],
                        2,
                    )
                )
            )

        return all_customers_dict

    @classmethod
    def get_top3_customers(cls):
        all_customers_dict = cls.get_all_customers_dict()
        top3_customers = sorted(
            all_customers_dict, key=all_customers_dict.get, reverse=True
        )[:3]

        return top3_customers

    @classmethod
    def get_top3_customers_values(cls):
        all_customers_dict = cls.get_all_customers_dict()
        top3_customers_values = sorted(
            all_customers_dict.values(), reverse=True
        )[:3]

        return list(map(lambda x: "{:.2f}".format(x), top3_customers_values))

    @classmethod
    def obtain_all_data_from_customers(cls):
        return {
            "most_requested_ingredient": (
                cls.get_most_ingredient_name_requested()
            ),
            "most_revenue_month": cls.get_max_month_revenue_in_orders(),
            "max_revenue": cls.get_max_revenue_in_orders(),
            "top_3_customers": cls.get_top3_customers(),
            "top_3_customers_values": cls.get_top3_customers_values(),
        }
