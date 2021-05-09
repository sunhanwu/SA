import sys
from tqdm import tqdm
sys.path.append('..')
import json
import os
import numpy as np
from PIL import Image
from utils.utils import filename2key, extractLabelDict
from utils.logger import log

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
    img_array = np.reshape(data, (png_size, png_size)).T
    img_array = np.uint8(img_array)
    img = Image.fromarray(img_array)
    img.save(png_path)


def precessingPcap(dataPath, T='7', length=3600, top_num=60000, flow_type='f'):
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
    for week in os.listdir(dataPath):
        week_path = os.path.join(dataPath, week)
        for day in os.listdir(week_path):
            day_path = os.path.join(week_path, day)
            if flow_type == 'f':
                flow_path = os.path.join(day_path, 'flow')
            else:
                flow_path = os.path.join(day_path, 'session')
            format_data_path = os.path.join(day_path, str(length))
            tcpdmp = "{}/tcpdump".format(day_path)
            label_file = "{}/tcpdump.list".format(day_path)
            if os.path.exists(flow_path):
                os.system("rm -rf {}".format(flow_path))
            if flow_type == 'f':
                pcap2session_cmd = "bash pcap2session.sh {} {} -f".format(tcpdmp, flow_path)
            else:
                pcap2session_cmd = "bash pcap2session.sh {} {} -s".format(tcpdmp, flow_path)
            os.system(pcap2session_cmd)
            print("rm -rf {}".format(format_data_path))
            os.system("rm -rf {}".format(format_data_path))
            processSeeion_cmd = "bash processSeeion.sh {}/{}/ {}/ {} {}".format(flow_path, session_type, format_data_path, top_num, length)
            os.system(processSeeion_cmd)

def precessSession(dataPath, dst_path_name, L7_path_name='3600', png_size=60, lable_file='tcpdump.list'):
    """
    将L7的bin文件
    :param dataPath:
    :param dst_path:
    :param png_size:
    :return:
    """
    png_logger = log("key-error")
    result = {}
    # for week in os.listdir(dataPath):
    for week in ['week6']:
        week_path = os.path.join(dataPath, week)
        for day in os.listdir(week_path):
            day_path = os.path.join(week_path, day)
            L7_path = os.path.join(day_path, L7_path_name)
            label_dict = extractLabelDict(os.path.join(day_path, lable_file))
            print(L7_path)
            for file in tqdm(os.listdir(L7_path)):
                try:
                    key = filename2key(file)
                    label = label_dict[key]
                    if label[0] in result.keys():
                        result[label[0]] += 1
                    else:
                        result[label[0]] = 0
                    save_path_dir = os.path.join(dst_path_name, label[0])
                    if not os.path.exists(save_path_dir):
                        os.mkdir(save_path_dir)
                    dst_file_path = os.path.join(save_path_dir, "{}_{}_{}_{}.bin".format(file.split('.')[1], label[0], label[1], result[label[0]] + 1))
                    file_path = os.path.join(L7_path, file)
                    os.system("cp {} {}".format(file_path, dst_file_path))
                    # pcap2png(file_path, dst_file_path, png_size)
                except:
                    png_logger.info("{} {} not found".format(L7_path, file))
    print(result)
    with open('../statistic.json', 'w') as f:
        json.dump(result, f)







if __name__ == '__main__':
    # pcap2png('./test.bin', './test.png')
    # precessingPcap("../../data/train", T='7', flow_type='s', length=3600)
    # precessingPcap("../../data/test", T='7', flow_type='s', length=3600)
    precessSession("../../data/train", "../../formatDataTrain3600Bin/")
    # precessSession("../../data/test", "../../formatDataTest3600Bin/", lable_file='tcpdump.lllist')
