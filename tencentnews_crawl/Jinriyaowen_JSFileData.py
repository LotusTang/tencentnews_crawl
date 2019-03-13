import requests
import json
import tencentnews_crawl.MysqlUtils as mysqlutils
import mysql.connector


def parse_response_to_dict(respo):
    start_index = respo.text.index("[")
    end_index = respo.text.rindex("]")
    encode_str = (respo.text[start_index: end_index + 1])\
        .encode('utf-8').decode('unicode_escape')
    # 移除掉反斜线
    last_str = encode_str.translate(str.maketrans('', '', '\\'))
    return json.loads(last_str)


def start_crawl_jinriyaowen(headers):
    re = requests.get("https://i.match.qq.com/ninja/fragcontent", params={
        'pull_urls': 'news_top_2018',
        'callback': '__jp1'
    }, headers=headers)
    connection = mysqlutils.connect_to_mysql()
    if re.status_code == 200:
        list_data = parse_response_to_dict(re)
        print("今日要闻部分: ")
        print(list_data)
        write_into_mysql(connection, list_data)
    # 关闭连接
    connection.close()


def write_into_mysql(connection, list_data):
    insert_count = 0
    sameitem_count = 0
    # 同样地，我们需要将其写入我们的数据库中
    insert_sql = ("""
        INSERT INTO jinriyaowen
        (article_id, title, url)
        VALUES 
        (%s, %s, %s)
    """)
    # 如果存在那么则不进行数据插入，也不需要更新
    check_exists_sql = ("""
        SELECT COUNT(*) FROM jinriyaowen
        WHERE article_id = %s
    """)
    cursor = connection.cursor(buffered=True)
    try:
        for item in list_data:
            cursor.execute(check_exists_sql, (item['article_id'], ))
            if cursor.fetchone()[0] < 1:
                insert_count += 1
                cursor.execute(insert_sql, (item['article_id'], item['title'], item['url']))
            else:
                sameitem_count += 1
    except mysql.connector.IntegrityError as err:
        connection.rollback()
        print("属于重复数据，不需要插入，更新即可")
        print(err)
    else:
        connection.commit()
        print("今日要闻新增数据" + str(insert_count) + "条")
        print("重复数据 " + str(sameitem_count) + "条")
    finally:
        cursor.close()


if __name__ == '__main__':
    start_crawl_jinriyaowen(None)








