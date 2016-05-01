#-*- coding: utf-8 -*-
#自动生成index.html
import os

def index_generate(file_list):
    containner_head = '''
<!DOCTYPE html>
<html>
  <head>	  
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="http://apps.bdimg.com/libs/bootstrap/3.3.0/css/bootstrap.min.css">
  </head>
  <body>
    <div class="container-fluid">
	<div class="row-fluid">
		<div class="span12">
			<div class="row-fluid">
    '''
    containner_end ='''
                </div>
        </div>
    </div>
    <script src="http://apps.bdimg.com/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="http://apps.bdimg.com/libs/bootstrap/3.3.0/js/bootstrap.min.js"></script>
  </body>
</html>
    '''
    count = 1
    with open("./pre_index.html",'w') as f:
        f.write(containner_head)
        f.write('''
        <div class="row-fluid">
        ''')
        for i in file_list:
            school_name = i.split('.')[0]
            if count%4 == 0:
                f.writelines('''
                <div class="row-fluid">
                ''')
                f.write('''
                    <div class="col-xs-3 span3">
                        <h3>
                            <a href="pages/%s">%s</a>
                        </h3>
                    </div>
                '''%(i,regular_institute_name(school_name)))
            elif count%4 == 3:
                 f.write('''
                        <div class="col-xs-3 span3">
                            <h3>
                                <a href="pages/%s">%s</a>
                            </h3>
                        </div>
                        '''%(i,regular_institute_name(school_name)))
                 f.write("</div>")
            else:
                 f.write('''
                    <div class="col-xs-3 span3">
                        <h3>
                            <a href="pages/%s">%s</a>
                        </h3>
                    </div>
                    '''%(i,regular_institute_name(school_name)))
            count +=1
        f.write(containner_end)   
 

def regular_institute_name(name):
    words_list = name.split(' ')
    index = 0
    for i in words_list:
        if len(i)>3:
            words_list[index] = i[0].upper() + i[1:]
        index +=1
    reg_name = ' '.join(words_list)
    return reg_name

def exe(path):
    fileList = []
    for root, dirs, files in os.walk(path):#递归path下所有目录
        for f_name in files:
            if f_name.lower().endswith('.html'):
                fileList.append(f_name)
    index_generate(fileList)
    
if __name__ =="__main__":
    fileList = []
    for root, dirs, files in os.walk('pages/'):#递归path下所有目录
        for f_name in files:
            if f_name.lower().endswith('.html'):
                fileList.append(f_name)
    index_generate(fileList)