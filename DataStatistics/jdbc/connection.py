# -*- coding:utf-8 -*-
'''
Created on 2017-8-31

@author: onewalnut
'''

import cx_Oracle 

def get_connection():
#     conn = cx_Oracle.connect('c##smartapdm','c##smartapdm','39.108.98.225:1521/orcl')
    conn = cx_Oracle.connect('c##smartapdm','c##smartapdm','120.78.215.146:1521/orcl')
    return conn

def free(conn, cursor):
    cursor.close()
    conn.close()
