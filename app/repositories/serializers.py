from app.plugins import ma
from .models import Item, Size, Order, OrderDetail


class ItemSerializer(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Item
        load_instance = True
        fields = ('_id', 'name', 'price', 'type')


class SizeSerializer(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Size
        load_instance = True
        fields = ('_id', 'name', 'price')


# class BeverageSerializer(ma.SQLAlchemyAutoSchema):

#     class Meta:
#         model = Beverage
#         load_instance = True
#         fields = ('_id', 'name', 'price')


class OrderDetailSerializer(ma.SQLAlchemyAutoSchema):

    item = ma.Nested(ItemSerializer)
    # beverage = ma.Nested(BeverageSerializer)

    class Meta:
        model = OrderDetail
        load_instance = True
        fields = (
            'item_price',
            'item',
            # 'beverage_price',  # !!!
            # 'beverage',  # !!!
        )


class OrderSerializer(ma.SQLAlchemyAutoSchema):
    size = ma.Nested(SizeSerializer)
    detail = ma.Nested(OrderDetailSerializer, many=True)

    class Meta:
        model = Order
        load_instance = True
        fields = (
            '_id',
            'client_name',
            'client_dni',
            'client_address',
            'client_phone',
            'date',
            'total_price',
            'size',
            'detail'
        )
