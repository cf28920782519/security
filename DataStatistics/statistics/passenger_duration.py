#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017-8-30

@author: long3
'''
from jdbc.query_table import get_sites, get_terminal_feature, get_mac_filter_data


def duration(conn, date, time):
    start = date[0:4]+'-'+date[4:6]+'-'+date[6:8]+' '+time+':00:00'
    #end_hour = int(time) + 1
    end = date[0:4]+'-'+date[4:6]+'-'+date[6:8]+' '+time+':59:59'
    
    rows = get_sites(conn)
    
    one_site_mac_duration = {}
    for row in rows:
        records = get_records_and_time_list(conn, start, end, row[0])
        map = {}
        for record in records:
            count = 0
            for i in records[record]:
                if i > 0: count = count+1 
            map[record] = count
        one_site_mac_duration[row[0]] = map
    
    return one_site_mac_duration

    
def get_records_and_time_list(conn, start_time, end_time, site_code):    
    rs = get_terminal_feature(conn, start_time, end_time, site_code)
    record_count = {}
    filter_mac_list = get_mac_filter_data(conn, start_time, end_time, site_code)
    #print filter_mac_list
    for row in rs:
        if not filter_mac_list.__contains__(row[0]):  #用hotspot表进行过滤
            if not record_count.has_key(row[0]):
                time_list = [0 for i in range(120)]
                record_count[row[0]] = time_list
        
            min = row[1].minute
            sec = row[1].second
            index = (int(min)*60+int(sec))/30
            record_count[row[0]][index] = 1

    return record_count


    