def zhuanzhi(a):
    return tuple(zip(*a))

list1 =  ['皖P80020', '皖P80630', '皖P83159', '皖P83460']
list2 = [64, 48, 35, 54]
list3 = [60, 46, 35, 53]
a = [list1,list2,list3]
print(a)
print(zhuanzhi(a))

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
        else: return x[i]
print(cal_x_y([4,3,2,1]))
print(cal_x([4,3,2,1],2.01,[0.25, 0.5, 0.75, 1.0],[0.4, 0.7, 0.9, 1.0]))