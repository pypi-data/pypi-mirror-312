# encoding: utf-8
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lane.chang on '07/07/2024'
    comment: 对pydantic包进行扩展
"""
import types
from typing import Union
from enum import Enum

from pydantic import BaseModel as BaseModel_


__all__ = ["BaseModel",
           "is_base_model",
           "is_generic_type"]


def is_base_model(model_field) -> bool:
    """ 是否BaseModel类
    """
    """
    """
    try:
        return issubclass(model_field.type_, BaseModel)
    except:
        return False


def is_generic_type(model_field) -> bool:
    """ 是否泛型
    """
    try:
        return issubclass(type(model_field.outer_type_), types.GenericAlias)
    except:
        return False


class BaseModel(BaseModel_):
    """ pydantic BaseModel的扩展
    """
    def __init__(self, assign_attrs=None, **kwargs):
        """
        """
        super(BaseModel, self).__init__(**kwargs)

        if assign_attrs:
            self.sets(assign_attrs)

    @classmethod
    def model_field(cls, name: str):
        """
        :param name:
        :return:
        """
        for k, v in cls.__fields__.items():
            if k != name:
                continue
            return v

    @classmethod
    def find_model_field(cls, loc: tuple):
        """
        """
        base_model = cls
        index = 0
        model_field = None
        for name in loc:
            if str(name).isdigit():
                index = int(str(name))
                continue

            model_field = base_model.model_field(name)
            if not model_field:
                break
            if is_generic_type(model_field):
                for v in model_field.sub_fields:
                    if not is_base_model(v):
                        continue
                    base_model = v.type_
            elif is_base_model(model_field):
                base_model = model_field.type_

        return model_field, index

    @classmethod
    def model_fields(cls, *args):
        """
        :param args:
        :return:
        """
        model_fields = []
        for arg in args:
            model_field = cls.model_field(arg)
            if not model_field:
                continue
            model_fields.append(model_field)

        return model_fields

    def sets(self, elements: Union[dict, BaseModel_]):
        """ 批量设置对象元素(dict)
        :param elements:
        :return:
        """
        if isinstance(elements, BaseModel_):
            elements = elements.dict()

        for k, v in elements.items():
            if not hasattr(self, k):
                continue

            model_field = self.__class__.model_field(k)
            if not model_field:
                continue

            # 泛型
            if is_generic_type(model_field):
                _instances = []

                _class = None
                for sub_field in model_field.sub_fields:
                    if not is_base_model(sub_field):
                        continue
                    _class = sub_field.type_

                if not _class:
                    continue

                if model_field.outer_type_.__origin__ is list:
                    for _v in v:
                        _instance = _class()
                        _instance.sets(_v)
                        _instances.append(_instance)

                    setattr(self, k, _instances)
                elif model_field.outer_type_.__origin__ is dict:

                    _instance = _class()
                    _instance.sets(v)

                    setattr(self, k, _instance)
                else:
                    setattr(self, k, v)
            #  callable(_model_field.type_) 是为了过滤typing.Union的场景
            elif is_base_model(model_field):
                _instance = model_field.type_()
                _instance.sets(v)
                setattr(self, k, _instance)
            else:
                setattr(self, k, v)

    def dict(self, *args, **kwargs) -> dict:
        """ 扩展dict功能
        :param args:
        :param kwargs:
        :return:
        """
        result = super(BaseModel, self).dict(*args, **kwargs)

        def _convert_enum(value: Union[list, dict]):
            """
            :param value:
            :return:
            """
            if isinstance(value, list):
                for idx, v in enumerate(value):
                    if isinstance(v, Enum):
                        value[idx] = v.value
                    elif isinstance(v, (list, dict)):
                        _convert_enum(v)

            elif isinstance(value, dict):
                for k, v in value.items():
                    # 支持枚举类型
                    if isinstance(v, Enum):
                        v = v.value
                    elif isinstance(v, (list, dict)):
                        _convert_enum(v)

                    value[k] = v

        _convert_enum(result)

        return result



