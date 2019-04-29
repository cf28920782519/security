import cx_Oracle
import datetime
#
def get_connection():
    conn = cx_Oracle.connect('scott/tiger@localhost/orcl')  # 用户名/密码@服务器地址/数据库名称
    return conn
def free(conn, cursor):
    cursor.close()
    conn.close()


def dangerous_vehicle_type2_query(conn):
    if conn == None:        # 确认建立数据库连接
        conn = get_connection() # 建立数据库连接

    cr = conn.cursor()  # 生成连接的游标

    sql_vehilce = "SELECT HPHM,HPZL,DJRQ FROM TRFF_VEHICLE WHERE CCDJRQ <= to_date('2009-01-01','YYYY-MM-DD') AND " \
                  "DJRQ <= to_date('2014-01-01','YYYY-MM-DD') AND " \
                  "QZBFQZ>= to_date('2019-01-01','YYYY-MM-DD')" # 查询2019年1月1日之前的所有报废车的车牌、类型、报废日期

    cr.execute(sql_vehilce)
    query_res = cr.fetchmany(1000)  # 查询结果为元组形式[(数据1),(数据2),(数据3)]
    cr.close()
    return query_res

# 性能类型2的车辆
def query_conv(query_res,str):
    num = len(query_res)    # 获得查询结果的长度
    HPHM = []   # 号牌号码
    HPZL = []   # 号牌种类
    YXQZ = [] # 检验有效期止,在最近定检日期之后的一年（车龄6年以上，1年1检）
    for i in range(num):
        HPHM.append(str + query_res[i][0])  # 从VEHICLE表中查询的车牌号没有皖，加 “皖”
        HPZL.append(query_res[i][1])
        YXQZ.append(query_res[i][2]+datetime.timedelta(days=365))
    return HPHM, HPZL, YXQZ
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
        if WFSJ_MAX_tuple[i][0] == None:    # 如果没查到违法时间，则最晚违法时间设置为1990年1月1日（VEHICLE表中的YXQZ最小为1992年6月8日）
            WFSJ_MAX.append(datetime.datetime(1990, 1, 1, 1, 1))
        else:
            WFSJ_MAX.append(WFSJ_MAX_tuple[i][0])   # 加入SURVEIL表的查询结果
    return WFSJ_MAX

def get_dangerous_vehicle_t2(YXQZ, WFSJ_MAX, HPHM, HPZL):
    if len(YXQZ) == len(WFSJ_MAX):
        num = len(YXQZ)
        dangerous_HPHM = [] # 危险车辆号牌号码
        dangerous_HPZL = [] # 危险车辆号牌种类
        WF_time_interval = []   # 非法时间段（从报废之日起，至最晚违法日期止）
        for i in range(num):
            if YXQZ[i] < WFSJ_MAX[i]:     # 最晚违法时间如果大于年检有效日期
                dangerous_HPHM.append(HPHM[i])  # 加入号牌号码
                dangerous_HPZL.append(HPZL[i])  # 加入号牌种类
                WF_time_interval.append((WFSJ_MAX[i]-YXQZ[i]).days)   # 加入非法时间段
            else: continue
        return dangerous_HPHM, dangerous_HPZL, WF_time_interval


if __name__ == '__main__':
    starttime = datetime.datetime.now()  # 统计程序的开始时刻

    conn = None
    query_res = dangerous_vehicle_type2_query(conn)
    HPHM, HPZL, YXQZ = query_conv(query_res,'皖')
    WFSJ_MAX = get_WFSJ_MAX(conn, HPHM, HPZL)
    print(HPZL)
    print(HPHM)
    print(YXQZ)
    print(len(YXQZ))
    dangerous_HPHM, dangerous_HPZL, WF_time_interval = get_dangerous_vehicle_t2(YXQZ,WFSJ_MAX,HPHM,HPZL)
    print(dangerous_HPZL)
    print(dangerous_HPHM)
    print(len(dangerous_HPHM))
    print(WF_time_interval)
