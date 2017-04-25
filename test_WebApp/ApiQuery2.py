# -*- coding: utf-8 -*-
# 修改 api 后未整理 2016-10-17

""" 获取数据 
利用微软学术提供的 API 查询获取目标学校的论文信息。
用长连接的方法查询获取信息
"""

__python_version__ = 2.7
__author__ = "Liu Kun"
__last_edit__ = "2017-04-25"

import httplib, urllib, base64
import re
import json
import socket
from threading import *

import settings

socket.setdefaulttimeout(300)
# 一个有效访问链接大概长这个样子 https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=Id=2140251882&count=10000&attributes=Id,AA.AuId,AA.AfId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
key_info = "f7cc29509a8443c5b3a5e56b0e38b5a6"
# Request parameters
params = urllib.urlencode({
    'expr': 'Composite(AA.AfN=\'east china normal university\')',
    'model': 'latest',
    'attributes': 'Id,Ti,CC,C.CN,J.JN,Y,AA.AuId,AA.AuN',
    'count': '100000',
    'offset': '0',
    'aborted':False,
    'Subscription-Key': key_info
})


def print_entity(enti_list):
    for i in enti_list:
        print i.get('Ti')
        AA_list = i.get('AA')
        for j in range(len(AA_list)):
            print '(%d)'%(j+1) + AA_list[j].get('AuN') + ' ',
        print ''        
        
def call_api(target_name):
    if not isinstance(target_name, str):
        print("Input expected to be string type")
        return
    params = urllib.urlencode({
        'expr': 'Composite(AA.AfN=\'%s\')'%target_name,
        'model': 'latest',
        'attributes': 'Id,Ti,CC,C.CN,J.JN,Y,AA.AuId,AA.AuN',
        'count': '70000',
        'offset': '0',
        'aborted':False,
        'Subscription-Key': key_info
    })
    try:
        conn = httplib.HTTPSConnection('oxfordhk.azure-api.net')
        conn.request("GET", "/academic/v1.0/evaluate?%s" % params)
        response = conn.getresponse()
        data = response.read()
        re_json = json.loads(data)
        save_file_name =  target_name.replace("\'",'')  + '.json'
        with open(save_file_name,'w') as f:
            f.write(data)
        enti_list = re_json.get('entities')
        print(target_name+ " has %d entities"%len(enti_list))
    except Exception as e:
        print(e)

def thread_run(target_list):
    thread_list = []
    for i in target_list:
        t = Thread(target=call_api(i))
        thread_list.append(t)
        t.start()
    for th in thread_list:
        th.join()

def main():
    school_list = settings.school_list
    thread_run(school_list)
    print("Query_The End")
if __name__ == "__main__":
    main()