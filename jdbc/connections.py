
import cx_Oracle

# 连接数据库
def get_connection():
    conn = cx_Oracle.connect('scott/tiger@localhost/orcl')  # 用户名/密码@服务器地址/数据库名称
    return conn
# 关闭连接
def free(conn, cursor):
    cursor.close()
    conn.close()