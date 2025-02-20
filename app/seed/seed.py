import os
from random import randint, uniform
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from datetime import date
from dotenv import load_dotenv
from app.settings import ProductionConfig, DevelopmentConfig
from app.repositories.models import (
    Ingredient,
    Order,
    OrderDetail,
    Size,
    Beverage,
)

load_dotenv()

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

database = (DevelopmentConfig.SQLALCHEMY_DATABASE_URI if
            os.environ.get("FLASK_ENV") == "development"
            else ProductionConfig.SQLALCHEMY_DATABASE_URI)

engine = db.create_engine(database)
session = sessionmaker(bind=engine)()


def random_date():
    year = 2022
    month = randint(1, 12)
    day = (
        randint(1, 28)
        if month == 2
        else randint(1, 31)
        if month in [1, 3, 5, 7, 8, 10, 12]
        else randint(1, 30)
    )
    return date(year, month, day)


def random_customer_generator():
    names = [
        "pepe",
        "pepito" "carla",
        "carlita",
        "juan",
        "juanito",
        "pedro",
        "pedrito",
        "mariaito",
        "jose",
        "joseito",
        "luis",
        "luisito",
        "maria",
    ]
    lastnames = [
        "perez",
        "gomez",
        "lopez",
        "martinez",
        "gonzalez",
        "rodriguez",
        "garcia",
        "zukita",
        "mirlaksivoc",
        "subeogme",
        "katuzird",
        "paredes",
        "gallo",
    ]
    client_address = [
        "falsa",
        "viva",
        "1337",
        "boucherl",
        "boulevard",
        "pepe",
        "rouvin",
        "kallow",
        "louiputi",
        "hunioned",
        "spovten",
    ]
    client_list = list(
        set(
            [
                (
                    (f"{names[randint(0, len(names)-1)]}"
                     f" {lastnames[randint(0, len(lastnames)-1)]}"),
                    (f"calle "
                     f"{client_address[randint(0,len(client_address)-1)]}"),
                    f"{ randint(20000000,90000000) }",
                    (f"+{randint(100, 999)},"
                     f"{randint(10,99)}{randint(100,999)}{randint(100,999)}"),
                )
                for _ in range(50)
            ]
        )
    )
    return client_list


def generate_random_number():
    return float("{:.2f}".format(round(uniform(1, 9), 2)))


def ingredients_random_generator():
    ingredients = [
        "pepperonii",
        "ham",
        "cheese",
        "cheddar",
        "anana",
        "tomato",
        "egg",
        "bacon",
        "onion",
        "champignon",
    ]
    return [
        [
            ingredients[i],
            generate_random_number(),
        ]
        for i in range(0, len(ingredients))
    ]


def size_random_generator():
    sizes = ["small", "medium", "large", "xl", "xxl"]
    return [{
        "size": size,
        "price": generate_random_number(),
    } for size in sizes]


def beverage_random_generator():
    beverages = [
        "licor",
        "whisky",
        "water",
        "red bull",
        "fanta",
        "coke",
        "monster",
    ]
    return [
        [beverages[i], generate_random_number()]
        for i in range(0, len(beverages))
    ]


def beverages_table_populator():
    beverages = beverage_random_generator()
    for i in range(1, len(beverages) + 1):
        session.add(
            Beverage(name=beverages[i - 1][0], price=beverages[i - 1][1])
        )
    session.commit()
    session.close()


def ingredients_table_populator():

    ingredients = ingredients_random_generator()
    for i in range(1, len(ingredients) + 1):
        session.add(
            Ingredient(name=ingredients[i - 1][0], price=ingredients[i - 1][1])
        )
    session.commit()
    session.close()


def sizes_table_populator():
    sizes = size_random_generator()
    for size in sizes:
        session.add(Size(
            name=size["size"],
            price=size["price"]
        ))
    session.commit()
    session.close()


def get_ingredients():
    ingredients = session.query(Ingredient).all()
    session.close()
    return ingredients


def get_sizes():
    sizes = session.query(Size).all()
    session.close()
    return sizes


def get_beverages():
    beverages = session.query(Beverage).all()
    session.close()
    return beverages


def get_id(table, name, price):
    id = session.query(table._id).filter_by(name=name, price=price).first()
    session.close()
    return id[0]


def order_detail_generator():
    ingredients = get_ingredients()
    beverages = get_beverages()
    order_detail = []

    for i in range(1, randint(2, 6)):
        ingredient = ingredients[randint(0, len(ingredients) - 1)]
        beverage = beverages[randint(0, len(beverages) - 1)]
        order_detail.append(
            [
                get_id(Ingredient, ingredient.name, ingredient.price),
                ingredient.price,
                get_id(Beverage, beverage.name, beverage.price),
                beverage.price,
            ]
        )

    return order_detail


def order_detail_populator(order_id: int, order_details: list):
    for order_detail in order_details:
        session.add(
            OrderDetail(
                order_id=order_id,
                ingredient_id=order_detail[0],
                ingredient_price=order_detail[1],
                beverage_id=order_detail[2],
                beverage_price=order_detail[3],
            )
        )

    session.commit()
    session.close()


def order_table_populator():
    client_list = random_customer_generator()
    sizes = get_sizes()

    for j in range(1, 101):
        random_client = client_list[randint(0, len(client_list) - 1)]

        next_id = session.query(Order).count() + 1

        order_details = order_detail_generator()
        order_details_sum = float(
            "{:.2f}".format(
                round(
                    sum(
                        [
                            order_details[i][1] + order_details[i][3]
                            for i in range(0, len(order_details))
                        ]
                    ),
                    2,
                )
            )
        )
        size = sizes[randint(0, len(sizes) - 1)]
        order = Order(
            client_name=random_client[0],
            client_address=random_client[1],
            client_dni=random_client[2],
            client_phone=random_client[3],
            date=random_date(),
            total_price=order_details_sum,
            size_id=get_id(Size, size.name, size.price),
        )
        session.add(order)
        session.commit()
        order_detail_populator(next_id, order_details)

    session.close()


def seed():
    sizes_table_populator()
    ingredients_table_populator()
    beverages_table_populator()
    order_table_populator()
