

import os

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker


@as_declarative(constructor=None)
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, *args, **kwargs):
        db.session.add(self)

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def find(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).all()

    id = Column(Integer, primary_key=True)


class Database:
    session = None
    engine = None

    def load_game(self, save_name):
        try:
            # This is temporary to ensure that there is always a fresh gamestate
            os.remove(f'saves/{save_name}.gs')
        except:
            pass
        self.engine = create_engine(f'sqlite:///saves/{save_name}.gs', echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


db = Database()