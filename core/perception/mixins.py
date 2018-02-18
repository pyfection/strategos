

from copy import copy


class CopyMixin:
    _perception = None

    def copy(self, perception):
        new = copy(self)
        new._perception = perception
        return new
