# -*- coding: utf-8 -*-

import cx_Oracle
import datetime
import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
#
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签,参考https://blog.csdn.net/GreenHandCGL/article/details/79814572

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

# 计算车辆和违法数积累曲线的横纵轴
def cal_x_y(WFSL):
    num = len(WFSL)
    x = []
    y = []
    sum = 0                     # 初始化违法数之和
    for i in range(num):        # 计算WFSL的列表中，所有的违法数量之和，作为y轴的分母
        sum += WFSL[i]
    WFSL_ele =0                 # y轴的分子，列表中，从WFSL[0]到WFSL[i]的元素之和
    for i in range(num):
        x.append(1.0*(i+1)/num)     # 计算x轴，由于以1辆车为单位，所以形式为[1/num,2/num,3/num...]
        WFSL_ele += WFSL[i]
        y.append(1.0*WFSL_ele/sum)
    return x, y

# 计算积累曲线的横轴,输入违法数量列表和给定的违法数y的均值以及上面的x,y列表，输出对应的x值（x为一个百分数，表示车辆数的占比）
def cal_x(WFSL,y_val,x,y):
    num = len(WFSL)
    denominator = 0
    for i in range(num):
       denominator += WFSL[i]
    numerator = 0
    for i in range(num):
        if WFSL[i] >= y_val:
            numerator += WFSL[i]
        else: break
    y_rate = 1.0*numerator/denominator
    for i in range(num):
        if y_rate > y[i]: continue
        else: return x[i], y[i]             # 多输出一个y[i]用于图上标注





if __name__ == '__main__':
    starttime = datetime.datetime.now()     # 统计程序的开始时刻

    conn = None
    query_res = get_Plate_WFSL(conn,1)      # 修改HPZL=1,2,15
    print(query_res)
    print(len(query_res))
    HPHM, WFSL = query_conv(query_res)
    print(HPHM)
    print(WFSL)
    print(len(HPHM))
    x, y = cal_x_y(WFSL)
    x_i, y_i = cal_x(WFSL, 11.1, x, y)      # 修改平均非现场违法数，对应HPZL=1,2,15
    print(x_i,y_i)

    # 画图展示计算结果
    # font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
    plt.plot(x,y,label=u"大型车",color='black')
    plt.plot([0,x_i],[y_i, y_i],'r--')
    plt.plot([x_i,x_i],[0,y_i],'r--')
    plt.scatter(x_i, y_i, c='r',label='拐点')
    plt.axis([0, 1.05, 0, 1.05])
    plt.xlabel('车辆累计百分比')
    plt.ylabel('违法数累计百分比')
    plt.title('非现场违法数-车辆数累计曲线')
    plt.annotate('(%4.1f%%, %4.1f%%)'%(x_i*100,y_i*100), xy=(x_i,y_i),xytext=(1.0*x_i,0.9*y_i))
    plt.legend()
    plt.show()

    # 统计程序结束时刻，并输出程序的运行时间
    endtime = datetime.datetime.now()
    print("the program runs : %d s" % (endtime - starttime).seconds)
