import torch
from tqdm import tqdm
import numpy as np
from torch.utils.data import random_split
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, recall_score, f1_score
import sys
sys.path.append('..')
from CNN.model import CNN_IDS
from CNN.dataloader import DARPA


if __name__ == '__main__':
    # 定义超参
    batch_size = 256
    lr = 1e-1
    epochs = 100

    # 定义数据集
    DARPA_train_data = DARPA('../../data/train/', mode='train')
    train_valid_len = len(DARPA_train_data)
    train_len = int(train_valid_len * 0.8)
    valid_len = train_valid_len - train_len
    test_data = DARPA('../../data/test/', mode='test')
    train_data, valid_data = random_split(DARPA_train_data, [train_len, valid_len])
    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=0)
    valid_loader = DataLoader(valid_data, batch_size=batch_size, shuffle=True, num_workers=0)
    test_loader =DataLoader(test_data, batch_size=batch_size, shuffle=True, num_workers=0)

    # 定义日志
    # train_log = log('CNN-0508')

    # 定义运行设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 定义模型，优化器，损失函数
    model = CNN_IDS()
    model = model.to(device)
    criterrion = torch.nn.BCELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.3)

    # 开始训练
    for epoch in range(epochs):
        model.train()
        y_pred_list = []
        y_true_list = []
        for step, (batch_X, batch_y) in enumerate(tqdm(train_loader)):
            batch_X = batch_X.float().to(device)
            y_pred = model(batch_X).squeeze(dim=-1)
            batch_y = batch_y.float().to(device).squeeze(dim=-1)
            loss = criterrion(y_pred, batch_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            y_pred_temp = ((np.array(y_pred.tolist()) >= 0.5) + 0).tolist()
            y_true_temp = batch_y.long().tolist()
            y_pred_list += y_pred_temp
            y_true_list += y_true_temp
        acc = accuracy_score(y_true_list, y_pred_list)
        recall = recall_score(y_true_list, y_pred_list)
        f1 = f1_score(y_true_list, y_pred_list)
        print("[epoch-train] {:03d}, loss: {:.2f}, acc:{:.2%}, recall: {:.2%}, f1: {:.2%}".format(epoch + 1, loss.item(), acc, recall, f1))
        # valid
        y_pred_list = []
        y_true_list = []
        model.eval()
        for step, (batch_X, batch_y) in enumerate(valid_loader):
            batch_X = batch_X.float().to(device)
            y_pred = model(batch_X).squeeze(dim=-1)
            batch_y = batch_y.float().to(device).squeeze(dim=-1)
            y_pred_temp = ((np.array(y_pred.tolist()) >= 0.5) + 0).tolist()
            y_true_temp = batch_y.long().tolist()
            y_pred_list += y_pred_temp
            y_true_list += y_true_temp
        acc = accuracy_score(y_true_list, y_pred_list)
        recall = recall_score(y_true_list, y_pred_list)
        f1 = f1_score(y_true_list, y_pred_list)
        print("[epoch-valid] {:03d}, acc:{:.2%}, recall: {:.2%}, f1: {:.2%}".format(epoch + 1, acc, recall, f1))

    # test
    y_pred_list = []
    y_true_list = []
    for step, (batch_X, batch_y) in enumerate(tqdm(test_loader)):
        batch_X = batch_X.float().to(device)
        y_pred = model(batch_X).squeeze(dim=-1)
        batch_y = batch_y.float().to(device).squeeze(dim=-1)
        loss = criterrion(y_pred, batch_y)
        y_pred_temp = ((np.array(y_pred.tolist()) >= 0.5) + 0).tolist()
        y_true_temp = batch_y.long().tolist()
        y_pred_list += y_pred_temp
        y_true_list += y_true_temp
    acc = accuracy_score(y_true_list, y_pred_list)
    recall = recall_score(y_true_list, y_pred_list)
    f1 = f1_score(y_true_list, y_pred_list)
    print("[ TEST ] {:03d}, acc:{:.2%}, recall: {:.2%}, f1: {:.2%}".format(epoch + 1, acc, recall, f1))





