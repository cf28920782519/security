# -*- coding: utf-8 -*-

import cx_Oracle
import datetime

# 连接数据库
def get_connection():
    conn = cx_Oracle.connect('scott/tiger@localhost/orcl')  # 用户名/密码@服务器地址/数据库名称
    return conn
# 关闭连接
def free(conn, cursor):
    cursor.close()
    conn.close()

# 通过TRFF_VEHICLE表，按类别获取车牌信息(返回了一个列表，里面的每个元素都是一个元组)
def get_plate_number(conn, HPZL):
    if conn == None:        # 确认建立数据库连接
        conn = get_connection()

    cr = conn.cursor()  # 生成连接的游标

    sql = ("SELECT HPHM FROM TRFF_VEHICLE WHERE HPZL=%d AND ZT NOT LIKE '%s' and ZT NOT LIKE '%s' AND ZT NOT LIKE '%s'")%(HPZL,'%E%','%P%','%M%')        # 定义从TRFF_VEHICLE表中查询待统计车辆的sql语句
    cr.execute(sql)                             # 执行sql语句
    # 下面的代码可以将查询结果分批量导入python的变量，避免炸内存
    plate_list_sql=[]
    while True:
        plate_list_tuple = cr.fetchmany(10000)          # 最后改成fetchall()
        plate_list_sql += plate_list_tuple
        if not plate_list_tuple:
            break
    return plate_list_sql
# 元组列表转成字符串列表，原本的查询结果是[(内容1),(内容2),(内容3)...]，即plate_list_sql
def plate_list(plate_list_sql):
    plate_list = []
    for i in plate_list_sql:
        j = ''.join(i)
        plate_list.append(j)
    return plate_list           # 返回的结果为['内容1', '内容2', '内容3']

# 加上省的简称，本函数的输入是函数plate_list函数的输出结果，str写省的简称
def plate_list_new(plate_list, str):
    plate_list_new = []
    for i in range(len(plate_list)):
        str_new = str + plate_list[i]
        plate_list_new.append(str_new)
    return plate_list_new

# 按车牌字符串，查询非现场违法次数及处理状态统计
def query_vio_surveil(conn, plate_list_new):
    if conn == None:
        conn = get_connection()
    cr = conn.cursor()
    query_num = len(plate_list_new)
    total_surveil = []
    CL_surveil = []
    for i in range(query_num):
        sql_surveil = "SELECT WFSJ, CLBJ FROM TRFF_VIO_SURVEIL WHERE HPHM='%s'"%(plate_list_new[i])
        cr.execute(sql_surveil)
        signal_result = cr.fetchall()
        if len(signal_result) == 0:         # 返回违章次数为0
            total_surveil.append(0)
            CL_surveil.append(0)
        else:                               # 统计总体违章次数及未处理次数
            total_surveil.append(len(signal_result))    # 返回结果的数组长度即为总违章次数
            CL_num = 0                      # 初始化已处理次数
            for j in range(len(signal_result)):     # 计算已处理的违法次数（CLBJ=1表示已处理）
                CL_num += int(signal_result[j][1])  # 返回数组的每个元素是一个元组，访问CLBJ列（处理标记列在第二列）
            CL_surveil.append(CL_num)
    cr.close()
    return total_surveil, CL_surveil

# 生成号牌类型标识的list（对应VEHICLE表的HPZL字段）
def HPZL_list(plate_list_new,HPZL):
    return [str(HPZL)]*len(plate_list_new)      # 返回结果形式为['HPZL', 'HPZL', 'HPZL']

# 计算结果整理成批量插入SQL数据库所需要的格式
def Trans_DataFrame(plate_list_new, total_surveil, CL_surveil, HPZL_list):         # 这3个list长度一致，等于所统计的车辆数
    a = [plate_list_new, total_surveil, CL_surveil, HPZL_list]
    return list(zip(*a))

# 批量插入数据库
def Insert_db(conn, result):
    if conn == None:
        conn = get_connection()
    cr = conn.cursor()

    sql = "INSERT INTO SURVEIL_Res(HPHM, WFSL, CLSL, HPZL) VALUES (:1, :2, :3, :4)"

    try:
        cr.executemany(sql, result)
        conn.commit()
    except:
        conn.rollback()

    # 关闭游标、关闭数据库连接
    cr.close()
    conn.close()
    return 0


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    conn = None
    tup = get_plate_number(conn,22)
    lis = plate_list(tup)
    lis_new = plate_list_new(lis,'皖')
    print(lis_new)
    print(len(lis_new))

    total_surveil, CL_surveil = query_vio_surveil(conn,lis_new)
    print(total_surveil, CL_surveil)
    print("the total number of surveil is:", sum(total_surveil[0:]))
    print("the pending surveil is ", sum(total_surveil[0:])-sum(CL_surveil[0:]))
    HPZL = HPZL_list(lis_new,22)         # 此时，HPZL = 1

    result = Trans_DataFrame(lis_new,total_surveil,CL_surveil,HPZL)
    print(result)
    Insert_db(conn, result)


    endtime = datetime.datetime.now()
    print("the program runs : %d s"%(endtime - starttime).seconds)








