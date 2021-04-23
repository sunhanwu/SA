#! /bin/bash

# AUTHOR: sunhanwu(sunhanwu@iie.ac.cn)
# CONTRIBUTOR: sps(sunpeishaui@iie.ac.cn)
# Reference from https://github.com/jeevan-thapa/USTC-TK2016

# help info
if [ "$#" -lt 3 ]; then
  echo "[ERROR] Wrong format of command!"
  echo "[INFO] Usage is: pcap2session.sh <SOURCE_DIR> <DESTINATION_DIR> <TYPE> <SplitCap_DIR=../tool/SplitCap.exe>"
  echo "[INFO] <SOURCE_DIR>: the pcap file path"
  echo "[INFO] <SOURCE_DIR>: path where results are stored"
  echo "[INFO] <TYPE>: -f (flow) | -s (session) | -p (pcaket)"
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
if [ "$3" = "-f" ]; then
  echo "[INFO] spliting the PCAP file info each flow"
  # split pcap file
  mono $SplitCap -p 1000 -b 50000 -r $Pcap -s flow -o $Destination/AllLayers
  # -p 指定一次同时处理多少个flow/session/packet -b 指定最大缓存字节数
  mono $SplitCap -p 1000 -b 50000 -r $Pcap -s flow -o $Destination/L7
  # remove duplicate files
  fdupes -rdN $Destination/AllLayers
  fdupes -rdN $Destination/L7
fi

