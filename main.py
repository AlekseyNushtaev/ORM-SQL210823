import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from models import create_tables, get_shops, json_to_db, Publisher, Shop, Sale, Stock, Book

if __name__ == '__main__':

    db_login = os.getenv('DB_LOGIN')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    DSN = f"postgresql://{db_login}:{db_password}@localhost:5432/{db_name}"
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    json_to_db('tests_data.json', session)
    pub = input('Введите название или id издателя\n')
    get_shops(pub, session)

    session.close()