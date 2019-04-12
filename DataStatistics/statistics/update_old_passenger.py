# -*- coding:utf-8 -*-
'''
Created on 2017��8��31��

@author: onewalnut
'''

from jdbc.connection import get_connection, free
from jdbc.query_table import insert_into_passenger_old_table, update_passenger_old_table
from jdbc.query_table import get_sites, get_terminal_feature

def update_old_passenger_table(conn,date):
    if conn == None:
        conn = get_connection()
    
    mac_list_map = duration_one_day(conn, date)
    
    for sitecode in mac_list_map.keys():
        if conn == None:
            conn = get_connection()
    
        macs = mac_list_map.get(sitecode)

        macs = macs + '#'
        cr = conn.cursor()

        sql = ("select F_PASSENGER_MACS, F_OLD_PERIOD from T_PASSENGER_OLD where F_SITE_CODE = '%s'")%(sitecode)    
        cr.execute(sql) 
      
        rs_macs = cr.fetchone()
   
        if rs_macs == None :
            insert_into_passenger_old_table(conn, sitecode, macs)
        else:
            old_macs = str(rs_macs[0].read())
            mac_list = old_macs.split('#')
            period = int(rs_macs[1])
            if not (len(mac_list) < period+1):
                start = old_macs.find('#')
                old_macs = old_macs[start+1:len(old_macs)]
            update_passenger_old_table(conn, sitecode, old_macs+macs)
    
        cr.close()



def duration_one_day(conn, date):
    start = date[0:4]+'-'+date[4:6]+'-'+date[6:8]+' '+'00:00:00'
    
    end = date[0:4]+'-'+date[4:6]+'-'+date[6:8]+' '+'23:59:59'
    
    rows = get_sites(conn)
    
    one_site_mac_list = {}
    for row in rows:
        mac_list = get_records_and_time_list(conn, start, end, row[0])      
        one_site_mac_list[row[0]] = mac_list
    
    return one_site_mac_list

    
def get_records_and_time_list(conn, start_time, end_time, site_code):
    
    rs = get_terminal_feature(conn, start_time, end_time, site_code)
    mac_list = ""
    for row in rs:
        if not mac_list.__contains__(row[0]):
            mac_list = mac_list + row[0] +","

    return mac_list
