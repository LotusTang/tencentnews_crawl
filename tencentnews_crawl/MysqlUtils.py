import mysql.connector
from mysql.connector import errorcode


def connect_to_mysql():
    config = {
        'user': 'root',
        'password': '123',
        'host': 'localhost',
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
    check_if_exists = ("""
            SELECT COUNT(1) FROM user
        """)
    print("测试连接数据库: ")
    connection = connect_to_mysql()
    print("Connect Success")
    # 测试在数据库中插入数据
    cursor = connection.cursor(buffered=True)
    cursor.execute(check_if_exists,)
    # print('是否已连接:' + str(connection.is_connected()))
    # row = cursor.fetchone()
    if cursor.fetchone()[0] < 1:
        print("不存在结果")
    else:
        print("存在结果")
    print("关闭连接: ")

    close_connection(connection)



