

import os
import uuid

from tinydb import TinyDB, Query
from tinydb.queries import where


class Base(object):
    __table__ = '_default'
    TYPES = {}
    _ = Query()
    type = ''
    id = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or str(uuid.uuid4())
        self.type = self.type  # this adds it to self.__dict__

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    @classmethod
    def all(cls):
        return (
            cls.TYPES[obj['type']](**obj)
            for obj in db.session.table(cls.__table__).all()
            if ((cls.type and cls.type == obj.get('type'))
                or (not cls.type and obj.get('type') in cls.TYPES))
        )

    @classmethod
    def find(cls, cond):
        return (
            cls.TYPES[obj['type']](**obj)
            for obj in db.session.table(cls.__table__).search(cond)
            if ((cls.type and cls.type == obj.get('type'))
                or (not cls.type and obj.get('type') in cls.TYPES))
        )

    @classmethod
    def get(cls, cond):
        if cls.type:
            cond = cond & where('type') == cls.type
        obj = db.session.table(cls.__table__).get(cond)
        return obj

    @property
    def table(self):
        return db.session.table(self.__table__)

    def save(self):
        d = self.__dict__
        self.table.upsert(d, where('id') == self.id)

    def reload(self):
        self.__dict__ = self.table.get(where('id') == self.id)

    def copy(self, **kwargs):
        d = {
            key: value
            for key, value
            in self.__dict__.items()
            if key.lower() == key and not key.startswith('_') and not key.endswith('id')
        }
        d.update(kwargs)
        return self.__class__(**d)


class Database:
    session = None

    def load_game(self, save_name):
        try:
            # This is temporary to ensure that there is always a fresh gamestate
            os.remove(f'saves/{save_name}.gs')
        except:
            pass
        self.session = TinyDB(f'saves/{save_name}.gs')


db = Database()
models = {}
