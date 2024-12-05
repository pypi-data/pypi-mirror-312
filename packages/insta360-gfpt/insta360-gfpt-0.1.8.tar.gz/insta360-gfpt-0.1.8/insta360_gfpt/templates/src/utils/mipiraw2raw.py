import os
import numpy as np
import argparse
import time
import cv2

global COLOR_BayerGB2BGR, COLOR_BayerRG2BGR, COLOR_BayerGR2BGR, COLOR_BayerBG2BGR
global bayer_order_maps

COLOR_BayerBG2BGR = 46
COLOR_BayerGB2BGR = 47
COLOR_BayerRG2BGR = 48
COLOR_BayerGR2BGR = 49

bayer_order_maps = {
    "bayer_bg": COLOR_BayerBG2BGR,
    "bayer_gb": COLOR_BayerGB2BGR,
    "bayer_rg": COLOR_BayerRG2BGR,
    "bayer_gr": COLOR_BayerGR2BGR,
    "gray": 0,
}
class mipiraw2raw:


    def unpack_mipi_raw10(self, byte_buf):
        data = np.frombuffer(byte_buf, dtype=np.uint8)
        # 5 bytes contain 4 10-bit pixels (5x8 == 4x10)
        b1, b2, b3, b4, b5 = np.reshape(
            data, (data.shape[0]//5, 5)).astype(np.uint16).T
        p1 = (b1 << 2) + ((b5) & 0x3)
        p2 = (b2 << 2) + ((b5 >> 2) & 0x3)
        p3 = (b3 << 2) + ((b5 >> 4) & 0x3)
        p4 = (b4 << 2) + ((b5 >> 6) & 0x3)
        unpacked = np.reshape(np.concatenate(
            (p1[:, None], p2[:, None], p3[:, None], p4[:, None]), axis=1),  4*p1.shape[0])
        return unpacked


    def unpack_mipi_raw12(self, byte_buf):
        data = np.frombuffer(byte_buf, dtype=np.uint8)
        # 5 bytes contain 4 10-bit pixels (5x8 == 4x10)
        b1, b2, b3 = np.reshape(
            data, (data.shape[0]//3, 3)).astype(np.uint16).T
        p1 = (b1 << 4) + ((b3) & 0xf)
        p2 = (b2 << 4) + ((b3 >> 4) & 0xf)
        unpacked = np.reshape(np.concatenate(
            (p1[:, None], p2[:, None]), axis=1),  2*p1.shape[0])
        return unpacked


    def unpack_mipi_raw14(self, byte_buf):
        data = np.frombuffer(byte_buf, dtype=np.uint8)
        # 5 bytes contain 4 10-bit pixels (5x8 == 4x10)
        b1, b2, b3, b4, b5, b6, b7 = np.reshape(
            data, (data.shape[0]//7, 7)).astype(np.uint16).T
        p1 = (b1 << 6) + (b5 & 0x3f)
        p2 = (b2 << 6) + (b5 >> 6) + (b6 & 0xf)
        p3 = (b3 << 6) + (b6 >> 4) + (b7 & 0x3)
        p4 = (b4 << 6) + (b7 >> 2)
        unpacked = np.reshape(np.concatenate(
            (p1[:, None], p2[:, None], p3[:, None], p4[:, None]), axis=1),  4*p1.shape[0])
        return unpacked


    def convertMipi2Raw(self, mipiFile, imgWidth, imgHeight, bitDeepth, bayer_order):
        global bayerData, img
        mipiData = np.fromfile(mipiFile, dtype='uint8')
        print("mipiraw file size:", mipiData.size)

        if bitDeepth == 16:
            print("raw8 and raw16 no need to unpack")
            mipiData = np.fromfile(mipiFile, dtype='uint16')
            img = np.frombuffer(mipiData, dtype=np.uint16)
            print('Array size before reshaping:', img.size)
            print('Desired reshaped array size:', imgHeight * imgWidth * 1)
            img = img.astype(np.uint16).reshape(imgHeight, imgWidth, 1)
            rgbimg = cv2.cvtColor(img, cv2.COLOR_BayerGR2BGR)
            cv2.imwrite(mipiFile[:-4] + '.jpg', rgbimg)
            return True
        elif bitDeepth == 8:
            print("raw8 and raw16 no need to unpack")
            mipiData = np.fromfile(mipiFile, dtype='uint8')
            img = np.frombuffer(mipiData, dtype=np.uint8)
            print('Array size before reshaping:', img.size)
            print('Desired reshaped array size:', imgHeight * imgWidth * 1)
            img = img.astype(np.uint16).reshape(imgHeight, imgWidth, 1)
            rgbimg = cv2.cvtColor(img, cv2.COLOR_BayerGR2BGR)
            cv2.imwrite(mipiFile[:-4] + '.jpg', rgbimg)
            return True
        elif bitDeepth == 10:
            # raw10
            bayerData = self.unpack_mipi_raw10(mipiData)
            img = bayerData >> 2
        elif bitDeepth == 12:
            # raw12
            bayerData = self.unpack_mipi_raw12(mipiData)
            img = bayerData >> 4
        elif bitDeepth == 14:
            # raw14
            bayerData = self.unpack_mipi_raw14(mipiData)
            img = bayerData >> 6
        else:
            print("unsupport bayer bitDeepth:", bitDeepth)

        try:
            bayerData.tofile(mipiFile[:-4]+'_raw16.raw')

            img = img.astype(np.uint8).reshape(imgHeight, imgWidth, 1)
            rgbimg = cv2.cvtColor(img, cv2.COLOR_BayerRG2BGR)
            cv2.imwrite(mipiFile[:-4]+'.jpg', rgbimg)
            return True
        except:
            return False

    def ProcSingleFile(self,rawFile, img_width, img_height, rawDepth, bayer_order):
        # (path, rawFile) = os.path.split(raw_name)
        print("process ", rawFile, "...")
        start_time = time.monotonic_ns()
        result = self.convertMipi2Raw(rawFile, img_width, img_height, rawDepth, bayer_order)
        end_time = time.monotonic_ns()
        print("convertMipi2Raw cost:",
              (end_time - start_time) // 1000000, 'ms')
        return result


    def ProcPath(self, path, img_width, img_height, rawDepth, bayer_order):
        file_list = os.listdir(path)
        for f in file_list:
            f_lower = f.lower()
            if f_lower.endswith('.raw'):
                raw_name = '%s\%s' % (path, f)
                self.ProcSingleFile(raw_name, img_width, img_height,
                               rawDepth, bayer_order)


if "__main__" == __name__:
    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument(
    #     "--path", help="input raw path", required=False, type=str)
    # parser.add_argument(
    #     "--file", help="input raw file name", required=False, type=str)
    # parser.add_argument("--width", help="raw image width",
    #                     required=True, type=int)
    # parser.add_argument("--height", help="raw image height",
    #                     required=True, type=int)
    # parser.add_argument(
    #     "--depth", help="raw image depth [8, 10, 12, 14, 16]", required=True, type=int)
    # parser.add_argument(
    #     "--bayer", help="bayer format [bayer_bg, bayer_rg, bayer_gb, bayer_gr]", required=True, type=str)
    #
    # args = parser.parse_args()
    #
    # rawPath = args.path
    # rawFile = args.file
    # img_width = args.width
    # img_height = args.height
    # rawDepth = args.depth
    # bayer = args.bayer
    # bayer_order = bayer_order_maps[bayer.lower()]

    rawFile = r"C:\Users\HFY\Downloads\near.raw"
    rawPath = None
    img_width = 3840
    img_height = 2160
    rawDepth = 10
    bayer = "bayer_gr"
    bayer_order = bayer_order_maps[bayer.lower()]
    xx = mipiraw2raw()
    if rawPath is not None:
        xx.ProcPath(rawPath, img_width, img_height, rawDepth, bayer_order)
    elif rawFile is not None:
        xx.ProcSingleFile(rawFile, img_width, img_height, rawDepth, bayer_order)
    else:
        print("parameters wrong!!! no path or file")