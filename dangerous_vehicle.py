# -*- coding: utf-8 -*-

import cx_Oracle
import datetime

def get_connection():
    conn = cx_Oracle.connect('scott/tiger@localhost/orcl')  # 用户名/密码@服务器地址/数据库名称
    return conn
def free(conn, cursor):
    cursor.close()
    conn.close()

def dangerous_vehicle_type1_query(conn):
    if conn == None:        # 确认建立数据库连接
        conn = get_connection() # 建立数据库连接

    cr = conn.cursor()  # 生成连接的游标

    sql_vehilce = "SELECT HPHM,HPZL,QZBFQZ FROM TRFF_VEHICLE WHERE QZBFQZ<= to_date('2019-01-01','YYYY-MM-DD')" # 查询2019年1月1日之前的所有报废车的车牌、类型、报废日期

    cr.execute(sql_vehilce)
    query_res = cr.fetchmany(1000)  # 查询结果为元组形式[(数据1),(数据2),(数据3)]
    return query_res
# 性能类型1的车辆
def query_conv(query_res,str):
    num = len(query_res)    # 获得查询结果的长度
    HPHM = []   # 号牌号码
    HPZL = []   # 号牌种类
    QZBFQZ = [] # 强制报废日期
    for i in range(num):
        HPHM.append(str + query_res[i][0])  # 从VEHICLE表中查询的车牌号没有皖，加 “皖”
        HPZL.append(query_res[i][1])
        QZBFQZ.append(query_res[i][2])
    return HPHM, HPZL, QZBFQZ
# 获得每辆车最后的违法时间
def get_WFSJ_MAX(conn, HPHM, HPZL):
    if conn == None:  # 确认建立数据库连接
        conn = get_connection()  # 建立数据库连接

    cr = conn.cursor()  # 生成连接的游标

    num = len(HPHM)     # 获得号牌号码列表的长度
    WFSJ_MAX_tuple = [] # 查询结果存放在一个列表中，列表元素为tuple
    for i in range(num):
        sql_max_WFSJ = ("SELECT MAX(WFSJ) FROM TRFF_VIO_SURVEIL WHERE HPHM='%s' AND HPZL='%s' ")%(HPHM[i],HPZL[i])  # 多条违法记录中，取时间最晚的，号牌号码和车辆种类2个字段确定一辆车
        cr.execute(sql_max_WFSJ)            # 执行查询语句
        WFSJ_MAX_tuple.append(cr.fetchone())    # 查询结果添加至列表
    WFSJ_MAX =[]    # 初始化最晚违法时间的列表
    for i in range(num):
        if WFSJ_MAX_tuple[i][0] == None:    # 如果没查到违法时间，则最晚违法时间设置为1990年1月1日（VEHICLE表中的QZBFQZ最小为1992年6月8日）
            WFSJ_MAX.append(datetime.datetime(1990, 1, 1, 1, 1))
        else:
            WFSJ_MAX.append(WFSJ_MAX_tuple[i][0])   # 加入SURVEIL表的查询结果
    return WFSJ_MAX

def get_dangerous_vehicle_t1(QZBFQZ, WFSJ_MAX, HPHM, HPZL):
    if len(QZBFQZ) == len(WFSJ_MAX):
        num = len(QZBFQZ)
        dangerous_HPHM = [] # 危险车辆号牌号码
        dangerous_HPZL = [] # 危险车辆号牌种类
        WF_time_interval = []   # 非法时间段（从报废之日起，至最晚违法日期止）
        for i in range(num):
            if QZBFQZ[i] < WFSJ_MAX[i]:     # 最晚违法时间如果大于强制报废日期
                dangerous_HPHM.append(HPHM[i])  # 加入号牌号码
                dangerous_HPZL.append(HPZL[i])  # 加入号牌种类
                WF_time_interval.append((WFSJ_MAX[i]-QZBFQZ[i]).days)   # 加入非法时间段
            else: continue
        return dangerous_HPHM, dangerous_HPZL, WF_time_interval

# 生成车牌号牌的危险类型标识的list（对应Dangerous_Vehicles表的Danger_Type字段）
def Danger_type_list(dangerous_HPHM,danger_tp):
    return [str(danger_tp)]*len(dangerous_HPHM)

# 计算结果整理成批量插入SQL数据库所需要的格式
def Trans_DataFrame(dangerous_HPHM, dangerous_HPZL, WF_time_interval, Danger_Type):         # 这3个list长度一致，等于所统计的车辆数
    a = [dangerous_HPHM, dangerous_HPZL, WF_time_interval, Danger_Type]
    return list(zip(*a))

# 批量插入数据库
def Insert_db(conn, result):
    if conn == None:
        conn = get_connection()
    cr = conn.cursor()
    # print('diaoyong')

    sql = "INSERT INTO DANGEROUS_VEHICLES(HPHM, HPZL, WF_Time_Interval, Danger_Type) VALUES (:1, :2, :3, :4)"

    try:
        cr.executemany(sql, result)
        conn.commit()
        print('insert successfully!')
    except:
        conn.rollback()

    # 关闭游标、关闭数据库连接
    free(conn, cr)
    return 0


if __name__ == '__main__':
    starttime = datetime.datetime.now()  # 统计程序的开始时刻

    conn = None
    query_res = dangerous_vehicle_type1_query(conn)
    HPHM, HPZL, QZBFQZ = query_conv(query_res,'皖')
    WFSJ_MAX = get_WFSJ_MAX(conn, HPHM, HPZL)
    # print(HPZL)
    # print(HPHM)
    # print(len(QZBFQZ))
    dangerous_HPHM, dangerous_HPZL, WF_time_interval = get_dangerous_vehicle_t1(QZBFQZ,WFSJ_MAX,HPHM,HPZL)
    # print(dangerous_HPZL)
    # print(dangerous_HPHM)
    # print(type(WF_time_interval[0]))
    Danger_Tp = Danger_type_list(dangerous_HPHM,'B') #  修改'B'（报废）为其他
    result = Trans_DataFrame(dangerous_HPHM, dangerous_HPZL, WF_time_interval, Danger_Tp)
    print(result)
    print(type(result[0][2]))
    conn = None
    Insert_db(conn, result)

    endtime = datetime.datetime.now()
    print("the program runs : %d s" % (endtime - starttime).seconds)




