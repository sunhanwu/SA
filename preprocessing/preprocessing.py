import os
import sys
import numpy as np
import binascii
from PIL import Image

def pcap2png(pcap_path:str, png_path:str, png_size=28):
    """
    将pcap转化为png图片
    pcap_path: pcap文件路径
    png_path: 目标png文件路径
    """    
    with open(pcap_path, 'rb') as f:
        data = f.read()
    data = [int(x) for x in data]
    data = np.array(data)
    img_array = np.reshape(data, (png_size, png_size))
    img_array = np.uint8(img_array)
    img = Image.fromarray(img_array)
    img.save(png_path)


if __name__ == '__main__':
    pcap2png('./test.bin', './test.png')
