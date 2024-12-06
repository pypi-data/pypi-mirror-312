from typing import Any, Generic, TypeVar, get_type_hints, List, Dict, Union, Optional
from datetime import datetime, date, time
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
import ctypes

T = TypeVar('T')

class PyGoBaseInput(BaseModel):
    """所有Go函数输入参数的基类"""
    
    def to_c_args(self) -> list:
        """将Pydantic模型转换为C参数列表"""
        values = []
        for field_name in self.model_fields:
            value = getattr(self, field_name)
            if value is None:
                values.append(None)
                continue
                
            field_type = self.model_fields[field_name].annotation
            base_type = self.__class__._get_base_type(field_type)
            
            converted_value = self._convert_value_to_c(value, base_type)
            values.append(converted_value)
            
        return values
    
    def _convert_value_to_c(self, value: Any, type_hint: Any) -> Any:
        """将Python值转换为C值"""
        if type_hint in self._basic_type_converters:
            return self._basic_type_converters[type_hint](value)
            
        if hasattr(type_hint, "__origin__"):
            origin = type_hint.__origin__
            if origin in (list, List):
                item_type = type_hint.__args__[0]
                return [self._convert_value_to_c(item, item_type) for item in value]
            elif origin in (dict, Dict):
                key_type, value_type = type_hint.__args__
                return {
                    self._convert_value_to_c(k, key_type): self._convert_value_to_c(v, value_type)
                    for k, v in value.items()
                }
            elif origin in (Union, Optional):
                if value is None:
                    return None
                non_none_type = next(t for t in type_hint.__args__ if t != type(None))
                return self._convert_value_to_c(value, non_none_type)
                
        raise ValueError(f"Unsupported type {type_hint}")
    
    @classmethod
    def _get_base_type(cls, type_hint: Any) -> Any:
        """获取类型的基础类型（处理Optional等包装类型）"""
        if hasattr(type_hint, "__origin__"):
            if type_hint.__origin__ in (Union, Optional):
                return next(t for t in type_hint.__args__ if t != type(None))
        return type_hint
    
    @property
    def _basic_type_converters(self) -> Dict[Any, callable]:
        """基础类型转换器映射"""
        return {
            str: lambda x: x.encode('utf-8'),
            int: lambda x: x,
            float: lambda x: x,
            Decimal: lambda x: float(x),
            bool: lambda x: bool(x),
            datetime: lambda x: x.isoformat().encode('utf-8'),
            date: lambda x: x.isoformat().encode('utf-8'),
            time: lambda x: x.isoformat().encode('utf-8'),
            UUID: lambda x: str(x).encode('utf-8'),
            bytes: lambda x: x,
            bytearray: lambda x: bytes(x),
        }
    
    @classmethod
    def c_arg_types(cls) -> list:
        """返回C参数类型列表"""
        types = []
        for field_name, field in cls.model_fields.items():
            field_type = field.annotation
            base_type = cls._get_base_type(field_type)
            c_type = cls._get_c_type(base_type)
            types.append(c_type)
        return types
    
    @classmethod
    def _get_c_type(cls, type_hint: Any) -> Any:
        """获取对应的C类型"""
        type_mapping = {
            str: ctypes.c_char_p,
            int: ctypes.c_int64,
            float: ctypes.c_double,
            Decimal: ctypes.c_double,
            bool: ctypes.c_bool,
            datetime: ctypes.c_char_p,
            date: ctypes.c_char_p,
            time: ctypes.c_char_p,
            UUID: ctypes.c_char_p,
            bytes: ctypes.c_char_p,
            bytearray: ctypes.c_char_p,
            type(None): ctypes.c_void_p,
        }
        
        if hasattr(type_hint, "__origin__"):
            origin = type_hint.__origin__
            if origin in (list, List):
                return ctypes.POINTER(cls._get_c_type(type_hint.__args__[0]))
            elif origin in (dict, Dict):
                return ctypes.c_char_p
            elif origin in (Union, Optional):
                non_none_type = next(t for t in type_hint.__args__ if t != type(None))
                return cls._get_c_type(non_none_type)
        
        if type_hint in type_mapping:
            return type_mapping[type_hint]
            
        raise ValueError(f"Unsupported type {type_hint}")

    class Config:
        """Pydantic配置"""
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            time: lambda v: v.isoformat(),
            UUID: str,
            bytes: lambda v: v.decode(),
            bytearray: lambda v: bytes(v).decode(),
        }

class GoResponse(BaseModel):
    """Go函数返回的标准响应结构"""
    status: str = Field(description="状态: succeed/failed")
    code: int = Field(description="状态码: 200成功,400参数错误,500内部错误")
    msg: str = Field(description="提示信息")
    data: Any = Field(description="实际数据")
    timing: int = Field(description="执行耗时(毫秒)")
    
    def is_success(self) -> bool:
        return self.status == 'succeed' and self.code == 200
    
    class Config:
        str_strip_whitespace = True
        arbitrary_types_allowed = True

class ExportExcelInput(PyGoBaseInput):
    """导出Excel的输入参数"""
    channel_code: str
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = "hashchat"
    database: str = "llx"
    worker_count: int = 500

class NewFunctionInput(PyGoBaseInput):
    """新函数的输入参数"""
    param1: str
    param2: int 