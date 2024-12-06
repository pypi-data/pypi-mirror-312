import os
import ctypes
from pathlib import Path
from loguru import logger
import ctypes
from ctypes import *

# 获取当前文件所在的目录
current_dir = Path(__file__).resolve().parent

# 加载 DLL 文件


def get_dll(project, file_name):
    dll_folder = current_dir / 'dlls'
    if not dll_folder.exists():
        raise FileNotFoundError(f"Could not find DLL folder at {dll_folder}")

    # 使用 os.add_dll_directory 添加路径
    old_path = os.environ.get('PATH', '')

    # 添加新的 DLL 文件夹路径到 PATH
    os.environ['PATH'] = f"{str(dll_folder)}{os.pathsep}{old_path}"
    if project == "vb":
        dll_path = current_dir / 'dlls' / file_name

        if not dll_path.exists():
            raise FileNotFoundError(f"Could not find DLL file at {dll_path}")

        # 加载 DLL
        my_custom_dll = ctypes.CDLL(str(dll_path))
        return my_custom_dll
    elif project == "iac3":
        dll_folder = current_dir / 'dlls/iac3'
        dll_path = current_dir / 'dlls/iac3' / file_name
        if not dll_folder.exists():
            raise FileNotFoundError(f"Could not find DLL folder at {dll_folder}")

        # 使用 os.add_dll_directory 添加路径
        old_path = os.environ.get('PATH', '')

        # 添加新的 DLL 文件夹路径到 PATH
        os.environ['PATH'] = f"{str(dll_folder)}{os.pathsep}{old_path}"
        if not dll_path.exists():
            raise FileNotFoundError(f"Could not find DLL file at {dll_path}")

        # 加载 DLL
        my_custom_dll = ctypes.CDLL(str(dll_path))
        return my_custom_dll
# 封装 DLL 函数
class vb:
    def __init__(self):
        self.dll = get_dll("vb", "vbSfr.dll")

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

class iac3:
    def __init__(self):
        self.sfr_dll = get_dll("iac3", "iacSfr.dll")
        self.stray_light_detect_dll = get_dll("iac3", "StrayLightDetectAlg.dll")

    def sfr_test(self, far_input_data, near_input_data, width, height, raw_path, raw_type, result_log, ny = 4):

        # 输入标准值
        self.sfr_dll.inputData.argtypes = [ctypes.c_int] * 8
        self.sfr_dll.inputData.restype = None
        self.sfr_dll.inputData(near_input_data[0], near_input_data[1], near_input_data[2], near_input_data[3],
                               far_input_data[0], far_input_data[1], far_input_data[2], far_input_data[3])

        # logger.info(f"输入标准值：({self._config['size'][0]}, {self._config['size'][1]})")

        logger.info(
            f"输入标准值：({width}, {height}, {ny})")  ##['size'][3]中“4”代表在刀口4分之一出找

        # 输入裁剪的分辨率
        self.sfr_dll.inputResolution.argtypes = [ctypes.c_int] * 3
        self.sfr_dll.inputResolution.restype = None
        self.sfr_dll.inputResolution(width, height, ny)

        getIAC3RawPathC = self.sfr_dll.getIAC3RawPathC
        getIAC3RawPathC.restype = c_int
        getIAC3RawPathC.argtypes = [c_char_p, POINTER(POINTER(c_char_p)), POINTER(c_int), c_char_p, c_char_p]

        freeStringArray = self.sfr_dll.freeStringArray
        freeStringArray.restype = None
        freeStringArray.argtypes = [POINTER(c_char_p), c_int]

        count = c_int()
        dataList = POINTER(c_char_p)()

        result = getIAC3RawPathC(raw_path.encode('gbk'), byref(dataList), byref(count), result_log.encode('gbk'),
                                 raw_type.encode('gbk'))
        logger.info(f"SFR SDK返回值: {result}")
        python_dataList = [dataList[i].decode('gbk') for i in range(count.value)]
        if dataList:
            freeStringArray(dataList, count.value)
        print(f"数据列表: {python_dataList}")
        return result, python_dataList