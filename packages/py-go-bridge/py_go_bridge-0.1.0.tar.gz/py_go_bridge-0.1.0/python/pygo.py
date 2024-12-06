import ctypes
import json
import os
from typing import TypeVar, Type, Generic, Any
from models import PyGoBaseInput, GoResponse

T = TypeVar('T', bound=PyGoBaseInput)

class PyGo:
    def __init__(self, lib_path: str):
        """初始化PyGo实例
        
        Args:
            lib_path: .so文件的完整路径
            
        Raises:
            ValueError: 当lib_path为空或.so文件不存在时
            OSError: 当加载.so文件失败时
        """
        if not lib_path:
            raise ValueError("lib_path must be specified")
            
        if not os.path.exists(lib_path):
            raise ValueError(f"Shared library not found: {lib_path}")
            
        if not lib_path.endswith('.so'):
            raise ValueError(f"Invalid shared library file: {lib_path} (must end with .so)")
            
        try:
            self.lib = ctypes.CDLL(lib_path)
        except OSError as e:
            raise OSError(f"Failed to load shared library {lib_path}: {str(e)}")
            
        self._init_free_string()
    
    def _init_free_string(self):
        """初始化FreeString函数"""
        self.lib.FreeString.argtypes = [ctypes.POINTER(ctypes.c_char)]
        self.lib.FreeString.restype = None
    
    def _setup_function(self, func_name: str, input_model: Type[PyGoBaseInput]):
        """设置Go函数的参数类型和返回类型"""
        func = getattr(self.lib, func_name)
        func.restype = ctypes.POINTER(ctypes.c_char)
        
        argtypes = input_model.c_arg_types()
        if not argtypes:
            raise ValueError(f"No argument types defined for {func_name}")
        func.argtypes = argtypes
        return func
    
    def _handle_result(self, result_ptr) -> GoResponse:
        """处理C函数返回的结果"""
        try:
            if not result_ptr:
                return GoResponse(
                    status="failed",
                    code=500,
                    msg="Null result from Go function",
                    data=None,
                    timing=0
                )
            
            result_bytes = ctypes.cast(result_ptr, ctypes.c_char_p).value
            if not result_bytes:
                return GoResponse(
                    status="failed",
                    code=500,
                    msg="Empty result from Go function",
                    data=None,
                    timing=0
                )
                
            json_str = result_bytes.decode('utf-8')
            return GoResponse.parse_raw(json_str)
            
        finally:
            if result_ptr:
                self.lib.FreeString(result_ptr)
    
    def call_go_function(self, func_name: str, input_data: PyGoBaseInput) -> GoResponse:
        """通用的Go函数调用方法"""
        try:
            func = self._setup_function(func_name, input_data.__class__)
            c_args = input_data.to_c_args()
            if not c_args:
                raise ValueError(f"No arguments provided for {func_name}")
            result_ptr = func(*c_args)
            return self._handle_result(result_ptr)
            
        except Exception as e:
            return GoResponse(
                status="failed",
                code=500,
                msg=str(e),
                data=None,
                timing=0
            )
    
    def __getattr__(self, name: str) -> Any:
        """动态处理所有函数调用"""
        def wrapper(input_data: PyGoBaseInput) -> GoResponse:
            # 将Python的snake_case转换为Go的PascalCase
            go_func_name = ''.join(word.capitalize() for word in name.split('_'))
            return self.call_go_function(go_func_name, input_data)
        return wrapper

def main():
    pygo = PyGo()
    
    # 测试新函数 - 可以使用snake_case命名
    from models import NewFunctionInput
    input_data = NewFunctionInput(
        param1="hello",
        param2=123
    )
    result = pygo.new_function(input_data)  # 或者 pygo.NewFunction(input_data)
    print("New Function Result:")
    print(result)
    print()

    # 测试导出Excel
    # from models import ExportExcelInput
    # input_data = ExportExcelInput(
    #     channel_code="cobazaar",
    #     host="localhost",
    #     port=3306,
    #     user="root",
    #     password="hashchat",
    #     database="llx",
    #     worker_count=16
    # )
    # result = pygo.export_excel(input_data)  # 或者 pygo.ExportExcel(input_data)
    # print("Export Excel Result:")
    # print(result)
    # print()

if __name__ == "__main__":
    main()