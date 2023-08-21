import sqlalchemy
import json
import os
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Sale, Stock, Book

if __name__ == '__main__':

    db_login = os.getenv('DB_LOGIN')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    DSN = f"postgresql://{db_login}:{db_password}@localhost:5432/{db_name}"
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('tests_data.json', 'r') as fd:
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

    pub_id = int(input('Введите id издателя\n'))
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == pub_id)
    for s in q.all():
        print(s[0] + ' | ' + s[1] + ' | ' + str(s[2]) + ' | ' + s[3].strftime("%d-%m-%Y"))
    session.close()