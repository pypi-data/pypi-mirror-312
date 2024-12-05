from ctypes import *
import os, time
# os.add_dll_directory(r"D:\desktop-dev\go3se-host\project\TC2\sfr")
def get_dll_ret(path):
    mydll = WinDLL(path)

    pic = "E:\\far_unpack.raw"
    pic = c_char_p(bytes(pic, "gbk"))
    print(pic)
    res_file = c_char_p(bytes("E://sfr.log", "gbk"))
    a = mydll.GetFarRet(pic, res_file)
    print("*" * 20)
    print(a)

if __name__ == '__main__':
    path = ""
    get_dll_ret()