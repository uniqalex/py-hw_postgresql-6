import sqlalchemy as sq
import json
from sqlalchemy.orm import sessionmaker
from config import DB_NAME, USER_NAME, USER_PASS
from models import create_tables, Publisher, Shop, Book, Stock, Sale


def populate_tables(path, session):
    with open(path, 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def get_publicher_sales(session):
    publisher_name = input('Type publisher name:')
    try:
        #If user typed publisher_id
        publisher_id = int(publisher_name)
        select = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock). \
            join(Shop).join(Sale).filter(Publisher.id == publisher_id).all()
        for c in select:
            print([c[0]] + [c[1]] + [str(c[2])] + [str(c[3])])
    except ValueError:
        # If this was publicher name
        select = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock). \
            join(Shop).join(Sale).filter(Publisher.name == publisher_name).all()
        for c in select:
            print([c[0]] + [c[1]] + [str(c[2])] + [str(c[3])])
    except Exception:
        print('Error. Exception occurred while converting to int')

if __name__ == '__main__':
    db_type = 'postgresql'
    server = 'localhost'
    port = '5432'
    if 'None' in (USER_NAME, USER_PASS, DB_NAME):
        print('Не заданы обязательные параметры окружения:user_name, user_pass, db_name. См. config')
        exit()
    dsn = f'{db_type}://{USER_NAME}:{USER_PASS}@{server}:{port}/{DB_NAME}'
    engine = sq.create_engine(dsn)
    create_tables(engine, is_drop=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    json_model_path = 'fixtures/tests_data.json'
    populate_tables(json_model_path, session)
    get_publicher_sales(session)

    session.close()







