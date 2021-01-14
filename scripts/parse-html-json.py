import os,sys
import pandas as pd
import numpy as np
import csv, re
import json
import shlex
from shutil import move
from pandas import DataFrame,Series
from ValueMap import VALUE_MAP
from Intrinsic_Type_List import INTRINSIC_TYPE_MAP
from optparse import OptionParser

ROOT_DIR=os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(ROOT_DIR, 'intrinsic_table.json' )

def get_expect_result(api):
    result = ''
    with open(JSON_FILE,'r') as f:
        rootNode = json.loads(f.read())
    for note in rootNode:
        if note['Expect_Result'] and note['Intrinsic_Name'].rstrip() == api:
            result = note['Expect_Result']
    return result

def json_to_csv(jsonpath,csvpath):
    # 1.分别 读，创建文件
    json_fp = open(jsonpath, "r",encoding='utf-8')
    csv_fp = open(csvpath, "w",encoding='utf-8',newline='')

    # 2.提出表头和表的内容
    data_list = json.load(json_fp)
    sheet_title = data_list[0].keys()
    sheet_data = []
    for data in data_list:
        sheet_data.append(data.values())

    # 3.csv 写入器
    writer = csv.writer(csv_fp)

    # 4.写入表头
    writer.writerow(sheet_title)

    # 5.写入内容
    writer.writerows(sheet_data)

    # 6.关闭两个文件
    json_fp.close()
    csv_fp.close()

def csv_to_json(csvpath,jsonpath):
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

def formalize_csv(csv_file):
    fo = open(csv_file, 'r', newline='')    # 打开csv文件
    dfs = csv.reader(fo)
    for n in range(len(dfs)):
        df=dfs[n].iloc[:,:1]
        df.insert(0,'ID','')
        df.insert(1,'Intrinsic_Type','')
    fo.close()

def html_to_csv(html_file,csv_file):
    file = open(html_file,'rb')
    html = file.read()
    dfs = pd.read_html(html)

    for n in range(len(dfs)):
        df=dfs[n].iloc[:,:1]
        if df.columns == 'Intrinsic':
            translations = {
                            r'(.*)\((.*)':r'\1 \2',
                            r'(.*)\)(.*)':r'\1 \2',
                            r'(.*)\*base(.*)':r'\1base[]\2'
                            }
            df.replace(translations,regex=True, inplace=True)
            df.replace('const ','',regex=True, inplace=True)
            df.replace(',','',regex=True, inplace=True)
            df.replace('enum ACCUM','enumACCUM',regex=True, inplace=True)
            df = df['Intrinsic'].str.split(' ',expand=True)
            df.to_csv(csv_file, mode='a', encoding='utf_8_sig', header=0, index=1)

def set_json_value(temp_file):
    rootNode={}
    with open(temp_file, 'r') as f:
        rootNode = json.loads(f.read())
    for data in rootNode:
        ##### Set Intrinsic_Type
        for key in INTRINSIC_TYPE_MAP:
            ret = re.match(INTRINSIC_TYPE_MAP[key],data['Intrinsic_Name'])
            if ret:
                data['Intrinsic_Type'] = key

        ##### Set Input_X_Value
        if 'CSR' in data['Intrinsic_Type']: pass
        else:
            for i in range(1,8):
                if data['Input_'+str(i)+'_Type'] =='': pass
                else:
                    if data['Input_'+str(i)+'_Value'] == '':
                        data['Input_'+str(i)+'_Value'] = VALUE_MAP[data['Input_'+str(i)+'_Type']][data['Input_'+str(i)+'_Variable']]
        
        #### Set Expect Result
        if 'CSR' in data['Intrinsic_Type']: pass
        else:
            if data['Expect_Result']== '':
                data['Expect_Result'] = get_expect_result(data['Intrinsic_Name'])

    with open(temp_file, 'w') as f2:
        json.dump(rootNode,f2,ensure_ascii=True,indent=4)

def main():
    parser=OptionParser()
    parser.add_option('--h2c', action='store_true',dest='h2c',default=False, help='transiton from html to csv')
    parser.add_option('--c2j', action='store_true',dest='c2j',default=False, help='transiton from csv to json')
    parser.add_option('--j2c', action='store_true',dest='j2c',default=False, help='transiton from json to csv')
    parser.add_option('--fcsv', action='store_true',dest='fcsv',default=False, help='formalize csv to insert ID and type')
    (options,args)=parser.parse_args()
    
    html_file = os.path.join(ROOT_DIR, 'intrinsic.html' )
    csv_file = os.path.join(ROOT_DIR, 'intrinsic_table.csv' )
    testing_result_csv_file = os.path.join(ROOT_DIR, 'intrinsic_testing.csv' )
    
    temp_json = os.path.join(ROOT_DIR, 'tmp.json' )

    if options.h2c:  #html -> csv
        html_to_csv(html_file,csv_file) 
        
    if options.fcsv: #formalize csv to insert ID and type
        formalize_csv(csv_file)  
        
    if options.c2j:  #csv -> json
        csv_to_json(csv_file,temp_json) 
        set_json_value(temp_json)
        move(temp_json, JSON_FILE)
        
    if options.j2c:  #json -> csv
        json_to_csv(JSON_FILE,testing_result_csv_file) 

if __name__ == '__main__':
    main()
        

        