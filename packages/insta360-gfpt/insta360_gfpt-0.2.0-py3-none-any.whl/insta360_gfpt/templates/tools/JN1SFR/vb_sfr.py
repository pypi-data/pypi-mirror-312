import ctypes
from ctypes import *

# Load the DLL
vbsfr_sdk = ctypes.CDLL('vbSfr.dll')

# Define the restype and argtypes for the getVbSfrNearC function
getVbSfrNearC = vbsfr_sdk.getVbSfrNearC
getVbSfrNearC.restype = c_int
getVbSfrNearC.argtypes = [c_char_p, POINTER(POINTER(c_char_p)), POINTER(c_int), c_int, c_int]

getVbSfrFarC = vbsfr_sdk.getVbSfrFarC
getVbSfrFarC.restype = c_int
getVbSfrFarC.argtypes = [c_char_p, POINTER(POINTER(c_char_p)), POINTER(c_int), c_int, c_int]

# Define the restype and argtypes for the freeStringArray function
freeStringArray = vbsfr_sdk.freeStringArray
freeStringArray.restype = None
freeStringArray.argtypes = [POINTER(c_char_p), c_int]

# Call the function and handle the pointers
raw_path = b"C:\\Users\\HFY\\Downloads\\004B3832391500002A1C000001000202_AutoFocusFar_LXSFR_far-3264-2448-GBRG.raw"
count = c_int()
count2 = c_int()
dataList = POINTER(c_char_p)()
dataList2 = POINTER(c_char_p)()
result = getVbSfrNearC(raw_path, byref(dataList), byref(count), 3264, 2448)
result2 = getVbSfrFarC(raw_path, byref(dataList2), byref(count2), 3264, 2448)
# Convert the array of strings to a Python list
python_dataList = [dataList[i].decode('utf-8') for i in range(count.value)]
python_dataList2 = [dataList2[i].decode('utf-8') for i in range(count2.value)]

# Free the allocated memory by the DLL
freeStringArray(dataList, count.value)
freeStringArray(dataList2, count.value)

for i in python_dataList:
    print(i)
print(type(python_dataList))
print(python_dataList2)