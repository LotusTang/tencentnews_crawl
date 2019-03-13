import requests
import json
import datetime
import tencentnews_crawl.MysqlUtils as pythonmysql
import mysql.connector
from bs4 import BeautifulSoup


def parse_response_to_dict(respo):
    start_index = respo.text.index("{")
    dict_text = json.loads(respo.text[start_index: len(respo.text) - 1])
    return dict_text


def get_next_reponse(data_dict, response):
    # 首先先获取到expIds的值
    expIds = ""
    for data_item in data_dict['data']:
        expIds += data_item['id'] + '|'
    # 去掉最后一个|
    expIds = expIds[:-1]
    # 再去获取到下一个请求对应的pagenumber以及callback
    callback = ""
    url_str = response.url
    page_number = int(url_str[url_str.index("page=") + 5: url_str.index("expIds") - 1]) + 1
    if page_number == 1:
        callback = '__jp5'
    else:
        callback = "__jp" + str(page_number + 4)
    params = {
        'cid': '108',
        'ext': '',
        'token': '349ee24cdf9327a050ddad8c166bd3e3',
        'page': page_number,
        'expIds': expIds,
        'callback': callback
    }
    return requests.get("https://pacaio.match.qq.com/irs/rcd", params=params)


def get_newscontent_dict(content_id):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'cookie': 'pgv_pvi=873498624; pgv_pvid=8030797876; RK=D2yMD/QFzz; ptcz=090544707cfb8295f419620e0e05125ba60ae0539d0b83b00b7227ca8d839f63; tvfe_boss_uuid=c274d92db377a818; eas_sid=m1n5D4y7r2G6O796b9c466d135; ts_uid=3349329104; luin=o2542479897; ptui_loginuin=2542479897; lskey=000100001b7a54fcd3301a6718003674b4dd3347c8d0ffff8abb81b50d0c27fcfbf01c34a07f0e4a6d04a41c; o_cookie=2542479897; pac_uid=1_2542479897; qq_openid=A2D3079EDC813B79C1BC3CFE63707361; qq_access_token=41F46BA1B8DF36761DB630851A9FDB9F; qq_client_id=101487368; pgv_info=ssid=s5016911484; pgv_si=s5524955136; ts_last=news.qq.com/; ad_play_index=13'
    }
    respo = requests.get("https://openapi.inews.qq.com/getQQNewsNormalContent", params={
        'id': content_id,
        'child': 'news_rss',
        'refer': 'mobilewwwqqcom',
        'otype': 'jsonp',
        'ext_data': 'all',
        'srcfrom': 'newsapp',
        'callback': 'getNewsContentOnlyOutput'
    }, headers=headers)
    start_index = respo.text.index("{")
    end_index = respo.text.rindex("}")
    encode_str = respo.text[start_index: end_index + 1]
    # 这个的返回值说实话，有那个relatedsearchwords在里面，感觉很难受，所以这里需要将那段去掉再进行解析
    if encode_str.find("relatedSearchWords") != -1:
        encode_str_2_startindex = encode_str.index("relatedSearchWords")
        encode_str_2_endindex = encode_str.index("mini_program_code")
        encode_str_slice1 = encode_str[: encode_str_2_startindex]
        encode_str_slice3 = encode_str[encode_str_2_endindex:]
        encode_str = encode_str_slice1 + encode_str_slice3
        last_str = encode_str.translate(str.maketrans('', '', '\\'))
    else:
        last_str = encode_str
    try:
        data_dict = json.loads(last_str)
    except json.decoder.JSONDecodeError as err:
        print(err)
        print("json数据解析失败")
        return {
            'article_content': ''
        }
    # 我们应该将数据中的内容抓取之后返回
    content_str = ""
    for con_item in data_dict['ext_data']['content']:
        if con_item['type'] != 'img_url' and con_item['desc'] is not None:
            content_str += con_item['desc']
    return {
        'article_content': content_str
    }


def get_newscontent_from_html(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, features="html.parser")
    div_content_tags = soup.find_all('p', {'class': 'one-p'})
    content_str = ""
    for item in div_content_tags:
        if item.string is not None:
            content_str += item.string
    return {
        'article_content': content_str
    }


def start_crawl_redianxinwen(headers):
    present_response = requests.get("https://pacaio.match.qq.com/irs/rcd", params={
        'cid': '108',
        'ext': '',
        'token': '349ee24cdf9327a050ddad8c166bd3e3',
        'page': '0',
        'expIds': '',
        'callback': '__jp2'
    }, headers=headers)
    status_code = present_response.status_code
    request_number_count = 0
    scrapy_url_list = []
    # 获取数据库连接
    connection = pythonmysql.connect_to_mysql()
    # 限制请求时间没有用，因为无论是在这里还是在浏览器中，到了指定数目都无法再加载
    #     # wait_everytime = 60
    #     # wait_everysixtimes = 600

    # 为下一个请求的url编写方法
    # 根据状态码我们确认是否继续抓取数据，且最多只能获取十个请求，浏览器中也是一样
    while status_code == 200 and request_number_count <= 10:
        request_number_count += 1
        scrapy_url_list.append(present_response.url)
        print("The No." + str(request_number_count) + " response.text: ", datetime.datetime.now())
        print(present_response.text)
        # 将当前的response转换为dict
        data_dict = parse_response_to_dict(present_response)
        # 将获取到的链接数据写入数据库，提供给scrapy用于爬取数据
        # 刚开始是想通过scrapy访问数据库去抓取，其实大可不必，直接存入数据库即可
        write_to_mysql(connection, data_dict)
        # 生成一个随机等待的时间表示差别，这里是一到两分钟
        # time.sleep(wait_everytime + random.randint(60, 120))
        next_response = get_next_reponse(data_dict, present_response)
        # 太频繁的提取数据肯定会导致我们无法进行请求的，但是我还是想测试一下这个一次最多快速可以获取到多少请求
        # 最多快速获取十个请求...然后就没数据了，我们试试看如果一次达到6个请求数的时候我们等待十分钟，看是否能够继续
        # 请求数据
        # if once_request_number >= 6:
        #     once_request_number = 0
        #     time.sleep(wait_everysixtimes + random.randint(120, 240))
        status_code = next_response.status_code
        present_response = next_response
    # 记得关闭连接
    pythonmysql.close_connection(connection)
    print("热点新闻部分:")
    print("最大请求数目: " + str(request_number_count))
    print("所有请求链接: ")
    for links in scrapy_url_list:
        print(links)


# 将获取到的一次的所有链接及其内容数据写入到mysql
def write_to_mysql(connection, dict_data):
    check_if_exists = ("""
        SELECT COUNT(*) FROM newsurl_list_tencent
        WHERE newsurl_id = %s
    """)
    update_url_info = ("""
        UPDATE newsurl_list_tencent SET
        comment_num = %s, view_count= %s
        WHERE newsurl_id = %s
    """)
    insert_url_statement = ("""
        INSERT INTO newsurl_list_tencent 
              (newsurl_id, content_id, news_title, 
              news_intro, keywords, main_category,
              sub_category, comment_id, comment_num,
              publish_time, page_url, source,
              view_count, is_ztlink) 
        VALUES 
            (%(newsurl_id)s, %(content_id)s, %(news_title)s, %(news_intro)s,
             %(keywords)s, %(main_category)s, %(main_category)s,
             %(comment_id)s, %(comment_num)s, %(publish_time)s,
             %(page_url)s, %(source)s, %(view_count)s, %(is_ztlink)s
            )
    """)
    # 寻找并插入内容

    # 将传递过来的数据转换成我们需要的格式
    datalist = list()
    for data_item in dict_data['data']:
        data = {
            'newsurl_id': data_item['id'],
            # 'content_id': data_item['app_id'],
            'news_title': data_item['title'],
            'news_intro': data_item['intro'],
            'keywords': data_item['keywords'],
            'main_category': data_item['category1_chn'],
            'sub_category': data_item['category2_chn'],
            'comment_id': data_item['comment_id'],
            'comment_num': data_item['comment_num'],
            'publish_time': data_item['publish_time'],
            'page_url': data_item['vurl'],
            'source': data_item['source'],
            'view_count': data_item['view_count']
            # 'is_ztlink': data_item['id']
        }
        # 由于content_id中存在null值，所以我们需要根据是否为专题分别从里面的url抓取到我们需要的链接
        # 而不能直接使用数据里面的app_id
        # 而且这里，可能是html结尾也可能没有html结尾,而对于这两种链接，我们需要分情况进行处理
        if data_item['vurl'].find("zt") == -1:
            data['is_ztlink'] = '0'
            if data['page_url'].find("htm") != -1:
                data['content_id'] = data['page_url'][(data['page_url'].rindex("/")) + 1:data['page_url'].rindex(".")]
                data['is_html'] = 1
            else:
                data['content_id'] = data['page_url'][(data['page_url'].rindex("/")) + 1:]
                data['is_html'] = 0
        else:
            data['is_ztlink'] = '1'
            data['content_id'] = data['page_url'][(data['page_url'].rindex("id=")) + 3:]
        datalist.append(data)
    # 如果不需要获取所有结果那么设置为buffered = True
    cursor = connection.cursor(buffered=True)
    try:
        # 如果数据不存在则选择插入到里面，如果存在那么我们更新view_count和comment_num字段即可
        for newsurl in datalist:
            # 这里也太坑了吧，需要一定是一个元组才行，所以我们需要在()里面加上一个逗号至少
            # 一般的cursor执行之后都会返回一个值表示影响的数目，但是如果执行的是函数就不会，
            # 这里count()只会返回None，如果需要执行存储过程那么就需要调用cursor.callproc
            # 然后返回值就是存储过程的结果，如果其它情况就需要fetch去获取了
            cursor.execute(check_if_exists, (newsurl['newsurl_id'], ))
            if cursor.fetchone()[0] < 1:
                cursor.execute(insert_url_statement, newsurl)
                # 插入url到表里面之后我们没有必要再分开单独去抽取数据再去爬取，可以直接爬取对应网页的内容
                if newsurl['is_ztlink'] == '0':
                    write_link_content_mysql\
                        (cursor, newsurl['content_id'], newsurl['page_url'], newsurl['is_html'],
                         newsurl['newsurl_id'], newsurl['publish_time'], newsurl['news_title'])
                else:
                    write_zt_content_mysql(cursor, newsurl['content_id'], newsurl['newsurl_id'])
            else:
                cursor.execute(update_url_info,
                               (newsurl['comment_num'], newsurl['view_count'], newsurl['newsurl_id']))
    except mysql.connector.IntegrityError as err:
        connection.rollback()
        print("属于重复数据，不需要插入，更新即可")
        print(err)
    # except mysql.connector.Error as err:
    #     connection.rollback()
    #     print("没有捕获的错误，请修改代码")
    #     print(err)
    else:
        connection.commit()
    finally:
        cursor.close()


# 先获取所有的id列表，然后我们再根据id获取到我们需要的内容
# 专题信息的话，我们直接将所有
def write_zt_content_mysql(cursor, content_id, unique_id):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'cookie': 'pgv_pvi=873498624; pgv_pvid=8030797876; RK=D2yMD/QFzz; ptcz=090544707cfb8295f419620e0e05125ba60ae0539d0b83b00b7227ca8d839f63; tvfe_boss_uuid=c274d92db377a818; eas_sid=m1n5D4y7r2G6O796b9c466d135; ts_uid=3349329104; luin=o2542479897; ptui_loginuin=2542479897; lskey=000100001b7a54fcd3301a6718003674b4dd3347c8d0ffff8abb81b50d0c27fcfbf01c34a07f0e4a6d04a41c; o_cookie=2542479897; pac_uid=1_2542479897; qq_openid=A2D3079EDC813B79C1BC3CFE63707361; qq_access_token=41F46BA1B8DF36761DB630851A9FDB9F; qq_client_id=101487368; pgv_info=ssid=s5016911484; pgv_si=s5524955136; ts_last=news.qq.com/; ad_play_index=13'
    }
    id_list = list()
    respo = requests.get("https://openapi.inews.qq.com/getQQNewsNormalContent", params={
        'chlid': 'news_auto',
        'refer': 'mobilewwwqqcom',
        'otype': 'jsonp',
        'ext_data': 'all',
        'id': content_id,
        'callback': 'getNewsContentOnlyOutput'
    }, headers=headers)
    insert_content_sql = """
            INSERT INTO newscontent_list_tencent (
            content_id, title, publish_time,
            article_content
            )
            VALUES 
            (%(content_id)s, %(title)s, %(publish_time)s, 
            %(article_content)s
            )
        """
    encode_str = respo.text
    encode_str = encode_str[encode_str.index("{"): encode_str.rindex("}") + 1]
    if encode_str.find("sectionData") != -1:
        start_ind = encode_str.index("sectionData")
        end_ind = encode_str.rindex("topPicW")
        encode_str = encode_str[start_ind + 13:end_ind - 2]
    data_list = json.loads(encode_str)
    for data_item in data_list:
        for url_item in data_item['artlist']:
            id_list.append(url_item)
    for id_item in id_list:
        article_respo = requests.get("https://openapi.inews.qq.com/getQQNewsNormalContent", params={
            'id': id_item,
            'chlid': 'news_rss',
            'refer': 'mobilewwwqqcom',
            'otype': 'jsonp',
            'ext_data': 'all',
            'srcfrom': 'newsapp',
            'callback': 'getNewsContentOnlyOutput'
        })
        intial_str = article_respo.text
        intial_str = intial_str[intial_str.index("{"): intial_str.rindex("}") + 1]
        intial_str = intial_str[:intial_str.index("ext_data")] \
                     + intial_str[intial_str.rindex("\"content\"") + 1:intial_str.index("relate_news_list") - 2] \
                     + "}"
        data_dict = json.loads(intial_str)
        content_str = ""
        for item_ in data_dict['content']:
            if item_['type'] == 1:
                content_str += item_['value']
        data = {
            'content_id': unique_id,
            'title': data_dict['title'],
            'publish_time': data_dict['pubtime'],
            'article_content': content_str
        }
        try:
            cursor.execute(insert_content_sql, data)
        except mysql.connector.errors.DatabaseError as errs:
            print(errs)
            print("json数据来说，文章内容过多")
            continue


# 直接将获得的网页的内容写入数据库，根据id进行主外键关联,这里分两种情况
# 一种是html内容，一种不是，所以我们需要分两种情况处理
def write_link_content_mysql(cursor, content_id, html_url, is_html, unique_id, pub_time, title):
    # 对于不是html的需要做解析,否则我们使用beautifulsoup去解析内容
    # 使用uniqueid只是作为主外键关联的作用
    content_data_dict = None
    if is_html == 0:
        content_data_dict = get_newscontent_dict(content_id)
    else:
        content_data_dict = get_newscontent_from_html(html_url)
    insert_content_sql = """
        INSERT INTO newscontent_list_tencent (
        content_id, title, publish_time,
        article_content
        )
        VALUES 
        (%(content_id)s, %(title)s, %(publish_time)s, 
        %(article_content)s
        )
    """
    data = {
        'content_id': unique_id,
        'title': title,
        'publish_time': pub_time,
        'article_content': content_data_dict['article_content']
    }
    cursor.execute(insert_content_sql, data)

