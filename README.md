# 态势感知实验

## download

由于DARPA数据集过于庞大，所以这里使用脚本的方式下载，并且数据存放的位置在代码目录之外。

执行如下命令下载数据集：

```bash
python utils/download.py
```

data文件夹位置在`../data` 与代码目录同级

## preprocessing

    1. 预安装软件：
       - mono: `sudo apt install mono`
       - fdupes: `sudo apt-get install fdupes`
       - SplitCap: 前往[SplitCap官网下载](https://www.netresec.com/?page=SplitCap)即可，注意存放位置，按照下面脚本所提示使用
  2. pcap2session.sh：处理pcap文件脚本，可以将pcap文件处理为flow, session和pcaket

     脚本一次处理一个pcap文件，支持按照flow， session和packet三种格式分割，用法如下：

     ```bash
     Usage is: pcap2session.sh <SOURCE_DIR> <DESTINATION_DIR> <TYPE>
     		<SOURCE_DIR>: pcap file path
     		<DESTINATION_DIR>: path where results are stored
     		<TYPE>: -f (flow) | -s (session) | -p (pcaket)
     		<SplitCap>: the SplitCap.exe path, default path is ../tool/SplitCap.exe
     ```
  3. 
