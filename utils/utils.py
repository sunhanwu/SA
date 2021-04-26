import os
import numpy as np

def extractLabelDict(tcpdump_list_path):
    """
    读取tcpdump_list_path文件，将其中的{五元组: label}键值对全部取出放在一个字典中返回
    tcpdump_list_path: label文件
    """
    result = {}
    with open(tcpdump_list_path, 'r') as f:
        data = [x.strip() for x in f.readlines()]
    for line in data:
        items = line.split(' ')
        ip_src = items[-4]
        ip_src = '-'.join([str(int(x)) for x in ip_src.split('.')])
        port_src = items[-6]
        ip_dst = items[-3]
        ip_dst = '-'.join([str(int(x)) for x in ip_dst.split('.')])
        port_dst = items[-5]
        label = int(items[-2])
        key = '_'.join([ip_src, port_src,ip_dst, port_dst ])
        if key not in result.keys():
            result[key] = label
    return result

def filename2key(filename:str):
    """
    将pcap文件名转化为key
    filename: 文件名
    """
    items = filename.split('.')
    keys = items[1].split('_')
    #keys = []
    key = '_'.join(keys[1:])
    return key

if __name__ == '__main__':
    #label_dict = 
    key = filename2key('tcpdump.TCP_12-5-132-10_80_172-16-117-111_10319.bin')
    print(key)
    
    

