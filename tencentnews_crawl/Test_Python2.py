import requests
import logging

# str = "ddwada"
# try:
#     str.index("123")
# except ValueError:
#     print("substring no found, josn格式出现问题")
# else:
#     print("没有问题")
# finally:
#     print("结束")


# def testlist(a):
#     a.append(2)
#
#
# a = list()
# a.append("1")
# testlist(a)
# print(a)

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'cookie': 'pgv_pvi=873498624; pgv_pvid=8030797876; RK=D2yMD/QFzz; ptcz=090544707cfb8295f419620e0e05125ba60ae0539d0b83b00b7227ca8d839f63; tvfe_boss_uuid=c274d92db377a818; eas_sid=m1n5D4y7r2G6O796b9c466d135; luin=o2542479897; ptui_loginuin=2542479897; lskey=000100001b7a54fcd3301a6718003674b4dd3347c8d0ffff8abb81b50d0c27fcfbf01c34a07f0e4a6d04a41c; o_cookie=2542479897; pac_uid=1_2542479897; uid=413994855; pgv_info=ssid=s7552449838; pgv_si=s2044055552'
}

respo = requests.get("https://openapi.inews.qq.com/getQQNewsNormalContent", params={
        'chlid': 'news_auto',
        'refer': 'mobilewwwqqcom',
        'otype': 'jsonp',
        'ext_data': 'all',
        'id': 'ENT2019031100853300',
        'callback': 'getNewsContentOnlyOutput'
    }, headers=headers)
print(respo.text)

logger = logging.getLogger("application")

logging.info("123")

