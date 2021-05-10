import sys
import os
import struct
sys.path.append("/home/sunhanwu/Course/SA/src/utils")
sys.path.append("./utils")
from utils2 import *

def read_length_time(file_name):
    f=open(file_name,"rb")
    whole_file=f.read()
    tmp=32
    time_list=[]
    lengths_list=[]
#     try:
#     print(1)
    try:
        pre_time1=struct.unpack('>I',whole_file[tmp-8:tmp-4])[0]
        pre_time2=struct.unpack('>I',whole_file[tmp-4:tmp])[0]
        pre_time=float(str(pre_time1)+"."+str(pre_time2))
        while whole_file[tmp:tmp+4]:
            IP_t = struct.unpack('>H',whole_file[tmp+20:tmp+22])[0]
            lengths=struct.unpack('>I',whole_file[tmp:tmp+4])[0]
            new_time1=struct.unpack('>I',whole_file[tmp-8:tmp-4])[0]
            new_time2=struct.unpack('>I',whole_file[tmp-4:tmp])[0]
            new_time=float(str(new_time1)+"."+str(new_time2))
            if IP_t == 2048:
                time_list.append(new_time-pre_time)
                lengths_list.append(lengths)
            else:
                print("no ip_v4")

            pre_time=new_time
            tmp+=16
            tmp+=lengths
    except:
        print("error",file_name)
#     except:
#         print("error")
#         pass
    f.close()
    return time_list,lengths_list


#大批量的数据
from tqdm import tqdm
def deal_data(mode="train"):
    label_list = []
    feature_list = []
    
    root_path = "/home/sunhanwu/Course/SA/data/"
    root_path+=mode+"/"
    if mode!="test" or mode!="train":
        return "error,please use test or train"
    
    weeks = os.listdir(root_path)
    for week in weeks:
        week_path = root_path+week+"/"
        print(week_path+"is running")
        days = os.listdir(week_path)
        for day in tqdm(days):
            day_path = week_path+day+"/"
            print(day_path+"is running")
            #首先获得标签字典（四元组）
            if mode=="test":
                tcp_dump="tcpdump.lllist"
            else:
                tcp_dump="tcpdump.list"
            label_dict = extractLabelDict(day_path+tcp_dump)
            day_file_path = week_path+day+"/"+"session/AllLayers/"
            file_names = os.listdir(day_file_path)
            no_nums=0
            for file_name in file_names:
                #获得四元组(从tcmdump中获得标签)
                four_tuple = filename2key(file_name)
                if four_tuple in label_dict:

                    time_list,lengths_list = read_length_time(day_file_path+file_name)
                    if time_list==[]:
                        continue
                    label_list.append(label_dict[four_tuple])
                    feature_list.append([time_list,lengths_list])
                else:
                    no_nums+=1
            print(day_file_path,"not found",no_nums)
    return label_list,feature_list

def write_file(label_list,feature_list,mode="train"):
    #写文件
    if mode =="train":
        file_w_name = "sps_lstm.txt"
    else:
        file_w_name = "sps_lstm_Test.txt"
    w = open(file_w_name,"w")
    for i in tqdm(range(len(label_list))):
        w.write(" ".join([str(i) for i in feature_list[i][0]])+"\t"+" ".join([str(i) for i in feature_list[i][1]])+"\t"+label_list[i]+"\n")
    w.close()
if __name__ == '__main__':
    #处理训练集数据
    label_list,feature_list = deal_data(mode = "train")
    write_file(label_list,feature_list)
    #处理测试数据
    label_list,feature_list = deal_data(mode = "test")
    write_file(label_list,feature_list)