# 态势感知实验

## download data &  Prepare the environment

1. 下载数据集

   由于DARPA数据集过于庞大，所以这里使用脚本的方式下载，并且数据存放的位置在代码目录之外。

   执行如下命令下载数据集：

   ```bash
   python utils/download.py
   ```

   data文件夹位置在`../data` 与代码目录同级

2. 环境准备

   + 准备python

     ```bash
     pip install -r requirements.txt
     ```

   + 准备预处理环境

     ```bash
     sudo apt-get install mono
     sudo apt-get install fdupes
     sudo apt-get install Tshark
     ```

## preprocessing

1. pcap2session.sh：处理pcap文件脚本，可以将pcap文件处理为flow和session

   脚本一次处理一个pcap文件，支持按照flow， session和packet三种格式分割，用法如下：

   ```bash
   Usage is: pcap2session.sh <SOURCE_DIR> <DESTINATION_DIR> <TYPE>
   		<SOURCE_DIR>: pcap file path
   		<DESTINATION_DIR>: path where results are stored
   		<TYPE>: -f (flow) | -s (session)
   		<SplitCap>: the SplitCap.exe path, default path is ../tool/SplitCap.exe
   ```

   + 例如`./pcap2session.sh ./test.pcap . -f`表示将当前目录下的test.pcap，按照flow的形式拆分后存储在当前`./flow`文件夹中

2. processSession.sh: 处理步骤1中的处理为flow和session的pcaps，将其截取784bytes, flow短于784，以0x00的形式补齐

   ```bash
   Usage is: processSession.sh <SOURCE_DIR> <DESTINATION_DIR> <SESSION_COUNT_MAX> <TRIMED_FILE_LIMIT>
   		<SOURCE_DIR>: the sessions pcaps path
   		<DESTINATION_DIR>: the result pcaps path
   		<SESSION_COUNT_MAX>: How many first to keep, optional
   		<TRIMED_FILE_LIMIT>: How many bytes are reserved for each pcap file, optional
   ```

   + 例如`./processSession.sh ./flow/ ./784/ 600 784`这条命令表示从flow文件夹中选取文件大小最大的600个文件，截取每个文件前784个字节，存储在./784/文件夹下

3. 