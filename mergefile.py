# coding = utf-8
# usr/bin/env python

'''
Author: Chuck
Email: zliu18@gmail.com

date: 30/10/2019 10:50 AM
desc:
'''
import shutil
import os
import datetime

save_path = '/Users/zliu/downloads/txcm1/'


def rename():
    for root, dirs, files in os.walk(save_path):
        for filename in files:
            texts = filename.split(' ')
            index = texts[0]
            while len(index) < 3:
                index = '0' + index
            new_file_name = index + ' ' + ' '.join(texts[1:])
            os.rename(save_path+filename , save_path + new_file_name)


def merge():
    with open(save_path+'output_file.txt','wb') as wfd:
        for root, dirs, files in os.walk(save_path):
            for f in files:
                with open(save_path+f,'rb') as fd:
                        wfd.write(fd.read())


if __name__ == '__main__':
    merge()
    print(datetime.datetime.fromtimestamp(1369481239).strftime('%Y-%m-%d %H:%M:%S'))