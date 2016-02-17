__author__ = 'supermacy'
import hashlib
import random
from connection import *
from uuid import getnode as get_mac
import time
from datetime import  datetime,timedelta

def login(user_data,device_id):
    username=user_data['username']
    password=user_data['password']
    query="SELECT id,password, salt,username  FROM horizon.User where username='{0}';".format(username);
    con=connect()
    cursor=con.cursor()
    cursor.execute(query)
    row=[]
    row=cursor.fetchone()
    mac = get_mac()
    if row:
        print row
        user_id=row[0]
        password_got=row[1]
        salt=row[2]
        cryptpass=hashlib.sha512( str(salt) + password ).hexdigest()
        #print cryptpass
        if password_got!= cryptpass:
            return  {"message":"wrong password","success":False}
        if password_got == cryptpass:
            r=random.randint(00000,99999)
            access_token=create_token(str(datetime.now()),salt,str(device_id))
            a=time.strftime('%Y-%m-%d %H:%M:%S')
            final_date=expiry_date(a)
            query_insert="insert into user_access (user_id,access_token,expiry,device_id,ip) values('{0}','{1}','{2}','{3}','{4}');".format(user_id,access_token,final_date,device_id,mac)
            try:
                cursor.execute(query_insert);
                con.commit();
            except Exception,e:
                if e[0]==1062:
                    a=time.strftime('%Y-%m-%d %H:%M:%S')
                    expiry=expiry_date(a)
                    query_update="update user_access set access_token ='{0}' ,expiry='{1}' where device_id='{2}' and user_id='{3}';".format(access_token,expiry,device_id,user_id)
                    cursor.execute(query_update)
                    con.commit()
            finally:
            	con.close();
                return {"message":"Authentication Successeded","success":True,"token":access_token}
                

    else:
          con.close()
          return {"message":"Unauthorized User" ,"success":False}


def create_token(password,salt,r):
    return  hashlib.sha512(str(salt)+password+r).hexdigest()


def expiry_date(a):
    time=str(a).split(" ")[0]
    time1=datetime.strptime(time , '%Y-%m-%d')
    EndDate = time1 + timedelta(days=2)
    return  EndDate


def logout(access_token):
    query_delete="delete from user_access where access_token='{0}';".format(access_token)
    try:
        con=connect()
        cursor=con.cursor()
        cursor.execute(query_delete)
        con.commit()
        return {"message":"user successfully logout","success":True}
    except Exception as e:
        print e
        pass
    finally:
        con.close()



