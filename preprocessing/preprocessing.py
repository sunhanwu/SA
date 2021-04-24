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

def precessingTrain(trainDataPath, T='a', length=784, top_num=1000):
    """
    预处理训练数据
    trainDataPath: 训练数据位置
    T: 预处理的格式，a表示保留所有层，7表示只保留应用层
    """
    assert T in ['a', '7']
    if T == 'a':
        session_type = 'AllLayers'
    else:
        session_type = 'L7'
    for week in os.listdir(trainDataPath):
        week_path = os.path.join(trainDataPath, week)
        for day in os.listdir(week_path):
            day_path = os.path.join(week_path, day)
            flow_path = os.path.join(day_path, 'flow')
            format_data_path = os.path.join(day_path, str(length))
            tcpdmp = "{}/tcpdump".format(day_path)
            label_file = "{}/tcpdump.list".format(day_path)
            pcap2session_cmd = "bash pcap2session.sh {} {} -f".format(tcpdmp, flow_path)
            os.system(pcap2session_cmd)
            processSeeion_cmd = "bash processSeeion.sh {}/{}/ {}/ {} {}".format(flow_path, session_type, format_data_path, top_num, length)
            os.system(processSeeion_cmd)




if __name__ == '__main__':
    # pcap2png('./test.bin', './test.png')
    precessingTrain("../../data/train")
