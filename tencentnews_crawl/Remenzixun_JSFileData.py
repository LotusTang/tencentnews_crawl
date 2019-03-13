import requests
import json
import tencentnews_crawl.MysqlUtils as mysqlutils
import mysql.connector
import datetime
from bs4 import BeautifulSoup


def parse_response_to_dict(respo):
    start_index = respo.text.index("{")
    dict_text = json.loads(respo.text[start_index: len(respo.text) - 1])
    return dict_text


def get_next_resp(headers, page_number):
    return requests.get("https://pacaio.match.qq.com/irs/rcd", params={
        'cid': 4,
        'token': '9513f1a78a663e1d25b46a826f248c3c',
        'ext': '',
        'page': page_number,
        'expIds': '',
        'callback': '__jp3'
    }, headers=headers)


def start_crawl_remenzixun(headers):
    present_resp = requests.get("https://pacaio.match.qq.com/irs/rcd", params={
        'cid': 4,
        'token': '9513f1a78a663e1d25b46a826f248c3c',
        'ext': '',
        'page': 0,
        'expIds': '',
        'callback': '__jp3'
    }, headers=headers)
    request_count = 0
    page_number = 0
    status_code = present_resp.status_code
    connection = mysqlutils.connect_to_mysql()

    while status_code == 200 and request_count <= 600:
        page_number += 1
        request_count += 1
        data_dict = parse_response_to_dict(present_resp)
        write_into_mysql(connection, data_dict, page_number)
        present_resp = get_next_resp(headers, page_number)
    # 关闭连接
    connection.close()


# 这个与热点精选是一模一样的写入数据库格式
def write_into_mysql(connection, dict_data, page_number):
    sameitem_count = 0
    insertitem_count = 0
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
                (%(newsurl_id)s,  %(content_id)s, %(news_title)s, %(news_intro)s,
                 %(keywords)s, %(main_category)s, %(main_category)s,
                 %(comment_id)s, %(comment_num)s, %(publish_time)s,
                 %(page_url)s, %(source)s, %(view_count)s, %(is_ztlink)s
                )
        """)
    datalist = list()
    for data_item in dict_data['data']:
        data = {
            'newsurl_id': data_item['id'],
            'content_id': data_item['app_id'],
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
        if data_item['vurl'].find("zt") == -1:
            data['is_ztlink'] = '0'
            if data['page_url'].find("htm") != -1:
                # 如果是html页面，那么不需要id进行下面的js请求，只需要将原本的id传入即可
                # 由于需要主外键的原因，所以还是需要这样做的
                data['content_id'] = data['page_url'][(data['page_url'].rindex("/")) + 1:data['page_url'].rindex(".")]
                data['is_html'] = 1
            else:
                data['content_id'] = data['page_url'][(data['page_url'].rindex("/")) + 1:]
                data['is_html'] = 0
        else:
            data['is_ztlink'] = '1'
            data['content_id'] = data['page_url'][(data['page_url'].rindex("id=")) + 3:]
        datalist.append(data)
    cursor = connection.cursor(buffered=True)
    try:
        for newsurl in datalist:
            cursor.execute(check_if_exists, (newsurl['newsurl_id'],))
            if cursor.fetchone()[0] < 1:
                cursor.execute(insert_url_statement, newsurl)
                # 统计
                insertitem_count += 1
                # 插入url到表里面之后我们没有必要再分开单独去抽取数据再去爬取，可以直接爬取对应网页的内容
                if newsurl['is_ztlink'] == '0':
                    write_link_content_mysql \
                        (cursor, newsurl['content_id'], newsurl['page_url'], newsurl['is_html'],
                         newsurl['newsurl_id'], newsurl['publish_time'], newsurl['news_title'])
                else:
                    write_zt_content_mysql(cursor, newsurl['content_id'], newsurl['newsurl_id'])
            else:
                cursor.execute(update_url_info,
                               (newsurl['comment_num'], newsurl['view_count'], newsurl['newsurl_id']))
                sameitem_count += 1
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
        print("热门资讯 No." + str(page_number) + "条 : ", datetime.datetime.now())
        print("新增数据: " + str(insertitem_count) + "条")
        print("重复数据: " + str(sameitem_count) + "条")
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
    try:
        data_list = json.loads(encode_str)
    except json.decoder.JSONDecodeError as err:
        print(err)
        print("解析json出现问题")
        print("问题字符串:", encode_str)
        return None
    for data_item in data_list:
        for url_item in data_item['artlist']:
            id_list.append(url_item)
    for id_item in id_list:
        try:
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
        except ValueError:
            print("json 格式出现问题")
            continue
        except requests.exceptions.ConnectionError:
            print("api请求等待时间过长")
            continue
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
        cursor.execute(insert_content_sql, data)


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
    if len(content_data_dict['article_content']) <= 21100:
        cursor.execute(insert_content_sql, data)
    else:
        print("文章内容过长:", len(content_data_dict['article_content']))


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
    data_dict = json.loads(last_str)
    # 我们应该将数据中的内容抓取之后返回
    content_str = ""
    for con_item in data_dict['ext_data']['content']:
        if con_item['type'] != 'img_url' and con_item['desc'] is not None:
            content_str += con_item['desc']
    return {
        'article_content': content_str
    }


def get_newscontent_from_html(url):
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        print(err)
        print("html请求连接超时")
        return {
            'article_content': ''
        }
    soup = BeautifulSoup(resp.text, features="html.parser")
    div_content_tags = soup.find_all('p', {'class': 'one-p'})
    content_str = ""
    for item in div_content_tags:
        if item.string is not None:
            content_str += item.string
    return {
        'article_content': content_str
    }


if __name__ == '__main__':
    start_crawl_remenzixun(None)




