import cx_Oracle

db=cx_Oracle.connect('scott/tiger@localhost/orcl')
cr=db.cursor()
sql="select Count(*) from TRFF_VEHICLE"
cr.execute(sql)
rs=cr.fetchall()
print ("the number of vehicles is: %s"%rs)

cr.close()
db.close()