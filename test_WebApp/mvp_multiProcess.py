#-*- coding: utf-8 -*-
""" MVP V2.0 
    多进程，快得一比
    2016-11-06
    author: liu kun
    默认脚本同数据文件在同一目录下
"""

__python_version__ = 2.7
__author__ = "Liu Kun"
__last_edit__ = "2017-04-25"

import json
import os
import BootstrapEngine as BS
import indexGenerator as g
import time
from multiprocessing import Process, Queue

import settings

CPU_KERNAL_NUMBER = 4

# 多线程处理器
class processor(Process):  
    def __init__(self,que):  
        Process.__init__(self)  
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
                    BS.dictRend(obj_list,out_file_path=os.path.join(settings.PAGE_PATH,school_name+".html"), title=regular_institute_name(school_name),a_count=len(entity_list))
                 except Exception as e:
                     print(str(e))  
            else:
                print("一个子进程结束了！\n")
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

# 处理英文机构名称书写格式
def regular_institute_name(name):
    words_list = name.split(' ')
    index = 0
    for i in words_list:
        if len(i)>3:
            words_list[index] = i[0].upper() + i[1:]
        index +=1
    reg_name = ' '.join(words_list)
    return reg_name

def main(json_data_path='./'):
    page_path = settings.PAGE_PATH
    fileList = []
    que = Queue()
    # 递归 path下所有目录寻找 .json 数据文件
    for root, dirs, files in os.walk('./'):
        for f_name in files:
            if f_name.lower().endswith('.json'):
                fileList.append(f_name)
    if not os.path.exists(page_path):
        os.mkdir(page_path)
    for i in fileList:
        que.put(i)
    start_time = time.clock()
    process_list = []
    for j in range(CPU_KERNAL_NUMBER):
        p = processor(que)
        # p.daemon = False  #子进程不会在主进程结束时终止
        process_list.append(p)
        p.start()
    for p in process_list:
        p.join()
    print('The process costed %f\'s'%(time.clock() - start_time))

if __name__ =="__main__":
    main()

 