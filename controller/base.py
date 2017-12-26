

class Base:
    MODEL = None
    __slots__ = ['_model']

    def __init__(self, model=None, **kwargs):
        assert self.MODEL
        if model:
            assert isinstance(model, self.MODEL)
            self._model = model
        else:
            self._model = self.MODEL()
        for key, value in kwargs.items():
            setattr(self, key, value)

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
        return [cls(model=model) for model in cls.MODEL.all()]

    @classmethod
    def find(cls, **kwargs):
        return [cls(model=model) for model in cls.MODEL.find(**kwargs)]

    def copy(self, **kwargs):
        d = {
            key: value
            for key, value
            in self._model.__dict__.items()
            if key.lower() == key and not key.startswith('_') and not key.endswith('id')
        }
        d.update(kwargs)
        return self.__class__(**d)
