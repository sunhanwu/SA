# 态势感知实验

## 一、环境准备与下载数据

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

## 二、数据预处理

1. pcap2session.sh：处理pcap文件脚本，可以将pcap文件处理为flow和session

   脚本一次处理一个pcap文件，支持按照flow， session和packet三种格式分割，用法如下：

   ```bash
   Usage is: pcap2session.sh <SOURCE_DIR> <DESTINATION_DIR> <TYPE>
   		<SOURCE_DIR>: pcap file path
   		<DESTINATION_DIR>: path where results are stored
   		<TYPE>: -f (flow) | -s (session)
   		<SplitCap>: the SplitCap.exe path, default path is ../tool/SplitCap.exe
   ```

   例如：`bash pcap2session test.pcap ./session -s`可以将当前目录下的test.pcap文件按照双向流的方式拆分为不同的流

2. processSession.sh：处理session文件脚本，将session文件进行预处理，用法如下：

   ```bash
   [ERROR] Wrong format of command!
   [INFO] Usage is: processSession.sh <SOURCE_DIR> <DESTINATION_DIR> <SESSION_COUNT_MAX> <TRIMED_FILE_LIMIT>
   [INFO] <SOURCE_DIR>: the sessions pcaps path
   [INFO] <DESTINATION_DIR>: the result pcaps path
   [INFO] <SESSION_COUNT_MAX>: How many first to keep, optional
   [INFO] <TRIMED_FILE_LIMIT>: How many bytes are reserved for each pcap file, optional
   ```

   对于一个文件夹中的所有session文件，脚本的处理步骤如下：

   + 将session文件夹所有文件按照文件大小降序排列，选择其中`SESSION_COUNT_MAX`个session文件
   + 对于选择出的每个文件，截取其前`TRIMED_FILE_LIMIT`个字节长度，如果不够，用`0X00`补齐
   + 将截取的文件复制到`DESTINATION_DIR`目录

3. preproessing.py: 预处理脚本，调用上述两种shell脚本，针对不同的深度学习模型(CNN和LSTM)处理成不同的数据

   preproessing.py中包含如下两个函数：

   + `precessingPcap`: 处理pcap文件

     + 参数列表

       + dataPath: 待处理的数据路径
       + T: 选择使用应用层数据还是所有层，7表示应用层，a表示所有层
       + ~: 截取文件长度
       + top_num: 每个文件夹中选取文件数目
       + flow_type: 使用单向流还是双向流

     + 功能说明

       函数会按照DARPA1998 数据集中文件存放的位置，遍历读取每一个tcpdump文件，并将且拆分为对应的单向流(或者双向流), 然后选取拆分后的文件中按照文件大小排序的前`top_num`个文件，截取每个文件的前`length`长度，不足补`0x00`，并将处理好的文件存储在对应位置。

   + `precessSession`函数：对每个流进行标注

     + 参数列表：
       + dataPath: 待处理的数据路径
       + dst_path_name: 目的路径
       + L7_path_name： 应用层目录名称(对应上面函数中的length)
       + png_size: 格式化为图片后图片的边长
       + lable_file: 指定label文件名称(DARPA数据集中train和test中label文件名称不一致)

## 三、算法模型

本次实验中使用了两种深度学习模型，分别是CNN模型和LSTM模型，使用和介绍分别如下。

### 3.1 CNN

1. 模型架构

   CNN模型架构图如下所示：

   ![](https://ipic-picgo.oss-cn-beijing.aliyuncs.com/CNN.png)

   模型一共包含三层CNN + MaxPooling

