def zhuanzhi(a):
    return tuple(zip(*a))

list1 =  ['皖P80020', '皖P80630', '皖P83159', '皖P83460']
list2 = [64, 48, 35, 54]
list3 = [60, 46, 35, 53]
a = [list1,list2,list3]
print(a)
print(zhuanzhi(a))