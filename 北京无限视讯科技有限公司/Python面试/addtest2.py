import ctypes

dll_path = "add.dll"  # 定义DLL文件路径
dll = ctypes.CDLL(dll_path)  # 加载DLL文件

function_name = "dlltest2"
function = getattr(dll, function_name)  # 查找函数地址

function.argtypes = [ctypes.c_int, ctypes.c_int]  # 设置函数参数和返回类型
function.restype = ctypes.c_int

# 调用函数

print(f"addtest2(23, 4)结果为{function(23, 4)}")
print(f"addtest2(4, 23)结果为{function(4, 23)}")
print(f"addtest2(16, 5)结果为{function(16, 5)}")
print(f"addtest2(5, 16)结果为{function(5, 16)}")

print(f"addtest2(0, 1)结果为{function(0, 1)}")
print(f"addtest2(1, 0)结果为{function(1, 0)}")
print(f"addtest2(6, 7)结果为{function(6, 7)}")
print(f"addtest2(7, 6)结果为{function(7, 6)}")

print(f"addtest2(23, 58)结果为{function(23, 58)}")
print(f"addtest2(58, 23)结果为{function(58, 23)}")
