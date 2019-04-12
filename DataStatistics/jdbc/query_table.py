# -*- coding:utf-8 -*-
'''
Created on 2017��8��31��

@author: onewalnut
'''
import cx_Oracle
from jdbc.connection import get_connection, free


def get_sites(conn):
    if conn == None:
        conn = get_connection()
    
    cr = conn.cursor()
    
    sql = "SELECT F_CODE FROM T_SITE"
    cr.execute(sql)
    rows = cr.fetchall()
    
    cr.close()
    
    return rows



def get_old_passenger_str(conn, sitecode):
    if conn == None:
        conn = get_connection()
    
    cr = conn.cursor()

    sql = ("select F_PASSENGER_MACS from T_PASSENGER_OLD where F_SITE_CODE = '%s'")%(sitecode)    
    cr.execute(sql) 
      
    rs_macs = cr.fetchone()
    
    return rs_macs[0]



def insert_into_passenger_old_table(conn, sitecode, macs):
    if conn == None:
        conn = get_connection()
    
    cr = conn.cursor()
    cr.setinputsizes(F_PASSENGER_MACS = cx_Oracle.CLOB)
    sql_insert = ("insert into T_PASSENGER_OLD values ('%s','', '', :F_PASSENGER_MACS , '7', sysdate)")%(sitecode) 
    cr.execute(sql_insert, F_PASSENGER_MACS = macs)
    conn.commit()
    cr.close()
    print "insert"



def update_passenger_old_table(conn, sitecode, macs):
    if conn == None:
        conn = get_connection()
    
    cr = conn.cursor()
    cr.setinputsizes(F_PASSENGER_MACS = cx_Oracle.CLOB)
    sql_update = ("update T_PASSENGER_OLD set F_PASSENGER_MACS = :F_PASSENGER_MACS, F_UPDATE_TIME = sysdate where F_SITE_CODE = '%s'")%(sitecode)
    cr.execute(sql_update, F_PASSENGER_MACS = macs)
    conn.commit()
    cr.close()
    print "update"



def get_terminal_feature(conn, start_time, end_time, site_code):
    if conn == None:
        conn = get_connection()
    
    sql = ("SELECT F_MAC, F_CAP_TIME FROM T_TERMINAL_FEATURE WHERE F_CAP_TIME BETWEEN"
           " TO_TIMESTAMP('%s', 'YYYY-MM-DD HH24-MI-SS') AND TO_TIMESTAMP('%s','YYYY-MM-DD HH24-MI-SS')"
           " AND F_SITE_CODE = '%s'") % (start_time, end_time, site_code)
    cr = conn.cursor()
    cr.execute(sql)
    rs = cr.fetchall()
    cr.close()
    
    return rs


def get_mac_filter_data(conn, start_time, end_time, site_code):
    if conn == None:
        conn = get_connection()
    
    sql = ("SELECT F_HOTSPOT_MAC FROM T_COLLECTION_HOTSPOT WHERE F_CAP_TIME BETWEEN"
           " TO_TIMESTAMP('%s', 'YYYY-MM-DD HH24-MI-SS') AND TO_TIMESTAMP('%s','YYYY-MM-DD HH24-MI-SS')"
           " AND F_SITE_CODE = '%s'")% (start_time, end_time, site_code)
           
    cr = conn.cursor()
    cr.execute(sql)
    rs = cr.fetchall()
    mac_list = ""
    for row in rs:
        mac_list = mac_list + str(row[0]) + ","
    
    cr.close()
    
    return mac_list
    
