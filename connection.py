import mysql.connector
from mysql.connector import Error


def connect():
    try:
        conn = mysql.connector.connect(host='192.168.68.210', database='horizon', user='root', password='chowmean')
        if conn.is_connected():
            return conn
	else:
	    return False
 
    except Error as e:
        print(e)



