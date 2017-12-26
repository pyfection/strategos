

class Base:
    MODEL = None
    __slots__ = ['_model']

    def __init__(self):
        assert self.MODEL
        self._model = self.MODEL()

    def __setattr__(self, key, value):
        if key in ('_model', 'MODEL'):
            super().__setattr__(key, value)
        self.MODEL.__setattr__(self._model, key, value)

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self.MODEL.__getattribute__(self._model, item)

    @classmethod
    def all(cls):
        return cls.MODEL.all()

    @classmethod
    def find(cls, **kwargs):
        return cls.MODEL.find(**kwargs)

    def load_from_model(self, model):
        self._model = model
