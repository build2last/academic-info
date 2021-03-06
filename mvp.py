﻿# -*- coding: utf-8 -*-
""" 分析原始数据文件统计学者论文引用情况并调用 Bootstrap 引擎生成 HTML 文件 
    多线程，然并卵。
    默认脚本同数据文件在同一目录下
"""

__start_date__ = "2016-11-06"
__python_version__ = 2.7
__author__ = "Liu Kun"
__last_edit__ = "2017-04-25"

import json
import os

import BootstrapEngine  as BS
import indexGenerator as g
import threading
import Queue

# 多线程处理器
class processor(threading.Thread):  
    def __init__(self,que):  
        threading.Thread.__init__(self)  
        self.que = que
    def run(self):
        while True:
            if not self.que.empty():  
                 try:
                    author_dic = dict()
                    school_name = self.que.get().split('.')[0]
                    file_name = school_name + '.json'
                    entity_list = getJson(file_name).get("entities")
                    for i in entity_list:
                        for au in i.get('AA'):
                            if au["AuId"] not in author_dic:
                                author_dic[au["AuId"]] = [au["AuN"],i.get("CC")]
                            else:
                                author_dic[au["AuId"]][1]+= i.get("CC")
                    obj_list = sorted(author_dic.items(),key = lambda e:e[1][1],reverse = True)[0:100]
                    BS.dictRend(obj_list,out_file_path=school_name+".html", title=regular_institute_name(school_name),a_count=len(entity_list))
                 except Exception as e:
                     print(str(e))  
            else:
                print("一个线程结束了！\n")
                break 

def getJson(file_name):
    with open(file_name) as f:
        js = json.loads(f.read())
        return js
 
def school_mvr(entities_json):
    author_dic = dict()
    entity_list = entities_json
    for i in entity_list:
        for au in i.get('AA'):
            if au["AuId"] not in author_dic:
                author_dic[au["AuId"]] = [au["AuN"],i.get("CC")]
            else:
                author_dic[au["AuId"]][1]+= i.get("CC")
    return author_dic

#Regular process for the English institute name
def regular_institute_name(name):
    words_list = name.split(' ')
    index = 0
    for i in words_list:
        if len(i)>3:
            words_list[index] = i[0].upper() + i[1:]
        index +=1
    reg_name = ' '.join(words_list)
    return reg_name
    
def exe():
    fileList = []
    que = Queue.Queue()
    for root, dirs, files in os.walk('./'):     # 递归path下所有目录
        for f_name in files:
            if f_name.lower().endswith('.json'):
                fileList.append(f_name)
    if not os.path.exists("pages"):
        os.mkdir("pages")
    for i in fileList:
        que.put(i)
    threads = []
    que_set_size = 0
    if que.qsize()<5:
        que_set_size = que.qsize()
    else:
        que_set_size =5
    for j in range(que_set_size):
        p = processor(que)
        p.start()
        threads.append(p)
    for t in threads:
        t.join()
    print("线程结束.")
    #调用生成index.html    
    g.exe('pages/')

if __name__ =="__main__":
    fileList = []
    que = Queue.Queue()
    for root, dirs, files in os.walk('./'):
        for f_name in files:
            if f_name.lower().endswith('.json'):
                fileList.append(f_name)
    if not os.path.exists("pages"):
        os.mkdir("pages")
    for i in fileList:
        que.put(i)
    threads = []
    
    que_set_size = 0
    if que.qsize()<5:
        que_set_size = que.qsize()
    else:
        que_set_size =5
    for j in range(que_set_size):
        p = processor(que)
        p.start()
        threads.append(p)
    for t in threads:
        t.join()
    print("所有线程结束.")
    # 调用生成index.html    
    g.exe('pages/')
 