# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18 
"""
from app import config
from redis import Redis


class JsonSerializer(object):

    __json_hidden__ = None
    __json_public__ = None
    __json_modifiers__ = None
    __json_extras__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def __getattr__(self, key, default=None):
        __json_extras__ = self.__json_extras__ or dict()
        value = __json_extras__.get(key)
        if value is None:
            try:
                value = self.__mapper__.get(key)
            except Exception:
                raise AttributeError(key)
        return value if value is not None else default

    def set_extras(self, extras):
        self.__json_extras__ = extras

    def to_dict(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or list(field_names)
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()
        extras = self.__json_extras__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        rv.update(extras)
        return rv

