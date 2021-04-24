#! /bin/bash

# AUTHOR: sunhanwu(sunhanwu@iie.ac.cn)
# Reference from https://github.com/jeevan-thapa/USTC-TK2016
# func: 取前MAX大个pcap文件，截取TRIMED_FILE_LIMIT长度


# help info
function help() {
  echo "[ERROR] Wrong format of command!"
  echo "[INFO] Usage is: processSession.sh <SOURCE_DIR> <SESSION_COUNT_MAX> <TRIMED_FILE_LIMIT>"
  echo "[INFO] <SOURCE_DIR>: the sessions pcaps path"
  echo "[INFO] <SESSION_COUNT_MAX>: How many first to keep, optional"
  echo "[INFO] <TRIMED_FILE_LIMIT>: How many bytes are reserved for each pcap file, optional"
  exit 1;
}

if [ "$#" -lt 1 ]; then
  help
fi

if [ ! $2 ]; then
  SESSION_COUNT_MAX=60000
else
  SESSION_COUNT_MAX=$2
fi
if [ ! $3 ]; then
  TRIMED_FILE_LIMIT=784
else
  TRIMED_FILE_LIMIT=$3
fi

echo $SESSION_COUNT_MAX
echo $TRIMED_FILE_LIMIT
