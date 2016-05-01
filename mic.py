#-*- coding: utf-8 -*-
import urllib
import re
import json
import urllib
import socket
import threading
import Queue
socket.setdefaulttimeout(30)

#https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=Id=2140251882&count=10000&attributes=Id,AA.AuId,AA.AfId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
url_head = "https://oxfordhk.azure-api.net/academic/v1.0/evaluate?"
key_info = "&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6"
school_list = ['peking university','tsinghua university','zhejiang university',
                        'nanjing university of science and technology','nanjing university of aeronautics',
                        'shanghai jiao tong university','fudan university','wuhan university',
                        'nanjing university','university of science and technology of china']
school_list2 = ['beihang university','sun yat sen university','beijing institute of technology'] 
school_list3 = ['stanford university','massachusetts institute of technology']
def print_entity(enti_list):
    for i in enti_list:
        print i.get('Ti')
        AA_list = i.get('AA')
        for j in range(len(AA_list)):
            print '(%d)'%(j+1) + AA_list[j].get('AuN') + ' ',
        print ''

def mvp_find(enti_list):
    pass
        
#多线程下载器
class download(threading.Thread):  
    def __init__(self,que):  
        threading.Thread.__init__(self)  
        self.que = que
    def run(self):  
         try:
            url = self.que.get()
            resp =urllib.urlopen(url)
            result = resp.read()
            re_json = json.loads(result)
            enti_list = re_json.get('entities')
            sch_name = re.findall('AfN=(.*)\)',url)[0]
            print sch_name+ " " + str(len(enti_list))
            save_file_name =  sch_name.replace("\'",'')  + '.txt'
            with open(save_file_name,'w') as f:
                f.write(result)
         except Exception as e:
             print(str(e))       

if __name__ == "__main__":
    que = Queue.Queue()
    try:
        for i in school_list+school_list2+school_list3:
            expr = "expr=Composite(AA.AfN='%s')&count=10&attributes=Id,Ti,CC,C.CN,J.JN,Y,AA.AuId,AA.AuN"%i
            obj_url = url_head + expr + key_info
            que.put(obj_url)
            d=download(que)  
            d.start()
    except Exception as e:
        print(str(e))