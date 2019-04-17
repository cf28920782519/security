# -*- coding: utf-8 -*-

import cx_Oracle
import datetime

def get_connection():
    conn = cx_Oracle.connect('scott/tiger@localhost/orcl')  # 用户名/密码@服务器地址/数据库名称
    return conn
def free(conn, cursor):
    cursor.close()
    conn.close()

# 获取列表的第二个元素
def takeSecond(elem):
    return elem[1]

# 查询号牌号码和违法数量并按违法数量的降序排序
def get_Plate_WFSL(conn, HPZL):
    if conn == None:        # 确认建立数据库连接
        conn = get_connection() # 建立数据库连接

    cr = conn.cursor()  # 生成连接的游标

    sql = ("SELECT HPHM,WFSL FROM SURVEIL_RES WHERE HPZL=%d ") % (HPZL)

    cr.execute(sql)
    query_res = cr.fetchall()       # 查询结果为元组形式[(数据1),(数据2),(数据3)]
    free(conn, cr)          # 关闭游标，关闭连接

    query_res.sort(key=takeSecond, reverse=True)    # 按第二个元素降序排序，查询结果形式为：[('皖P40994',0), ('皖P33549',1)...]，升序是reverse=False(默认)
    return query_res


# 将oracle查询结果，按列放入list
def query_conv(query_res):  # 输入的查询结果形式为：[('皖P40994',0), ('皖P33549',1)...]
    num = len(query_res)    # 获得查询结果的列表长度，作为循环次数
    HPHM = []           # 建立存放号牌号码的list
    WFSL = []           # 建立存放违法数量的list
    for i in range(num):
        HPHM.append(query_res[i][0])    # 在列表的尾部加入查询结果第i个元组的第1个数据（即车牌号）
        WFSL.append(query_res[i][1])    # 在列表的尾部加入查询结果第i个元组的第2个数据（即违法数量）
    return HPHM, WFSL






if __name__ == '__main__':
    starttime = datetime.datetime.now()
    conn = None
    query_res = get_Plate_WFSL(conn,1)
    print(query_res)
    print(len(query_res))
    HPHM, WFSL = query_conv(query_res)
    print(HPHM)
    print(WFSL)
    print(len(HPHM))


    endtime = datetime.datetime.now()
    print("the program runs : %d s" % (endtime - starttime).seconds)
