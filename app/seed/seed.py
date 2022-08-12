import os
import random
import sqlalchemy as db
from alembic import op
from datetime import date
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import sessionmaker

from app.repositories.models import Order

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


def date_random():
    year = random.randint(2000, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 28) if month == 2 else random.randint(
        1, 31) if month in [1, 3, 5, 7, 8, 10, 12] else random.randint(1, 30)
    return date(year, month, day)

# Create an ad-hoc table to use for the insert statement.


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


def random_ingredient_generator():
          ingredients = ['pepperonii', 'ham', 'cheese',
              'cheddar', 'anana', 'tomato', 'egg', 'bacon']
          prices = float(range(0, 10))


     def seed():
       
#     f'{names[random.randint(0, len(names))]} {lastnames[random.randint(0, len(lastnames))]}'

    engine = db.create_engine(
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pizza.sqlite')))
    session = sessionmaker(bind=engine)()
#     for i in range(0, 100):

#     print(client_set)
#         order = Order(
#             client_name=,
#             client_address=,
#             client_phone=,
#             date=date.today(),
#             total_price=i,
#             size_id=1
#         )

#     order = Order(date=date.today(), _id=199, total_price=0, client_name='Juan',
#                   client_dni='12345678', client_address='Calle falsa 123', client_phone='12345678', size_id=1)
#     session.add(order)
#     session.commit()

    #   {'_id': 200, 'client_name': 'John Smith', 'client_dni': 12345678, 'client_address': 'Calle Falsa 123',
    #       'client_phone': 12345678, 'date': date(2020, 1, 1), 'total_price': 100, 'size_id': 1},
    #   {'_id': 201, 'client_name': 'Ed Williams', 'client_dni': 87654321, 'client_address': 'Calle Verdadera 123',
    #    'client_phone': 87654321, 'date': date(2020, 1, 1), 'total_price': 200, 'size_id': 2},
    #   {'_id': , 'client_name': 'Wendy Jones', 'client_dni': 12345678, 'client_address': 'Calle Falsa 123',
    #    'client_phone': 12345678, 'date': date(2020, 1, 1), 'total_price': 300, 'size_id': 3},

    # op.execute(
    # order_table.update().
    # where(order_table.c.name == op.inline_literal('order 1')).
    # values({'client_name': op.inline_literal('order 2')})
    # )

    # # query = db.select([order_table])
    # # result_proxy = connection.execute(query)
