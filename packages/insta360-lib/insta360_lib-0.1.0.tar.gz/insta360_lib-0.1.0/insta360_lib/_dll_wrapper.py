import os
import ctypes
from pathlib import Path
from loguru import logger
import ctypes
from ctypes import *

# 获取当前文件所在的目录
current_dir = Path(__file__).resolve().parent

# 加载 DLL 文件


def get_dll(file_name):
    dll_folder = current_dir / 'dlls'
    dll_path = current_dir / 'dlls' / file_name
    if not dll_folder.exists():
        raise FileNotFoundError(f"Could not find DLL folder at {dll_folder}")

    # 使用 os.add_dll_directory 添加路径
    os.add_dll_directory(str(dll_folder))
    if not dll_path.exists():
        raise FileNotFoundError(f"Could not find DLL file at {dll_path}")

    # 加载 DLL
    my_custom_dll = ctypes.CDLL(str(dll_path))
    return my_custom_dll
# 封装 DLL 函数
class vb:
    def __init__(self):
        self.dll = get_dll("vb.dll")

    def dirty_test(self, raw_path, width, height):
        getVbSfrNearC = self.dll.getVbDerityResultC
        getVbSfrNearC.restype = c_int
        getVbSfrNearC.argtypes = [c_char_p, POINTER(POINTER(c_char_p)), POINTER(c_int), c_int, c_int]

        freeStringArray = self.dll.freeStringArray
        freeStringArray.restype = None
        freeStringArray.argtypes = [POINTER(c_char_p), c_int]

        count = c_int()
        dataList = POINTER(c_char_p)()
        result = getVbSfrNearC(raw_path.encode('utf-8'), byref(dataList), byref(count), width, height)
        python_dataList = [dataList[i].decode('utf-8') for i in range(count.value)]
        freeStringArray(dataList, count.value)

        print(f"返回结果: {result}")
        print(f"数据列表: {python_dataList}")

        return result, python_dataList