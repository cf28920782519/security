# -*- coding:utf-8 -*-
'''
Created on 2017-8-31

@author: onewalnut
'''
from jdbc.query_table import get_sites, get_old_passenger_str

def passenger_statistics(conn, mac_info):
    
    rows = get_sites(conn)
    
    site_statistics_info = {}
    for row in rows:
        macs_all = []
        macs_into_store = [] 
        macs_new = []
        macs_old = []
        
        if mac_info.has_key(row[0]):
            site_old_macs = str(get_old_passenger_str(conn, row[0]))
            #print "old_macs:"+site_old_macs;
            one_detail = mac_info.get(row[0])           
            for key in one_detail.keys():
                macs_all.append(key)
                if one_detail.get(key) > 10:
                    macs_into_store.append(key)
                    if(key in site_old_macs):
                        macs_old.append(key)
                    else:
                        macs_new.append(key)
                    
        res = [macs_all, macs_into_store, macs_new, macs_old]
        site_statistics_info[row[0]] = res
    
    
    return site_statistics_info          
                    
