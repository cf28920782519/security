# -*- coding:utf-8 -*-
'''
Created on 2017-8-31

@author: onewalnut
'''
from jdbc.connection import get_connection, free

from statistics.passenger_duration import duration
from statistics.passenger_info_statistics import passenger_statistics
from statistics.update_old_passenger import update_old_passenger_table

if __name__ == '__main__':
    
    
    conn = get_connection()
    date = '20170921' 
    time = '18'
    
    mac_duration =  duration(conn, date, time)
    
    statistics_res = passenger_statistics(conn, mac_duration)
    #print statistics_res
    #打印过滤后的客流人数
    for item in statistics_res:
        print item + ":" + str(statistics_res[item][0].__len__()) +"@"+ str(statistics_res[item])
     
    #update_old_passenger_table(conn, date)
    conn.close()
    pass
