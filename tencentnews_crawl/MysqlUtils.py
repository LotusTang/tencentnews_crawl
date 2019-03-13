import mysql.connector
from mysql.connector import errorcode


def connect_to_mysql():
    config = {
        'user': 'root',
        'password': '123',
        'host': '127.0.0.1',
        'database': 'tencentnews_data',
        'raise_on_warnings': True
    }
    _connection = None
    try:
        _connection = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return _connection


def close_connection(con):
    con.close()


if __name__ == '__main__':
    print("测试连接数据库: ")
    connection = connect_to_mysql()
    print("Connect Success")
    # 测试在数据库中插入数据
    data = {
        'newsurl_id': '123',
        'news_title': 'mytitle',
        'news_intro': 'myintro',
        'keywords': 'keywords',
        'main_category': 'ca1',
        'sub_category': 'ca2',
        'comment_id': '1231231231',
        'comment_num': 1111,
        'publish_time': '2019-03-04 12:38:40',
        'page_url': 'news.qq.com',
        'source': '腾讯新闻',
        'view_count': 10000,
        'is_ztlink': '1'
    }
    print("关闭连接: ")
    close_connection(connection)



