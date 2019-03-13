import time
import datetime
import json
import requests
from bs4 import BeautifulSoup


str = '__jp2\n    ({"code":0"'
print(len(str))
print(str[0])
print(str.index('{'))
# 获取当前时间
print(datetime.datetime.now())
# print("我先睡眠五秒")
# time.sleep(5)

list_1 = [1, 2, 3]
for item in list_1:
    print(item)
print(list_1)
print(str[:-1])

print(len("https://new.qq.com/omn/20190225/20190225A05F0J.html"))
print(len("紧急呼叫丨涞源反杀案当事人出狱与家人团聚：听到消息以为在做梦"))
print(len("庞某琪生前照片 公安部儿童失踪信息紧急发布平台提供新京报讯（记者 张彤）3日23时许，公安部儿童失踪信息紧急发布平台发消息称，走失39小时的4岁女童庞某琪遗体于失踪地点附近水渠底部被找到，目前，警方……"))


test_str = "转基因大豆;空心菜;致癌;酱油;西瓜;蘑菇;较真;低钠盐;食物"
print(len(test_str))

data = "https://new.qq.com/omn/20181224/20181224A1J4TQ00"

print(data[(data.rindex("/")) + 1:])

data2 = "https://new.qq.com/zt/template/?id=NBA2018113000276100"

print(data2[(data2.rindex("id=")) + 3:])

str1 = ""


