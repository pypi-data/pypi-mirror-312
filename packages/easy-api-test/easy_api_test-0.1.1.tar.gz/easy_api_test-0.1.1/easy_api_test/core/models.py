import re
from typing import Any, Self, Sequence, Type, get_type_hints, Union, get_origin, get_args, TypeVar
from collections.abc import Iterable
import types

T = TypeVar('T', bound='Model')  # 用于泛型约束

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs, readonly=False):
        # 收集类的注解和默认值
        annotations = {}
        defaults = {}
        
        # 从基类继承注解和默认值
        for base in bases:
            if hasattr(base, '__annotations__'):
                annotations.update(base.__annotations__)
            if hasattr(base, '__default__'):
                defaults.update(base.__default__)
        
        # 更新当前类的注解和默认值
        if '__annotations__' in attrs:
            annotations.update(attrs['__annotations__'])
        
        # 设置类属性
        attrs['__annotations__'] = annotations
        attrs['__annotations__'].pop('__show__', None)
        attrs['__default__'] = defaults
        attrs['__readonly__'] = readonly
        
        return super().__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):
    __show__: str | Sequence[str] | None = None
    
    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """将字典转换为模型对象"""
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data)}")
            
        converted_data = {}
        for key, value in data.items():
            # 递归处理嵌套的数据结构
            if isinstance(value, dict):
                converted_data[key] = cls.from_dict(value)
            elif isinstance(value, list):
                converted_data[key] = cls.from_list(value)
            else:
                converted_data[key] = value
        return cls(**converted_data)
    
    @classmethod
    def from_list(cls: Type[T], data: list) -> list[Union[T, list, Any]]:
        """将列表转换为模型对象列表"""
        if not isinstance(data, list):
            raise ValueError(f"Expected list, got {type(data)}")
            
        return [
            cls.from_dict(item) if isinstance(item, dict)
            else cls.from_list(item) if isinstance(item, list)
            else item
            for item in data
        ]
    
    def __init__(self, **kwargs):
        super().__init__()
        readonly, self.__readonly__ = self.__readonly__, False
        
        # 直接保存所有字段，包括额外字段
        for key, value in kwargs.items():
            self[key] = value
            
        self.__readonly__ = readonly
    
    def __getattr__(self, key: str) -> Any:
        """支持通过属性方式访问字段"""
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __str__(self):
        show = self.__show__
        if not show:
            show = list(self.keys())  # 显示所有字段
        if isinstance(show, str):
            show = re.split(r'[,\s]+', show.strip())
        val = ', '.join(f"{key}={self[key]!r}" for key in show if key in self)
        return f'{self.__class__.__name__}({val})'

    __repr__ = __str__



if __name__ == "__main__":
    pass