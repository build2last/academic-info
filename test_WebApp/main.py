# -*- coding: utf-8 -*-

import os
import ApiQuery2 as AQ
import indexGenerator
import mvp_multiProcess as mvp
from server import RunServer
import settings

def main():
    AQ.main() # 完成下载数据任务
    mvp.main() # 完成分析和绘制 html 任务
    indexGenerator.main() # 完成主页生成任务
    os.chdir(settings.SERVER_ROOT_PATH)
    RunServer.main() # 运行服务器

if __name__ == '__main__':
    main()