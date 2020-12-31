import pandas as pd
import numpy as np
import csv
import json
import shlex
from pandas import DataFrame,Series

HTML_FILE = '/home/test/intrinsic.html'
JSON_FILE = '/home/test/intrinsic_table.json'
CSV_FILE = '/home/test/intrinsic_table.csv'

#file:csv to json
def transjson(jsonpath, csvpath):
    fw = open(jsonpath, 'w', encoding='utf8')   # 打开json文件
    fo = open(csvpath, 'r', newline='')    # 打开csv文件
    reader = csv.reader(fo)

    ls = []
    for line in reader:
        ls.append(line)
        #line = line.replace("\n", "")  # 将换行换成空
        #ls.append(line.split(","))  # 以，为分隔
    #print(ls)
    #write into json file
    for i in range(1, len(ls)):  # 遍历文件的每一行内容，除了列名
        ls[i] = dict(zip(ls[0], ls[i]))  # ls[0]为列名，所以为key,ls[i]为value,
        # zip()是一个内置函数，将两个长度相同的列表组合成一个关系对

    json.dump(ls[1:], fw, sort_keys=False, indent=4)
    #将Python数据类型转换成json格式，编码过程
    #默认是顺序存放，sort_keys是对字典元素按照key进行排序
    #indet参数用语增加数据缩进，使文件更具有可读性

    # close files
    fo.close()
    fw.close()

def html_to_csv(html):
    dfs = pd.read_html(html)

    for n in range(len(dfs)):
        df=dfs[n].iloc[:,:1]
        if df.columns == 'Intrinsic':
            df.replace('const ','',regex=True, inplace=True)
            df = df['Intrinsic'].str.split(' ',expand=True)
            df.to_csv(r'/home/test/intrinsic_table.csv', mode='a', encoding='utf_8_sig', header=0, index=1)

if __name__ == '__main__':
    #file = open(HTML_FILE,'rb')
    #html = file.read()
    #html_to_csv(html)

    transjson(JSON_FILE,CSV_FILE)

    
        

        