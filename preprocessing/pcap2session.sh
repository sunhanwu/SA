#! /bin/bash

# AUTHOR: sunhanwu(sunhanwu@iie.ac.cn)
# Reference from https://github.com/jeevan-thapa/USTC-TK2016

# help info
if [ "$#" -lt 3 ]; then
  echo "[ERROR] Wrong format of command!"
  echo "[INFO] Usage is: pcap2session.sh <SOURCE_DIR> <DESTINATION_DIR> <TYPE> <SplitCap_DIR=../tool/SplitCap.exe>"
  echo "[INFO] <SOURCE_DIR>: the pcap file path"
  echo "[INFO] <SOURCE_DIR>: path where results are stored"
  echo "[INFO] <TYPE>: -f (flow) | -s (session)"
  echo "[INFO] <SplitCap>: the SplitCap.exe path, default path is ../tool/SplitCap.exe"
  exit 1;
fi

# Determine whether there is SplitCap.exe
if [ "$#" -eq 4 ]; then
  SplitCap=$4
else 
  SplitCap="../tool/SplitCap.exe"
fi
Pcap=$1
Destination=$2
Type=$3

# start split
if [ "$Type" = "-f" ]; then
  echo "[INFO] spliting the $Pcap info flows(save all layers)"
  # split pcap file into flows
  # -p 指定一次同时处理多少个flow/session/packet
  # -b 指定最大缓存字节数
  # -s 指定分割的格式, 支持flow/host/mac/session(default)
  # -y L7 指定只保存应用层数据
  mono $SplitCap -p 1000 -b 50000 -r $Pcap -s flow -o $Destination/AllLayers
  echo "[INFO] spliting the $Pcap info flows(save L7)"
  mono $SplitCap -p 1000 -b 50000 -r $Pcap -s flow -y L7 -o $Destination/L7

  # remove duplicate files
  # fdupes 用法
  # -r 递归执行
  # -d 删除重复文件，只保留一个副本文件
  # -N 没有删除提示
  echo "[INFO] spliting the $Pcap info flows(remove duplicate files)"
  fdupes -rdN $Destination/AllLayers
  fdupes -rdN $Destination/L7
elif [ "$Type" = "-s" ]; then
  echo "[INFO] spliting the $Pcap info each session(save all layers)"
  # split pcap file into sessions
  mono $SplitCap -p 1000 -b 50000 -r $Pcap -o $Destination/AllLayers -y L7
  echo "[INFO] spliting the $Pcap info each session(save L7)"
  # split pcap file into sessions
  mono $SplitCap -p 1000 -b 50000 -r $Pcap -o $Destination/L7 -y L7
  # remove duplicate files
  echo "[INFO] spliting the $Pcap info each session(remove duplicate files)"
  fdupes -rdN $Destination/AllLayers
  fdupes -rdN $Destination/L7
else
  echo "[ERROR] Wrong format of command!"
  echo "[INFO] Usage is: pcap2session.sh <SOURCE_DIR> <DESTINATION_DIR> <TYPE> <SplitCap_DIR=../tool/SplitCap.exe>"
  echo "[INFO] <SOURCE_DIR>: the pcap file path"
  echo "[INFO] <SOURCE_DIR>: path where results are stored"
  echo "[INFO] <TYPE>: -f (flow) | -s (session) | -p (pcaket)"
  echo "[INFO] <SplitCap>: the SplitCap.exe path, default path is ../tool/SplitCap.exe"
  exit 1;
fi

