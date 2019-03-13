import win32serviceutil
import win32service
import win32event
import time
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import tencentnews_crawl.CrawlTencentNewsJSFileData as crawldata


class CrawlTencentNewsService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CrawlTencentNewsService"             #服务名
    _svc_display_name_ = "CrawlTencentNewsJob"         #job在windows services上显示的名字
    _svc_description_ = "Crawl Tencent News to Database"           #job的描述

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.run = True


    def SvcDoRun(self):
        try:
            while self.run:
                # 调用方法抓取新闻信息
                crawldata.run()
                time.sleep(60 * 60 * 3)
        except Exception as e:
            print(e)
            time.sleep(60 * 30)


    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(CrawlTencentNewsService)



















