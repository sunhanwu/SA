import sys
from tqdm import tqdm
sys.path.append('..')
import torch
import os
from PIL import Image
from torch.utils.data import  Dataset
import random
from torchvision import transforms
import numpy as np
from utils.utils import extractLabelDict, filename2key

class DARPA(Dataset):
    """
    DARPA 数据集封装成的dataset
    """
    def __init__(self, data_path, length=3600, mode='train', size=60, max_num=10000):
        """
        初始化
        """
        self.length = length
        self.size = size
        self.mode = mode
        self.max_num = max_num
        result = self.load_data(data_path)
        self.data = []
        for k, v in result.items():
            for file in v:
                self.data.append((file, int(k)))
        random.shuffle(self.data)

    def load_data(self, data_path):
        """
        加载数据
        :param data_path:
        :return:
        """
        print("load data: {}".format(data_path))
        result = {}
        except_num = 0
        # if self.mode == 'train':
        #     weeks = ['week7']
        # else:
        #     # weeks = [x for x in os.listdir(data_path)]
        #     weeks = ['week1']
        # for week in weeks:
        for week in tqdm(os.listdir(data_path)):
            week_path = os.path.join(data_path, week)
            for day in os.listdir(week_path):
                day_path = os.path.join(week_path, day)
                files_path = os.path.join(day_path, 'session/L7/')
                # rm_empyt_cmd = 'find {} -name "*" -type f -size 0c | xargs -n 1 rm -f '.format(files_path)
                # os.system(rm_empyt_cmd)
                if self.mode == 'train':
                    labelDict = extractLabelDict(os.path.join(day_path, 'tcpdump.list'))
                else:
                    labelDict = extractLabelDict(os.path.join(day_path, 'tcpdump.lllist'))
                for file in os.listdir(files_path):
                    pcap_path = os.path.join(files_path, file)
                    file_key = filename2key(file)
                    try:
                        label = labelDict.get(file_key)
                        if label[0] in result.keys():
                            result[label[0]].append(pcap_path)
                        else:
                            result[label[0]] = [pcap_path]
                    except:
                        except_num += 1
                        continue
        for k, v in result.items():
            if len(v) > self.max_num:
                random.shuffle(v)
                result[k] = v[:self.max_num]
                print("{}: {}/{}".format(k, self.max_num, len(v)))
            else:
                print("{}: {}/{}".format(k, self.max_num, len(v), len(v)))
        print("except num: {}".format(except_num))
        return result

    def pcap2idx(self, filepath):
        """
        将图片处理成28*28的array矩阵
        :param filepath:
        :return:
        """
        with open(filepath, 'rb') as f:
            data = [x / 255 for x in f.read()]
            # data = [x for x in f.read()]
        if len(data) >= self.length:
            data = data[:self.length]
        else:
            data += [0.0] * (self.length - len(data))
        data = np.array([data]).reshape(self.size, self.size)
        data = torch.from_numpy(data).unsqueeze(0)
        return data

    def __getitem__(self, index):
        img = self.pcap2idx(self.data[index][0])
        label = self.data[index][1]
        return img, torch.Tensor([label])

    def __len__(self):
        return len(self.data)


if __name__ == '__main__':
    data = DARPA('../../data/train/', mode='train')
    # test = data[0]


