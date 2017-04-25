# -*- coding: utf-8 -*-
""" 这个模块只被调用 """
__python_version__ = 2.7
__author__ = "Liu Kun"
__last_edit__ = "2017-04-25"

html_head = """
<!DOCTYPE html>
<html>
  <head>	  
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://apps.bdimg.com/libs/bootstrap/3.3.0/css/bootstrap.min.css">
        <title>{{  title  }}</title>
  </head>
  <body>
"""

html_end = """
    <script src="http://apps.bdimg.com/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="http://apps.bdimg.com/libs/bootstrap/3.3.0/js/bootstrap.min.js"></script>
  </body>
  <footer>
  <p align="center">All data from a collection of Microsoft oxford academic API in 2016-05-01</p>
  <p align="center">Author: Liukun</p>
  </footer>
</html>
"""

#try to make it more auto in the future
def dictRend(source_dic,out_file_path="BootstrapOutput.html",title = "Title",a_count=0):
    table_head = '''
    <div class="container" ><font face="Arial">
       <h2>%s &nbsp</h2>
       <p>paper number:%d</p>
       <p>Most Valuable Researcher :) </p>
      <table class="table table-striped table-hover table-bordered">
        <thead>
          <tr>
            <th>rank</th>
            <th>Author</th>
            <th>Cite count from local data</th>
          </tr>
        </thead>
        '''%(title,a_count)
    table_end = '''
            </tbody>
        </table>
    </div>
    '''
    with open(out_file_path,'w') as f:
        f.write(html_head.replace("{{  title  }}","Rank of " + title))
        f.write(table_head)
        f.writelines("<tbody>")
        count = 0
        for i in source_dic:
            count +=1
            author = i[1][0]
            CC = i[1][1]
            f.write("""
            <tr>
            <td>%d</td>
            <td><a href="%s" target="_blank">%s</a></td>
            <td><a href="%s" target = "_blank">%d</a></td>
            </tr>"""%(count,search_url(author),author,search_url(author,school=title,mode = 2),CC))
        f.write(table_end)
        f.write(html_end)
        
# 敲完这个函数名，刹那间如梦境重现，这一幕在哪一晚的梦中梦到过，
# 不知道编程至今，算不算入门了呢？加油吧
# http://cn.bing.com/academic/search?q=jingyu+yang
def search_url(name,school='',mode=1):
    url = "http://cn.bing.com/academic/search?q=" + name.replace(" ",'+')
    if mode == 1:
        return url
    elif mode == 2:
        return url +'+' + school.lower().replace(" ",'+')
  
