import tencentnews_crawl.RedianJinXuan_JSFileData as redianjs
import tencentnews_crawl.Jinriyaowen_JSFileData as jinruyaowen
import tencentnews_crawl.Remenzixun_JSFileData as remenzixun
import datetime
import logging
import tencentnews_crawl.PythonLog as pythonlog


def run():
    # 为我们的请求添加头信息
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'cookie': 'pgv_pvi=873498624; pgv_pvid=8030797876; RK=D2yMD/QFzz; ptcz=090544707cfb8295f419620e0e05125ba60ae0539d0b83b00b7227ca8d839f63; tvfe_boss_uuid=c274d92db377a818; eas_sid=m1n5D4y7r2G6O796b9c466d135; ts_uid=3349329104; luin=o2542479897; ptui_loginuin=2542479897; lskey=000100001b7a54fcd3301a6718003674b4dd3347c8d0ffff8abb81b50d0c27fcfbf01c34a07f0e4a6d04a41c; o_cookie=2542479897; pac_uid=1_2542479897; qq_openid=A2D3079EDC813B79C1BC3CFE63707361; qq_access_token=41F46BA1B8DF36761DB630851A9FDB9F; qq_client_id=101487368; pgv_info=ssid=s5016911484; pgv_si=s5524955136; ts_last=news.qq.com/; ad_play_index=13'
    }
    # 这里我应该将所有的js文件的抓取放在一个程序统一入口里面，然后再指派给不同的py文件去处理这样子
    # 试试多线程? 那么问题来了，如果使用多线程去加快程序运行速度呢? 这里涉及到的是http请求接着又是把数据插入
    # 数据库中，难道分别将这两个分开么?
    # 我觉得这个问题可以留到后面解决，给自己留个todo吧，先完成主线任务好了
    logger = logging.getLogger('tencentenws_application')
    t1 = datetime.datetime.now()
    redianjs.start_crawl_redianxinwen(headers)
    t2 = datetime.datetime.now()
    # 今日要闻的数据就不往数据库里插入了，因为数据量太少，而且没多大意义觉着
    jinruyaowen.start_crawl_jinriyaowen(headers)
    t3 = datetime.datetime.now()
    remenzixun.start_crawl_remenzixun(headers)
    t4 = datetime.datetime.now()
    logger.info("热点新闻耗时: ", (t2 - t1).seconds, "s")
    logger.info("今日要闻耗时: ", (t3 - t2).seconds, "s")
    logger.info("热门资讯耗时: ", (t4 - t3).seconds, "s")
    logger.info("本次抓取总耗时: ", (t4 - t1).seconds, "s")
    # 仅两天的信息，就有三千多条...我的天
    # 下面该做的事情是，拿着这些数据库里的链接，根据日期，每次只爬取一天的所有网站的信息就ok了，我应该再添加
    # 一个字段，表示是否该站点已经被爬取


if __name__ == '__main__':
    run()



