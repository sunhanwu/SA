# 态势感知实验

## preprocessing
  1. 预安装软件：
   + mono: `sudo apt install mono`
   + SplitCap: 前往[SplitCap官网下载](https://www.netresec.com/?page=SplitCap)即可，注意存放位置，按照下面脚本所提示使用
  2. pcap2session.sh：处理pcap文件脚本，可以将pcap文件处理为flow, session和pcaket
   + Usage is: pcap2session.sh <SOURCE_DIR> <DESTINATION_DIR> <TYPE>
   + <SOURCE_DIR>: pcap file path
   + <DESTINATION_DIR>: path where results are stored
   + <TYPE>: -f (flow) | -s (session) | -p (pcaket)
   + <SplitCap>: the SplitCap.exe.path, default path is ../tool/SplitCap.exe
  3. 
