# -*- coding: utf-8 -*-
# 修改 api 后未整理 2016-10-17
import httplib, urllib, base64
import re
import json
import socket
from threading import *

socket.setdefaulttimeout(300)

#https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=Id=2140251882&count=10000&attributes=Id,AA.AuId,AA.AfId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
url_head = "https://oxfordhk.azure-api.net/academic/v1.0/evaluate?"
key_info = "{key}"
"""
school_list = ['peking university','tsinghua university','zhejiang university',
                        'nanjing university of science and technology','nanjing university of aeronautics',
                        'shanghai jiao tong university','fudan university','wuhan university',
                        'nanjing university','university of science and technology of china']
school_list2 = ['beihang university','sun yat sen university','beijing institute of technology'] 
"""

new_list = ['East China Normal University'.lower()]
school_list = new_list
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '9c5e14d41af7453d95b1f502f396d76d',
}

params = urllib.urlencode({
    # Request parameters
    'expr': 'Composite(AA.AfN=\'east china normal university\')',
    'model': 'latest',
    'attributes': 'Id,Ti,CC,C.CN,J.JN,Y,AA.AuId,AA.AuN',
    'count': '70000',
    'offset': '0',
    'aborted':False
})


def print_entity(enti_list):
    for i in enti_list:
        print i.get('Ti')
        AA_list = i.get('AA')
        for j in range(len(AA_list)):
            print '(%d)'%(j+1) + AA_list[j].get('AuN') + ' ',
        print ''
        
        
def call_api(url):
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print data
        re_json = json.loads(data)
        save_file_name =  sch_name.replace("\'",'')  + '.json'
        with open(save_file_name,'w') as f:
            f.write(data)
        enti_list = re_json.get('entities')
        sch_name = 'East China Normal University'.lower()#re.findall('AfN=(.*)\)',url)[0]
        print sch_name+ " " + str(len(enti_list))
        #print_entity(enti_list)
    except Exception as e:
        print(str(e))

def attack(url):
    try:
        call_api(url)
    except Exception as e:
        print str(e)   
 
def thread_run(url):
    t = Thread(target=attack(url))
    t.start()
 
if __name__ == "__main__":
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print data
    re_json = json.loads(data)
    save_file_name = 'east china normal university.json'
    with open(save_file_name,'w') as f:
        f.write(data)
"""
    try:
        for i in school_list:
            expr = "expr=Composite(AA.AfN='%s')&count=70000&attributes=Id,Ti,CC,C.CN,J.JN,Y,AA.AuId,AA.AuN"%i
            obj_url = url_head + expr + key_info
            thread_run(obj_url)
    except Exception as e:
        print(str(e))
"""