import os
import ctypes
import time
from pathlib import Path
from loguru import logger
import ctypes
from ctypes import *

# 获取当前文件所在的目录
current_dir = Path(__file__).resolve().parent

# 加载 DLL 文件



# 封装 DLL 函数
class vb:
    def __init__(self):
        self.dll = self.get_dll("vbSfr.dll")

    def get_dll(self, file_name):
        dll_folder = current_dir / 'dlls/VB'
        if not dll_folder.exists():
            raise FileNotFoundError(f"Could not find DLL folder at {dll_folder}")

        # 使用 os.add_dll_directory 添加路径
        old_path = os.environ.get('PATH', '')

        # 添加新的 DLL 文件夹路径到 PATH
        os.environ['PATH'] = f"{str(dll_folder)}{os.pathsep}{old_path}"

        dll_path = current_dir / 'dlls/VB' / file_name

        if not dll_path.exists():
            raise FileNotFoundError(f"Could not find DLL file at {dll_path}")

        # 加载 DLL
        logger.info(f"加载: {str(dll_path)}")
        my_custom_dll = ctypes.CDLL(str(dll_path))
        return my_custom_dll
    def dirty_test(self, raw_path, width, height):
        getVbSfrNearC = self.dll.getVbDerityResultC
        getVbSfrNearC.restype = c_int
        getVbSfrNearC.argtypes = [c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_char))), POINTER(c_int), c_int, c_int]

        freeStringArray = self.dll.freeStringArray
        freeStringArray.restype = None
        freeStringArray.argtypes = [POINTER(c_char_p), c_int]


        count = c_int(0)
        # dataList = POINTER(c_char_p)()
        dataList = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))()

        result = getVbSfrNearC(raw_path.encode('utf-8'), byref(dataList), byref(count), width, height)
        python_dataList = [dataList[i].decode('utf-8') for i in range(count.value)]


        print(f"返回结果: {result}")
        print(f"数据列表: {python_dataList}")

        # if dataList:
        freeStringArray(dataList, count.value)

        python_dataList = []

        if result == 0 and count.value > 0:
            for i in range(count.value):
                xx = ctypes.string_at(dataList[i]).decode('utf-8')
                python_dataList.append(xx)

            logger.info(f"python_dataList2: {python_dataList}")


        # 释放内存

        if dataList and count.value > 0:
            # 解引用 dataList 以获取 char** 类型的指针
            data_ptr = ctypes.cast(dataList, ctypes.POINTER(ctypes.c_char_p))
            self.dll.freeStringArray(data_ptr, count.value)
            logger.info("Free datalist")


        return result, python_dataList



class iac3:
    def __init__(self):
        self.sfr_dll = self.get_dll("iacSfr.dll")
        self.stray_light_detect_dll = self.get_dll( "StrayLightDetectAlg.dll")

    def get_dll(self, file_name):

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

    def stray_light_detect(self, jpg_path, width, height, type):
        jpg_path = ctypes.create_string_buffer(jpg_path.encode('gbk'))

        class LightResult(ctypes.Structure):
            _fields_ = [
                ("m_Result", ctypes.c_float),
                ("m_Cx", ctypes.c_int),
                ("m_Cy", ctypes.c_int),
                ("m_halo", ctypes.c_float),
                ("m_Longphotospine", ctypes.c_float),
                ("m_Numphotospine", ctypes.c_float),
                ("m_Luxphotospine", ctypes.c_float)
            ]

        my_result = LightResult()
        logger.info("运行光刺算法中")
        logger.info(f"jpg_path: {jpg_path}")
        light_flag = self.stray_light_detect_dll.StrayLightDetectAlg(jpg_path, width, height,
                                             type, ctypes.byref(my_result))
        logger.info(
            f"光刺 SDK返回值: {light_flag};算法返回结果：{my_result.m_Result}, 坐标【{my_result.m_Cx}， {my_result.m_Cy}】，其他参数：{my_result.m_halo, my_result.m_Longphotospine, my_result.m_Numphotospine, my_result.m_Luxphotospine}")
        return light_flag, my_result

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
        getIAC3RawPathC.argtypes = [c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_char))), POINTER(c_int), c_char_p, c_char_p]

        freeStringArray = self.sfr_dll.freeStringArray
        freeStringArray.restype = None
        freeStringArray.argtypes = [POINTER(c_char_p), c_int]

        count = c_int(0)
        # dataList = POINTER(c_char_p)()
        dataList = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))()
        result = getIAC3RawPathC(raw_path.encode('utf-8'), byref(dataList), byref(count), result_log.encode('utf-8'),
                                 raw_type.encode('utf-8'))
        logger.info(f"SFR SDK返回值: {result}")
        python_dataList2 = []
        python_dataList4 = []
        python_dataListX = []
        if result == 0 and count.value > 0:
            for i in range(count.value):
                xx = ctypes.string_at(dataList[i]).decode('utf-8')
                mm = xx.strip(";")
                # xx = xx.strip(";")
                print(type(xx))

                mm = [part.strip() for part in xx.split(';')]
                print(mm)
                python_dataList2.append(mm[0])
                python_dataList4.append(mm[1])
                python_dataListX.append(mm[2])
            logger.info(f"python_dataList2: {python_dataList2}")
            logger.info(f"python_dataList4: {python_dataList4}")
            logger.info(f"python_dataListX: {python_dataListX}")

        # 释放内存

        if dataList and count.value > 0:
            # 解引用 dataList 以获取 char** 类型的指针
            data_ptr = ctypes.cast(dataList, ctypes.POINTER(ctypes.c_char_p))
            self.sfr_dll.freeStringArray(data_ptr, count.value)
            logger.info("Free datalist")

        # python_dataList = [dataList[i].decode('utf-8') for i in range(count.value)]
        # # if dataList:
        # freeStringArray(dataList, count.value)
        # logger.info(f"数据列表: {python_dataList}")
        return result, python_dataList2, python_dataList4, python_dataListX



