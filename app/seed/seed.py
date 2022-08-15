import os
import random
import sqlalchemy as db
from datetime import date
from sqlalchemy.orm import sessionmaker

from app.repositories.models import Ingredient, Order, OrderDetail, Size, Beverage

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

engine = db.create_engine(
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pizza.sqlite')))
session = sessionmaker(bind=engine)()

def random_date():
    year = 2022
    month = random.randint(1, 12)
    day = random.randint(1, 28) if month == 2 else random.randint(
        1, 31) if month in [1, 3, 5, 7, 8, 10, 12] else random.randint(1, 30)
    return date(year, month, day)


def random_customer_generator():
    names = ['pepe', 'pepito' 'carla', 'carlita', 'juan', 'juanito', 'pedro',
             'pedrito', 'mariaito', 'jose', 'joseito', 'luis', 'luisito', 'maria']
    lastnames = ['perez', 'gomez', 'lopez', 'martinez',  'gonzalez', 'rodriguez',
                 'garcia', 'zukita', 'mirlaksivoc', 'subeogme', 'katuzird', 'paredes', 'gallo']
    client_address = ['falsa', 'viva', '1337', 'boucherl', 'boulevard',
                      'pepe', 'rouvin', 'kallow', 'louiputi', 'hunioned', 'spovten']
    client_list = list(set([(f'{names[random.randint(0, len(names)-1)]} {lastnames[random.randint(0, len(lastnames)-1)]}', f'calle     {client_address[random.randint(0, len(client_address)-1)]}', f'{ random.randint(20000000,90000000) }', f'+{random.randint(100,  999) }, { random.randint(10,99) } { random.randint(100,999)} { random.randint(1000,9999)}')
                            for _ in range(50)
                            ]))
    return client_list


def ingredients_random_generator():
    ingredients = ['pepperonii', 'ham', 'cheese',
                   'cheddar', 'anana', 'tomato', 'egg', 'bacon', 'onion', 'champignon']
    return [[ingredients[i], float("{:.2f}".format(round(random.uniform(1, 9), 2)))]
            for i in range(0, len(ingredients))]


def size_random_generator():
    sizes = ['small', 'medium', 'large', 'xl', 'xxl']
    return [[sizes[i], float("{:.2f}".format(round(random.uniform(1, 9), 2)))]
            for i in range(0, len(sizes))]


def beverage_random_generator():
    beverages = ['licor', 'whisky', 'water',
                 'red bull', 'fanta', 'coke', 'monster']
    return [[beverages[i], float("{:.2f}".format(round(random.uniform(1, 9), 2)))]
            for i in range(0, len(beverages))]


def beverages_table_populator():
    beverages = beverage_random_generator()
    for i in range(1, len(beverages) + 1):
        session.add(Beverage(name=beverages[i - 1][0], price=beverages[i - 1][1]))
    session.commit()
    session.close()


def ingredients_table_populator():
    
    ingredients = ingredients_random_generator()
    for i in range(1, len(ingredients) + 1):
        session.add(Ingredient(
            name=ingredients[i - 1][0], price=ingredients[i - 1][1]))
    session.commit()
    session.close()


def sizes_table_populator():
    sizes = size_random_generator()
    for i in range(1, len(sizes) + 1):
        session.add(Size(name=sizes[i - 1][0], price=sizes[i - 1][1]))
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

    for i in range(1, random.randint(2, 6)):
        ingredient = ingredients[random.randint(0, len(ingredients)-1)]
        beverage = beverages[random.randint(0, len(beverages)-1)]
        order_detail.append([get_id(Ingredient, ingredient.name, ingredient.price),
                             ingredient.price, get_id(
                                 Beverage, beverage.name, beverage.price),
                             beverage.price])

    return order_detail


def order_detail_populator(order_id: int, order_details: list):
    for order_detail in order_details:
        session.add(OrderDetail(order_id=order_id,
                    ingredient_id=order_detail[0], ingredient_price=order_detail[1], beverage_id=order_detail[2], beverage_price=order_detail[3]))

    session.commit()
    session.close()


def order_table_populator():
    client_list = random_customer_generator()
    sizes = get_sizes()

    for j in range(1, 101):
        random_client = client_list[random.randint(0, len(client_list) - 1)]

        next_id = session.query(Order).count() + 1

        order_details = order_detail_generator()
        order_detail_populator(next_id, order_details)
        order_details_sum = float("{:.2f}".format(round(sum([order_details[i][1] + order_details[i][3]
                                                             for i in range(0, len(order_details))]), 2)))
        size = sizes[random.randint(0, len(sizes) - 1)]
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

    session.close()


def seed():
    sizes_table_populator()
    ingredients_table_populator()
    beverages_table_populator()
    order_table_populator()
    print("Seeding done")
