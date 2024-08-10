import ctypes

dll_path = "add.dll"  # 定义DLL文件路径
dll = ctypes.CDLL(dll_path)  # 加载DLL文件

function_name = "dlltest1"
function = getattr(dll, function_name)  # 查找函数地址

function.argtypes = [ctypes.c_int, ctypes.c_int]  # 设置函数参数和返回类型
function.restype = ctypes.c_int

# 调用函数

print(f"function(3, 4)结果为{function(3, 4)}")
print(f"function(3, 5)结果为{function(3, 5)}")
print(f"function(3, 6)结果为{function(3, 6)}")
print(f"function(4, 4)结果为{function(4, 4)}")
print(f"function(5, 4)结果为{function(4, 5)}")
print(f"function(6, 4)结果为{function(4, 6)}")

print(f"function(1, 1)结果为{function(1, 1)}")
print(f"function(2, 2)结果为{function(2, 2)}")
print(f"function(3, 3)结果为{function(3, 3)}")

print(f"function(-1, -1)结果为{function(-1, -1)}")
print(f"function(0, 1)结果为{function(0, 1)}")
