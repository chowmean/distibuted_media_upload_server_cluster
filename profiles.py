from connection import *
import time

def get_profile(username,access='restrict'):
	user_id=get_user_id_from_username(username)
	if user_id==-1:
		return {'message':'this user profile does not exist','success':False}
	conn=connect()
	query = "select name,email,phone,profile_pic,genre,height,chest,achievement,user_id from profile where user_id='{0}'".format(user_id)
	cursor=conn.cursor()
	cursor.execute(query)
	row=cursor.fetchone()
	result=dict()
	while row is not None:
		result['name']=row[0]
		if access=='full':
			result['email']=row[1]
			result['phone']=row[2]
		result['profile_pic']=row[3]
		result['genre']=row[4]  #genre will be json
		result['height']=row[5]
		result['chest']=row[6]
		result['achievement']=row[7]
		result['user_id']=row[8]
		row=cursor.fetchone()
	conn.close()
	return result


def get_user_id_from_username(username):
	conn=connect()
	query="select id from User where username='{0}';".format(username)
	cursor=conn.cursor()
	cursor.execute(query)
	row=cursor.fetchone()
	if row is not None:
		user_id=row[0]
	else:
		user_id=-1
	conn.close()
	return user_id
	
	
	
	
	

def get_username_from_user_id(user_id):
	conn=connect()
	query="select username from User where id='{0}';".format(user_id)
	cursor=conn.cursor()
	cursor.execute(query)
	row=cursor.fetchone()
	if row is not None:
		username=row[0]
	else:
		username=-1
	conn.close()
	return username
	
	
	

def is_friend(user_id,friend_id):
	conn=connect()
        query="select * from friend where user_id='{0}' and friend_id='{1}' and pending=0;".format(user_id,friend_id)
        cursor=conn.cursor()
        cursor.execute(query)
	row=cursor.fetchone()
        if row is not None:
		 conn.close()
		 return True
	else:
		 query="select * from friend where user_id='{0}' and friend_id='{1}' and pending=0;".format(friend_id,user_id)
	         cursor=conn.cursor()
       		 cursor.execute(query)
       		 row=cursor.fetchone()
		 if row is not None:
			conn.close()
			return True	
	         else:		
			return False

#changes done on 18 august by supermacy

def get_user_id(access_token):
        conn=connect()
        query="select user_id from user_access where access_token='{0}'".format(access_token)
        cursor=conn.cursor()
        cursor.execute(query)
        row=cursor.fetchone()
        if row is not None:
                user_id=row[0]
		conn.close()
                return user_id
        else :
		conn.close()
                return -1
                
                
                
def get_connections(user_id,f_id="",access="full"):
        conn=connect()
        if f_id != "":
        	query="select f_id from friend where user_id='{0}' and pending=0;".format(f_id)
        	query2="select user_id from friend where f_id='{0}' and pending=0;".format(f_id)
        else:
        	query="select f_id from friend where user_id='{0}' and pending=0;".format(user_id)
        	query2="select user_id from friend where f_id='{0}' and pending=0;".format(user_id)
        cursor=conn.cursor()
        cursor.execute(query)
        row=cursor.fetchone()
 	frnd=dict()
 	i=0
        if row is not None:
                frnd[i]=row[0]
                i=i+1
		row=cursor.fetchone()
		
	cursor=conn.cursor()
        cursor.execute(query2)
        row=cursor.fetchone()
	if row is not None:
                frnd[i]=row[0]
                i=i+1
		row=cursor.fetchone()
				
				
	connection_list=dict()		
	if access=="full":
		i=0
		for key, value in frnd.iteritems():
			connection_list[i]=get_profile(get_username_from_user_id(value),"full")
			i=i+1
		return {"success":True,"friends":connection_list,"total_connections":i}
	else:
		return {"total_connections":i,"succes":True}		                
                
                
                
                
                
'''               
def request_friend(user_id,friend_id):
			con=connect();
			query_insert="insert into friend (user_id,friend_id,date_added,pending,follower) values('{0}','{1}','{2}','{3}','{4}');".format(user_id,friend_id,time.strftime('%Y-%m-%d %H:%M:%S'),1,True)
			try:
				cursor.execute(query_insert)
				con.commit()
			except Exception,e:
				if e[0]==1062:
					query="select pending,date_added,follower from friend where user_id='{0}' and friend_id='{1}';".format(user_id,friend_id)
					cursor=con.cursor()
					cursor.execute()
					row=cursor.fetchone()
                	if row is not None:
                		if row[0]==1:
                			pending =True
                		date=row[1]
                		follower=row[2]
                		row=cursor.fetchone()
                	con.close()
                	return {"message":"friend request allready sent","pending":pending,"date_requested":date, "is_following":follower,"success":True}
                	else:
                		con.close()
                		return {"message":"internal error","success":False}
            finally:
            	con.close()
                return {"message":"friend request sent","success":True,"is_following":True,"pending":True,"date_requested":time.strftime('%Y-%m-%d %H:%M:%S')}
                
                
                
def confirm_friend(user_id,friend_id,response):
			con=connect();
			if response==1:
				query_update="update friend set pending = 0 ,date_added='{0}' where user_id='{1}' and friend_id='{2}';".format(time.strftime('%Y-%m-%d %H:%M:%S'),friend_id,user_id)
		        try:
		            cursor.execute(query_update);
		            con.commit();
		        except Exception,e:
		        	con.close()
		            return {"message":"internal server error(confirm friend)","success":False}
		        finally:
		        	con.close()
		            return {"message":"friend added","success":True, "is_following":True,"accepted":True,"date_added":time.strftime('%Y-%m-%d %H:%M:%S')}
          	elif response==-1:
          		 query_update="delete from friend where user_id='{1}' and friend_id='{2}';".format(friend_id,user_id)
		        try:
		            cursor.execute(query_update);
		            con.commit();
		        except Exception,e:
		        	con.close()
		            return {"message":"internal server error(confirm friend)","success":False}
		        finally:
		        	con.close()
		            return {"message":"friend request rejected","success":True, "is_following":False,"accepted":False,"date_rejected":time.strftime('%Y-%m-%d %H:%M:%S')}
			else:
				return {"message":"ignored for now","success":True}	
           
'''
