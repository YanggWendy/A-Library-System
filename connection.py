import pymysql

def connection():
    con = pymysql.connect(host='localhost',user='root',password='MYmy0402',db='ALS')
    return con
