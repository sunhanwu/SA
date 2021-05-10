#dataloader
import torch
from torch.utils.data import Dataset, DataLoader
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import numpy as np
import random
class mydataset(Dataset):
    def __init__(self, file_name,max_length,mode):  # self参数必须，其他参数及其形式随程序需要而不同，比如(self,*inputs)
        self.max_length = max_length
        self.nums = 3
        self.mode = mode
        self.data, self.label = self.load_file(file_name)
        print(len(self.data))
        
    # 加载数据
    def load_file(self, file_name):
        # 语料格式  【q1】\t【q2】\t label（0 or 1）
        f = open(file_name, "r", encoding="utf-8")
        data = []
        label = []
        for i, line in enumerate(f.readlines()):

            if self.mode =="train":
                if random.random()<0.2:
                    continue
                
                if line[2]=="1" and random.random()<0.5:
                    continue
            # 有一些数据格式不太好，会有多个\t,得把他们过滤掉
            line = [x for x in line.strip().split("\t")]
            if len(line) != self.nums:
                print(line, "error")
                continue
            
            time_ = line[0].split()
            lengths_ = line[1].split()
            if time_==[] or lengths_==[]:
                print("kongbai")
                continue
            tokens = [[min(int(lengths_[i]),1520)] for i in range(len(time_))]
            if len(tokens)<= self.max_length:
                tokens+=[[0]]*(self.max_length-len(tokens))
            else:
                tokens=tokens[:self.max_length]

            tokens.append(int(line[2]))
#             label.append(int(line[2]))

            
            data.append(tokens)
        random.shuffle(data)


        label = [i[-1] for i in data]
        data = [i[:self.max_length] for i in data]
        data = torch.LongTensor(data)
        label = torch.LongTensor(label)
        
#         shuffle_indices = np.random.permutation(np.arange(len(y)))
#         data_shuffle = data[shuffle_indices]
#         label_shuffle = label[shuffle_indices]
        return data,label
        

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data = self.data
        label = self.label
        return data,label

#定义模型
class BiLSTM(nn.Module):

    def __init__(self, input_dim, hidden_dim, label_nums,embedding_dim):
        super(BiLSTM, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.embedding_dim = embedding_dim
        self.word_embeds = nn.Embedding(1520, embedding_dim)
        self.tagset_size = label_nums
        #LSTM层
        self.lstm = nn.LSTM(embedding_dim, hidden_dim,num_layers=1,batch_first=True)

        #全连接层
        self.dense = nn.Linear(hidden_dim, self.tagset_size)
        self.softmax = nn.Softmax()
    
    def forward(self,inputs):
        embeds = self.word_embeds(inputs).view(inputs.size(0),inputs.size(1),-1)
#         print(embeds.size())
        layer1_output,layer1_hidden = self.lstm(embeds)
        layer2_output = self.dense(layer1_output)
        layer2_output = layer2_output[:,-1,:]#取出一个batch中每个句子最后一个单词的输出向量即该句子的语义量！！！！！！！,layer2_output的维度是[batch_size,sequence_length,embedding_dim],layer2_output[:,-1,:]-1表示第二个维度sequence_length的最后一个数据也就是一句话中最后一个字的语义向量。
        return layer2_output
# 		#-------或者使用隐藏层向量作为线性层的输入-------
# 		layer1_output,layer1_hidden = self.layer1(inputs)
# 		layer2_output = self.layer2(layer1_hidden)
# 		return layer2_output

#开始训练
#超参数
def main():
    #读取数据
    MAX_SEQ = 64
    INPUT_DIM = 1
    HIDDEN_DIM = 512
    LABEL_NUMS = 4
    epochs = 4
    logger_steps = 500
    BATCH_SIZE = 512
    embedding_dim = 64
    LR = 0.01
    file_name = "sps_lstm.txt"
    train_data = mydataset(file_name,max_length=MAX_SEQ,mode="train")
    # train_dataloader = DataLoader(train_data[0], batch_size=BATCH_SIZE, shuffle=True)
    print("data_pre is finished")

    file_name = "sps_lstm_Test.txt"
    test_data = mydataset(file_name,max_length=MAX_SEQ,mode="test")
    


    device = "cuda" if torch.cuda.is_available() else "cpu"


    print("data_pre is finished")
    model = BiLSTM(input_dim=INPUT_DIM, hidden_dim=HIDDEN_DIM , label_nums=LABEL_NUMS,embedding_dim=embedding_dim).to(device)
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=1e-4,betas=(0.8, 0.999))
    criterion = nn.CrossEntropyLoss() #二分类损失函数


    for epoch in range(epochs):
        acc_nums = 0
        nums_all = 0
        j=0
        batch = 0
        acc_list=[]
        f1_list = []
        while batch+128<=len(train_data.data):
            data = train_data.data[batch:batch+128]
            label = train_data.label[batch:batch+128]
            data = data.to(device)
            label = label.to(device)

            model.zero_grad()
            prediction = model(data)
            loss = criterion(prediction,label)
            loss.backward()
            optimizer.step()
            acc_nums += (label == prediction.max(1).indices).sum().detach().cpu().numpy()
            nums_all += len(data)
            batch+=128
            if batch % (128*logger_steps) == 0:
                acc = acc_nums/nums_all
                print('training: epoch:{0}, item:{1}, loss:{2}, acc:{3}'.format(
                    epoch, int(batch/128), loss, acc))
                acc_list.append(acc)
                TP, TN, FP, FN = 0, 0, 0, 0
                test_loss_all = 0
                test_batch = 0

                while test_batch<=len(test_data.data):
                    with torch.no_grad():
                        data = test_data.data[batch:batch+128]
                        label = test_data.label[batch:batch+128]
                        data = data.to(device)
                        test_batch += 128
                        prediction = model(data)
                        outlabel = prediction.max(1).indices.to("cpu")                    

                        TP += int(((outlabel == 1) & (label == 1)).sum())
                        FP += int(((outlabel == 1) & (label == 0)).sum())
                        FN += int(((outlabel == 0) & (label == 1)).sum())
                        TN += int(((outlabel == 0) & (label == 0)).sum())

                pre = TP/(TP+FP+0.0000001)  # 避免÷0
                rec = TP/(TP+FN+0.0000001)
                f1 = 2*pre*rec/(rec+pre+0.00000000000000001)
                f1_list.append(f1)
                print("testing, \
                             pre:{:.4f}, rec:{:.4f}, f1:{:.4f}".format(pre, rec, f1))

if __name__ == "__main__":
    main()