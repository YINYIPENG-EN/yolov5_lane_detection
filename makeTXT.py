import os
import random

trainval_percent = 0.9  # 训练验证集的划分
train_percent = 0.9  # 训练集的划分
xmlfilepath = 'datasets/Annotations'  # xml路径
txtsavepath = 'datasets/ImageSets'  # 要生成txt文件的路径
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)  # 获取验证集数量
tr = int(tv * train_percent)  # 获取训练集数量
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open('datasets/ImageSets/trainval.txt', 'w')  # 用于写入trainval.txt
ftest = open('datasets/ImageSets/test.txt', 'w')
ftrain = open('datasets/ImageSets/train.txt', 'w')
fval = open('datasets/ImageSets/val.txt', 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'  # 取图像的名字
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
print("完成")