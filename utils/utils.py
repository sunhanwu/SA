import os
import numpy as np

def name2LabelDict(tcpdump_list_path):
    """
    读取tcpdump_list_path文件，将其中的{五元组: label}键值对全部取出放在一个字典中返回
    tcpdump_list_path: label文件
    """
    result = {}
    with open(tcpdump_list_path, 'r') as f:
        data = [x.strip() for x in f.readlnes()]
    
    

