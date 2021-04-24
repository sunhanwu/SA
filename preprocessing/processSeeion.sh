#! /bin/bash

# AUTHOR: sunhanwu(sunhanwu@iie.ac.cn)
# Reference from https://github.com/jeevan-thapa/USTC-TK2016
# func: 取前MAX大个pcap文件，截取TRIMED_FILE_LIMIT长度

# help info
# void help(void);
function help() {
  echo "[ERROR] Wrong format of command!"
  echo "[INFO] Usage is: processSession.sh <SOURCE_DIR> <DESTINATION_DIR> <SESSION_COUNT_MAX> <TRIMED_FILE_LIMIT>"
  echo "[INFO] <SOURCE_DIR>: the sessions pcaps path"
  echo "[INFO] <DESTINATION_DIR>: the result pcaps path"
  echo "[INFO] <SESSION_COUNT_MAX>: How many first to keep, optional"
  echo "[INFO] <TRIMED_FILE_LIMIT>: How many bytes are reserved for each pcap file, optional"
  exit 1;
}

# 选取SOURCE_DIR中按照文件大小排序的前TOP_NUM个文件名
# files topNfile(SOURCE_DIR, TOP_NUM)
function topNfile() {
  echo "[INFO] read $1 $2 files"
  # 接受第一个可选参数
  if [ ! $1 ]; then
    SOURCE_DIR=.
  else
    SOURCE_DIR=$1 
  fi
  # 接受第二个可选参数
  if [ ! $2 ]; then
    TOP_NUM=600
  else
    TOP_NUM=$2
  fi
  # 读取SOURCE_DIR目录，取文件最大的前TOP_NUM个文件名
  files=`ls -S $SOURCE_DIR | head -n "$TOP_NUM"`
  # 转化为数组
  files=($files)
}

if [ "$#" -lt 2 ]; then
  help
fi
SOURCE_DIR=$1
DESTINATION_DIR=$2

if [ ! $3 ]; then
  SESSION_COUNT_MAX=60000
else
  SESSION_COUNT_MAX=$3
fi
if [ ! $4 ]; then
  TRIMED_FILE_LIMIT=784
else
  TRIMED_FILE_LIMIT=$4
fi

topNfile $SOURCE_DIR $SESSION_COUNT_MAX
echo "[INFO] cut $SOURCE_DIR $TOP_NUM files, limit $TRIMED_FILE_LIMIT"
for file in ${files[@]};
do
  # 使用dd命令截取pcap文件前TRIMED_FIEL_LIMIT个字节内容
  dd if=$SOURCE_DIR$file of=$DESTINATION_DIR$file ibs=$TRIMED_FILE_LIMIT conv=sync
done